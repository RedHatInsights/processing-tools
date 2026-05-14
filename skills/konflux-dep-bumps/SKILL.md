---
name: konflux-dep-bumps
description: Triage and fix failing Konflux/MintMaker dependency bump PRs (bot-authored, auto-merge enabled). Use when a Renovate/MintMaker PR is stuck due to CI failures. Covers Go and Python repos in the RedHatInsights org.
---

# Konflux Dependency Bump Triage Skill

MintMaker (Renovate via Konflux) opens dependency bump PRs with auto-merge enabled. When CI fails the PR stalls. This skill covers triage, investigation, and resolution. Renovate documentation: https://github.com/renovatebot/renovate

---

## Step 0 — Get the current open Konflux bot PRs

**Source of truth:** https://github.com/RedHatInsights/processing-tools/tree/master/open_mr_pr/github

Check the `open-prs-konflux.md` file there. The date at the top of that file tells you when it was last generated. **If the date does not match today's date, the file is stale — run the fetcher locally and inform the user before proceeding:**

```bash
cd open_mr_pr/github
python3 list_repos_prs.py
cat open-prs-konflux.md
```

---

## Step 1 — Check what is failing

For each stuck PR:

```bash
gh pr checks <PR_NUMBER> --repo RedHatInsights/<REPO>
```

Note every failing check. The most common are: Go tests, lint, BDD (Behavior-Driven Development) tests, Konflux pipeline, enterprise contract, artifact update (`renovate/artifacts`). Multiple failures often share a single root cause — fix the root and the rest clear.

---

## Step 2 — Read the logs and identify the root cause

**GitHub Actions failures** — use `gh run view`:

```bash
gh run view <RUN_ID> --repo RedHatInsights/<REPO> --log-failed 2>&1 | grep -E "undefined|cannot use|no field|incompatible|conflict|Error|FAILED" | head -40
```

**Konflux pipeline failures (bonfire-tekton, on-pull-request, or any check containing "konflux")** — see the Konflux / bonfire failures subsection in Step 3 for how to read the logs. Do not skip it.

**Understand what broke before deciding how to fix it.** The PR description lists every bumped package with links to release notes — read them for the relevant version. Look specifically for breaking changes: removed fields, renamed types, changed function signatures, altered dependency requirements.

Key questions to answer:
- Which bumped package introduced the breakage?
- Is it the bumped package itself that broke, or something that depends on it?
- Is the broken package archived or unmaintained?
- Is the breakage in this repo's own code, or in a shared library that this repo depends on?

**The last question matters most for scoping the fix.** If the breakage originates in a shared library, fixing it there unblocks all downstream repos at once. Always check whether a direct dependency of the repo is pulling in the broken package transitively (`go mod graph`, `go.mod` indirect entries) before deciding where to fix.

---

## Step 3 — Apply the fix

Each approach below has a specific use case. Read the logs first before choosing.

### go mod tidy

**When:** `go: updates to go.mod needed`, missing go.sum entries, or any broken go.mod/go.sum artifact after a version bump.

```bash
BRANCH=$(gh pr view <PR_NUMBER> --repo RedHatInsights/<REPO> --json headRefName --jq '.headRefName')
git clone git@github.com:RedHatInsights/<REPO>.git /tmp/<REPO>-fix
cd /tmp/<REPO>-fix
git fetch origin $BRANCH && git checkout FETCH_HEAD -b fix-go-sum
go mod tidy
go build ./...
git add go.mod go.sum
git commit -m "chore: run go mod tidy to fix missing go.sum entries"
git push origin fix-go-sum:$BRANCH
```

If `go mod tidy` reverts all of Renovate's changes (go.mod ends up the same as master), the bot PR has no real effect. Let the user know and present the options — do not act yourself:
- **Let pipelines run and merge** — preferred, signals to Renovate the bump is handled and prevents recreation.
- **Close** — may cause Renovate to recreate the PR.

### Rebase (empty commit)

**When:** changes have been merged to master since the bot PR was opened and no new commit has re-triggered CI with the updated base. An empty commit kicks off a fresh CI run picking up the latest state.

**Read the logs first** — do not rebase without understanding what failed.

Note: `/rebase` as a comment does **not** work in these repos. The rebase checkbox in the PR description also works as an alternative to the empty commit.

```bash
BRANCH=$(gh pr view <PR_NUMBER> --repo RedHatInsights/<REPO> --json headRefName --jq '.headRefName')
git fetch origin $BRANCH && git checkout $BRANCH
git commit --allow-empty -m "chore: trigger Renovate rebase"
git push origin $BRANCH
```

### Retest

**When:** the failure is environmental or infrastructure-related and unrelated to the dependency change. In practice this is most relevant for Konflux jobs — e.g. Kafka unreachable, OpenShift Cluster Manager API errors, bonfire `reserve-namespace` timeout, cluster resource pressure. `/retest` re-triggers CI and has the same effect as an empty commit for this purpose.

**Read the logs first** — confirm the failure is actually environmental before retesting. Check if the Konflux pipeline passed while GitHub Actions failed, or if the error is clearly infra (e.g. `Insufficient cpu`, `ImagePullBackOff` caused by image pull rate limits being exceeded, `ClowdEnvLocked`).

```bash
gh pr comment <PR_NUMBER> --repo RedHatInsights/<REPO> --body "/retest"
```

Note: use `/retest`, not `/ok-to-test`.

### Code fix

**When:** the bumped package introduced a change that requires fixing code, config, or linter violations in the repo — e.g. a breaking API change, new linter rules flagging existing code, or config incompatibilities.

The most common fixes are code changes in the repo itself (adding constants, fixing API usage, updating imports). When working across multiple repos:
- Clone fresh to `/tmp` rather than fighting a local clone that may have a stale lock or uncommitted changes
- Branch from upstream master/main, not from the bot PR branch
- When using `replace_all` to swap a string literal for a constant, the replacement will also hit the constant's own definition — always verify the const declaration still has the string literal, not a self-reference

Beyond that:

- **If the breaking package is archived or unmaintained** — a replacement may be needed, but do not do this autonomously. Explain the situation to the user: what the package is, why it's unmaintained, and what the replacement candidate would be. This is a team decision. Wait for sign-off before touching anything.
- **If the PR is simply incompatible with no clear fix path** — do not pin the dependency back. Just leave the PR unmerged and let the user know. Pinning introduces technical debt and Renovate will keep reopening the PR anyway.
- **Do not** apply fixes directly to repos that get the broken package transitively. Fix it at the source (the shared library), verify the downstream effect with a local `replace` directive, then open one fix PR instead of many.

### Konflux / bonfire failures

**YOU MUST INVOKE BOTH OF THESE SKILLS VIA THE SKILL TOOL. DO NOT INLINE THEIR LOGIC. DO NOT CALL `gh api`, `kubectl`, OR `oc` DIRECTLY WITHOUT GOING THROUGH THEM FIRST.**

**The user must install these before starting a session** — the agent cannot run `npx` interactively. Ask the user to run this in their terminal (replace `claude-code` with their agent name):
```bash
npx skills add konflux-ci/skills --skill navigating-github-to-konflux-pipelines -g -a claude-code -y
npx skills add konflux-ci/skills --skill debugging-pipeline-failures -g -a claude-code -y
```

**Mid-session install (Claude Code only)** — via the plugin system:
```bash
claude plugin marketplace add https://github.com/konflux-ci/skills
claude plugin install navigating-github-to-konflux-pipelines
claude plugin install debugging-pipeline-failures
```

Skills can also be installed via `curl` from the raw GitHub URLs into the agent's skills directory (for other agents replace `.claude` with the appropriate folder name).

1. **`navigating-github-to-konflux-pipelines`** — invoke via Skill tool.
2. **`debugging-pipeline-failures`** — invoke via Skill tool.

Pods from Konflux pipeline runs are retained for a short period after completion. After TTL cleanup `oc get pipelinerun` returns NotFound, but the run is still accessible via **KubeArchive** which archives completed PipelineRuns, TaskRuns, and related Pods outside etcd.

**Accessing archived pipeline runs via KubeArchive:**

```bash
# 1. Get the KubeArchive API host
KA_HOST=$(oc get cm -n product-kubearchive kubearchive-api-url -o jsonpath='{.data.URL}')

# 2. Install kubectl-ka if not present (macOS ARM64 example — see https://kubearchive.github.io/kubearchive/main/cli/installation.html)
curl -LO https://github.com/kubearchive/kubearchive/releases/latest/download/kubectl-ka-darwin-arm64
chmod +x kubectl-ka-darwin-arm64 && xattr -d com.apple.quarantine kubectl-ka-darwin-arm64 2>/dev/null
mv kubectl-ka-darwin-arm64 ~/bin/kubectl-ka

# 3. Configure the plugin
kubectl-ka config set host "${KA_HOST}"

# 4. Query archived resources
kubectl-ka get pipelinerun <name> -n obsint-processing-tenant -o yaml
kubectl-ka get taskrun -n obsint-processing-tenant -l tekton.dev/pipelineRun=<pr-name> -o yaml

# 5. Get logs — use the pod name from the TaskRun's .status.podName field
POD=$(kubectl-ka get taskrun <taskrun-name> -n obsint-processing-tenant -o yaml | grep podName | awk '{print $2}')
kubectl-ka logs ${POD} -n obsint-processing-tenant -c step-<step-name>
```

If the token is expired, run `oc login --web --server=https://api.stone-prd-rh01.pg1f.p1.openshiftapps.com:6443` to refresh it — the user handles the browser part.

**WRONG:**
- ❌ Saying "I cannot access the logs"
- ❌ Saying "the token is expired, please paste the logs"
- ❌ Calling `gh api check-runs` directly without using the navigating skill
- ❌ Guessing the root cause without reading the logs

**CORRECT:**
- ✅ Invoke `navigating-github-to-konflux-pipelines` via Skill tool → get PipelineRun details
- ✅ Invoke `debugging-pipeline-failures` via Skill tool → read the actual logs
- ✅ If token is expired: refresh it and retry
- ✅ Report what the logs actually say

---

## Step 4 — Verify the fix before opening a PR

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

For any fix repo, always run all available tests and the linter locally:

```bash
# Go
go build ./... && go test ./...
# Also check Makefile for additional targets (BDD, integration, e2e)
grep -E "^test|^bdd|^e2e|^integration" Makefile

# Python
pip install -r requirements.txt && python -m pytest

# Linter — use the bumped version from the bot PR's .pre-commit-config.yaml, not the current one on master
golangci-lint run ./...
```

**Do not push without local tests and linter passing.**

---

## Step 5 — Open the fix PR

Use your existing fork, create a branch from the upstream default branch, apply the fix, run tests, then open a PR.

The PR description must include:
- What broke and why (cite the specific breaking change from release notes with a link)
- Why this fix is the right approach (not just what changed)
- A link to the Konflux bot PR it unblocks
- If fixing a shared library: note which downstream repos are affected

After opening, comment on the stuck Konflux bot PR linking to the fix and noting it can be retested once the fix merges.

---

## Step 6 — After the fix merges

Bot PRs do not auto-rebase when a fix lands. Trigger it manually using `gh pr update-branch` (preferred) or an empty commit as described in Step 3.

```bash
gh pr update-branch <PR_NUMBER> --repo RedHatInsights/<REPO>
```

For fixes in shared libraries, downstream bot PRs will not pick up the fix until Renovate opens a new bump including the updated shared library version.

---

## Triage standards

- **One root cause can affect many repos.** Always check the full list of open Konflux PRs before starting — a pattern across repos may point to a shared dependency or shared library as the source, or the same issue appearing independently in each repo due to the bumped package (e.g. a linter version bump introducing the same violation type across all repos).
- **Check the package's maintenance status** (archived? last commit date? open issues?) before deciding on a fix strategy. An archived package needs replacement — always raise this with the user before acting.
- **Check release dates.** If a breaking change was released very recently, downstream packages may not have had time to react yet. Document this and park the PR rather than applying a workaround.
- **The renovate.json in these repos is centrally managed** (synced from `processing-tools`) — do not edit it in downstream repos to work around dependency conflicts. Fix the conflict properly.
- **If a failure involves a processing-tools version bump** (pre-commit hooks, shared workflows, shared scripts), always ask the user before fixing it in the downstream repo. The right fix may be upstream in `processing-tools` itself — which is our repo and where the change should live. Fixing it downstream is a workaround; fixing it upstream unblocks all repos at once.
- **Never add files to repos unnecessarily.** The fix should be the minimum change that resolves the incompatibility — a go.mod update, an import swap, a version bump. Not a new source file unless genuinely required.
