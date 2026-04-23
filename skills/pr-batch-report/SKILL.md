---
name: pr-batch-report
description: >-
  Build a review-oriented Markdown (or JSON) report for a list
  of GitHub PRs: links, title, description excerpt, CI rollup
  status, line and file stats, and optional unified diffs. Use
  when the user pastes multiple PR URLs, asks for a PR batch
  table, "review these PRs", or wants CI/diff summaries across
  several pulls.
---

# pr-batch-report

Produces a **single document** summarizing many pull requests using
the GitHub CLI (`gh`). Each row includes the PR link, title, a short
description excerpt, a coarse **CI** label from `statusCheckRollup`,
additions/deletions/total touched lines, file count, and paths inferred
from `gh pr diff`.

## Prerequisites

- [`gh`](https://cli.github.com/) installed and authenticated:
  `gh auth status`
- Network access to `github.com`

## Usage

From the repository root (or any directory):

```bash
python3 skills/pr-batch-report/scripts/pr_batch_report.py \
  'https://github.com/org/repo/pull/1' \
  'https://github.com/org/repo/pull/2/changes'
```

URLs may include a trailing `/changes` segment; it is stripped.

**Input from a file** (one URL per line; `#` starts a comment):

```bash
python3 skills/pr-batch-report/scripts/pr_batch_report.py --file urls.txt
```

**Stdin** (when no positional URLs and no `--file`, non-TTY stdin is read):

```bash
cat urls.txt | python3 skills/pr-batch-report/scripts/pr_batch_report.py
```

### Options

| Flag | Description |
|------|-------------|
| `--format markdown` | Default. Emits a GitHub-flavored Markdown report. |
| `--format json` | Machine-readable array of objects (includes `diff` unless `--no-diff`). |
| `--no-diff` | Skip `gh pr diff` (faster; path column stays empty in markdown). |
| `--diff-mode inline` | Print each diff in a fenced `diff` block (default). |
| `--diff-mode collapse` | Wrap each diff in `<details><summary>…</summary>` (renders on GitHub). |
| `--diff-mode none` | Table + CI notes only; still fetches diffs unless `--no-diff` (for path hints). |
| `--max-desc N` | Truncate description excerpts in the table (default: 240). |
| `-j N` | Parallel `gh` calls (default: 8). |

### Examples

```bash
# Compact table, no patch bodies
python3 skills/pr-batch-report/scripts/pr_batch_report.py --no-diff -f urls.txt

# GitHub-friendly long report with collapsible diffs
python3 skills/pr-batch-report/scripts/pr_batch_report.py --diff-mode collapse -f urls.txt > report.md
```

## Workflow (for agents)

1. Confirm `gh auth status` works for the target org (e.g. `RedHatInsights`).
2. Normalize the user’s list: one canonical PR URL per line; remove `/changes` if present (the script does this automatically).
3. Prefer **`--diff-mode collapse`** when the list is large so the chat or issue stays readable.
4. Paste or save the script **stdout** for the user. Mention that **CI** is derived from the API rollup: `passing` means no failed or in-progress checks in that rollup; **`NEUTRAL` / `SKIPPED`** on individual jobs are not treated as failures.
5. If any row shows **`failing`** or **`pending`**, call out those PRs first.
6. If everything is passing, you can suggest the user to approve the PRs using `gh pr review --approve`.

## CI semantics

The script classifies rollup entries from `gh pr view --json statusCheckRollup`:

- **`failing`** — any `CheckRun` with `conclusion` in
  `FAILURE`, `ERROR`, `TIMED_OUT`, `CANCELLED`, `ACTION_REQUIRED`,
  or a `StatusContext` with `state` `FAILURE`.
- **`pending`** — any check still `IN_PROGRESS`, `PENDING`, `QUEUED`, etc.
- **`passing`** — otherwise (including completed `SUCCESS`, `SKIPPED`, `NEUTRAL`).

This matches a quick human review but **does not** know branch-protection
required-check rules; use the GitHub UI for authoritative merge gating.

## Constraints

- Read-only: only `gh pr view` and `gh pr diff`.
- Rate limits apply when querying many PRs; use `-j` modestly if you hit throttling.
- Very large diffs inflate the report; combine `--diff-mode collapse` with selective URLs or `--no-diff` for overview-only passes.
