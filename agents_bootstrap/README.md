# AGENTS.md bootstrap

One-shot helper that opens **draft** PRs adding a **minimal** root `AGENTS.md` to ObsInt service repos that do not already have one.

This is **not** continuous file-sync (unlike [`.github/sync.yml`](../.github/sync.yml) for CODEOWNERS / CI wrappers). Existing `AGENTS.md` files are never overwritten.

## What gets written

From [`AGENTS.md.tmpl`](./AGENTS.md.tmpl) via simple `{{ repo_name }}` text replacement (same placeholder style as `workflows_examples/*.tmpl`):

- Short pointer to `./README.md`
- Shared **Team context** (team-info skill links)
- External references:
  - `./README.md`
  - GitHub Pages at `https://redhatinsights.github.io/<repo-name>/` (conventional URL; may 404 until Pages are enabled)

No architecture inventing, Common Tasks, or Makefile scraping — enrich later by hand or with the `create-agents-md` skill.

## Target list

Repos are the top-level keys of [`.github/sync.yml`](../.github/sync.yml) (same fleet as CODEOWNERS / reusable workflow sync). Repos that already have `AGENTS.md` are skipped automatically, so the list can grow when new sync targets are added; re-run the workflow anytime.

## How to run

### GitHub Actions (preferred)

Actions → **Bootstrap AGENTS.md** → Run workflow:

| Input | Meaning |
|-------|---------|
| `dry_run` | Default `true` — log skips / would-create only |
| `repo` | Optional `Owner/name` to limit to one repo; empty = all sync.yml targets |

Set `dry_run` to `false` when you want draft PRs opened as `obsint-processing-app`.

### Locally

Needs [`gh`](https://cli.github.com/) and `jq` (both available on GitHub-hosted runners):

```bash
./agents_bootstrap/bootstrap.sh --dry-run
./agents_bootstrap/bootstrap.sh --dry-run --repo RedHatInsights/some-repo
# Live (opens draft PRs):
./agents_bootstrap/bootstrap.sh --repo RedHatInsights/some-repo
```

## Branch / PR shape

- Branch: `obsint-processing-app/bootstrap-agents-md`
- Draft PR title: `docs: bootstrap minimal AGENTS.md`
