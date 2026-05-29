import os
from datetime import datetime, timezone

from jira_glitchtip_mixin import (
    get_glitchtip_issues_with_no_jira,
    get_jira_issues_with_last_seen_older_than,
)

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
{glitchtip_table_rows}"""


def format_issues_as_markdown(data):
    """Format Jira issues with Glitchtip events as markdown table rows."""
    rows = []
    for composite in data:
        jira_link = composite.jira_md_link()
        glitchtip_link = composite.glitchtip_link()
        days = composite.last_seen_in_days()
        rows.append(f"| {jira_link} | {glitchtip_link} | {days} |")
    return "\n".join(rows) if rows else "| No issues found | | |"


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
            jira_count=len(jira_issues_with_last_seen),
            jira_table_rows=format_issues_as_markdown(jira_issues_with_last_seen),
            glitchtip_count=len(glitchtip_issues_no_jira),
            glitchtip_table_rows=format_glitchtip_issues_as_markdown(
                glitchtip_issues_no_jira
            ),
        )
    )
