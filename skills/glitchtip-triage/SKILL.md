---
name: glitchtip-triage
description: Triage Glitchtip-sourced Jira tickets in the CCXDEV project — detect duplicates, investigate root causes via stack traces and source code, and post "[AI suggestion]" comments. Use this skill whenever the user mentions triaging Glitchtip errors, reviewing ccx-processing/obsint-processing Jira tickets, deduplicating error reports, or investigating production/staging errors tracked in Jira with the glitchtip label.
---

# Glitchtip Ticket Triage

Automate triage of Jira tickets created by the "App SRE Jira bot" from Glitchtip error reports in the CCXDEV project. These tickets are auto-created when errors hit Glitchtip, so the same root error often produces multiple tickets (logged at different code layers, or the same infra failure surfacing in different services). The goal is to deduplicate them and investigate the root cause of unique errors.

## Prerequisites

- **jira CLI**: Must be configured and authenticated.
- **Glitchtip API token**: Read from the file `~/.config/glitchtip/token` (a single-line file containing just the token). Environment variables do not persist between shell invocations in Claude Code, so the token must be stored in a file. If the file does not exist, ask the user to create it:
  ```bash
  mkdir -p ~/.config/glitchtip && echo "YOUR_TOKEN_HERE" > ~/.config/glitchtip/token && chmod 600 ~/.config/glitchtip/token
  ```
  The token can be obtained from `https://glitchtip.devshift.net` under Profile > Auth Tokens. In all `curl` commands, read the token inline: `-H "Authorization: Bearer $(cat ~/.config/glitchtip/token)"`.
- **Git access via SSH**: All repositories (both GitHub and gitlab.cee.redhat.com) are cloned over SSH. Always use SSH URLs:
  - GitHub: `git@github.com:RedHatInsights/{repo}.git`
  - GitLab: `git@gitlab.cee.redhat.com:{group}/{repo}.git`

  The user's SSH keys must be registered with both services.

## User invocation

The user may say things like:
- "triage glitchtip tickets"
- "check new glitchtip errors"
- "triage CCXDEV-12345 CCXDEV-12346" (specific tickets only)
- "triage 5 glitchtip tickets" (limit count)
- "dry run glitchtip triage" (preview without posting comments)

### Restricting scope

The user can restrict which tickets get triaged:
- **By ticket IDs**: Only triage the listed tickets, but still use all already-triaged tickets for duplicate matching.
- **By count**: Take the first N untriaged tickets.
- **No restriction**: Process every untriaged ticket.

### Dry-run mode

If the user says "dry run", "preview", or "what would you do", show exactly what comments would be posted and to which tickets, but do not actually post anything. Present the results in a summary table.

## Workflow

### Phase 1: Fetch all open Glitchtip tickets

Use this JQL to get all matching tickets:

```bash
jira issue list --project CCXDEV \
  -q 'labels = glitchtip AND (labels = "ccx-processing" OR labels = "obsint-processing") AND status != Done AND status != Closed' \
  --plain --no-truncate --columns KEY,SUMMARY,STATUS,LABELS \
  --paginate 100
```

Paginate if there are more than 100 results (increment the paginate offset).

### Phase 2: Separate triaged from untriaged

For each ticket, fetch its **Jira comments** (this is where `[AI suggestion]` comments live — not in Glitchtip):

```bash
jira issue view CCXDEV-XXXXX --comments 50 --plain
```

To speed this up when there are many tickets, batch the comment checks — run several `jira issue view` commands in a single shell invocation using a for loop, piping through `grep` to check for `[AI suggestion]`:

```bash
for ticket in CCXDEV-16388 CCXDEV-16387 CCXDEV-16386; do
  echo "=== $ticket ==="
  jira issue view $ticket --comments 50 --plain 2>&1 | grep -A2 "\[AI suggestion\]" || echo "No AI suggestion comment"
done
```

Split into two groups based on whether the ticket has an `[AI suggestion]` Jira comment:

- **Triaged pool**: Tickets whose `[AI suggestion]` comment contains root-cause analysis (not a duplicate marker). These are the reference tickets for duplicate detection. Only tickets with genuine root-cause investigation belong here — tickets that were themselves marked as duplicates do not enter the pool.
- **Needs triage**: Tickets with no `[AI suggestion]` comment at all.

When splitting tickets that already have `[AI suggestion]` comments, check the content: if it starts with `[AI suggestion] This seems to be duplicate of`, it is a duplicate marker — do not add it to the triaged pool. Only add tickets whose `[AI suggestion]` comment contains root-cause analysis.

Apply the user's scope restriction (ticket IDs or count limit) to the "Needs triage" group only.

### Phase 3: Build the triaged-pool context

For each ticket in the triaged pool, gather:

| Field | Source |
|-------|--------|
| Ticket ID | KEY column |
| Error message | SUMMARY (this is the error text) |
| Glitchtip issue ID | From the URL label `https://glitchtip.devshift.net/ccx/issues/{ID}` |
| Service | Label matching `project:*` |
| Environment | Label matching `environment:*` |
| Existing triage | Content of `[AI suggestion]` comment |

Also fetch the **Glitchtip event data** (stack traces, error details) for each triaged-pool ticket via the Glitchtip REST API (see step 4b for how). This is a different system from Jira — Glitchtip holds the actual error logs and stack traces, while Jira holds the triage comments. Store the stack traces in working memory alongside each triaged-pool entry.

This context is what you match against when checking for duplicates. It grows during the run, but only when a ticket receives root-cause analysis (never when marked as duplicate).

### Phase 4: Triage each untriaged ticket

Process tickets one by one.

**Pool growth rule**: After triaging a ticket with root-cause analysis, add it to the triaged pool (including its stack trace and triage comment) so subsequent tickets can be matched against it. Tickets marked as duplicates do NOT enter the pool — duplicate chains should always point back to a ticket with actual root-cause analysis, never to another duplicate.

#### 4a. Extract metadata from labels

From the ticket's labels, extract:
- **Glitchtip issue ID**: From the URL label `https://glitchtip.devshift.net/ccx/issues/{ID}` — the numeric ID at the end.
- **Service name**: From the `project:*` label.
- **Environment**: From the `environment:*` label.

#### 4b. Fetch error data from Glitchtip API

Before checking for duplicates, fetch the actual error data from the Glitchtip REST API — the Jira ticket summary alone is not enough to determine duplicates. Glitchtip stores the real stack traces and error details; Jira only has a one-line summary.

```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/glitchtip/token)" \
  "https://glitchtip.devshift.net/api/0/issues/{issue_id}/" | python3 -m json.tool
```

```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/glitchtip/token)" \
  "https://glitchtip.devshift.net/api/0/issues/{issue_id}/events/?limit=5" | python3 -m json.tool
```

From the response, extract:
- Full stack trace (frames with file, function, line number)
- Error message and exception type
- Number of occurrences (count)
- First/last seen timestamps

**Parsing the events response**: Use a Python one-liner to extract structured data from the JSON. The events are a JSON array of objects with an `entries` field containing `exception` or `message` typed entries:

```bash
curl -s -H "Authorization: Bearer $(cat ~/.config/glitchtip/token)" \
  "https://glitchtip.devshift.net/api/0/issues/{issue_id}/events/?limit=3" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for ev in data:
    for entry in ev.get('entries', []):
        if entry.get('type') == 'exception':
            for val in entry['data'].get('values', []):
                print('Type:', val.get('type'))
                print('Value:', val.get('value'))
                for f in (val.get('stacktrace', {}).get('frames') or []):
                    print(f'  {f.get(\"filename\",\"?\")}:{f.get(\"lineNo\",\"?\")} in {f.get(\"function\",\"?\")}')
        elif entry.get('type') == 'message':
            print('Message:', entry.get('data', {}).get('formatted', ''))
"
```

**Go stack traces often lack file paths.** Go binaries compiled without debug info show `?` as the filename — you get only `?:lineNo in functionName`. When this happens, search the repo by function name (`grep -rn "func.*functionName"`) rather than by file path.

If the Glitchtip API returns 401/403, ask the user for a valid token. If 404, note that the Glitchtip issue may have been deleted and post a comment noting this.

#### 4c. Check for duplicates against the triaged pool

Compare this ticket's **actual stack trace and error data** against the triaged pool. Do not rely solely on the Jira ticket summary — two tickets with similar-sounding titles can have completely different root causes, and two tickets with different titles can share the same root cause.

Compare the stack traces: if the current ticket's error originates from the same code path as a triaged-pool ticket (same function, same file, same exception), or if the current ticket's error is a downstream consequence of a triaged-pool ticket's error (the current error's stack trace contains the triaged error's originating function further up the call chain), it is a duplicate.

Signs of a duplicate based on logs:
- **Shared stack frames**: The stack traces overlap significantly — especially the bottom frames where the error originates.
- **Same exception at the same code location**: Identical file + function + line throwing the same exception type.
- **Error propagation**: The current ticket's stack trace shows the error being caught and re-raised or re-logged at a higher layer. The original error (in the triaged pool) is from the lower layer.
- **Parametrized error messages**: The error message includes variable data (request IDs, UUIDs, item IDs, IP addresses, timestamps) that causes Glitchtip to create a separate issue for each unique value, even though the underlying error and code path are identical. Look for tickets from the same service with the same stack trace but error messages that differ only in an embedded ID or value. For example, `invalid request ID: 'abc123'` and `invalid request ID: 'def456'` are the same error — Glitchtip just groups them separately because the message strings differ.
- **Same infrastructure failure, different symptom**: Multiple tickets from the same service hitting the same external dependency failure (e.g., `connection refused`, `connection timed out`, `connection reset by peer` to the same IP:port). Even if the error messages and stack traces diverge at different error-handling branches, the root cause is the same unavailable dependency. Treat these as duplicates when the target address matches and the errors are from the same service and environment.
- **Overlapping event times**: Compare `firstSeen`/`lastSeen` timestamps from Glitchtip. If two errors from the same service have overlapping time windows, that strengthens a duplicate match — they likely stem from the same incident. Conversely, if two errors have similar stack traces but occurred weeks apart with no overlap, they may be separate incidents worth investigating independently.

**If duplicate — post this comment** (or show it in dry-run):

```
[AI suggestion] This seems to be duplicate of https://redhat.atlassian.net/browse/CCXDEV-YYYYY. {logging_fix}
```

Where `{logging_fix}` suggests how to prevent this duplicate ticket from being created in the future. The fix depends on **why** the duplicate exists — there are two distinct patterns:

**Pattern 1: Same error logged at multiple code paths.** The outer layer catches and re-logs the error at ERROR level, which triggers a separate Glitchtip issue. Suggest changing that outer log statement from ERROR to WARNING — this preserves the diagnostic information in logs but prevents Glitchtip from creating a separate issue for it (Glitchtip only captures ERROR and above).

Example:
```
[AI suggestion] This seems to be duplicate of https://redhat.atlassian.net/browse/CCXDEV-12345. The error originates in `storage.go:142` (archive decompression) and is re-logged at ERROR level in `handler.go:89`. Consider lowering the log level in `handler.go:89` from ERROR to WARNING — the root error is already captured by Glitchtip via the original log in `storage.go`, so the second ERROR-level log just creates a duplicate ticket.
```

**Pattern 2: Parametrized error messages.** The error message embeds variable data (e.g., a request ID, item ID, UUID), so Glitchtip treats each unique value as a separate issue. The fix is to remove the variable data from the message string and pass it as a structured field instead. Do NOT suggest lowering the log level — that would silence the error entirely, losing real issues. The error should still be logged at ERROR level, just with a static message so all occurrences group into one Glitchtip issue.

Example:
```
[AI suggestion] This seems to be duplicate of https://redhat.atlassian.net/browse/CCXDEV-12345. Both are "invalid request ID" validation errors from the same code path (`router_utils.go:193 ValidateRequestID`). Glitchtip creates a separate issue for each unique request ID because the ID is embedded in the error message string. To fix, change the log at `router_utils.go:193` from `log.Error().Err(err).Msg(message)` (where `message` contains the request ID) to `log.Error().Str("request_id", requestID).Msg("invalid request ID")` — this keeps the ID as a structured field but uses a static message string, so Glitchtip groups all occurrences into a single issue.
```

Also set the priority to **Low** — the original ticket carries the real priority:

```bash
jira issue edit CCXDEV-XXXXX --priority Low --no-input
```

Do NOT add this ticket to the triaged pool. Move to the next ticket.

#### 4d. Find the source repository

If not a duplicate, you need to investigate the code. First load the `team-info` skill (`skills/team-info/SKILL.md` in the processing-tools repo) — its **Repositories** tables list all team repos and their descriptions, and the **Data Flow** section explains which services share codebases (e.g., archive-sync, dvo-extractor, rules-processing, and rules-uploader are all deployments of insights-ccx-messaging). Use the `project:*` label from the ticket to find the matching repo.

If the team-info skill doesn't resolve it, use these sources:

**Source 1 — the stack trace itself.** The stack trace file paths reveal the real package name:
- Python: the top-level directory in the path (e.g., `ccx_messaging/watchers/stats_watcher.py` → package is `ccx_messaging`, repo is likely `ccx-messaging` or `insights-ccx-messaging`)
- Go: the import path is the repo (e.g., `github.com/RedHatInsights/insights-results-smart-proxy/server` → repo is `insights-results-smart-proxy`). But if the stack trace shows `?` for filenames (common with stripped Go binaries), you only have function names — skip to Source 2 or the naming pattern fallback.

**Source 2 — app-interface deployment configs.** Fetch files listing components from:
- `https://gitlab.cee.redhat.com/service/app-interface/-/tree/master/data/services/insights/ccx-data-pipeline/external-data-pipeline`
- `https://gitlab.cee.redhat.com/service/app-interface/-/tree/master/data/services/insights/ccx-data-pipeline/internal-data-pipeline`

Look for YAML files whose name or content matches the service name. These files contain a `url` field pointing to the source repository.

**Fallback — try naming patterns** (always SSH). The RedHatInsights org frequently uses an `insights-` prefix, so try multiple variants:
- `git@github.com:RedHatInsights/{service-name}.git`
- `git@github.com:RedHatInsights/insights-{service-name}.git`
- `git@github.com:RedHatInsights/insights-{package-name}.git` (from stack trace)
- `git@gitlab.cee.redhat.com:ccx/{service-name}.git`
- `git@gitlab.cee.redhat.com:ccx/{package-name}.git`

If none of these work, ask the user which repo contains the service.

#### 4e. Investigate the root cause

Clone the repo (shallow clone to save time/space):

```bash
git clone --depth 1 <repo-url> /tmp/glitchtip-triage/{service-name}
```

If already cloned from a previous ticket, reuse the existing clone.

**Classify the error first.** Not all errors are code bugs. Determine whether this is:

1. **A code bug** — missing input validation, unexpected data format, logic error, unhandled edge case. Proceed with source code investigation below.
2. **An infrastructure/transient error** — database unreachable, connection timeout/refused/reset, Kafka unavailable, upstream service 503. These are caused by deployments, pod restarts, network issues, or resource exhaustion — not code bugs. Use the infrastructure error template in step 4f.
3. **A data quality error** — corrupt input data (e.g., truncated archives, malformed JSON). The error is in the data, not the code. Suggest adding error handling to gracefully skip bad data.

**For code bugs and data quality errors**, investigate:
1. Find the file and line where the error originates. For Go stack traces with `?` filenames, search by function name: `grep -rn "func.*functionName" /tmp/glitchtip-triage/{service-name}/`.
2. Read the surrounding code. Understand the function's purpose, what inputs it expects, and what went wrong.
3. Check if the error is caused by: missing input validation, unexpected data format, configuration issue, race condition, resource exhaustion, or an upstream service failure.
4. Run `git log --oneline -10 -- <file>` to see if a recent change introduced the issue.
5. Formulate a specific, actionable fix.

#### 4f. Set priority and post the triage comment

After classifying the error (step 4e), set the ticket priority. Consider these factors together — no single factor determines priority alone:

- **Classification**: code bug, data quality, or infrastructure/transient
- **Occurrence count**: from Glitchtip (`count`, `firstSeen`/`lastSeen`)
- **Environment**: prod errors are more urgent than stage
- **Data loss risk**: does the error cause data to be silently dropped, truncated, or written incorrectly?
- **Service stability risk**: can the error crash the service, exhaust resources, or trigger a restart loop?
- **User-facing impact**: does the error result in failed API responses, broken UI, or missed notifications?

| Priority | When to use |
|----------|-------------|
| Blocker | Service crash or restart loop in prod; confirmed data loss in prod |
| Critical | Data loss without crash (e.g., failed writes, dropped messages); very high frequency (>1000) user-facing error in prod |
| High | Code bug in prod without data loss; data quality errors in prod with high frequency; infrastructure error indicating a persistent (non-transient) outage |
| Normal | Code bugs in stage; moderate frequency data quality errors; infrastructure errors in prod that are transient and self-healing |
| Low | Low frequency infrastructure/transient errors; infrastructure errors in stage; all duplicates (the original ticket carries the priority) |

```bash
jira issue edit CCXDEV-XXXXX --priority <Blocker|Critical|High|Normal|Low> --no-input
```

In dry-run mode, show the priority that would be set alongside the comment.

**For code bugs and data quality errors**, use this template:

```bash
cat > /tmp/glitchtip-comment.txt << 'COMMENT'
[AI suggestion] **Root cause**: <what causes the error>

**Affected code**: <repo-name — file path:line number>

**Stack trace analysis**: <brief explanation of the error path>

**Suggested fix**: <specific code change or configuration fix>

**Occurrences**: <count from Glitchtip, first/last seen>
COMMENT

jira issue comment add CCXDEV-XXXXX --body "$(cat /tmp/glitchtip-comment.txt)" --no-input
```

**For infrastructure/transient errors**, use this template instead:

```bash
cat > /tmp/glitchtip-comment.txt << 'COMMENT'
[AI suggestion] **Root cause**: Infrastructure/transient — <what external dependency failed and how>

**Affected service**: <service name, environment>

**Error pattern**: <connection refused/timeout/reset/unavailable — target address and port if visible>

**Assessment**: This is not a code bug. The error occurs when <dependency> is temporarily unreachable, likely due to <deployments/restarts/network issues>. <If count is high: "The high occurrence count (N) suggests an extended outage window.">

**Suggested action**: <If the error is logged at ERROR level in multiple code paths, suggest consolidating or lowering log level to WARNING to reduce Glitchtip noise. If transient and self-healing, suggest monitoring rather than code changes.>

**Occurrences**: <count from Glitchtip, first/last seen>
COMMENT

jira issue comment add CCXDEV-XXXXX --body "$(cat /tmp/glitchtip-comment.txt)" --no-input
```

In dry-run mode, display the comment content and target ticket without posting.

**Add this ticket to the triaged pool** (with its stack trace and root-cause comment) so subsequent tickets can be matched against it.

### Phase 5: Summary

After processing all tickets, present a summary:

```
## Triage Summary

**Processed**: X tickets
**Duplicates found**: Y (linked to originals)
**Root causes identified**: Z
**Could not resolve**: W (reasons listed below)

### Duplicate chains
- CCXDEV-111, CCXDEV-222 → duplicate of CCXDEV-333 (same ValueError in archive-sync storage.go:142)

### Root causes found
- CCXDEV-444: Missing null check in config parser (insights-results-smart-proxy)
- CCXDEV-555: Decompression failure on corrupted archive (archive-sync)

### Unresolved
- CCXDEV-666: Glitchtip issue deleted, no stack trace available
```

### After triage

Clean up cloned repos:
```bash
rm -rf /tmp/glitchtip-triage/
```

## Important guidance

- **Be conservative with duplicates.** Only mark as duplicate when the stack traces confirm the same root cause. Similar ticket summaries are not sufficient — always compare the actual Glitchtip logs. When uncertain, investigate the error individually rather than marking as duplicate.
- **Check event times for duplicates.** Overlapping `firstSeen`/`lastSeen` windows strengthen a duplicate match. Errors that occurred weeks apart may be separate incidents even if the stack traces look similar.
- **Infrastructure duplicates are an exception.** When multiple tickets from the same service and environment show connection failures (refused/timeout/reset) to the same IP:port within overlapping time windows, they share a root cause even if the stack traces diverge at different error-handling branches.
- **Only match against the triaged pool.** The triaged pool contains only tickets with genuine root-cause analysis. Tickets marked as duplicates never enter the pool. This ensures duplicate chains always point to a properly investigated original, never to another duplicate.
- **Never modify or delete existing comments.** Only add new `[AI suggestion]` comments.
- **One comment per ticket.** If you find both a duplicate relationship and a root cause, prefer the duplicate comment (the original ticket should have the root cause analysis).
- **Respect rate limits.** Space Glitchtip API calls with a brief pause (1-2 seconds between requests) if processing many tickets.
