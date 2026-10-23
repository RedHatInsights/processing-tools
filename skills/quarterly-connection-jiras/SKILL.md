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

## Access requirements

Default Jira site: `https://redhat.atlassian.net`.
Default project: `CCXDEV`.
Default board: `1553` / **CCX Core - Processing**.

Preferred Pi-compatible access path:

- **`acli`** for Jira searches and issue reads. Verify with:
  ```bash
  acli jira auth status
  acli jira project view --key CCXDEV --json
  acli jira board view --id 1553 --json
  ```
- **`curl --netrc`** for read-only Jira REST fallback when `acli` cannot fetch
  a needed field such as changelog/comments. Verify with:
  ```bash
  curl --netrc https://redhat.atlassian.net/rest/api/3/myself
  ```
- **Atlassian MCP** (`plugin-atlassian-atlassian`) is optional. If MCP tools are
  available, you may use `getAccessibleAtlassianResources`,
  `searchJiraIssuesUsingJql`, and `getJiraIssue`; otherwise use `acli`/REST.

Do not create, edit, comment on, link, or transition Jira issues for this report
unless the user explicitly asks. Never ask the user to paste Jira tokens.

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

Collect these fields: `key`, `summary`, `status`, `duedate`, `labels`,
`assignee`, `priority`, `updated`.

Use one of these access paths:

- MCP, if available: call `searchJiraIssuesUsingJql` with the fields above.
- Pi default: use `acli` and JSON output:
  ```bash
  acli jira workitem search \
    --jql '<JQL from above>' \
    --fields key,summary,status,duedate,labels,assignee,priority,updated \
    --paginate \
    --json
  ```

### Step 1.1: Gather information about the epics

Use the epic summary, description, comments and status updates to understand
what the epic is about. With `acli`, fetch issue details like this:

```bash
acli jira workitem view {EPIC_KEY} \
  --fields key,summary,status,assignee,description,comment,updated \
  --json
```

If changelog/status-history detail is needed and not available through `acli`,
use read-only Jira REST with `curl --netrc`:

```bash
curl --netrc \
  'https://redhat.atlassian.net/rest/api/3/issue/{EPIC_KEY}?expand=changelog&fields=summary,status,assignee,description,comment,updated'
```

Also, collect the number of tasks assigned to the user in that epic vs the total
number of tasks in that epic.

### Step 1.2: If the information is missing or too vague

Ask the user for more information about that specific epic.

## Step 2: Gather other tasks

Sometimes users work on epics that are assigned to others. We need to gather
these tasks as well.

```jql
project = {PROJECT}
AND issuetype != Epic
AND fixVersion = "{QUARTER}"
AND assignee = "{ASSIGNEE}"
AND parent is not EMPTY
AND assignee was "{ASSIGNEE}"
ORDER BY parent ASC, updated DESC
```

Use the "Parent" column to group the tasks by epic. You can then use the
Parent key to query the API and get more information about the epics:

```jql
project = {PROJECT}
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

## Quick reference — Jira access

Preferred Pi CLI path:

```bash
acli jira auth status
acli jira workitem search --jql '<JQL>' --fields key,summary,status,duedate,labels,assignee,priority,updated --paginate --json
acli jira workitem view CCXDEV-123 --fields key,summary,status,assignee,description,comment,updated --json
curl --netrc 'https://redhat.atlassian.net/rest/api/3/issue/CCXDEV-123?expand=changelog&fields=summary,status,assignee,description,comment,updated'
```

Optional MCP path, when available:

```text
getAccessibleAtlassianResources → cloudId
searchJiraIssuesUsingJql       → epic/task lists
getJiraIssue(expand=changelog,comments) → status updates per epic
```
