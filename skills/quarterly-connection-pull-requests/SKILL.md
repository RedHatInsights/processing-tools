---
name: quarterly-connection-pull-requests
description: >-
  Collect GitHub PRs and GitLab MRs authored by a user during a given
  quarter. Produces a themed report of code contributions across team
  repositories. Use alongside the quarterly-connection-jiras skill to complement
  Jira-based reports with actual code work, or standalone when the user
  asks for a PR/MR summary.
---

# quarterly-connection-pull-requests

Collect and report all PRs (GitHub) and MRs (GitLab) authored by the
given user during a given quarter across team repositories.

## Pre-requisites

- **gh CLI**: Must be authenticated. Verify with `gh auth status`. The
  user's GitHub username is obtained via `gh api user --jq '.login'`.
- **glab CLI**: Must be authenticated for `gitlab.cee.redhat.com`. Verify
  with `glab auth status --hostname gitlab.cee.redhat.com`. The token
  needs `read_api` scope. If not authenticated, ask the user to run
  `glab auth login --hostname gitlab.cee.redhat.com`.

## Defaults

- **Quarter:** Should contain the year and quarter number (e.g. 2026Q2
  for April–June 2026). The skill converts this to date ranges
  (e.g. `2026-04-01..2026-06-30`).
- **Assignee:** The current authenticated user (resolved from `gh` and
  `glab`).

## User invocation

The user may say things like:
- "collect my PRs for 2026Q2"
- "show my GitHub and GitLab contributions this quarter"
- "quarterly PR report"
- "find my merge requests for Q2"

## Step 1: Collect GitHub PRs

### 1a. Get the GitHub username

```bash
gh api user --jq '.login'
```

### 1b. Search for authored PRs

Search for PRs created in the quarter and PRs merged in the quarter but
created before it (to capture carry-over work):

```bash
gh search prs --author={username} --created="{YYYY-MM-DD}..{YYYY-MM-DD}" --limit 1000
gh search prs --author={username} --merged-at="{YYYY-MM-DD}..{YYYY-MM-DD}" --limit 1000
```

Deduplicate across both result sets.

If either command returns exactly 1000 results, warn the user that the
GitHub search API cap was hit and some PRs may be missing. Suggest
narrowing the date range (e.g. splitting the quarter into monthly
searches) to work around the limit.

### 1c. Get PR details

For each PR, collect stats via `gh pr view`:

```bash
gh pr view {number} --repo {owner/repo} --json title,state,createdAt,mergedAt,additions,deletions,changedFiles,url,body \
  --jq '{title: .title, state: .state, createdAt: .createdAt, mergedAt: .mergedAt, additions: .additions, deletions: .deletions, files: .changedFiles, url: .url, body: (.body[:400])}'
```

Record: repo, PR number, title, state, createdAt, mergedAt,
additions/deletions/files changed, and the first 400 chars of the body
for context.

Use `state` and `mergedAt` to classify each PR:
- **MERGED** — `state` is `MERGED` (has a `mergedAt` timestamp).
- **CLOSED** — `state` is `CLOSED` and `mergedAt` is null (closed
  without merging; includes superseded PRs).
- **OPEN** — `state` is `OPEN` (still in progress).

Apply the same classification to the report summary counts and when
sorting PRs into the "Closed / superseded" theme section.

## Step 2: Collect GitLab MRs

### 2a. Get the GitLab token and user ID

Extract the token from glab config and resolve the user ID:

```bash
GL_TOKEN=$(grep -A1 'gitlab.cee.redhat.com' \
  ~/Library/Application\ Support/glab-cli/config.yml \
  | grep 'token:' | awk '{print $2}')

curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/user"
```

If the config path does not exist (Linux), check `~/.config/glab-cli/config.yml`.

### 2b. Search for authored MRs

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/merge_requests?author_id={user_id}&created_after={start}T00:00:00Z&created_before={end}T23:59:59Z&scope=all&per_page=100&state=all"
```

This returns MRs across all projects the user has access to. Filter to
only those in team-relevant projects (see below).

### 2c. Search active repos under the ccx group

List all active projects in the `ccx` GitLab group:

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/groups/ccx/projects?per_page=100&include_subgroups=true"
```

For each project with `last_activity_at` within or after the quarter,
search for the user's MRs:

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/projects/{project_id}/merge_requests?author_id={user_id}&created_after={start}T00:00:00Z&created_before={end}T23:59:59Z&state=all&per_page=50"
```

### 2d. Include repos outside the ccx group

Also search these team-relevant repos that live outside `ccx/`:

- `insights-qe/iqe-ccx-plugin`
- `service/app-interface`
- `ccit/jenkins-csb-customers/ccx-dev-casc-main`

Use URL-encoded project paths:

```bash
curl -s --header "PRIVATE-TOKEN: $GL_TOKEN" \
  "https://gitlab.cee.redhat.com/api/v4/projects/insights-qe%2Fiqe-ccx-plugin/merge_requests?author_id={user_id}&created_after={start}T00:00:00Z&created_before={end}T23:59:59Z&state=all&per_page=50"
```

### 2e. Deduplicate MRs

Steps 2b–2d may return the same MR more than once (the global search in
2b overlaps with per-project searches in 2c/2d). Before collecting
details or computing totals, deduplicate the combined result set using
`project_id` + `iid` as the key (or equivalently, `web_url`). Retain
only the first record seen for each unique key.

### 2f. Collect MR details

For each MR, record: project path, MR iid, title, state, created/merged
dates, web_url, and changes_count.

## Step 3: Write the report

Produce a markdown report listing all PRs/MRs grouped by theme:

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

- Link every GitHub PR to `https://github.com/{owner}/{repo}/pull/{number}`.
- Link every GitLab MR to `https://gitlab.cee.redhat.com/{project}/-/merge_requests/{iid}`.
- Be factual; do not invent or embellish PR descriptions.
- Include closed/superseded PRs in a separate section for completeness.

Export the report as a markdown file named
`quarterly-connection-{QUARTER}-pull-requests.md` (e.g. `quarterly-connection-2026Q2-pull-requests.md`).

## Quick reference — CLI commands

```
gh api user                    → GitHub username (Step 1)
gh search prs                  → GitHub PRs (Step 1)
gh pr view                     → PR details (Step 1)
curl gitlab.cee.redhat.com/api/v4/user          → GitLab user ID (Step 2)
curl gitlab.cee.redhat.com/api/v4/merge_requests → GitLab MRs (Step 2)
curl gitlab.cee.redhat.com/api/v4/groups/ccx/projects → ccx repos (Step 2)
```
