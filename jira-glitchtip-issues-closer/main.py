import os
from datetime import datetime, timezone

from glitchtip import GLITCHTIP_DATE_FORMAT, GLITCHTIP_DOMAIN, get_issue
from glitchtip import get_issues as glitchtip_issues
from jira import JIRA_DOMAIN, get_issues

DEFAULT_MAX_DAYS_OF_INACTIVITY = 7
MAX_DAYS_OF_INACTIVITY = int(
    os.environ.get("MAX_DAYS_OF_INACTIVITY", DEFAULT_MAX_DAYS_OF_INACTIVITY)
)

TEMPLATE = """# Glitchtip <-> Jira integration checker

*Last updated: {timestamp}*

## Open Jira issues for Glitchtip events

**Total: {jira_count} issue(s)**

| Jira | Glitchtip | Days since last event |
|------|-----------|----------------------|
{jira_table_rows}

## Glitchtip events with no Jira issues

**Total: {glitchtip_count} issue(s)**

| Glitchtip | Days since last event |
|-----------|----------------------|
{glitchtip_table_rows}
"""


def get_last_seen_in_days(issue):
    try:
        last_seen = datetime.strptime(issue["lastSeen"], GLITCHTIP_DATE_FORMAT)
    except KeyError:
        return None

    diff = datetime.now(timezone.utc) - last_seen
    return diff.days


def get_jira_issues_with_last_seen_older_than(max_days_of_inactivity: int):
    """
    This function retrieves all Jira issues with Glitchtip last seen date
    greater than .
    """
    data = get_issues()

    out = {"issues": []}
    for issue in data["issues"]:
        glitchtip_url = None
        for label in issue["fields"]["labels"]:
            if "https://glitchtip.devshift.net" in label:
                glitchtip_url = label
                break
        issue_data = get_issue(glitchtip_url.split("/")[-1])

        last_seen_in_days = get_last_seen_in_days(issue_data)
        if last_seen_in_days is not None and last_seen_in_days < max_days_of_inactivity:
            continue

        issue["glitchtip_url"] = glitchtip_url
        issue["last_seen_in_days"] = last_seen_in_days

        out["issues"].append(issue)

    return out


def format_issues_as_markdown(data):
    """Format Jira issues with Glitchtip events as markdown table rows."""
    rows = []
    for issue in data["issues"]:
        jira_url = f"https://{JIRA_DOMAIN}/browse/{issue['key']}"
        jira_link = f"[{issue['key']}]({jira_url})"
        glitchtip_link = f"[Link]({issue['glitchtip_url']})"
        days = (
            issue["last_seen_in_days"]
            if issue["last_seen_in_days"] is not None
            else "N/A"
        )
        rows.append(f"| {jira_link} | {glitchtip_link} | {days} |")
    return "\n".join(rows) if rows else "| No issues found | | |"


def get_glitchtip_issues_with_no_jira(max_days_of_inactivity: int):
    """Get Glitchtip issues with no associated Jira issues."""
    out = []
    issues = glitchtip_issues()
    for issue in issues:
        last_seen_in_days = get_last_seen_in_days(issue)
        if last_seen_in_days >= max_days_of_inactivity:
            continue
        glitchtip_url = f"https://{GLITCHTIP_DOMAIN}/ccx/issues/{issue['id']}"
        jira_issues = get_issues(
            f'project = CCXDEV AND labels = "{glitchtip_url}" AND status != CLOSED'
        )
        if len(jira_issues["issues"]) == 0:
            out.append({"glitchtip_url": glitchtip_url, "diff": last_seen_in_days})
    return out


def format_glitchtip_issues_as_markdown(issues):
    """Format Glitchtip issues without Jira as markdown table rows."""
    rows = []
    for item in issues:
        glitchtip_link = f"[Link]({item['glitchtip_url']})"
        days = item["diff"] if item["diff"] is not None else "N/A"
        rows.append(f"| {glitchtip_link} | {days} |")
    return "\n".join(rows) if rows else "| No issues found | |"


if __name__ == "__main__":
    jira_issues_with_last_seen = get_jira_issues_with_last_seen_older_than(
        MAX_DAYS_OF_INACTIVITY
    )
    glitchtip_issues_no_jira = get_glitchtip_issues_with_no_jira(MAX_DAYS_OF_INACTIVITY)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print(
        TEMPLATE.format(
            timestamp=timestamp,
            jira_count=len(jira_issues_with_last_seen["issues"]),
            jira_table_rows=format_issues_as_markdown(jira_issues_with_last_seen),
            glitchtip_count=len(glitchtip_issues_no_jira),
            glitchtip_table_rows=format_glitchtip_issues_as_markdown(
                glitchtip_issues_no_jira
            ),
        )
    )
