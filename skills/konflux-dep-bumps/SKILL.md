---
name: konflux-dep-bumps
description: Triage and fix failing Konflux/MintMaker dependency bump PRs (bot-authored, auto-merge enabled). Use when a Renovate/MintMaker PR is stuck due to CI failures. Covers Go and Python repos in the RedHatInsights org.
---

# Konflux Dependency Bump Triage Skill

MintMaker (Renovate via Konflux) opens dependency bump PRs with auto-merge enabled. When CI fails the PR stalls. This skill covers triage, investigation, and resolution.

---

## Step 0 — Get the current open Konflux bot PRs

**Source of truth:** https://github.com/RedHatInsights/processing-tools/tree/master/open_mr_pr/github

Check the `open-prs-konflux.md` file there. The date at the top of that file tells you when it was last generated. **If the date does not match today's date, the file is stale — run the fetcher locally and inform the user before proceeding:**

```bash
cd /Users/lsolarov/Documents/processing-tools-gh/open_mr_pr/github
python3 list_repos_prs.py
cat open-prs-konflux.md
```

---

## Step 1 — Check what is failing

For each stuck PR:

```bash
gh pr checks <PR_NUMBER> --repo RedHatInsights/<REPO>
```

Note every failing check. The most common are: Go tests, lint, BDD tests, Konflux pipeline, enterprise contract, artifact update (`renovate/artifacts`). Multiple failures often share a single root cause — fix the root and the rest clear.

---

## Step 2 — Try the cheap fixes first

Before investigating root cause, try these in order. They resolve a large portion of stuck PRs with no code change.

**Rebase** — covers stale go.sum, go.mod drift, or Renovate artifact failures:

Push an empty commit to the bot PR branch — this re-triggers CI and prompts Renovate to rebase with fresh artifacts:

```bash
BRANCH=$(gh pr view <PR_NUMBER> --repo RedHatInsights/<REPO> --json headRefName --jq '.headRefName')
git fetch origin $BRANCH
git checkout $BRANCH
git commit --allow-empty -m "chore: trigger Renovate rebase"
git push origin $BRANCH
```

Note: `/rebase` as a comment does **not** work in these repos.

**Retest** — covers flaky or environment-dependent failures (infrastructure errors clearly unrelated to the dependency change, e.g. Kafka unreachable, OCM API client errors, DB dial failures). Check whether the Konflux pipeline itself passed even if GitHub Actions failed — that is a strong signal the failure is environmental:

```bash
gh pr comment <PR_NUMBER> --repo RedHatInsights/<REPO> --body "/retest"
```

Note: use `/retest`, not `/ok-to-test` — the latter may not be wired up in all repos.

If either of these resolves it, move on. If not, proceed to root cause investigation.

---

## Step 3 — Read the logs and identify the root cause

Pull the failed run logs:

```bash
gh run view <RUN_ID> --repo RedHatInsights/<REPO> --log-failed 2>&1 | grep -E "undefined|cannot use|no field|incompatible|conflict|Error|FAILED" | head -40
```

**Understand what broke before deciding how to fix it.** The PR description lists every bumped package with links to release notes — read them for the relevant version. Look specifically for breaking changes: removed fields, renamed types, changed function signatures, altered dependency requirements.

Key questions to answer:
- Which bumped package introduced the breakage?
- Is it the bumped package itself that broke, or something that depends on it?
- Is the broken package archived / unmaintained?
- Does a newer compatible version of the affected package exist already?
- Is the breakage in this repo's own code, or in a shared library that this repo depends on?

**The last question matters most for scoping the fix.** If the breakage originates in a shared library, fixing it there unblocks all downstream repos at once. Always check whether a direct dependency of the repo is pulling in the broken package transitively (`go mod graph`, `go.mod` indirect entries) before deciding where to fix.

---

## Step 4 — Choose the right fix

In order of preference:

1. **Bump the affected package** to a version that is compatible with the newly bumped dependency — the cleanest outcome, keeps everything current.

2. **Replace an archived or unmaintained package** with its maintained equivalent — required when the affected package will never release a fix. Verify the replacement on the Go module proxy or PyPI before committing to it. Check that the package is actually published and not just present in a GitHub repo.

3. **Pin the breaking dependency back** to the last working version — last resort only, and only temporarily. Renovate will keep reopening the bump PR, so this is a holding pattern until option 1 or 2 becomes available. Document clearly in the PR why it is pinned.

**Do not** create new source files or replace packages solely because a native alternative exists in another library. The reason to replace must be concrete: the package is archived, unmaintained, or structurally incompatible with no fix path.

**Do not** apply the fix directly to repos that get the broken package transitively. Fix it at the source (the shared library), verify the downstream effect with a local `replace` directive, then open one PR instead of many.

---

## Step 5 — Verify the fix before opening a PR

**Always verify locally before pushing — no exceptions.**

For a fix in a shared library, verify the downstream effect by pointing a dependent repo at the local fix using a `replace` directive:

```bash
# In the downstream repo's go.mod, temporarily add:
replace github.com/RedHatInsights/<SHARED-LIB> => /path/to/local/fix

go mod tidy
go build ./...
go test ./...
```

If the broken package disappears from `go.mod` and all tests pass, the fix is correct.

For any fix repo, always run all available tests locally:

```bash
# Go
go build ./... && go test ./...
# Also check Makefile for additional targets (BDD, integration, e2e)
grep -E "^test|^bdd|^e2e|^integration" Makefile

# Python
pip install -r requirements.txt && python -m pytest
```

**Do not push without local tests passing.**

---

## Step 6 — Open the fix PR

Fork the repo, create a branch from the upstream default branch, apply the fix, run tests, then open a PR.

The PR description must include:
- What broke and why (cite the specific breaking change from release notes with a link)
- Why this fix is the right approach (not just what changed)
- A link to the Konflux bot PR it unblocks
- If fixing a shared library: note which downstream repos are affected

After opening, comment on the stuck Konflux bot PR linking to the fix and noting it can be retested once the fix merges.

---

## Step 7 — After the fix merges

Renovate will rebase the bot PR automatically once the fix lands. If it does not rebase within a few hours, trigger it manually via the rebase checkbox or comment. For fixes in shared libraries, downstream bot PRs will not self-heal until Renovate opens a new bump that includes the updated shared library version — closing and recreating the bot PRs may be needed.

---

## CI / workflow gotchas

- **`gh run rerun` does not re-fetch reusable workflows.** When a workflow uses `uses: some-repo/.github/workflows/foo.yaml@master`, the `@master` SHA is resolved once when the run is first created and baked in. `gh run rerun` replays with that same SHA — even if master has since changed. To pick up a new workflow version, push a new commit to trigger a completely fresh run.

- **Multiple PRs with the same root cause — fix them all at once.** When a wave of bot PRs hits with identical failures (e.g. missing go.sum entry across 5 repos), clone each branch, run `go mod tidy`, and push in one session rather than one by one.

- **After your fix PR merges, bot PRs targeting the same files will have conflicts.** Tick the rebase checkbox to get Renovate to rebase. If the conflict is in go.mod/go.sum, Renovate will re-run artifact updates as part of the rebase.

- **Coverage drop from removing covered code is not a regression to fix with arbitrary tests.** If you delete duplicated or misplaced code that happened to be well-covered, overall coverage may dip. The right response is to explain why to the team — not to add pointless tests just to hit a number. If coverage is enforced as a CI gate and blocking merges, consider making it non-blocking (`continue-on-error: true`) rather than gaming the percentage.

## Triage standards

- **One root cause can affect many repos.** Always check the full list of open Konflux PRs before starting — a pattern across repos points to a shared dependency or a shared library as the source.
- **Check the package's maintenance status** (archived? last commit date? open issues?) before deciding on a fix strategy. An archived package needs replacement; a recently released package may just need a version bump.
- **Check release dates.** If a breaking change was released very recently, downstream packages may not have had time to react yet. Document this and park the PR rather than applying a workaround.
- **The renovate.json in these repos is centrally managed** (synced from `processing-tools`) — do not edit it in downstream repos to work around dependency conflicts. Fix the conflict properly.
- **If a failure involves a processing-tools version bump** (pre-commit hooks, shared workflows, shared scripts), always ask the user before fixing it in the downstream repo. The right fix may be upstream in `processing-tools` itself — which is our repo and where the change should live. Fixing it downstream is a workaround; fixing it upstream unblocks all repos at once.
- **Never add files to repos unnecessarily.** The fix should be the minimum change that resolves the incompatibility — a go.mod update, an import swap, a version bump. Not a new source file unless genuinely required.

---

## Common failure patterns

| Symptom | Likely cause | Where to look |
|---------|-------------|---------------|
| Build fails with `undefined`, `no field`, `cannot use` on a transitive dep | Breaking API change in a bumped package used by a shared library | Check which shared library pulls in the broken package; fix there |
| Python `ResolutionImpossible` | Two bumped packages require incompatible ranges of a shared transitive dep | Read both packages' dependency specs; align the versions |
| `go: updates to go.mod needed` | Renovate artifact update failed; go.sum is stale — often caused by a bogus module path in go.mod | See below |
| All checks fail on a Go PR, Konflux pipeline also fails | Usually a compile error, not flaky tests | Read build logs, not test logs |
| GitHub Actions fail but Konflux pipeline passes | Environmental / infrastructure failure in GHA | `/retest` to retrigger |

### Fixing a stale or broken go.mod on a bot PR branch

When `go mod tidy` is needed and the rebase checkbox hasn't helped, fix it directly on the bot branch:

```bash
BRANCH=$(gh pr view <PR_NUMBER> --repo RedHatInsights/<REPO> --json headRefName --jq '.headRefName')
git clone git@github.com:RedHatInsights/<REPO>.git <REPO>-fix
cd <REPO>-fix
git fetch origin $BRANCH && git checkout $BRANCH
```

Check for obviously wrong entries — Renovate occasionally introduces bogus module paths (e.g. changing `github.com/foo/bar v1+incompatible` to `github.com/foo/bar/v3` when the real v3 is at a completely different path). If something looks wrong, remove it:

```bash
sed -i '' '/bogus-module-path/d' go.mod
go mod tidy
go build ./...
go test ./...
git add go.mod go.sum
git commit -m "chore: fix go.mod and run go mod tidy"
git push origin $BRANCH
```

`go mod tidy` will restore any indirect dependency that is genuinely still needed (at the correct module path), and drop anything that isn't. Trust it.
