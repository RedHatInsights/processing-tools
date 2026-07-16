---
name: quarterly-connection-jiras
description: >-
  Generate a report of what you have worked on in a given quarter.
  The Quarterly Connection is something all Red Hat users must complete
  after a quarter has ended. There you talk what you have accomplished, the
  goals you had and the goals you want to set up for the next quarter.
  Most of this information is already in Jira, so we can use that to generate
  the report and help the user remember what they have done in those months.
  This should be used when the user asks for help writing the quarterly
  connection on Workday.
---

# quarterly-connection-jiras

Produce a quarter status report for CCX Core - Processing epics owned by the
given user and for a given quarter.

## Pre-requisites

Use the **Atlassian MCP** server (`plugin-atlassian-atlassian`).
If tools are unavailable, call `mcp_auth` first, then retry.

Get `cloudId` via `getAccessibleAtlassianResources` (Red Hat site:
`https://redhat.atlassian.net`).

## Defaults

- **Project:** CCXDEV (override with `--project KEY`)
- **Quarter filter:** Should contain the year and quarter number (e.g. 2026Q2 for April–June 2026)
- **Assignee:** The user's name

## I/O operations

You can use intermediate files to store the information about the epics and
tasks. These files will be deleted after the report is generated. They can be
CSVs or markdown files. You can use Python or shell to work with them.

Use it as a short-term memory so that the context is not oversized.

## Step 1: Find assigned epics

Search with this JQL (adjust labels only if the user specifies otherwise):

```jql
project = {PROJECT}
AND issuetype = Epic
AND fixVersion = "{QUARTER}"
AND assignee = "{ASSIGNEE}"
AND labels in (CCX-PROCESSING, ccx-processing, obsint-processing)
ORDER BY due ASC
```

Call `searchJiraIssuesUsingJql` with fields:
`summary`, `status`, `duedate`, `labels`, `assignee`, `priority`,
`updated`.

### Step 1.1: Gather information about the epics

Use the epic summary, description, comments and status updates to understand
what the epic is about.

Also, collect the number of tasks assigned to the user in that epic vs the total
number of tasks in that epic.

### Step 1.2: If the information is missing or too vague

Ask the user for more information about that specific epic.

## Step 2: Gather other tasks

Sometimes users work on epics that are assigned to others. We need to gather
these tasks as well.

```jql
project = CCXDEV
AND issuetype != Epic
AND fixVersion = "2026Q1"
AND assignee = "Juan Díaz Suárez"
AND parent is not EMPTY
AND assignee was "Juan Díaz Suárez"
ORDER BY parent ASC, updated DESC
```

Use the "Parent" column to group the tasks by epic. You can then use the
Parent key to query the API and get more information about the epics:

```jql
project = CCXDEV
AND issuetype = Epic
AND key in (CCXDEV-123, CCXDEV-456, CCXDEV-789)
ORDER BY due ASC
```

For each epic, collect the same information as in Step 1.1 but also what the
user did specifically in that epic and the amount of work (assigned tasks vs
total number of tasks in that epic).

## Step 3: Write the report

Use this structure for **each epic**, then a summary table.

```markdown
# Assignee Epics — Quarterly Connection ({QUARTER})

---

- **N. [KEY](https://redhat.atlassian.net/browse/KEY)** Summary: X% (done/active) | **Assignee:** Name | **Due:** date or —
  - Description: {description from step 1.1}.
  - **Status update:** whether it was completed, is in progress, or is blocked.
  - Items: completed vs in progress vs not started children tasks

---
```

End with **Summary at a glance**:

| Epic | Completion | Summary |
|------|------------|---------|

Add a short **Highlights** paragraph (2–4 sentences): busiest epics,
blockers, epics that slipped (yellow/red), tasks with no movement.

## Output rules

- Link every epic and key task to `https://redhat.atlassian.net/browse/{KEY}`.
- Be factual; do not invent progress not visible in Jira.
- If Status Summary text is truncated in the API (`...`), present
  what is available and link to the epic for the full text.
- Do not create or edit Jira issues unless the user explicitly asks.

Export the report as a markdown file named
`quarterly-connection-{QUARTER}-jiras.md` (e.g. `quarterly-connection-2026Q2-jiras.md`).

## Example trigger phrases

- "Generate the quarterly connection report for 2026Q1 and Juan Díaz Suárez"
- "Help me write my quarterly connection?"

## Quick reference — MCP calls

```
getAccessibleAtlassianResources → cloudId
searchJiraIssuesUsingJql       → epic list (Step 1)
searchJiraIssuesUsingJql       → child issues, one epic per call, paginate
getJiraIssue(expand=changelog,comments) → status updates per epic
```
