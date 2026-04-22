#!/usr/bin/env bash
# Update all GitHub/GitLab refs in ccx-data-pipeline saas files to latest commit SHAs.
# Skips ref: internal (ephemeral/bonfire targets), main and master.
# Usage: update_refs.sh [--dry-run] [--repo <name-or-url>]... [--local-folder <path>]
# --repo filters by exact repo name or full URL (can be repeated).
# --local-folder uses an existing app-interface checkout instead of cloning.
set -uo pipefail

declare -A SHA_CACHE=()  # repo_url -> latest_sha
declare -A BRANCH_CACHE=()  # repo_url -> default_branch
declare -a REPO_FILTERS=()  # exact repo URLs/names to update
DRY_RUN=false
PATH_TO_APP_INTERFACE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; echo "=== DRY RUN ===" ;;
        --repo)
            [[ -z "${2:-}" ]] && echo "ERROR: --repo requires a value" >&2 && exit 1
            REPO_FILTERS+=("$2"); shift ;;
        --local-folder)
            [[ -z "${2:-}" ]] && echo "ERROR: --local-folder requires a path" >&2 && exit 1
            PATH_TO_APP_INTERFACE="$2"; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
    shift
done

if [[ -z "$PATH_TO_APP_INTERFACE" ]]; then
    PATH_TO_APP_INTERFACE="/tmp/app-interface"
    if [[ -d "$PATH_TO_APP_INTERFACE/.git" ]]; then
        echo "App-interface repo already exists at $PATH_TO_APP_INTERFACE, skipping clone."
    else
        git clone --depth 1 git@gitlab.cee.redhat.com:service/app-interface.git "$PATH_TO_APP_INTERFACE"
    fi
fi

cd "$PATH_TO_APP_INTERFACE" || exit 1

git fetch origin master
git checkout master
git pull origin master

BASE_DIR="data/services/insights/ccx-data-pipeline"

repo_matches() {
    local url="$1"
    [[ ${#REPO_FILTERS[@]} -eq 0 ]] && return 0
    local repo_name="${url##*/}"
    for filter in "${REPO_FILTERS[@]}"; do
        [[ "$url" == "$filter" || "$repo_name" == "$filter" ]] && return 0
    done
    return 1
}

get_default_branch() {
    local url="$1"
    if [[ -n "${BRANCH_CACHE[$url]:-}" ]]; then
        REPLY="${BRANCH_CACHE[$url]}"
        return
    fi
    REPLY=$(git ls-remote --symref "$url" HEAD 2>/dev/null \
        | awk '/^ref:/{sub("ref: refs/heads/",""); print $1; exit}')
    [[ -z "$REPLY" ]] && REPLY="main"
    BRANCH_CACHE["$url"]="$REPLY"
}

get_latest_sha() {
    local url="$1"
    if [[ -n "${SHA_CACHE[$url]:-}" ]]; then
        REPLY="${SHA_CACHE[$url]}"
        return
    fi
    get_default_branch "$url"
    local branch="$REPLY"
    REPLY=$(git ls-remote "$url" "refs/heads/$branch" 2>/dev/null | awk '{print $1}')
    if [[ -z "$REPLY" ]]; then
        echo "WARNING: Could not fetch SHA for $url ($branch)" >&2
        return 1
    fi
    SHA_CACHE["$url"]="$REPLY"
}

process_file() {
    local file="$1"
    local current_url="" changes=0
    local tmpfile
    tmpfile=$(mktemp)

    while IFS= read -r line; do
        # Track current url context
        if [[ "$line" =~ ^[[:space:]]+url:[[:space:]]+(https://[^[:space:]]+) ]]; then
            current_url="${BASH_REMATCH[1]}"
        fi

        # Match ref lines, skip 'internal'
        if [[ "$line" =~ ^([[:space:]]+ref:[[:space:]]+)([^[:space:]]+)$ ]]; then
            local prefix="${BASH_REMATCH[1]}"
            local old_ref="${BASH_REMATCH[2]}"

            if [[ "$old_ref" != "internal" && "$old_ref" != "main" && "$old_ref" != "master" && -n "$current_url" ]] && repo_matches "$current_url"; then
                if get_latest_sha "$current_url"; then
                    local new_sha="$REPLY"
                    if [[ "$old_ref" != "$new_sha" ]]; then
                        echo "  $old_ref -> ${new_sha:0:7}... ($current_url)" >&2
                        line="${prefix}${new_sha}"
                        ((changes++)) || true
                    fi
                fi
            fi
        fi
        printf '%s\n' "$line"
    done < "$file" > "$tmpfile"

    if (( changes > 0 )); then
        echo "[$file] $changes ref(s) updated"
        if [[ "$DRY_RUN" == false ]]; then
            mv "$tmpfile" "$file"
        else
            rm "$tmpfile"
        fi
    else
        rm "$tmpfile"
    fi
}

if [[ ${#REPO_FILTERS[@]} -gt 0 ]]; then
    echo "Filtering repos: ${REPO_FILTERS[*]}"
fi

echo "Collecting YAML files from $BASE_DIR ..."
mapfile -t files < <(find "$BASE_DIR" -type f \( -name '*.yml' -o -name '*.yaml' \) | sort)

echo "Found ${#files[@]} YAML files. Scanning for refs..."
echo

for f in "${files[@]}"; do
    # Quick check: skip files without both url: and ref:
    if grep -qE '^\s+url:\s+https://' "$f" && grep -qE '^\s+ref:\s' "$f"; then
        process_file "$f"
    fi
done

echo
echo "Done. ${#SHA_CACHE[@]} unique repo(s) processed."
