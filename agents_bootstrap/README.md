# AGENTS.md sync

Minimal root `AGENTS.md` for ObsInt service repos, distributed by the existing
[repo-file-sync](../.github/workflows/sync.yaml) / [`.github/sync.yml`](../.github/sync.yml)
mechanism (same as CODEOWNERS and CI workflow wrappers).

## How it works

1. [`AGENTS.md.tmpl`](./AGENTS.md.tmpl) is rendered with Jinja. Optional
   `pages_url` includes a GitHub Pages link only when that variable is set in
   `sync.yml` (omit it when the repo has no Pages site).
2. Only repos that list this file in [`.github/sync.yml`](../.github/sync.yml)
   receive it — that list **is** the allowlist. Repos that already maintain their
   own `AGENTS.md` simply omit this entry.
3. On push to `master` / `main` (or manual sync dispatch), sync opens PRs in those
   targets via `obsint-processing-app`.

## Adding a repo

In `.github/sync.yml`, under that repo, add:

```yaml
  - source: agents_bootstrap/AGENTS.md.tmpl
    dest: AGENTS.md
    template:
      repo_name: <github-repo-name>
      # only if Pages are enabled (check: gh api repos/RedHatInsights/<name>/pages):
      pages_url: https://redhatinsights.github.io/<github-repo-name>/
```

## Taking ownership / enriching AGENTS.md

If a repo replaces the stub with a richer hand-written `AGENTS.md`, **remove** the
`agents_bootstrap/AGENTS.md.tmpl` entry from `.github/sync.yml` for that repo so
sync does not overwrite it.

## Local preview

```bash
# same substitution sync performs for repo_name
sed 's/{{ repo_name }}/insights-results-aggregator-exporter/g' agents_bootstrap/AGENTS.md.tmpl
```

Sync only **writes** `AGENTS.md`. It does not open or require `README.md`, architecture docs, or live Pages — missing docs are fine (links may simply 404 until added).
