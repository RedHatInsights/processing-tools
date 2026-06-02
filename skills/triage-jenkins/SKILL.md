---
name: triage-jenkins
description: Triage CCX Jenkins CI failures — classifies failure patterns (isolated blip, consecutive, flapping), analyzes logs, matches against known issues, and recommends action. Covers all active CCX jobs.
allowed-tools: Bash(curl:*), Bash(python3:*), AskUserQuestion
---

# Triage Jenkins

Triage failures for CCX Jenkins CI jobs. Classify whether a failure needs immediate investigation or is likely transient, analyze console logs for root cause, and match against known issues.

## Jenkins Instances

The script covers two Jenkins instances. Both are unauthenticated. A third (App-SRE Jenkins at `ci.int.devshift.net`) requires auth and is not covered.

| Instance | Base URL | Jobs path |
|----------|----------|-----------|
| **qe** (IQE CSB) | `https://jenkins-csb-insights-qe-main.dno.corp.redhat.com` | `/job/ccx/job/{JOB}` |
| **idp** (CCX CSB) | `https://jenkins-csb-ccx-dev-main.dno.corp.redhat.com` | `/job/{JOB}` |

Key APIs (same pattern on both, adjust path prefix):

| Endpoint | Returns |
|----------|---------|
| `{base}/api/json` | All jobs with `name`, `color` (blue=pass, red=fail, disabled) |
| `{base}/job/{JOB}/api/json` | Job overview: `lastBuild`, `lastFailedBuild`, `builds[]` |
| `{base}/job/{JOB}/{BUILD}/wfapi/describe` | Pipeline stages with status, duration |
| `{base}/job/{JOB}/{BUILD}/consoleText` | Full console log (plain text) |

## Active Jobs

### IQE CSB Jenkins (qe) — External Data Pipeline & UI

| Job Name | Environment | Area |
|----------|-------------|------|
| `ccx-external-data-pipeline-prod` | prod | External pipeline integration tests |
| `ccx-external-data-pipeline-stage-master` | stage | External pipeline integration tests |
| `ccx-advisor-ui-prod` | prod | Advisor UI tests |
| `ccx-advisor-ui-stage` | stage | Advisor UI tests |
| `ccx-fuzzy-stage` | stage | Fuzzy/fuzz tests |
| `ccx-io-gathering-prod` | prod | IO gathering tests |
| `ccx-io-gathering-stage-master` | stage | IO gathering tests |
| `ccx-notif-servicelog-prod-check` | prod | Notification/ServiceLog checks |
| `ccx-notif-servicelog-stage-check` | stage | Notification/ServiceLog checks |
| `ccx-prod-check` | prod | General prod health checks |
| `ccx-stage-check` | stage | General stage health checks |
| `ccx-update-risk-backend-prod` | prod | Upgrade risk prediction backend tests |
| `ccx-update-risk-backend-stage-master` | stage | Upgrade risk prediction backend tests |

### CCX CSB Jenkins (idp) — Internal Data Pipeline

| Job Name | Environment | Area |
|----------|-------------|------|
| `internal-pipeline-tests-prod` | prod | Internal pipeline integration tests |
| `internal-pipeline-tests-stage` | stage | Internal pipeline integration tests |
| `internal-pipeline-test-rules-version-prod` | prod | Rules version validation |
| `internal-pipeline-test-rules-version-stage` | stage | Rules version validation |
| `ccx-load-test-stage` | stage | Load/performance tests |

## Invocation

```text
/triage-jenkins                           # Overview of all active jobs
/triage-jenkins <job-name>                # Triage specific job
/triage-jenkins <job-name> <build-num>    # Triage specific build
/triage-jenkins <full-jenkins-url>        # Parse job/build from URL
```

When a full URL is passed, extract the job name and optional build number from it:
- `https://jenkins-csb-insights-qe-main.dno.corp.redhat.com/job/ccx/job/ccx-external-data-pipeline-prod/7756/display/redirect` → job=`ccx-external-data-pipeline-prod`, build=`7756`
- `https://jenkins-csb-insights-qe-main.dno.corp.redhat.com/blue/organizations/jenkins/ccx%2Fccx-external-data-pipeline-prod/activity` → job=`ccx-external-data-pipeline-prod`, no build
- `https://jenkins-csb-ccx-dev-main.dno.corp.redhat.com/job/internal-pipeline-tests-prod/5340/` → job=`internal-pipeline-tests-prod`, build=`5340`

## Script

The data-fetching script `triage_jenkins.py` lives next to this SKILL.md file. It outputs JSON — the agent does the pattern classification and triage logic described below.

## Execution

### Mode 1: Overview (no arguments)

Run `python3 triage_jenkins.py` to get all jobs from both Jenkins instances with their last 7 builds, then classify:

1. The script fetches from both instances and returns a combined job list. Each job has an `instance` field (`qe` or `idp`).
2. For each non-disabled job, classify:
   - **healthy** — all green
   - **isolated-blip** — single red surrounded by green, and the most recent build is green
   - **flapping** — alternating red/green (3+ status changes in last 7 builds)
   - **consecutive-fail** — 2+ reds in a row at the head (most recent builds failing)
   - **recovering** — was failing, most recent build is green

3. Present a dashboard table:

```text
CCX Jenkins Dashboard
=====================

Job                                      Status           Last Fail   Pattern
─────────────────────────────────────────────────────────────────────────────────
ccx-external-data-pipeline-prod          ✅ healthy        #7756 (1d)  isolated-blip (resolved)
ccx-update-risk-backend-stage-master     ⚠️  flapping      #4746 (2h)  alternating pass/fail
ccx-advisor-ui-prod                      ✅ healthy        —           all green
...
```

4. For any job that is **flapping** or **consecutive-fail**, automatically run Phase 2 analysis.

### Mode 2: Single Job Triage

#### Phase 1 — Pattern Classification

1. Fetch the last 7 builds for the job:
   ```text
   for build_num in range(last_build, last_build-7, -1):
       GET /job/ccx/job/{JOB_NAME}/{build_num}/api/json?tree=number,result,timestamp,duration
   ```

2. Classify the failure pattern:

   **isolated-blip**: The failed build has SUCCESS on both sides (before and after). This means:
   - The next build (higher number) after the failure is SUCCESS
   - The build immediately before the failure is SUCCESS
   - Verdict: "Transient failure. Build #{N+1} passed. No action needed unless this recurs."

   **consecutive-fail**: 2+ FAILURE results in a row at the head of the build history (most recent builds).
   - Verdict: "Persistent failure — needs investigation. Failing since build #{first_fail}."

   **flapping**: 3+ status transitions in the last 7 builds (e.g. pass→fail→pass→fail).
   - Verdict: "Intermittent/flaky — investigate for environmental instability or flaky tests."

   **recovering**: Last build is SUCCESS but there were recent failures.
   - Verdict: "Recently recovered. Monitor for recurrence."

3. If the pattern is **isolated-blip** and the most recent build is green, report the verdict and stop unless the user asks for details.

#### Phase 2 — Failure Analysis

For **consecutive-fail**, **flapping**, or when the user asks for details:

1. Run `python3 triage_jenkins.py <job-name> <build-num>` to get stages, failed tests, and error messages.

2. **Match against known issues** (see Known Issues Catalog below).

3. **Cross-build comparison** — for flapping failures, run the script for the last 2-3 failed builds and check if the same tests fail each time:
   - Same tests every time → likely a real bug
   - Different tests → likely environmental instability

## Known Issues Catalog

Match these patterns against the `short test summary info` lines and error messages.

### SSO_RATE_LIMIT
- **Pattern:** `429.*Too Many Requests.*sso.` or `429 Client Error.*sso.stage.redhat.com`
- **Meaning:** SSO token endpoint is rate-limiting the test runner.
- **Typical cause:** Too many token requests in a short window.
- **Action:** Self-resolves.

## Adding New Known Issues

When you encounter a novel failure pattern that recurs, add it to this catalog following the format above. Each entry needs:
- A short `SCREAMING_SNAKE_CASE` identifier
- **Pattern:** regex or substring to match in the test summary or error message
- **Meaning:** what the error indicates
- **Typical cause:** most common root cause
- **Action:** concrete next step for the triager

## Edge Cases

- **Build still running:** If the latest build has `result: null` and `building: true`, note it's in progress and triage the last completed build instead.
- **No failures found:** Report "All green — no failures in the last N builds."
- **Console log unavailable:** Some builds may have been cleaned up. Note that the log is unavailable and rely on the build metadata only.
- **Very large console logs:** The console logs can be 10k+ lines. The script extracts the `short test summary info` section automatically — do not attempt to read raw logs directly.
- **Multiple job URLs in input:** If the user pastes multiple URLs, triage each one.
- **Non-CCX job URL:** If the URL points to a non-CCX job, attempt the triage anyway — the same pattern classification logic applies.
