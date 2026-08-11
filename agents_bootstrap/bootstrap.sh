#!/usr/bin/env bash
# Bootstrap a minimal AGENTS.md into ObsInt repos that do not have one.
#
# Targets = top-level Owner/repo keys in .github/sync.yml (same fleet as
# CODEOWNERS / CI sync). Skips repos that already have root AGENTS.md.
# Renders AGENTS.md.tmpl with simple text replacement of {{ repo_name }}.
#
# Usage:
#   ./agents_bootstrap/bootstrap.sh --dry-run
#   ./agents_bootstrap/bootstrap.sh --dry-run --repo RedHatInsights/foo
#   ./agents_bootstrap/bootstrap.sh --repo RedHatInsights/foo

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SYNC_YML="${REPO_ROOT}/.github/sync.yml"
TEMPLATE="${SCRIPT_DIR}/AGENTS.md.tmpl"
BRANCH_NAME="obsint-processing-app/bootstrap-agents-md"
PAGES_BASE="https://redhatinsights.github.io"
DRY_RUN=false
FILTER_REPOS=()

usage() {
  sed -n '2,14p' "$0" | sed 's/^# \?//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --sync-yml) SYNC_YML="$2"; shift 2 ;;
    --template) TEMPLATE="$2"; shift 2 ;;
    --repo) FILTER_REPOS+=("$2"); shift 2 ;;
    -h|--help) usage 0 ;;
    *) echo "Unknown arg: $1" >&2; usage 1 ;;
  esac
done

if [[ ! -f "${SYNC_YML}" ]]; then
  echo "sync.yml not found: ${SYNC_YML}" >&2
  exit 1
fi
if [[ ! -f "${TEMPLATE}" ]]; then
  echo "template not found: ${TEMPLATE}" >&2
  exit 1
fi
command -v gh >/dev/null || { echo "gh CLI required" >&2; exit 1; }

# Top-level keys like "RedHatInsights/foo:" from sync.yml (ignore comments / nested)
list_repos_from_sync() {
  grep -E '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+:[[:space:]]*$' "${SYNC_YML}" \
    | sed 's/:[[:space:]]*$//' \
    | sort -u
}

agents_md_exists() {
  local full_name="$1"
  local out
  if out="$(gh api "repos/${full_name}/contents/AGENTS.md" --jq .path 2>/dev/null)"; then
    [[ -n "${out}" ]]
  else
    return 1
  fi
}

render_template() {
  local repo_name="$1"
  # Same {{ var }} style as workflows_examples/*.tmpl / sync.yml templates
  sed "s/{{ repo_name }}/${repo_name}/g" "${TEMPLATE}"
}

ensure_branch() {
  local full_name="$1" base="$2" branch="$3"
  if gh api "repos/${full_name}/git/ref/heads/${branch}" >/dev/null 2>&1; then
    return 0
  fi
  local sha
  sha="$(gh api "repos/${full_name}/git/ref/heads/${base}" --jq .object.sha)"
  gh api --method POST "repos/${full_name}/git/refs" \
    -f "ref=refs/heads/${branch}" \
    -f "sha=${sha}" >/dev/null
}

put_agents_md() {
  local full_name="$1" branch="$2" content="$3"
  local encoded payload sha
  encoded="$(printf '%s' "${content}" | base64 | tr -d '\n')"
  payload="$(jq -n \
    --arg msg "docs: bootstrap minimal AGENTS.md" \
    --arg content "${encoded}" \
    --arg branch "${branch}" \
    '{message: $msg, content: $content, branch: $branch}')"
  if sha="$(gh api "repos/${full_name}/contents/AGENTS.md?ref=${branch}" --jq .sha 2>/dev/null)"; then
    payload="$(jq -c --arg sha "${sha}" '. + {sha: $sha}' <<<"${payload}")"
  fi
  gh api --method PUT "repos/${full_name}/contents/AGENTS.md" --input - <<<"${payload}" >/dev/null
}

open_draft_pr() {
  local full_name="$1" base="$2" branch="$3" repo_name="$4"
  local existing body
  existing="$(gh pr list --repo "${full_name}" --head "${branch}" --state open \
    --json url --jq '.[0].url' 2>/dev/null || true)"
  if [[ -n "${existing}" && "${existing}" != "null" ]]; then
    echo "${existing}"
    return 0
  fi
  body="$(cat <<EOF
## Summary
- Bootstrap a **minimal** root \`AGENTS.md\` for agent onboarding.
- Includes ObsInt Processing **Team context** (team-info links) plus stable links to \`./README.md\` and GitHub Pages (\`${PAGES_BASE}/${repo_name}/\`).

## Notes
- This is an intentional thin stub — not a full architecture / Common Tasks doc.
- Enrich later by hand, or use the \`create-agents-md\` skill in processing-tools for a deeper pass.
- Pages URL follows the conventional \`redhatinsights.github.io/<repo>/\` pattern; it may 404 until Pages are enabled.

## Test plan
- [ ] Skim AGENTS.md Team context + External References
- [ ] Confirm README / Pages links are acceptable for this repo
EOF
)"
  gh pr create --repo "${full_name}" --draft --base "${base}" --head "${branch}" \
    --title "docs: bootstrap minimal AGENTS.md" \
    --body "${body}"
}

process_repo() {
  local full_name="$1"
  local owner repo_name content base url
  owner="${full_name%%/*}"
  repo_name="${full_name#*/}"

  if agents_md_exists "${full_name}"; then
    echo "SKIP ${full_name}: AGENTS.md already present"
    return 0
  fi

  content="$(render_template "${repo_name}")"

  if [[ "${DRY_RUN}" == true ]]; then
    echo "DRY-RUN ${full_name}: would open draft PR adding AGENTS.md (Pages → ${PAGES_BASE}/${repo_name}/)"
    return 0
  fi

  base="$(gh api "repos/${full_name}" --jq .default_branch)"
  ensure_branch "${full_name}" "${base}" "${BRANCH_NAME}"
  put_agents_md "${full_name}" "${BRANCH_NAME}" "${content}"
  url="$(open_draft_pr "${full_name}" "${base}" "${BRANCH_NAME}" "${repo_name}")"
  echo "PR ${full_name}: ${url}"
}

repos=()
if [[ ${#FILTER_REPOS[@]} -gt 0 ]]; then
  repos=("${FILTER_REPOS[@]}")
else
  while IFS= read -r line; do
    [[ -n "${line}" ]] && repos+=("${line}")
  done < <(list_repos_from_sync)
fi

if [[ ${#repos[@]} -eq 0 ]]; then
  echo "No target repos" >&2
  exit 1
fi

echo "Targets: ${#repos[@]} repo(s); dry_run=${DRY_RUN}"
failures=0
for full_name in "${repos[@]}"; do
  if ! process_repo "${full_name}"; then
    echo "ERROR ${full_name}" >&2
    failures=$((failures + 1))
  fi
done
exit "${failures}"
