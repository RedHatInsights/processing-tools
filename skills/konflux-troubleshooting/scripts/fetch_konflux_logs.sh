#!/usr/bin/env bash
# Fetch Konflux PipelineRun task logs from the live cluster or KubeArchive.
set -euo pipefail

KA_HOST="${KA_HOST:-https://kubearchive-api-server-product-kubearchive.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com}"
CLUSTER_API="${CLUSTER_API:-https://api.stone-prd-rh01.pg1f.p1.openshiftapps.com:6443}"

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
}

fetch_live() {
  local args=(-n "$NAMESPACE")
  [[ -n "$TASK" ]] && args+=(-t "$TASK")
  tkn pipelinerun logs "$PIPELINERUN" "${args[@]}" 2>/dev/null
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
    | jq -r '.items[] | "\(.metadata.name)\t\(.metadata.labels["tekton.dev/pipelineTask"])\t\(.status.conditions[-1].reason // "?")"'
}

fetch_archived_task_logs() {
  local taskrun="$1"
  local token pod container
  token="$(oc whoami -t)"

  pod="$(curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods?labelSelector=tekton.dev/taskRun=${taskrun}" \
    | jq -r '.items[0].metadata.name')"

  if [[ -z "$pod" || "$pod" == "null" ]]; then
    echo "error: no archived pod found for taskrun ${taskrun}" >&2
    return 1
  fi

  # step-build is the main container for build-container; fall back to all containers.
  container="$(curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods/${pod}" \
    | jq -r '.spec.containers[0].name')"

  curl -sf -H "Authorization: Bearer ${token}" \
    "${KA_HOST}/api/v1/namespaces/${NAMESPACE}/pods/${pod}/log?container=${container}"
}

resolve_taskrun() {
  local line taskrun task_name
  while IFS=$'\t' read -r taskrun task_name _; do
    if [[ -z "$TASK" || "$task_name" == "$TASK" ]]; then
      echo "$taskrun"
      return 0
    fi
  done < <(list_archived_taskruns)
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
if logs="$(fetch_live)"; then
  {
    header
    echo "=== Source: live cluster ==="
    echo "$logs"
  } | write_output
  exit 0
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
