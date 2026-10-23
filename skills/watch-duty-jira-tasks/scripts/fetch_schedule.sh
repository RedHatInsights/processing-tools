#!/usr/bin/env bash
#
# Fetch the CCX processing IC (watch duty) schedule YAML from app-interface
# over HTTPS. This is the source of truth for the on-call rotation.
#
# Usage: ./fetch_schedule.sh [ref]
#   ref  git ref to read from (default: master)
#
# Requires: curl. If the file lives in a private GitLab project, export
# GITLAB_TOKEN with read access; it will be sent as a PRIVATE-TOKEN header.

set -euo pipefail

REF="${1:-master}"

# app-interface project on gitlab.cee.redhat.com and the schedule path.
GITLAB_HOST="${GITLAB_HOST:-gitlab.cee.redhat.com}"
PROJECT_PATH="service/app-interface"
FILE_PATH="data/teams/insights/schedules/ccx-processing-ic.yml"

# URL-encode the project path and file path for the GitLab raw files API.
enc() { python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' "$1"; }

url="https://${GITLAB_HOST}/api/v4/projects/$(enc "$PROJECT_PATH")/repository/files/$(enc "$FILE_PATH")/raw?ref=${REF}"

if [[ -n "${GITLAB_TOKEN:-}" ]]; then
    curl -fsSL -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" "$url"
else
    curl -fsSL "$url"
fi
