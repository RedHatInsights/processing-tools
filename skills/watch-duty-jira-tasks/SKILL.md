---
name: watch-duty-jira-tasks
description: Read the CCX processing watch-duty (IC) rotation YAML from app-interface and ensure a Jira task exists and is correctly assigned for each requested week. Use when asked to "create watch-duty Jira tickets", "generate on-call tasks", or reconcile the rota tasks for given dates/weeks.
---

# Watch Duty — Jira Task Creator

For the week(s)/date(s) the user asks about, this skill:

1. Reads the on-call rotation (source of truth: a YAML file in app-interface).
2. Finds the engineer assigned that week.
3. Checks Jira for an existing watch-duty task for that week.
   - **If it exists**, ensures it is assigned to the engineer from the YAML
     (updating the assignee if it differs).
   - **If it does not exist**, creates the task from the template.

This skill is **read-only** against app-interface and can **create/update**
issues in Jira (project **CCXDEV**) when the user confirms write mode. It also
supports a **dry-run/test mode** that reports the exact planned Jira changes
without creating or editing anything. To *edit the rotation itself*, use
`watch-duty-schedule-update`.

## Prerequisites

Schedule resolution requirements:

- `curl` (used by `scripts/fetch_schedule.sh`).
- `python3` with PyYAML (used by `scripts/resolve_duty.py`).
- Network access to `gitlab.cee.redhat.com` (public read of the schedule).
- If the schedule becomes private, export `GITLAB_TOKEN` with read access.

Jira access requirements — use **one** of these backends:

1. **Jira MCP server** (preferred when available in the agent harness):
   - Use the Atlassian/Jira MCP server tools.
   - If tools are unavailable, authenticate first (for example with `mcp_auth`,
     when supported by the harness), then retry.
   - Get `cloudId` once per session with `getAccessibleAtlassianResources`
     and pass it to every Jira MCP call.
2. **acli** (Atlassian CLI) configured and authenticated:
   - Install docs: https://developer.atlassian.com/cloud/acli/guides/install-acli/
   - Verify with `acli --version`.

## When to use

- "Create the watch-duty Jira tickets for the next few weeks"
- "Make sure the on-call tasks for September are assigned correctly"

## Step 1 — Resolve who is on duty

Fetch the schedule and resolve the engineer(s) for each requested date. Pass the
dates the user cares about (one per week is enough — any date inside a week
resolves that week's entry):

```bash
cd skills/watch-duty-jira-tasks
./scripts/fetch_schedule.sh | ./scripts/resolve_duty.py --json 2026-09-03 2026-09-10
```

Output per date: `found`, the week `start`/`end`, and each engineer's
`org_username` and derived `email` (`<org_username>@redhat.com`). The Jira
assignee is derived from that email. Also derive the Jira fix version from the
year and quarter of the week assignment date: `YYYYQN` (for example,
weeks 44–47 of 2026 are in Q4, so use `2026Q4`). Skip dates where `found` is
false and tell the user.

## Step 2 — Choose run mode and Jira backend

### Run mode

Use **dry-run/test mode by default** unless the user explicitly asks to apply the
changes or confirms after reviewing the plan.

- **Dry-run/test mode:** resolve the schedule and search Jira, then print the
  actions that would be taken. Do **not** call `createJiraIssue`,
  `editJiraIssue`, `transitionJiraIssue`, or any `acli` command that writes to
  Jira.
- **Apply/write mode:** after user confirmation, perform the create/reassign
  operations and report the resulting Jira keys.

Dry-run output must include enough detail for review:

```text
DRY RUN — no Jira changes will be made.

Week: 2026-09-03 → 2026-09-10
Engineer: jdoe <jdoe@redhat.com>
Planned action: create Jira task
Project: CCXDEV
Issue type: <TYPE>
Summary: <SUMMARY with week + engineer>
Assignee: jdoe@redhat.com
Labels: <labels, always including obsint-processing>
Fix version: 2026Q4
Sprint: <sprint name/id whose timespan contains the week start, or "not found">
Due date / custom fields: <field values>
Description:
<full multi-paragraph description body>
```

For an existing task with a different assignee, fix version, and/or sprint,
dry-run output should say:

```text
DRY RUN — no Jira changes will be made.

Week: 2026-09-03 → 2026-09-10
Existing task: CCXDEV-123 https://redhat.atlassian.net/browse/CCXDEV-123
Planned action: reassign from <current assignee> to jdoe <jdoe@redhat.com>
Planned action: update fix version from <current fix version> to 2026Q4
Planned action: move to sprint <sprint name/id>
```

Only include the action lines that are needed. If the task is already correct,
dry-run output should say `already correct` and show the matching issue key/link.

### Jira backend

Use the Jira MCP path when MCP tools are available. Use the acli path when MCP
is unavailable or the user explicitly asks for CLI commands.

The same safety rules apply to both backends and both run modes:

- Build one JQL per week using the convention below.
- **0 matches** → plan or create the task (Step 4a).
- **1 match** → plan or verify/fix assignee (Step 4b).
- **>1 matches** → do not guess; report the duplicates to the user.

## Step 3 — Look up existing Jira tasks

Search CCXDEV for an existing watch-duty task for the week.

> **TODO (user to provide): JQL convention.** The exact JQL that identifies a
> watch-duty task for a given week — which field carries the week/date and its
> format. Placeholder shape:
> `project = CCXDEV AND <field> = "<week-date>" AND <watch-duty filter>`

### Option A — Jira MCP lookup

Use MCP from `codemode` or the harness MCP tool interface. Do not try to call
MCP tools from a shell script.

Required MCP operations:

- `getAccessibleAtlassianResources` → choose the Red Hat site
  (`https://redhat.atlassian.net`) and cache its `cloudId`.
- `searchJiraIssuesUsingJql` → find matching task(s). Request fields such as
  `summary`, `status`, `assignee`, `fixVersions`, `customfield_10020` (Sprint),
  `duedate`, `labels`, `parent`, and `updated`.
- `getJiraIssue` → read a single issue if the search result does not contain
  enough assignee/detail fields.

Example codemode shape:

```javascript
const resources = await tools.mcp__jira__getAccessibleAtlassianResources({});
const cloudId = /* pick Red Hat / redhat.atlassian.net from resources */;
const jql = 'project = CCXDEV AND <field> = "2026-09-03" AND <watch-duty filter>';

const matches = await tools.mcp__jira__searchJiraIssuesUsingJql({
  cloudId,
  jql,
  fields: ['summary', 'status', 'assignee', 'fixVersions', 'customfield_10020', 'duedate', 'labels', 'parent', 'updated'],
  maxResults: 10,
  view: 'evidence',
});
```

If you need an assignee account ID, resolve it before create/edit. Prefer the
assignable-user operation (it validates project/issue assignability); discover it
if it is not exposed as a primary tool:

```javascript
// Discover once if needed:
// await tools.mcp__jira__discover({query: 'find assignable Jira users for a project by email'});

const assignable = await tools.mcp__jira__executeRead({
  cloudId,
  name: 'listJiraIssueAssignableUsers',
  inputs: {project: 'CCXDEV', query: '<org_username>@redhat.com'},
});
const assigneeAccountId = /* choose the matching active user accountId */;
```

If possible, resolve the sprint before creating/updating the Jira task. Use the
Sprint custom field on recent watch-duty tasks to identify the board. Existing
processing watch-duty tasks have shown Sprint field `customfield_10020` with
board ID `1553`; prefer deriving this from Jira data rather than hard-coding it.
Then list/resolve sprints on that board and pick the sprint whose timespan
contains the watch-duty week start (`start <= week_start < end`). If no sprint
contains the week start, leave sprint assignment out and report that it could not
be determined.

```javascript
// Discover once if needed:
// await tools.mcp__jira__discover({query: 'list Jira sprints on board with startDate endDate'});

const sprintData = await tools.mcp__jira__executeRead({
  cloudId,
  name: 'getJiraBoardSprintData',
  inputs: {boardId: '<BOARD-ID-FROM-EXISTING-WATCH-DUTY-TASK>', includeIssues: false},
});
const sprintId = /* choose sprint where startDate <= week start < endDate */;
```

### Option B — acli lookup

```bash
acli jira workitem search --jql '<JQL — SEE ABOVE>'
```

## Step 4a — Create or plan the task (no existing task)

> **TODO (user to provide): task template.** Issue type, summary format,
> description body, labels, due/start date mapping (which YAML field → which Jira
> field + format), and any other fields (priority/components/parent).
>
> Required field convention: set Jira `fixVersion` / `fixVersions` to the
> assignment quarter in the form `YYYYQN`, where `YYYY` is the year of the week
> assignment date and `N` is the quarter number. Examples: a task for
> 2026-11-09 uses `2026Q4`; a task for 2027-01-05 uses `2027Q1`.
>
> Required label convention: always add label `obsint-processing`, even when the
> Jira template does not include it. Preserve template labels such as
> `CCX-PROCESSING` and `maintenance` unless the user says otherwise.

First render the full intended issue payload from the template: project, issue
type, summary, description, assignee, labels (including `obsint-processing`),
fix version, sprint (if found), due/start/custom fields, priority, components,
parent, etc.

- In **dry-run/test mode**, stop here and print the full payload using the
  dry-run format from Step 2. Do not call create commands.
- In **apply/write mode**, create the Jira task with one of the backend-specific
  commands below.

### Option A — Jira MCP create

Use `createJiraIssue`. Its `assignee` parameter expects an Atlassian `accountId`,
not an email address; resolve it with `listJiraIssueAssignableUsers` first.

```javascript
const created = await tools.mcp__jira__createJiraIssue({
  cloudId,
  projectKey: 'CCXDEV',
  issueType: '<TYPE>',
  summary: '<SUMMARY with week + engineer>',
  description: '<DESCRIPTION>',
  assignee: assigneeAccountId,
  labels: ['CCX-PROCESSING', 'maintenance', 'obsint-processing'],
  assignToSprint: '<SPRINT-ID-OR-EXACT-SPRINT-NAME>', // only when resolved
  // priority: '<PRIORITY>',
  // parent: '<PARENT-KEY>',
  additional_fields: {
    fixVersions: [{name: '<YYYYQN>'}],
    // duedate: 'YYYY-MM-DD',
    // ...
  },
});
```

If Jira rejects a field, follow the MCP tool `repairHint`/allowed-values output
and retry with the corrected field shape. If creation succeeds but a secondary
operation (for example sprint assignment) fails, do **not** create a duplicate;
report/fix the secondary operation separately.

### Option B — acli create

```bash
acli jira workitem create \
  --project CCXDEV \
  --type '<TYPE>' \
  --summary '<SUMMARY with week + engineer>' \
  --description '<DESCRIPTION>' \
  --assignee '<org_username>@redhat.com'
  # + labels including obsint-processing / fixVersion=<YYYYQN> / sprint=<resolved sprint> / due date / other fields per template
```

> Note: `acli` create/assign flag names were not verified in this environment.
> Confirm with `acli jira workitem create --help` and
> `acli jira workitem assign --help`.

## Step 4b — Verify / plan / fix assignee, fix version, and sprint (existing task)

Compare the task's current assignee, fix version, and sprint to the expected
values from the YAML/date. With MCP, compare the Jira assignee account/user
returned by the issue/search result to the account resolved from
`<org_username>@redhat.com`, compare `fixVersions` to the expected `YYYYQN`, and
compare Sprint (`customfield_10020`) to the sprint whose timespan contains the
week start. With acli, compare the viewed assignee, fix version, and sprint to
those expected values.

If assignee, fix version, and sprint already match, leave it unchanged and report
"already correct".

If any of assignee, fix version, or sprint differs:

- In **dry-run/test mode**, report the planned reassignment, fix-version update,
  and/or sprint move and do not call edit, transition, or assign commands.
- In **apply/write mode**, update the issue with one of the backend-specific
  commands below.

### Option A — Jira MCP update

Resolve the assignee account ID, then edit the issue. For an existing issue,
prefer `listJiraIssueAssignableUsers` with `issueKey` because Jira evaluates
issue-level permissions/security.

```javascript
const assignable = await tools.mcp__jira__executeRead({
  cloudId,
  name: 'listJiraIssueAssignableUsers',
  inputs: {issueKey: '<KEY>', query: '<org_username>@redhat.com'},
});
const assigneeAccountId = /* choose the matching active user accountId */;

const updated = await tools.mcp__jira__editJiraIssue({
  cloudId,
  issueIdOrKey: '<KEY>',
  fields: {
    assignee: {accountId: assigneeAccountId},
    fixVersions: [{name: '<YYYYQN>'}],
  },
});

// Move to the sprint separately if a sprint was resolved and it differs.
const moved = await tools.mcp__jira__transitionJiraIssue({
  cloudId,
  issueIdOrKey: '<KEY>',
  sprintId: <SPRINT-ID>,
});
```

### Option B — acli view/update

```bash
acli jira workitem view {KEY}
```

If the assignee differs (or is empty), reassign to the YAML engineer:

```bash
acli jira workitem assign --key {KEY} --assignee '<org_username>@redhat.com'
```

If the fix version differs, update it to `<YYYYQN>` using the appropriate acli
field-edit syntax for `fixVersion`/`fixVersions` after confirming it with
`acli jira workitem edit --help`.

If the sprint differs and a target sprint was resolved, move the task to that
sprint using the appropriate acli sprint/board command after confirming it with
`acli jira workitem --help` / `acli jira sprint --help`.

## Step 5 — Report

Summarize per week:

- In dry-run/test mode: `would create`, `would reassign {KEY} to <engineer>`,
  `would update fix version {KEY} to <YYYYQN>`, `would move {KEY} to sprint
  <sprint>`, `already correct {KEY}`, `skipped (no schedule entry)`, or
  `ambiguous (multiple tasks)`.
- In apply/write mode: `created {KEY}`, `reassigned {KEY} to <engineer>`,
  `updated fix version {KEY} to <YYYYQN>`, `moved {KEY} to sprint <sprint>`,
  `already correct {KEY}`, `skipped (no schedule entry)`, or
  `ambiguous (multiple tasks)`.

Always include Jira links for existing/created issues. For planned creations,
include the labels (including `obsint-processing`), fix version, sprint (or that
no matching sprint was found), full summary, and full multi-paragraph description
so the user can review the exact Jira task before it is created.

## Reference

- Skill scripts:
  - `scripts/fetch_schedule.sh`: fetches the schedule YAML from app-interface via
    the GitLab raw-file API.
  - `scripts/resolve_duty.py`: parses YAML and resolves requested dates to
    schedule entries; supports JSON output for automation.
- Schedule path: `data/teams/insights/schedules/ccx-processing-ic.yml`
- Schedule YAML entry: `start`, `end`, `users: [{$ref: .../<org_username>.yml}]`
  — interval is `[start, end)` (start inclusive, end exclusive).
- Fix version convention: derive from the assignment date as `YYYYQN`; weeks 44,
  45, 46, and 47 of 2026 should all use `2026Q4`.
- Label convention: always include `obsint-processing` on created watch-duty
  tasks, even if it is missing from the Jira template.
- Sprint convention: when Jira exposes sprint metadata, assign the task to the
  sprint whose `[startDate, endDate)` interval contains the watch-duty week
  start. Derive the board from existing watch-duty tasks' Sprint field when
  possible (recent examples showed `customfield_10020` on board `1553`).
- Docs: https://ccx.pages.redhat.com/ccx-docs/docs/processing/on_call_duty/
- Jira project: **CCXDEV**
