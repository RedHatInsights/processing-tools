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

Produce a quarter status report for CCX Core - Processing epics owned by or
contributed to by the given user for a given quarter. Contributions include
assigned work, historical assignee work, reported work, and Jira issues where
the user added quarter-relevant comments.

## Access requirements

Default Jira site: `https://redhat.atlassian.net`.
Default project: `CCXDEV`.
Default board: `1553` / **CCX Core - Processing**.

Use any authenticated, read-only Jira access path available in the local
environment. Keep the skill tool-agnostic: prefer the most complete/reliable
tool for each query, and fall back as needed. Common paths, in recommended order
for RH Jira today:

- **`acli`** for auth checks and simple Jira searches/issue reads. Verify with:
  ```bash
  acli jira auth status
  acli jira project view --key CCXDEV --json
  acli jira board view --id 1553 --json
  ```
- **`curl --netrc`** for read-only Jira REST when a `.netrc` entry for
  `redhat.atlassian.net` is already configured and `acli` cannot fetch a needed
  field such as `parent`, `duedate`, `updated`, changelog, or comments. Verify
  with:
  ```bash
  curl --netrc https://redhat.atlassian.net/rest/api/3/myself
  ```
  If this fails because credentials are not configured, use `acli`, MCP, or
  another authenticated read-only access path instead of asking for tokens.
- **Atlassian MCP** (`plugin-atlassian-atlassian`) is optional and should not be
  required. If MCP tools are available, you may use
  `getAccessibleAtlassianResources`, `searchJiraIssuesUsingJql`, and
  `getJiraIssue`; otherwise use `acli`/REST.

Do not create, edit, comment on, link, or transition Jira issues for this report
unless the user explicitly asks. Never ask the user to paste Jira tokens.

## Defaults

- **Project:** CCXDEV (override with `--project KEY`)
- **Quarter filter:** Should contain the year and quarter number (e.g. 2026Q2
  for April–June 2026)
- **Person:** The Quarterly Connection owner's Jira identity. By default this is
  the authenticated Jira user. Resolve the user's Jira identity to an Atlassian
  `accountId` when possible and use display name only for human-facing report
  labels. Treat the user as assignee, historical assignee, reporter, and
  commenter unless the user explicitly asks for a narrower scope.

## I/O operations

You can use intermediate files to store the information about epics, tasks, and
comments. These files should be deleted after the report is generated. They can
be JSON, CSV, or markdown files. Use them as short-term memory so context is not
oversized.

## Jira REST notes

Atlassian removed the old `/rest/api/3/search` endpoint. For REST fallback, use
`/rest/api/3/search/jql` and always paginate with `nextPageToken` until no token
is returned. The helper script in this skill directory keeps pagination logic out
of the skill text and can be used for repeatable REST queries:

```bash
python3 skills/quarterly-connection-jiras/jira_rest_helper.py search \
  --jql '<JQL>' \
  --fields key,summary,status,assignee,reporter,parent,priority,updated,issuetype,fixVersions,labels,duedate,description,comment
```

The helper uses existing REST authentication, such as an already configured
`.netrc` entry; it does not accept raw tokens on the command line.

For one-off checks, this is the first request only; keep following
`nextPageToken` in later requests:

```bash
curl --netrc \
  'https://redhat.atlassian.net/rest/api/3/search/jql?jql=<URL_ENCODED_JQL>&fields=key,summary,status,assignee,reporter,parent,priority,updated,issuetype,fixVersions,labels,duedate,description,comment&maxResults=100'
```

With `acli`, some fields such as `parent`, `duedate`, or `updated` may not be
allowed in `--fields`. If that happens, switch to REST `/search/jql` instead of
retrying the same `acli` command.

Convert `{QUARTER}` to a date range when scanning comments or `updatedBy`, e.g.
`2026Q3` → `2026-07-01` through `2026-09-30`.

## Step 1: Find directly assigned epics

Search with this JQL (adjust labels only if the user specifies otherwise):

```jql
project = {PROJECT}
AND issuetype = Epic
AND fixVersion = "{QUARTER}"
AND assignee = "{PERSON}"
AND labels in (CCX-PROCESSING, ccx-processing, obsint-processing)
ORDER BY due ASC
```

Collect these fields: `key`, `summary`, `status`, `duedate`, `labels`,
`assignee`, `reporter`, `priority`, `updated`, `description`, and `comment`.

Use one of these access paths:

- MCP, if available: call `searchJiraIssuesUsingJql` with the fields above.
- `acli` if the requested fields are supported:
  ```bash
  acli jira workitem search \
    --jql '<JQL from above>' \
    --fields key,summary,status,assignee,priority \
    --paginate \
    --json
  ```
- REST fallback, preferred when field coverage matters: use the `search_jql`
  helper from **Jira REST notes** so results are paginated with `nextPageToken`.

### Step 1.1: Gather information about the epics

Use the epic summary, description, comments, and status updates to understand
what the epic is about. With `acli`, fetch basic details like this:

```bash
acli jira workitem view {EPIC_KEY} \
  --fields key,summary,status,assignee,description,comment,updated \
  --json
```

If changelog/status-history detail is needed, use read-only Jira REST:

```bash
curl --netrc \
  'https://redhat.atlassian.net/rest/api/3/issue/{EPIC_KEY}?expand=changelog&fields=summary,status,assignee,reporter,description,comment,updated,labels,duedate,fixVersions'
```

Also collect direct child-task counts for the epic: direct children
assigned/reported/commented by the user versus all direct children in that epic.
These direct-child totals are useful for Jira-visible epic progress, but they do
not automatically include subtasks grouped under the epic through an ancestor
chain. If you include subtasks in user-involved counts, label that count
separately or resolve ancestors for totals using the same method.

For direct child totals, query:

```jql
project = {PROJECT} AND parent = {EPIC_KEY}
```

and also a quarter-limited version:

```jql
project = {PROJECT} AND parent = {EPIC_KEY} AND fixVersion = "{QUARTER}"
```

### Step 1.2: If the information is missing or too vague

Ask the user for more information about that specific epic.

## Step 2: Gather other epics and tasks in the quarter

Sometimes users work on epics assigned to others, or they reported / previously
owned an epic that has no matching child task. First gather contributed epics
with a dedicated Epic query:

```jql
project = {PROJECT}
AND issuetype = Epic
AND fixVersion = "{QUARTER}"
AND (assignee = "{PERSON}" OR assignee was "{PERSON}" OR reporter = "{PERSON}")
AND labels in (CCX-PROCESSING, ccx-processing, obsint-processing)
ORDER BY due ASC
```

Deduplicate the directly assigned epics from Step 1 and the contributed epics
from this query by issue key before grouping, counting, or writing the report.
Do not list the same epic twice.

Then gather non-Epic child work where the user is current assignee, historical
assignee, or reporter.

```jql
project = {PROJECT}
AND issuetype != Epic
AND fixVersion = "{QUARTER}"
AND parent is not EMPTY
AND (assignee = "{PERSON}" OR assignee was "{PERSON}" OR reporter = "{PERSON}")
ORDER BY parent ASC, updated DESC
```

Prefer REST `/search/jql` for these queries because `acli` may not allow
`parent`, `parentEpic`, or other needed fields in `--fields`.

When grouping non-Epic issues by epic, do not blindly treat `parent` as the epic:
subtasks usually have a Story/Task as their immediate parent. Use `parentEpic`
where Jira returns it; otherwise resolve the parent chain with issue detail
requests until an Epic is found. Keep the original issue filters unchanged while
resolving the ancestor epic. After resolving an ancestor, keep it only when its
Epic key is in the deduplicated Step 1/Step 2 Epic set; discard out-of-scope
ancestors before querying or reporting epic details. If this adds subtasks to the
user's involved-work count, make the scope explicit: direct Epic child totals may
differ from ancestor-grouped user-involved issues.

For each parent/ancestor epic, query the epic details:

```jql
project = {PROJECT}
AND issuetype = Epic
AND key in (CCXDEV-123, CCXDEV-456, CCXDEV-789)
ORDER BY due ASC
```

For each epic, collect the same information as in Step 1.1 plus:

- what the user did specifically in that epic
- the amount of work in the quarter (direct user-involved child tasks vs all
  direct quarter child tasks, plus separately labeled ancestor-grouped subtasks
  when applicable)
- overall epic child status counts when useful (closed / in progress / not
  started)
- whether a task was included because of current assignment, assignment history,
  reporter, or comments

## Step 3: Gather quarter comments by the user

Also check Jira issues where the user commented during the quarter. This catches
cross-quarter follow-ups, verification comments, CVE checks, and work that may
not have the quarter fixVersion.

Use a broad update search for issues touched by the user in the quarter. For the
authenticated Jira user, you may use `currentUser()` in supported user-field
predicates such as `assignee = currentUser()`, and resolve the account ID from
`/rest/api/3/myself`. For `updatedBy()`, use an identifier accepted by the tenant
for that function, such as the user's Atlassian `accountId` if supported;
otherwise use a broader candidate scan and rely on the exact comment-author and
date filters below. Resolve the user's Jira identity to an Atlassian `accountId`
before filtering comments; if a name search is ambiguous, ask the user to
confirm the intended Jira user.

```jql
project = {PROJECT}
AND issue in updatedBy("{PERSON}", "{YYYY/MM/DD_START}", "{YYYY/MM/DD_END_PLUS_ONE}")
ORDER BY updated DESC
```

Then fetch comments for each issue and keep only comments where:

- `comment.author.accountId` equals the resolved Atlassian account ID for
  `{PERSON}`
- comment `created` is within the quarter date range

REST comment endpoint. Paginate with `startAt` and `maxResults` until all
comments are fetched. The helper script handles this pagination:

```bash
python3 skills/quarterly-connection-jiras/jira_rest_helper.py comments {KEY}
```

For one-off checks, this is the first request only; keep incrementing `startAt`
until all comments are returned:

```bash
curl --netrc \
  'https://redhat.atlassian.net/rest/api/3/issue/{KEY}/comment?startAt=0&maxResults=100&orderBy=created'
```

For each comment-discovered issue, collect issue details and parent information.
If the issue was already included from Step 1 or Step 2, use the comments as
additional context. If it was not already included, add it to an **Additional
{QUARTER} comment-discovered Jira work** section. Include cross-quarter items,
e.g. previous-quarter watch duty tasks, CVE verification, production rollout
validation, or next-quarter follow-up epics, but clearly label their fixVersion
or no-fixVersion status.

Do not use `comment ~ "{PERSON}"` as the primary source for authored comments;
it searches comment text, not author identity. It can be useful only as a
fallback or sanity check.

## Step 4: Write the report

Use this structure for each epic, then a summary table.

```markdown
# Assignee/Reporter/Commenter Epics — Quarterly Connection ({QUARTER})

**Project:** {PROJECT}
**Assignee/reporter/commenter:** {PERSON}
**Base Jira scope:** `fixVersion = {QUARTER}` and {PERSON} as current assignee,
historical assignee, or reporter; grouped by parent epic.
**Additional comment scan:** {PROJECT} issues updated by {PERSON} during the
quarter were fetched, then comments authored by {PERSON} in that date range were
reviewed.

> If no directly assigned epics are found, say so and explain that the report
> focuses on child issues grouped by parent epic.

---

- **N. [KEY](https://redhat.atlassian.net/browse/KEY)** Summary: X% (done/active) | **Assignee:** Name | **Due:** date or —
  - Description: {description from step 1.1}.
  - **Status update:** whether it was completed, is in progress, or is blocked.
  - {PERSON}'s contribution: linked key tasks and factual one-line summaries.
  - Items: completed vs in progress vs not started children tasks.

---
```

If Step 3 found extra issues, add:

```markdown
## Additional {QUARTER} comment-discovered Jira work

| Issue | Parent | Status / fixVersion | What {PERSON}'s {QUARTER} comments show |
|------|--------|---------------------|----------------------------------------|
```

End with **Summary at a glance**:

| Epic | Completion | Summary |
|------|------------|---------|

Add a short **Highlights** paragraph (2–4 sentences): busiest epics, blockers,
epics that slipped (yellow/red), tasks with no movement, and important
comment-discovered cross-quarter/follow-up work.

## Output rules

- Link every epic and key task to `https://redhat.atlassian.net/browse/{KEY}`.
- Be factual; do not invent progress not visible in Jira.
- If Status Summary text is truncated in the API (`...`), present what is
  available and link to the epic for the full text.
- Keep comment-discovered issues separate when they are outside the base quarter
  fixVersion scope.
- Do not create or edit Jira issues unless the user explicitly asks.

Export the report as a markdown file named
`quarterly-connection-{QUARTER}-jiras.md` (e.g. `quarterly-connection-2026Q2-jiras.md`).

## Example trigger phrases

- "Generate the quarterly connection report for 2026Q1 and Juan Díaz Suárez"
- "Generate for 2026Q3 and Martin Zibricky assignee/reporter name Martin Zibricky, project CCXDEV"
- "Also check Jiras where Martin Zibricky commented"
- "Help me write my quarterly connection?"

## Quick reference — Jira access

Preferred CLI path:

```bash
acli jira auth status
acli jira workitem search --jql '<JQL>' --fields key,summary,status,assignee,priority --paginate --json
acli jira workitem view CCXDEV-123 --fields key,summary,status,assignee,description,comment,updated --json
# For /search/jql, follow nextPageToken until no token remains.
python3 skills/quarterly-connection-jiras/jira_rest_helper.py search --jql '<JQL>' --fields key,summary,status,assignee,reporter,parent,parentEpic,priority,updated,issuetype,fixVersions,labels,duedate,description,comment
curl --netrc 'https://redhat.atlassian.net/rest/api/3/search/jql?jql=<URL_ENCODED_JQL>&fields=key,summary,status,assignee,reporter,parent,parentEpic,priority,updated,issuetype,fixVersions,labels,duedate,description,comment&maxResults=100'
curl --netrc 'https://redhat.atlassian.net/rest/api/3/issue/CCXDEV-123?expand=changelog&fields=summary,status,assignee,reporter,parent,parentEpic,description,comment,updated,labels,duedate,fixVersions'
# For comments, increment startAt until startAt >= total.
python3 skills/quarterly-connection-jiras/jira_rest_helper.py comments CCXDEV-123
curl --netrc 'https://redhat.atlassian.net/rest/api/3/issue/CCXDEV-123/comment?startAt=0&maxResults=100&orderBy=created'
```

Optional MCP path, when available:

```text
getAccessibleAtlassianResources → cloudId
searchJiraIssuesUsingJql       → epic/task/comment candidate lists
getJiraIssue(expand=changelog,comments) → status updates per epic/issue
```
