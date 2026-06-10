#!/usr/bin/env bash
# Check a list of Jira tickets for [AI suggestion] comments.
# Usage: ./check_triaged.sh CCXDEV-111 CCXDEV-222 CCXDEV-333
set -euo pipefail

for ticket in "$@"; do
    echo "=== $ticket ==="
    jira issue view "$ticket" --comments 50 --plain 2>&1 \
        | grep -A2 "\[AI suggestion\]" || echo "No AI suggestion comment"
done
