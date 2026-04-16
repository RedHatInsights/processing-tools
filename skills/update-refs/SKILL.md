---
name: update-refs
description: >-
  Update SaaS file refs in app-interface to the latest
  commit SHAs. Use when the user says "update refs",
  "bump refs", "promote", or asks to update
  ccx-data-pipeline service references.
---

# update-refs

Updates `ref:` fields in ccx-data-pipeline SaaS YAML files
(in app-interface) to the latest commit SHA from each repo's
default branch. Skips `ref: internal`, `main`, and `master`.

## Prerequisites

- Git access to `https://gitlab.cee.redhat.com/service/app-interface.git`
- Git access to the GitHub repos whose refs are being updated
- Bash 4+ (for associative arrays)

## Usage

Run the script from the `skills/update-refs` directory:

```bash
./scripts/update_refs.sh [--dry-run] [--repo <name-or-url>]... [--local-folder <path>]
```

### Options

| Flag | Description |
|------|-------------|
| `--dry-run` | Show what would change without modifying files |
| `--repo <value>` | Only update refs for this repo (repeatable). Accepts a full URL or just the repo name. Uses **exact match** — `insights-results-aggregator` will not match `insights-results-aggregator-cleaner`. |
| `--local-folder <path>` | Use an existing local app-interface checkout instead of cloning to `/tmp/app-interface`. |

### Examples

```bash
# Dry-run for all repos
./scripts/update_refs.sh --dry-run

# Update a single repo
./scripts/update_refs.sh --repo insights-results-aggregator

# Update two specific repos
./scripts/update_refs.sh --repo insights-results-aggregator --repo ccx-notification-writer

# Full URL also works
./scripts/update_refs.sh --repo https://github.com/RedHatInsights/insights-results-aggregator
```

## Workflow

1. **Ask the user** which repos to update, or whether to update all.
   Always start with `--dry-run` so the user can review changes.
2. **Ask the user** if you should clone the app-interface repository or use
   the local one. If so, use `--local-folder` option.
3. Run the script with `--dry-run` and present the output.
4. After user confirmation, run without `--dry-run`.
5. The script modifies files inside the local app-interface
   clone at `/tmp/app-interface`. The user can then `cd` there
   to review and submit a merge request.
6. Checkout to a branch named `update-refs-<timestamp>` and push the changes.
   If not using `--local-folder`, **ask the user** for the fork:
```bash
BRANCH="update-refs-$(date +%Y%m%d)"
git checkout -b $BRANCH
git add .
git commit -m "chore: update refs"
git push -o merge_request.create \
            -o merge_request.remove_source_branch \
            -o merge_request.target=master \
            -o merge_request.title="chore: update refs" \
            fork ${BRANCH} --verbose
```
1. Tell the user to follow the merge request CI in order
   to ask the rest of the team to review the changes.

## How it works

1. Clones (or reuses) app-interface to `/tmp/app-interface`. But we always
   clone in /tmp in order not to create conflicts with the user's local
   app-interface clone.
2. Scans all YAML files under `data/services/insights/ccx-data-pipeline`.
3. For each `url:` + `ref:` pair, fetches the latest SHA from
   the repo's default branch via `git ls-remote`.
4. Replaces outdated SHA refs in-place (or reports them in dry-run).

## Constraints

- **Always dry-run first** — never modify files without user review.
- **Do not touch branch refs** — `main`, `master`, and `internal`
  are intentionally skipped.
- The script requires VPN network access to both GitLab (app-interface)
  and GitHub (source repos).
