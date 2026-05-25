---
name: epic-status-update
description: Generate status update summaries for open In Progress Jira epics in the current quarter. Finds the last status update comment (GREEN/YELLOW/RED), gathers all activity since then (status changes, PRs, commits, comments, sprint plans), and offers to post a summary comment.
allowed-tools: mcp__Atlassian__jira_search, mcp__Atlassian__jira_get_issue, mcp__Atlassian__jira_batch_get_changelogs, mcp__Atlassian__jira_get_issues_development_info, mcp__Atlassian__jira_get_issue_development_info, mcp__Atlassian__jira_add_comment, mcp__Atlassian__jira_get_agile_boards, mcp__Atlassian__jira_get_sprints_from_board, mcp__Atlassian__jira_get_board_issues, AskUserQuestion, Bash(gh search prs:*)
---

# Epic Status Update

Generate a status update summary for each of my open In Progress epics in the current quarter, and offer to post it as a Jira comment.

## Defaults

- **Jira user:** `currentUser()` (the authenticated Jira user)
- **Project:** CCXDEV (override with `--project KEY`)
- **Fix version:** Current quarter (e.g. `2026Q2` — derived from today's date)
- **Epic status filter:** In Progress only (skip New, To Do, Closed, Done, Resolved)
- **Scrum board:** auto-detected from project (override with `--board ID`)
- **GitHub org:** RedHatInsights (override with `--org NAME`)
- **Behavior:** show summary first, ask before posting

If the user passes a specific epic key (e.g. `CCXDEV-16273`), only process that epic.

## Execution Steps

Run these steps in order. Use parallel tool calls wherever possible.

### Step 1: Find In Progress epics for current quarter

```
JQL: project = {PROJECT} AND issuetype = Epic AND assignee = currentUser() AND status = "In Progress" AND fixVersion = "{CURRENT_QUARTER}"
Fields: summary,status,assignee,updated,fixVersions
Limit: 50
```

Derive the fix version from today's date: `{YEAR}Q{QUARTER}` (e.g. `2026Q2` for April–June 2026).

If a specific epic key was passed as an argument, skip this search and use that key directly.

Show the user a numbered list of found epics and ask which ones to generate updates for (default: all).

### Step 2: Determine lookback period (since last status update)

For each epic, fetch comments with `comment_limit: 30` (these epics accumulate context comments over time — 10 is often not enough).

Find the most recent comment whose body starts with `GREEN`, `YELLOW`, or `RED` (case-insensitive, may have `:` or whitespace after). Use that comment's `created` date as the lookback start.

If no status update comment exists, fall back to 7 days.

### Step 3: Gather child issues

```
JQL: parentEpic = {EPIC_KEY} ORDER BY status ASC, updated DESC
Fields: summary,status,assignee,issuetype,created,updated,priority,labels
Limit: 50
```

**Fallback** if `parentEpic` doesn't work:
1. `"Epic Link" = {EPIC_KEY}`
2. `parent = {EPIC_KEY}`

### Step 4: Check current sprint

Find the scrum board for the project (or use the configured board ID):
```
jira_get_agile_boards with project_key, board_type = "scrum"
```

Find the active sprint on that board, then query which child issues of this epic are in the current sprint:
```
JQL: sprint = {SPRINT_ID} AND parentEpic = {EPIC_KEY}
```

This tells you what's planned for the current sprint vs backlog. Include sprint name and dates in the summary.

### Step 5: Get status change history

Use `jira_batch_get_changelogs` on all child issue keys at once with `fields: status`.

Filter changelog entries to only those since the lookback date (Step 2).

Categorize:
- **Completed:** Status changed TO any of: Closed, Done, Resolved, Verified, MODIFIED, ON_QA, POST
- **Newly started:** Status changed TO "In Progress" or similar active statuses
- **Newly created:** Issues with `created` date within the lookback period

### Step 6: Get development info (PRs, commits)

**Primary:** Try `jira_get_issue_development_info` for each child issue.

**Fallback (important):** The Jira dev info API frequently returns empty results or 500 errors even when PRs are linked (the issue's `customfield_10000` dev summary field may show linked PRs that the API fails to return). When the API returns empty, use `gh search prs` as a fallback:

```bash
gh search prs "ISSUE_KEY" --owner {GITHUB_ORG} --json repository,title,url,state,number
```

Run this for every child issue that had activity in the lookback period.

**Bot comments as dev info source:** Bot comments (e.g. "App SRE Jira bot") on child issues often contain links to GitLab MRs (app-interface, etc.). Parse these for merge request URLs — they count as development activity. Example pattern:
```
[User] mentioned this issue in [merge request !NNNNN](gitlab-url)
```

### Step 7: Get comments on active child issues

For each child issue that had activity in the lookback period (status change, new PR, was created, or is In Progress), fetch comments with `comment_limit: 10`.

Filter to comments created within the lookback period.

**Include substantive bot comments** that link MRs/PRs (see Step 6).

**Focus on:** decisions, scope clarifications, blockers, disagreements and their resolutions, technical trade-offs. These are the "Notable Activity" items. Summarize the discussion, not just that it happened — e.g. "Daniel raised security concerns about Vault access; Lena clarified the skill is a procedural guide, not direct automation. Scope aligned."

### Step 8: Compile the summary

The summary comment starts with a color-coded status line, then details.

**Color coding:**
- **GREEN:** — on track, no blockers
- **YELLOW:** — at risk, minor concerns or delays
- **RED:** — blocked, needs attention

The user will manually color the GREEN/YELLOW/RED text in Jira after posting — programmatic color formatting is not supported via the MCP tool.

**Important:** The `jira_add_comment` MCP tool accepts **Markdown**, NOT Jira wiki markup. Use standard Markdown syntax.

Format:

```
**GREEN:** {one-line overall status}. {key highlight}. {blocker status}.

### Completed
- **ISSUE_KEY** {summary} — {who closed it}. {reason/outcome from comments}

### In Progress
- **ISSUE_KEY** {summary} — {context: who, what changed, linked PR if any}

### Planned this sprint (Sprint {N}, {start} – {end})
- **ISSUE_KEY** {summary} — {status} ({assignee}). {notable comment context if any}

### Notable Activity
- {Substantive discussions, decisions, scope changes, resolutions}

### Backlog
- **ISSUE_KEY** {summary} — ({assignee or "unassigned"})
```

Always include a Completed section for tasks whose status changed to Closed/Done/Resolved since the last status update. Include the reason or outcome from the task's comments — not just that it was closed.

**Formatting rules:**
- Use **Markdown** (not Jira wiki markup): `###` for headings, `**bold**` for bold, `[text](url)` for links
- Issue keys like CCXDEV-16273 auto-link in Jira — no special syntax needed, just write them plain or bold
- Bold the issue keys: `**CCXDEV-16279**`
- Link PRs as `[repo#number|url]`
- Link GitLab MRs as `[app-interface !NNNNN|url]`
- Keep it concise — one line per item, but include enough context to be useful (assignee, what changed, linked PRs)
- Omit sections with no items entirely
- Include comment context inline with the relevant task, not as a separate dry list
- The summary should be scannable in under 30 seconds

### Step 9: Present to user and post

Show the compiled summary in the chat. Ask per epic: "Post this as a comment on {EPIC_KEY}?"

If approved, use `jira_add_comment` to post. The body should be in Jira wiki markup (not GitHub markdown).

## Edge Cases

- **No activity since last status update:** Say "No activity found for {EPIC_KEY} since last update on {date}" and skip.
- **Epic with no child issues:** Note this and suggest adding stories/tasks.
- **Jira dev info API empty/erroring:** Fall back to `gh search prs` — this is common and expected.
- **Large epics (>50 child issues):** Paginate if needed, but note this in the summary.
- **Multiple status update comments on same day:** Use the latest one.

## Example Invocations

- `/epic-status-update` — all In Progress epics for current quarter
- `/epic-status-update CCXDEV-16273` — specific epic only
- `/epic-status-update --days 14` — override lookback to 14 days instead of auto-detecting
- `/epic-status-update --project RHCLOUD` — different project
- `/epic-status-update --board 8473` — different scrum board
