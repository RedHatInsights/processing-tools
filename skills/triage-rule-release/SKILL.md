---
name: triage-rule-release
description: Triage CCX rule release pipeline failures — identifies failed stage/job, classifies root cause, and suggests a fix.
allowed-tools: Bash(curl:*), Bash(python3:*), Bash(gh pr:*), Bash(gh search:*), Bash(gh api:*), Bash(podman manifest inspect:*), AskUserQuestion
---

# Triage Rule Release

Triage failures in the CCX rule release pipeline ([ccx/ccx-rules-releaser](https://gitlab.cee.redhat.com/ccx/ccx-rules-releaser)).

## Prerequisites

- **VPN:** Red Hat VPN required — `gitlab.cee.redhat.com` is internal. If the script can't connect, check VPN.
- **Token:** `GITLAB_TOKEN` or `GL_TOKEN` env var — personal access token with `read_api` scope.
- **macOS SSL:** Python can't verify the Red Hat internal CA from the Keychain. One-time setup: `security find-certificate -a -p > ~/.ssl/certs.pem` then `export SSL_CERT_FILE=~/.ssl/certs.pem`. On Linux this is usually not needed.
- **Script:** `triage_rule_release.py` next to this file. Outputs JSON.

## Invocation

```
/triage-rule-release                        # Latest pipeline
/triage-rule-release <pipeline-id>          # Specific pipeline
/triage-rule-release <gitlab-url>           # Parse from URL
```

## Execution

1. Run `python3 triage_rule_release.py` (with optional pipeline ID or URL)
2. Show pipeline status and all jobs
3. For failed/stuck jobs, check downstream repos and images
4. For Jenkins failures, fetch the console log and find the actual error

## Pipeline

The pipeline triggers on a new `ccx-rules-ocp` tag (or manually with `CCX_RULES_TAG` variable). Notifications go to `#ccx-dev-notifications`.

Pipeline stages and jobs are defined in the [release.yaml](https://gitlab.cee.redhat.com/ccx/ccx-rules-releaser/-/blob/master/.gitlab/pipelines/release.yaml) file in the releaser repo. Refer to that file for the current list of jobs and their configuration.

## Images

After PRs merge in content-service and data-pipeline, Konflux push builds produce images. The `rules-containers-private` image is built by the rules-containers pipeline triggered earlier. Verify images exist with `podman manifest inspect <image>`.

| Image | Tag |
|-------|-----|
| `quay.io/redhat-services-prod/obsint-processing-tenant/content-service/content-service` | First 7 chars of content-service merge commit SHA |
| `quay.io/redhat-services-prod/obsint-processing-tenant/data-pipeline/data-pipeline` | First 7 chars of data-pipeline merge commit SHA |
| `quay.io/redhat-services-prod/obsint-processing-tenant/rules-containers/rules-containers-private` | `CCX_RULES_TAG` date (e.g. `2026.06.16`) |

Find merge commit SHA: `gh pr view <number> --repo RedHatInsights/<repo> --json mergeCommit --jq '.mergeCommit.oid[:7]'`

Check Konflux build: `gh api repos/RedHatInsights/<repo>/commits/<sha>/check-runs --jq '.check_runs[] | select(.name | test("on-push")) | {name, status, conclusion, completed_at}'`

## Checking downstream PRs

**GitHub** (content-service, data-pipeline):
```bash
gh pr list --repo RedHatInsights/<repo> --state all --search "ccx-rules-ocp" --limit 3
gh pr view <number> --repo RedHatInsights/<repo> --json state,mergeable,statusCheckRollup
```

**GitLab** (ccx-rules-metrics, rules-containers, molodec, iqe-ccx-plugin):
```bash
curl -s -H "PRIVATE-TOKEN: ${GITLAB_TOKEN:-$GL_TOKEN}" \
  "https://gitlab.cee.redhat.com/api/v4/projects/<url-encoded-path>/merge_requests?state=all&per_page=3&order_by=created_at&sort=desc"
```

URL-encoded paths: `ccx%2Fccx-rules-metrics`, `ccx%2Frules-containers`, `ccx%2Fmolodec`, `insights-qe%2Fiqe-ccx-plugin`

**Jenkins logs** (for `wait-rules-in-stage-internal`, `wait-inter-prod`, `jenkins-exter-pipe-test-prod`):
```bash
curl -s "https://jenkins-csb-ccx-dev-main.dno.corp.redhat.com/job/<job-name>/<build-num>/consoleText" | grep -B5 "FAILED\|AssertionError\|short test summary"
```
