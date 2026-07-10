---
name: quarterly-connection
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

# quarterly-connection

Produce a quarter status report for CCX Core - Processing epics owned by the
given user and for a given quarter.

## Pre-requisites

Use the **Atlassian MCP** server (`plugin-atlassian-atlassian`).
If tools are unavailable, call `mcp_auth` first, then retry.

Get `cloudId` via `getAccessibleAtlassianResources` (Red Hat site:
`https://redhat.atlassian.net`).

- **gh CLI**: Must be authenticated. Verify with `gh auth status`. The
  user's GitHub username is obtained via `gh api user --jq '.login'`.
- **glab CLI**: Must be authenticated for `gitlab.cee.redhat.com`. Verify
  with `glab auth status --hostname gitlab.cee.redhat.com`. The token
  needs `read_api` scope. If not authenticated, ask the user to run
  `glab auth login --hostname gitlab.cee.redhat.com`.

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

## Step 3: Collect GitHub PRs

Collect PRs authored by the user during the quarter from GitHub.

### 3a. Get the GitHub username

```bash
gh api user --jq '.login'
```

### 3b. Search for authored PRs

Search for PRs created in the quarter and PRs merged in the quarter but
created before it (to capture carry-over work):

```bash
gh search prs --author={username} --created="{YYYY-MM-DD}..{YYYY-MM-DD}" --limit 100
gh search prs --author={username} --merged-at="{YYYY-MM-DD}..{YYYY-MM-DD}" --limit 100
```

Deduplicate across both result sets.

### 3c. Get PR details

For each PR, collect stats via `gh pr view`:

```bash
gh pr view {number} --repo {owner/repo} --json title,additions,deletions,changedFiles,url,body \
  --jq '{title: .title, additions: .additions, deletions: .deletions, files: .changedFiles, url: .url, body: (.body[:400])}'
```

Record: repo, PR number, title, state, additions/deletions/files changed,
and the first 400 chars of the body for context.

### 3d. Cross-reference with Jira

Check each PR title for `CCXDEV-*` patterns. If a PR references a Jira
ticket found in Steps 1–2, mark it as "Jira-tracked". Still include it in
the report — the PR list shows the actual code work behind the Jira items.

## Step 4: Collect GitLab MRs

Collect MRs authored by the user during the quarter from the internal
GitLab instance (`gitlab.cee.redhat.com`).

### 4a. Get the GitLab token and user ID

Extract the token from glab config and resolve the user ID:

```bash
GL_TOKEN=$(grep -A1 'gitlab.cee.redhat.com' \
  ~/Library/Application\ Support/glab-cli/config.yml \
  | grep 'token:' | awk '{print $2}')

curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/user"
```

If the config path does not exist (Linux), check `~/.config/glab-cli/config.yml`.

### 4b. Search for authored MRs

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/merge_requests?author_id={user_id}&created_after={start}T00:00:00Z&created_before={end}T00:00:00Z&scope=all&per_page=100&state=all"
```

This returns MRs across all projects the user has access to. Filter to
only those in team-relevant projects (see below).

### 4c. Search active repos under the ccx group

List all active projects in the `ccx` GitLab group:

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/groups/ccx/projects?per_page=100&include_subgroups=true"
```

For each project with `last_activity_at` within or after the quarter,
search for the user's MRs:

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/projects/{project_id}/merge_requests?author_id={user_id}&created_after={start}T00:00:00Z&created_before={end}T00:00:00Z&state=all&per_page=50"
```

### 4d. Include repos outside the ccx group

Also search these team-relevant repos that live outside `ccx/`:

- `insights-qe/iqe-ccx-plugin`
- `service/app-interface`
- `ccit/jenkins-csb-customers/ccx-dev-casc-main`

Use URL-encoded project paths:

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/projects/insights-qe%2Fiqe-ccx-plugin/merge_requests?author_id={user_id}&created_after={start}T00:00:00Z&created_before={end}T00:00:00Z&state=all&per_page=50"
```

### 4e. Collect MR details

For each MR, record: project path, MR iid, title, state, created/merged
dates, web_url, and changes_count.

## Step 5: Write the report

Use this structure for **each epic**, then a summary table, then the
PR/MR section.

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

### PR/MR section

After the highlights, add a section listing all PRs and MRs:

```markdown
## All PRs/MRs — {QUARTER}

{total} PRs/MRs authored across {repo_count} repositories ({merged} merged, {closed} closed).

### {Theme 1} ({related repos})

| # | PR | Repo | Details |
|---|---|---|---|
| 1 | [#N](url) Title | repo-name | **Impact.** One-line description. +X/−Y, Z files. |
```

Group PRs/MRs by logical theme — **not** chronologically. Typical themes:
- Feature work tied to a specific epic or initiative
- Cross-team / external contributions
- Dependency management / supply chain
- Documentation
- Infrastructure / CI
- Closed / superseded (for completeness)

Within each group, rank by impact (largest/most important first).

For each PR/MR include: link, title, repo name, and a one-line impact
description with additions/deletions stats where available.

## Output rules

- Link every epic and key task to `https://redhat.atlassian.net/browse/{KEY}`.
- Link every GitHub PR to `https://github.com/{owner}/{repo}/pull/{number}`.
- Link every GitLab MR to `https://gitlab.cee.redhat.com/{project}/-/merge_requests/{iid}`.
- Be factual; do not invent progress not visible in Jira.
- If Status Summary text is truncated in the API (`...`), present
  what is available and link to the epic for the full text.
- Do not create or edit Jira issues unless the user explicitly asks.

Export the report as a markdown file.

## Example trigger phrases

- "Generate the quarterly connection report for 2026Q1 and Juan Díaz Suárez"
- "Help me write my quarterly connection?"

## Quick reference — MCP calls and CLI commands

```
getAccessibleAtlassianResources → cloudId
searchJiraIssuesUsingJql       → epic list (Step 1)
searchJiraIssuesUsingJql       → child issues, one epic per call, paginate
getJiraIssue(expand=changelog,comments) → status updates per epic
gh api user                    → GitHub username (Step 3)
gh search prs                  → GitHub PRs (Step 3)
gh pr view                     → PR details (Step 3)
curl gitlab.cee.redhat.com/api/v4/user          → GitLab user ID (Step 4)
curl gitlab.cee.redhat.com/api/v4/merge_requests → GitLab MRs (Step 4)
curl gitlab.cee.redhat.com/api/v4/groups/ccx/projects → ccx repos (Step 4)
```
