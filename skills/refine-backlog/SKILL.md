---
name: refine-backlog
description: Backlog refinement for the CCX Processing team (CCXDEV). Walks three Jira views — the active sprint, the current quarter, and the rest of the backlog — runs a small set of checks over each, and applies the resulting fix. Dry run by default; writes only with --apply. Use when the user says "refine the backlog", "backlog refinement", or on the recurring refinement cadence.
---

# refine-backlog

Project **CCXDEV**, board **1553** (`CCX Core - Processing`).

Three views of the backlog, each with its own checks. Everything the skill
needs is in this file — there is no configuration to load.

| View | What it covers | Checks |
|---|---|---|
| `sprint` | the active sprint | `C1` quarter set · `C2` points set |
| `quarter` | this quarter, not yet in the sprint | `C2` points set |
| `backlog` | everything else, created in the last 14 days | `C3` points **and** quarter set |

Checks are shared across views; the **action** a check triggers depends on the
view it fired in. That mapping is the table in Step 3 — it is the one place to
look when changing the skill's behaviour.

## Invocation

```text
/refine-backlog                     # dry run, all three views
/refine-backlog --apply             # perform the Jira writes
/refine-backlog --view sprint       # one view only (sprint | quarter | backlog)
/refine-backlog --apply --max 20    # cap items touched per view (default 100)
```

**Dry run is the default.** Without `--apply` the skill calls read tools only
(`jira_search`, `jira_get_issue`, `jira_get_sprints_from_board`) and never
`jira_update_issue`, `jira_add_comment`, or `jira_add_issues_to_sprint`.

---

## Step 1 — Setup

1. **Check Jira access.** `jira_search` with
   `jql: "project = CCXDEV ORDER BY created DESC"`, `limit: 1`.
   Fails → abort: `refine-backlog: no Jira access (mcp-atlassian unavailable)`.
2. **Resolve the current quarter** from today's date, as `YYYYQn`
   (2026-10-09 → `2026Q4`). Calendar quarters, not fiscal.
3. **Resolve the mode** and echo it as the first line of output:
   `refine-backlog — DRY RUN (no Jira writes)` or
   `refine-backlog — APPLY MODE (Jira will be modified)`.
4. **Find the refinement sprint.** `jira_get_sprints_from_board` on board
   `1553`, and locate the sprint named exactly **`To be refined items`**.
   Not found → actions `A3` are all reported as
   `BLOCKED: refinement sprint not found`; the rest of the run continues.

---

## Step 2 — The three views

Run each view in turn (or just the one named by `--view`). Request the fields
`key, summary, status, labels, fixVersions, created, customfield_10028`;
`customfield_10028` is story points. Stop at `--max` items per view and say so
in the report when the cap truncated the list.

### V1 — Active sprint

```text
project = CCXDEV AND sprint IN openSprints() AND statusCategory != Done
  AND labels IN (obsint-processing, ccx-processing)
  AND issueType not in (Epic)
  ORDER BY created DESC
```

Run `C1` and `C2`.

### V2 — Current quarter

```text
project = CCXDEV AND fixVersion = "<current quarter>" AND statusCategory != Done
  AND (sprint IS Empty OR sprint NOT IN openSprints())
  AND labels IN (obsint-processing, ccx-processing)
  AND issueType not in (Epic)
  ORDER BY created DESC
```

Run `C2`.

The `sprint NOT IN openSprints()` clause keeps this view disjoint from V1, so
an unestimated sprint item gets a comment (V1) rather than being moved out of
the sprint it is being worked in (V2).

### V3 — Rest of the backlog

```text
project = CCXDEV AND statusCategory != Done AND created >= -14d
  AND sprint IS EMPTY
  AND labels IN (obsint-processing, ccx-processing)
  AND labels NOT IN (glitchtip)
  AND issueType not in (Epic)
  ORDER BY created DESC
```

Run `C3`.

Only the last 14 days: the point is to catch newly filed items before they go
stale, not to re-litigate the whole backlog. At the same time, we are skipping
Glitchtip issues, as their refinement (and deduplication) is much more complicated.

---

## Step 3 — Checks and actions

### Checks

| Check | Fires when |
|---|---|
| `C1` | no fixVersion equal to the current quarter |
| `C2` | story points (`customfield_10028`) empty or zero |
| `C3` | story points empty **or** no fixVersion at all |

### What each check does, per view

| View | Check | Action |
|---|---|---|
| `sprint` | `C1` | `A1` — add the current quarter to `fixVersions` |
| `sprint` | `C2` | `A2` — comment asking for a story point estimate |
| `quarter` | `C2` | `A3` — move to the `To be refined items` sprint |
| `backlog` | `C3` | `A3` — move to the `To be refined items` sprint |

An item can trigger at most one action per check. If both `C1` and `C2` fire on
a sprint item, it gets both `A1` and `A2`.

### Actions

**`A1` — add the current quarter to fixVersions.**
`jira_update_issue`, setting `fixVersions` to the existing list **plus** the
current quarter. Additive only — never drop or replace an existing fixVersion,
including a past or future quarter.

**`A2` — comment asking for story points.**
`jira_add_comment`. At most one per item per run; skip if the same comment is
already the newest bot comment on the item.

```markdown
**Backlog refinement**

This item is in the active sprint but has no story point estimate. Please add
one, or move it out of the sprint.

---
_Automated backlog refinement. Reply here if this is wrong._
```

**`A3` — move to the refinement sprint.**
`jira_add_issues_to_sprint` with the sprint resolved in Step 1.4. Jira moves
the item out of its current sprint, if any. Never remove an item from a sprint
without adding it to this one.

### Output shape

One line per action, same shape in both modes so a dry run diffs cleanly
against the apply run that follows:

```text
WOULD: A1 CCXDEV-14207 — add fixVersion 2026Q4          [C1, view sprint]
DID:   A2 CCXDEV-14210 — comment: story points missing  [C2, view sprint]
SKIP:  A3 CCXDEV-14233 — move to To be refined items    [already in that sprint]
```

---

## Step 4 — Report

```text
refine-backlog — DRY RUN
Current quarter: 2026Q4 · refinement sprint: To be refined items (id 2041)

sprint    12 items ·  3 C1 ·  2 C2  →  3 A1, 2 A2
quarter    8 items ·  4 C2          →  4 A3
backlog   15 items ·  6 C3          →  6 A3

Writes planned: 15 (3 fixVersions, 2 comments, 10 sprint moves)
Run `/refine-backlog --apply` to perform them.
```

In apply mode the header reads `APPLIED` and the last line is dropped.

---

## Constraints

- Dry run unless `--apply`.
- Only three fields are ever written: `fixVersions`, comments, sprint
  membership. Story points are read and reported, **never set by the bot** —
  estimation is a team activity.
- Never transition status, never close an item, never touch assignee,
  priority, summary, or description.
- `fixVersions` writes are additive. No removals, no overwrites.
- One comment per item per run.
- Respect `--max` (default 100) in every view.
- Jira only. No code changes, no PRs.

## Edge cases

- **Zero items in a view** — report `no items` for that view and carry on. Not
  an error.
- **Refinement sprint missing or closed** — `A3` is blocked, `A1` and `A2`
  still run. Say so in the report.
- **Current quarter is not a released version in CCXDEV** — `A1` will fail.
  Report it and do not try to create the version.
- **Item already in `To be refined items`** — `SKIP:`, not a re-add.
- **Story points set to 0** — treated as unestimated by `C2` and `C3`. Flip
  this here if the team uses 0 deliberately.
- **A write fails mid-run** — stop, and report which items were already
  modified and which were not. A partially applied run must be visible.
