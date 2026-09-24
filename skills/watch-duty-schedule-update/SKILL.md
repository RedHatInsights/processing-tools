---
name: watch-duty-schedule-update
description: Update the CCX processing watch-duty (IC) rotation from a natural-language instruction by editing the schedule YAML in app-interface and opening a merge request. Use when asked to change who is on watch duty, e.g. "make @user the assignee next Thursday", "swap on-call for next week", "add a one-day override".
---

# Watch Duty — Schedule Updater

Applies a plain-language change to the on-call / watch-duty rotation. The source
of truth is a YAML file in the app-interface repo; this skill edits that file on
a branch and opens a merge request for review.

This skill **writes** to app-interface (via a reviewable MR). To *create Jira
tasks* from the schedule, use `watch-duty-jira-tasks` instead.

## When to use

- "Update the watch duty for next Thursday so @user is assigned just that day"
- "Swap next week's on-call from @a to @b"
- "Add a one-day override for @user"

## Prerequisites

- **SSH access to `gitlab.cee.redhat.com`** as yourself. Verify with
  `ssh -T git@gitlab.cee.redhat.com` (should print `Welcome to GitLab, @you!`).
- A **personal fork** of app-interface (e.g. `jsegural/app-interface`). You
  **cannot push to `service/app-interface` directly** — pushes are rejected with
  "You are not allowed to push code to this project." Check your fork exists:
  `git ls-remote git@gitlab.cee.redhat.com:<you>/app-interface.git HEAD`. If it
  doesn't, create the fork once via the GitLab web UI.
- **PyYAML** for the fetch/resolve scripts and validation
  (`pip install pyyaml` or `dnf install python3-pyyaml`). The scripts fail with
  `ModuleNotFoundError: No module named 'yaml'` without it.
- `glab` and a `GITLAB_TOKEN` are **not required** — the MR is opened with git
  push options over SSH (see step 6).

## Write path: fork clone + push-options MR

1. **Read the current schedule for context** (public HTTPS read, no auth):
   ```bash
   ./scripts/fetch_schedule.sh > /tmp/ic-schedule.yml
   ./scripts/resolve_duty.py <date> < /tmp/ic-schedule.yml   # who is on duty now
   ```

2. **Clone app-interface — full commit history, blobless. Do NOT use
   `--depth 1`.** app-interface is one of the largest repos on the server; a
   shallow clone breaks push negotiation against your (diverged) fork and makes
   the later push try to transfer the *entire* history — it will hang/time out.
   A blobless, sparse clone is cheap and negotiates correctly:
   ```bash
   git clone --filter=blob:none --sparse \
     git@gitlab.cee.redhat.com:service/app-interface.git /tmp/app-interface
   cd /tmp/app-interface
   git sparse-checkout set data/teams/insights/schedules
   git remote add fork git@gitlab.cee.redhat.com:<you>/app-interface.git
   git fetch fork          # gives push a common ancestor to negotiate against
   ```
   (If you already have a `--depth 1` clone lying around, fix it with
   `git fetch --unshallow --filter=blob:none origin` before pushing.)

3. **Parse the request into a concrete change** — dates, user, and whether it's
   a permanent rotation change or a one-day override (see "Kinds of change").

4. **Edit** `data/teams/insights/schedules/ccx-processing-ic.yml` on a new
   branch (`git checkout -b ccx-ic-override-<user>-<YYYY-MM-DD>`).

5. **Validate before committing** (see "Validation").

6. **Commit, push to your fork, and open the MR with git push options.** This is
   the path that works without `glab` or a token:
   ```bash
   git push -u fork <branch> \
     -o merge_request.create \
     -o merge_request.target=master \
     -o merge_request.target_project=service/app-interface \
     -o merge_request.remove_source_branch \
     -o merge_request.title="CCX IC: <one-line summary>" \
     -o merge_request.description="<what changed and why>"
   ```
   The push output prints the MR URL (`View merge request for <branch>: …`).
   Report that link to the user. **Never merge it** — leave it for review.

## Kinds of change

An entry is a half-open interval `[start, end)` on **06:00→06:00 day
boundaries** (times are in the schedule's local convention — a "day" runs from
06:00 to 06:00 the next day):

```yaml
- start: '2026-08-31 06:00'
  end: '2026-09-07 06:00'
  users:
  - $ref: /teams/insights/users/ccx/jsegural.yml
```

**One-day override** — reassign a single day while keeping the rest of the week
with the original person. **Split the containing week into up to three
contiguous entries** and change the assignee on the middle one only. Example:
override just 2026-09-03 to `jdiazsua`, leaving the rest with `jsegural`:

```yaml
- start: '2026-08-31 06:00'      # unchanged head of week
  end: '2026-09-03 06:00'
  users:
  - $ref: /teams/insights/users/ccx/jsegural.yml
- start: '2026-09-03 06:00'      # the override (06:00 → 06:00 next day)
  end: '2026-09-04 06:00'
  users:
  - $ref: /teams/insights/users/ccx/jdiazsua.yml
- start: '2026-09-04 06:00'      # unchanged tail of week
  end: '2026-09-07 06:00'
  users:
  - $ref: /teams/insights/users/ccx/jsegural.yml
```
(If the target day is the first or last day of the week, you only need two
entries.)

**Whole-week swap** — change the `$ref` on the entry whose interval contains the
requested week. No splitting needed.

## Guidance / guardrails

- **Username resolution:** an `org_username` maps to
  `$ref: /teams/insights/users/ccx/<org_username>.yml`. Before committing,
  confirm the user is real — cheapest check is that the username already appears
  somewhere in the schedule; otherwise verify the user YAML exists in
  app-interface. The Jira assignee (for the companion skill) is
  `<org_username>@redhat.com`.
- **Date parsing:** resolve relative dates ("tomorrow", "next Thursday")
  against today's date, then map to the 06:00→06:00 day boundary. State the
  concrete resolved date(s) back to the user in your summary.
- **Branch / MR naming:** branch `ccx-ic-override-<user>-<YYYY-MM-DD>` (or
  `-swap-` for week swaps); MR title `CCX IC: <one-line summary>`.

## Validation

Parse the edited file and assert intervals are well-formed. Note the file may
already contain pre-existing schema violations (e.g. an interval with
`start > end` from years past) — compare against the baseline rather than
failing outright; only flag issues your edit introduced.

```python
import yaml
from datetime import datetime
f = "/tmp/app-interface/data/teams/insights/schedules/ccx-processing-ic.yml"
sched = yaml.safe_load(open(f))["schedule"]
p = lambda s: datetime.strptime(str(s), "%Y-%m-%d %H:%M")
# every interval start < end, and the entries you touched have no gaps/overlaps
for e in sched:
    assert p(e["start"]) < p(e["end"]) or print("pre-existing bad:", e["start"])
```

Also eyeball `git diff` — it should show only the intended entry split/swap.

## Notes

- Schedule path in app-interface:
  `data/teams/insights/schedules/ccx-processing-ic.yml`
- Editing the source of truth requires review — never commit to the default
  branch and never merge your own MR; always leave it for review.
- Docs: https://ccx.pages.redhat.com/ccx-docs/docs/processing/on_call_duty/
