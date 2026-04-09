from jira import close_issue
from main import MAX_DAYS_OF_INACTIVITY, get_jira_issues_with_last_seen_older_than

if __name__ == "__main__":
    jira_issues_with_last_seen = get_jira_issues_with_last_seen_older_than(
        MAX_DAYS_OF_INACTIVITY
    )

    for issue in jira_issues_with_last_seen["issues"]:
        print(f"Closing {issue['key']}")
        comment = (
            f"This issue has been inactive for {MAX_DAYS_OF_INACTIVITY} days so it might be a "
            "duplicate.\n"
            "You may need to delete it on Glitchtip so that it creates a new Jira if it ever "
            "happens again."
        )

        response = close_issue(
            issue["id"],
            comment=comment,
        )
