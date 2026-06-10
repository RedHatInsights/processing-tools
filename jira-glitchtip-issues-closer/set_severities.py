import sys
from datetime import datetime, timezone

from jira_glitchtip_mixin import get_glitchtip_issue_from_jira_issue
from jira_helper import get_issues as get_jira_issues

events_per_sec_threshold = {
    0.005: "Critical",
    0.0005: "Major",
    0.0: "Normal",
}


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    issues = get_jira_issues()

    for issue in issues:
        if (
            not force
            and issue.fields.priority is not None
            and issue.fields.priority.name != "Undefined"
        ):
            continue  # already defined by the script or manually, skip it

        glitchtip_issue = get_glitchtip_issue_from_jira_issue(issue)
        if glitchtip_issue is None:
            continue  # Jira closer script will handle this

        try:
            first_seen = datetime.fromisoformat(glitchtip_issue.get("firstSeen"))
            time_since_first_seen = datetime.now(timezone.utc) - first_seen
            events_per_sec = (
                int(glitchtip_issue.get("count"))
                / time_since_first_seen.total_seconds()
            )

        except Exception:
            print(
                f"Could not parse firstSeen for {issue.key}: {glitchtip_issue.get('firstSeen')}"
            )
            continue

        for threshold, severity in events_per_sec_threshold.items():
            if events_per_sec >= threshold:
                severity = severity
                break

        print(f"Setting severity of {issue.key} to {severity}")

        if not dry_run:
            try:
                issue.update(fields={"priority": {"name": severity}})

            except Exception as e:
                print(f"Could not set severity of {issue.key} to {severity}: {e}")
                continue
