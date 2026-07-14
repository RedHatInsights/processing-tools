import os
import sys

from jira_glitchtip_mixin import get_jira_issues_with_last_seen_older_than
from jira_helper import close_issue

DEFAULT_MAX_DAYS_OF_INACTIVITY = 7
MAX_DAYS_OF_INACTIVITY = int(
    os.environ.get("MAX_DAYS_OF_INACTIVITY", DEFAULT_MAX_DAYS_OF_INACTIVITY)
)

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv or os.environ.get("DRY_RUN", "").lower() in (
        "1",
        "true",
    )

    jira_issues_with_last_seen = get_jira_issues_with_last_seen_older_than(
        MAX_DAYS_OF_INACTIVITY
    )

    if dry_run:
        print(
            f"[DRY RUN] {len(jira_issues_with_last_seen)} issue(s) would be closed:\n"
        )

    for issue in jira_issues_with_last_seen:
        prefix = "[DRY RUN] Would close" if dry_run else "Closing"
        print(f"{prefix} {issue.jira_key}")
        comment = (
            f"This issue has been inactive for {MAX_DAYS_OF_INACTIVITY} days so it might be a "
            "duplicate.\n"
            "You may need to delete it on Glitchtip so that it creates a new Jira if it ever "
            "happens again."
        )

        if not dry_run:
            close_issue(issue.jira_key, comment=comment)
