---
name: konflux-troubleshooting
description: >-
  Troubleshoot Konflux PipelineRun failures on stone-prd-rh01 for the
  obsint-processing tenant. Fetch task logs (live cluster or KubeArchive),
  summarize failures, and escalate to upstream investigation skills. Use when
  a Konflux check fails, the user shares a Konflux UI URL, or asks why a
  build/pipeline failed or is slow.
---

# Konflux Troubleshooting

End-to-end troubleshooting for Konflux PipelineRuns on `stone-prd-rh01`. Completed runs are garbage-collected quickly — always try the live cluster first, then fall back to KubeArchive.

This skill covers **obsint-processing tenant workflows** (log fetch, local cluster constants, common failure patterns). For systematic PLR investigation and slow-build analysis, use the upstream skills from [konflux-ci/agent-plugins](https://github.com/konflux-ci/agent-plugins/tree/main/skills) ([PR #44](https://github.com/konflux-ci/agent-plugins/pull/44)):

| Skill | Use when |
|-------|----------|
| [investigating-failed-plrs](https://github.com/konflux-ci/agent-plugins/tree/main/skills/investigating-failed-plrs) | Root-cause analysis of failed PipelineRuns via KubeArchive (`oc ka`) |
| [investigating-slow-builds](https://github.com/konflux-ci/agent-plugins/tree/main/skills/investigating-slow-builds) | Slow builds — kueue queue time, task durations, quota pressure |
| [navigating-github-to-konflux-pipelines](https://github.com/konflux-ci/agent-plugins/tree/main/skills/navigating-github-to-konflux-pipelines) | Mapping a GitHub PR/commit to its Konflux PipelineRun |
| [component-build-status](https://github.com/konflux-ci/agent-plugins/tree/main/skills/component-build-status) | Checking overall component build health |
| [understanding-konflux-resources](https://github.com/konflux-ci/agent-plugins/tree/main/skills/understanding-konflux-resources) | Components, Applications, Snapshots, IntegrationTests |
| [konflux-architecture](https://github.com/konflux-ci/agent-plugins/tree/main/skills/konflux-architecture) | How Konflux pieces fit together |
| [working-with-provenance](https://github.com/konflux-ci/agent-plugins/tree/main/skills/working-with-provenance) | SLSA/provenance and attestation issues |

Install upstream skills when needed:

```bash
npx skills add konflux-ci/agent-plugins --skill navigating-github-to-konflux-pipelines -g -a claude-code -y
npx skills add konflux-ci/agent-plugins --skill investigating-failed-plrs -g -a claude-code -y
npx skills add konflux-ci/agent-plugins --skill investigating-slow-builds -g -a claude-code -y
```

## Prerequisites

The **user must log in to the cluster before the agent runs anything**:

```bash
oc login https://api.stone-prd-rh01.pg1f.p1.openshiftapps.com:6443 --web
```

Verify: `oc whoami`

### Dependencies

| Tool | Purpose | Install (macOS) |
|------|---------|-----------------|
| `oc` | Cluster auth + API token | `brew install openshift-cli` |
| `tkn` | Live PipelineRun logs | `brew install tektoncd-cli` |
| `jq` | Parse KubeArchive JSON | `brew install jq` |
| `curl` | KubeArchive HTTP API | usually preinstalled |

## Workflow

Copy this checklist when troubleshooting:

```text
- [ ] Confirm user is logged in (`oc whoami`)
- [ ] If starting from a GitHub PR, invoke navigating-github-to-konflux-pipelines → get PipelineRun URL/name
- [ ] Run fetch_konflux_logs.sh with the Konflux URL or pipelinerun name
- [ ] If live cluster fails, script auto-falls back to KubeArchive
- [ ] Summarize status, failed task, and root-cause error lines
- [ ] If logs alone are insufficient, invoke investigating-failed-plrs or investigating-slow-builds
- [ ] Save full logs to a file with --output when user may need them later
```

### Step 1 — Check login

```bash
oc whoami
```

If this fails, stop and ask the user to run `oc login ... --web`.

### Step 2 — Resolve the PipelineRun

- **Konflux UI URL provided** — extract namespace, pipelinerun, and optional task from the URL (see Quick start).
- **GitHub PR only** — invoke upstream `navigating-github-to-konflux-pipelines` to find the failing PipelineRun.

### Step 3 — Fetch logs (use the bundled script)

**Always use the bundled script** — do not re-implement the fetch logic inline:

```bash
bash skills/konflux-troubleshooting/scripts/fetch_konflux_logs.sh '<konflux-ui-url>'
```

Or with explicit args:

```bash
bash skills/konflux-troubleshooting/scripts/fetch_konflux_logs.sh \
  --namespace obsint-processing-tenant \
  --pipelinerun insights-on-prem-on-pull-request-hlg4m \
  --task build-container \
  --output /tmp/build-container.log
```

Konflux UI URL format:

```text
https://konflux-ui.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com/ns/{namespace}/applications/{app}/pipelineruns/{pipelinerun}/logs?task={task}
```

The script:
1. Sets the active project to the target namespace
2. Tries `tkn pipelinerun logs <name> -n <ns> [-t <task>]`
3. On "not found", queries KubeArchive for PipelineRun status, TaskRuns, and pod logs

### Step 4 — Summarize for the user

Report:
- PipelineRun name, namespace, overall status/reason
- Which task failed (e.g. `build-container` → `StepFailed`)
- The root-cause error lines (not the full log unless asked)
- Path to saved log file if `--output` was used

### Step 5 — Deeper investigation

If the failure needs more than a log read:
- **Failed/stuck PLR** — invoke upstream [investigating-failed-plrs](https://github.com/konflux-ci/agent-plugins/tree/main/skills/investigating-failed-plrs) (PLR conditions, TaskRun errors, timing scripts)
- **Slow/queued build** — invoke upstream [investigating-slow-builds](https://github.com/konflux-ci/agent-plugins/tree/main/skills/investigating-slow-builds)

Browse the full [skills index](https://github.com/konflux-ci/agent-plugins/tree/main/skills) for other relevant topics.

## Cluster constants

| Constant | Value |
|----------|-------|
| Cluster API | `https://api.stone-prd-rh01.pg1f.p1.openshiftapps.com:6443` |
| Konflux UI | `https://konflux-ui.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com` |
| KubeArchive API | `https://kubearchive-api-server-product-kubearchive.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com` |

Common namespace for obsint-processing: `obsint-processing-tenant`

## Manual fallback (only if script is unavailable)

```bash
# Live cluster
oc project <namespace>
tkn pipelinerun logs <pipelinerun> -n <namespace> -t <task>

# KubeArchive — PipelineRun status
curl -s -H "Authorization: Bearer $(oc whoami -t)" \
  "${KA_HOST}/apis/tekton.dev/v1/namespaces/<ns>/pipelineruns/<pr>"

# KubeArchive — list taskruns
curl -s -H "Authorization: Bearer $(oc whoami -t)" \
  "${KA_HOST}/apis/tekton.dev/v1/namespaces/<ns>/taskruns?labelSelector=tekton.dev/pipelineRun=<pr>"

# KubeArchive — pod logs (replace TASKRUN with e.g. <pr>-build-container)
POD=$(curl -s -H "Authorization: Bearer $(oc whoami -t)" \
  "${KA_HOST}/api/v1/namespaces/<ns>/pods?labelSelector=tekton.dev/taskRun=<TASKRUN>" \
  | jq -r '.items[0].metadata.name')
curl -s -H "Authorization: Bearer $(oc whoami -t)" \
  "${KA_HOST}/api/v1/namespaces/<ns>/pods/${POD}/log?container=step-build"
```

## Common failure patterns

| Symptom in logs | Likely cause |
|-----------------|--------------|
| `pg_config executable not found` during pip install | `psycopg2-binary` built from sdist; missing `postgresql-devel` in RPM prefetch |
| `SSLCertVerificationError` during prefetch | Missing `activation-key` secret in namespace |
| `nothing provides glibc = ...` in hermetic build | `rpms.in.yaml` `context.image` out of sync with Dockerfile `FROM` |
| PipelineRun not found (live + archive) | Wrong namespace/name, or archive retention expired |
| `Insufficient cpu`, long queue times | Quota/queue pressure — use investigating-slow-builds |

## Edge cases

- **Konflux UI URL without `?task=`**: script fetches the first matching taskrun; ask user which task if multiple failed.
- **Multiple failed tasks**: list taskruns from script output, re-run with `--task <name>`.
- **No logs in KubeArchive**: pod logs may have been purged; use TaskRun status/message only.
- **Wrong cluster**: this skill targets `stone-prd-rh01` only. Other clusters need different API/KubeArchive hosts.
