---
name: scrum-of-scrums
description: >-
  Generate the weekly Processing team Scrum of Scrums report from
  Jira epics. Compares progress over the last 7 days (report day
  is usually Wednesday): child-task movement, epic completion %,
  and epic status updates. Use when the user asks for a scrum of
  scrums, SoS report, weekly epic status, processing epic report,
  or Wednesday status report.
---

# scrum-of-scrums

Produce a weekly status report for **CCX Core - Processing** epics.
The report compares **the last 7 days** of activity and is normally
run on **Wednesdays** (report period: previous Wednesday through today).

## Pre-requisites

Use the **Atlassian MCP** server (`plugin-atlassian-atlassian`).
If tools are unavailable, call `mcp_auth` first, then retry.

Get `cloudId` via `getAccessibleAtlassianResources` (Red Hat site:
`https://redhat.atlassian.net`).

## Defaults

- **Project:** CCXDEV (override with `--project KEY`)
- **Epic status filter:** In Progress only (skip New, To Do, Closed, Done, Resolved)

## Step 1: Find in-progress epics

Search with this JQL (adjust labels only if the user specifies otherwise):

```jql
project = {PROJECT}
AND issuetype = Epic
AND status = "In Progress"
AND fixVersion = "{CURRENT_QUARTER}"
AND labels in (CCX-PROCESSING, ccx-processing, obsint-processing)
ORDER BY due ASC
```

Derive the fix version from today's date: {YEAR}Q{QUARTER} (e.g. 2026Q2 for April–June 2026).

Call `searchJiraIssuesUsingJql` with fields:
`summary`, `status`, `duedate`, `labels`, `assignee`, `priority`,
`updated`.

If the user provides a different JQL or epic list, use that instead.

## Step 2: Check if the epic has a detailed status report

In case the epic has a detailed status report (including issues completion),
use that and jump to step.

## Step 3: If the status update is missing or too vague

Make use of the `lenasolarova/skills/epic-status-update` skill to generate
a status update for the epic. Don't add any comment to the epic, unless
the user explicitly asks for it.

## Step 4: Write the report

Use this structure for **each epic**, then a summary table.

```markdown
# Processing Epics — Weekly Report ({start}–{end})

Report period: last 7 days. Completion % = closed child issues / active child issues.

---

- **N. [KEY](https://redhat.atlassian.net/browse/KEY)** Summary: X% (done/active) | **Assignee:** Name | **Due:** date or —
  - **Status update ({date}):** text from Status Summary or comment.
  - Last 7 days: {N closed, M active, or "No task movement"}.
  - Closed: nested bullet list
  - In progress / review: nested bullet list

---
```

End with **Summary at a glance**:

| Epic | Completion | Closed this week | Health trend |
|------|-----------|------------------|--------------|

Add a short **Highlights** paragraph (2–4 sentences): busiest epics,
blockers, epics that slipped (yellow/red), epics with no movement.

## Output rules

- Link every epic and key task to `https://redhat.atlassian.net/browse/{KEY}`.
- Be factual; do not invent progress not visible in Jira.
- If an epic has open child issues (`To Do`, `In Progress`, etc.),
  completion % must be below 100% — re-check pagination if it shows 100%
  while the epic is still In Progress.
- If an epic has no child issues from either query, report `0% (0/0)` and
  note that work may be tracked outside Epic Link / parent.
- If Status Summary text is truncated in the API (`...`), present
  what is available and link to the epic for the full text.
- Do not create or edit Jira issues unless the user explicitly asks.

Export the report as a markdown file.

## Example trigger phrases

- "Generate the scrum of scrums report"
- "Weekly epic status for processing"
- "What changed in our epics since last Wednesday?"
- "SoS report"

## Quick reference — MCP calls

```
getAccessibleAtlassianResources → cloudId
searchJiraIssuesUsingJql       → epic list (Step 1)
searchJiraIssuesUsingJql       → child issues, one epic per call, paginate
getJiraIssue(expand=changelog,comments) → status updates per epic
```
