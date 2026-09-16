#!/usr/bin/env bash
# Fetch Konflux PipelineRun task logs from the live cluster or KubeArchive.
set -euo pipefail

readonly KA_HOST="https://kubearchive-api-server-product-kubearchive.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com"
readonly CLUSTER_API="https://api.stone-prd-rh01.pg1f.p1.openshiftapps.com:6443"

usage() {
  cat <<'EOF'
Usage:
  fetch_konflux_logs.sh <konflux-ui-url>
  fetch_konflux_logs.sh --namespace NS --pipelinerun NAME [--task TASK] [--output FILE]

Examples:
  fetch_konflux_logs.sh 'https://konflux-ui.apps.stone-prd-rh01.../ns/obsint-processing-tenant/applications/insights-on-prem/pipelineruns/insights-on-prem-on-pull-request-hlg4m/logs?task=build-container'
  fetch_konflux_logs.sh -n obsint-processing-tenant -p insights-on-prem-on-pull-request-hlg4m -t build-container -o build.log

Requires: oc (logged in), tkn, jq, curl
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "error: '$1' not found in PATH" >&2
    exit 1
  }
}

normalize_server() {
  local url="${1%/}"
  url="${url#https://}"
  url="${url#http://}"
  echo "$url"
}

parse_url() {
  local url="$1"
  [[ "$url" =~ /ns/([^/]+)/applications/[^/]+/pipelineruns/([^/?]+) ]] || {
    echo "error: could not parse namespace/pipelinerun from URL" >&2
    exit 1
  }
  NAMESPACE="${BASH_REMATCH[1]}"
  PIPELINERUN="${BASH_REMATCH[2]}"
  if [[ "$url" =~ task=([^&]+) ]]; then
    TASK="${BASH_REMATCH[1]}"
  fi
}

ensure_logged_in() {
  if ! oc whoami >/dev/null 2>&1; then
    echo "error: not logged in. Run:" >&2
    echo "  oc login ${CLUSTER_API} --web" >&2
    exit 1
  fi

  local current expected
  current="$(normalize_server "$(oc whoami --show-server)")"
  expected="$(normalize_server "$CLUSTER_API")"
  if [[ "$current" != "$expected" ]]; then
    echo "error: logged in to wrong cluster (${current}). Run:" >&2
    echo "  oc login ${CLUSTER_API} --web" >&2
    exit 1
  fi
}

fetch_live() {
  local args=(-n "$NAMESPACE")
  [[ -n "$TASK" ]] && args+=(-t "$TASK")

  local stderr_file logs err
  stderr_file="$(mktemp)"
  if logs="$(tkn pipelinerun logs "$PIPELINERUN" "${args[@]}" 2>"$stderr_file")"; then
    rm -f "$stderr_file"
    echo "$logs"
    return 0
  fi

  err="$(cat "$stderr_file")"
  rm -f "$stderr_file"

  if echo "$err" | grep -qiE 'not found|doesn.t exist|couldn.t find|no pipelinerun'; then
    return 2
  fi

  echo "error: failed to fetch live logs:" >&2
  echo "$err" >&2
  return 1
}

fetch_archived_status() {
  local token
  token="$(oc whoami -t)"
  curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/apis/tekton.dev/v1/namespaces/${NAMESPACE}/pipelineruns/${PIPELINERUN}" \
    | jq -r '.status.conditions[-1] | "\(.status)\t\(.reason)\t\(.message // "")"'
}

list_archived_taskruns() {
  local token
  token="$(oc whoami -t)"
  curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/apis/tekton.dev/v1/namespaces/${NAMESPACE}/taskruns?labelSelector=tekton.dev/pipelineRun=${PIPELINERUN}" \
    | jq -r '.items[] | "\(.metadata.name)\t\(.metadata.labels["tekton.dev/pipelineTask"])\t\(.status.conditions[-1].status // "?")\t\(.status.conditions[-1].reason // "?")"'
}

fetch_archived_task_logs() {
  local taskrun="$1"
  local token pod taskrun_json failed_steps step container
  token="$(oc whoami -t)"

  taskrun_json="$(curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/apis/tekton.dev/v1/namespaces/${NAMESPACE}/taskruns/${taskrun}")"

  pod="$(echo "$taskrun_json" | jq -r '.status.podName // empty')"
  if [[ -z "$pod" || "$pod" == "null" ]]; then
    pod="$(curl -sf -H "Authorization: Bearer ${token}" \
      "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods?labelSelector=tekton.dev/taskRun=${taskrun}" \
      | jq -r '.items[0].metadata.name')"
  fi

  if [[ -z "$pod" || "$pod" == "null" ]]; then
    echo "error: no archived pod found for taskrun ${taskrun}" >&2
    return 1
  fi

  failed_steps="$(echo "$taskrun_json" | jq -r '
    .status.steps[]? | select(.terminated.exitCode != 0 and .terminated.exitCode != null) | .name
  ')"

  if [[ -n "$failed_steps" ]]; then
    while IFS= read -r step; do
      [[ -z "$step" ]] && continue
      container="step-${step}"
      echo "=== ${container} ==="
      curl -sf -H "Authorization: Bearer ${token}" \
        "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods/${pod}/log?container=${container}" || \
        echo "warning: no logs for ${container}" >&2
    done <<< "$failed_steps"
    return 0
  fi

  container="$(curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods/${pod}" \
    | jq -r '[.spec.containers[].name | select(startswith("step-"))] | last // .spec.containers[0].name')"

  curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods/${pod}/log?container=${container}"
}

resolve_taskrun() {
  local -a taskruns=()
  local -a failed=()
  local line taskrun task_name status reason

  while IFS=$'\t' read -r taskrun task_name status reason; do
    [[ -z "$taskrun" ]] && continue
    if [[ -n "$TASK" && "$task_name" != "$TASK" ]]; then
      continue
    fi
    taskruns+=("$taskrun")
    if [[ "$status" == "False" ]]; then
      failed+=("$taskrun")
    fi
  done < <(list_archived_taskruns)

  if [[ ${#failed[@]} -gt 1 && -z "$TASK" ]]; then
    echo "error: multiple failed tasks; specify --task:" >&2
    list_archived_taskruns >&2
    return 1
  fi

  if [[ ${#failed[@]} -eq 1 ]]; then
    echo "${failed[0]}"
    return 0
  fi

  if [[ ${#taskruns[@]} -ge 1 ]]; then
    echo "${taskruns[0]}"
    return 0
  fi

  return 1
}

NAMESPACE=""
PIPELINERUN=""
TASK=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    -n|--namespace) NAMESPACE="$2"; shift 2 ;;
    -p|--pipelinerun) PIPELINERUN="$2"; shift 2 ;;
    -t|--task) TASK="$2"; shift 2 ;;
    -o|--output) OUTPUT="$2"; shift 2 ;;
    http*) parse_url "$1"; shift ;;
    *) echo "error: unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "$NAMESPACE" && -n "$PIPELINERUN" ]] || {
  echo "error: namespace and pipelinerun are required" >&2
  usage
  exit 1
}

require_cmd oc
require_cmd tkn
require_cmd jq
require_cmd curl
ensure_logged_in

oc project "$NAMESPACE" >/dev/null

header() {
  echo "=== PipelineRun: ${PIPELINERUN} (namespace: ${NAMESPACE}) ==="
  [[ -n "$TASK" ]] && echo "=== Task: ${TASK} ==="
}

write_output() {
  if [[ -n "$OUTPUT" ]]; then
    cat >"$OUTPUT"
    echo "Logs saved to ${OUTPUT} ($(wc -l <"$OUTPUT") lines)" >&2
  else
    cat
  fi
}

# Try live cluster first.
fetch_live_result=0
logs="$(fetch_live)" || fetch_live_result=$?

if [[ "$fetch_live_result" -eq 0 ]]; then
  {
    header
    echo "=== Source: live cluster ==="
    echo "$logs"
  } | write_output
  exit 0
fi

if [[ "$fetch_live_result" -eq 1 ]]; then
  exit 1
fi

# Fall back to KubeArchive (PipelineRuns are GC'd quickly on stone-prd-rh01).
{
  header
  echo "=== Source: KubeArchive (PipelineRun not on live cluster) ==="
  echo
  echo "=== PipelineRun status ==="
  fetch_archived_status || echo "PipelineRun not found in KubeArchive"
  echo
  echo "=== TaskRuns ==="
  list_archived_taskruns
  echo

  taskrun="$(resolve_taskrun)" || {
    echo "error: no matching taskrun found${TASK:+ for task ${TASK}}" >&2
    exit 1
  }
  echo "=== Logs: ${taskrun} ==="
  fetch_archived_task_logs "$taskrun"
} | write_output
