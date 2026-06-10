from glitchtip import (
    GLITCHTIP_DOMAIN,
    get_last_seen_in_days,
)
from glitchtip import (
    get_issue as get_glitchtip_issue,
)
from glitchtip import (
    get_issues as get_glitchtip_issues,
)
from jira_helper import get_issues as get_jira_issues


class JiraGlitchtipComposite:
    def __init__(self, jira_issue, glitchtip_issue):
        self.jira_issue = jira_issue
        self.glitchtip_issue = glitchtip_issue

    @property
    def jira_key(self):
        return self.jira_issue.key

    def jira_md_link(self):
        return f"[{self.jira_issue.key}]({self.jira_issue.permalink()})"

    def glitchtip_link(self):
        if "permalink" in self.glitchtip_issue:
            return f"[Link]({self.glitchtip_issue['permalink']})"
        else:
            return f"[Link]({self.glitchtip_issue['glitchtip_url']})"

    def last_seen_in_days(self):
        return get_last_seen_in_days(self.glitchtip_issue)

    def __repr__(self):
        return (
            f"JiraGlitchtipComposite(jira_issue={self.jira_issue}, "
            f"glitchtip_issue={self.glitchtip_issue.get('id', '<missing>')})"
        )


def get_jira_issues_with_last_seen_older_than(
    max_days_of_inactivity: int,
) -> list[JiraGlitchtipComposite]:
    """
    This function retrieves all Jira issues with Glitchtip last seen date
    greater than .
    """
    results = get_jira_issues()
    out = []

    for issue in results:
        glitchtip_url = None
        for label in issue.get_field("labels"):
            if "https://glitchtip.devshift.net" in label:
                glitchtip_url = label
                break

        if not glitchtip_url:
            continue

        issue_data = get_glitchtip_issue(glitchtip_url.split("/")[-1])
        last_seen_in_days = get_last_seen_in_days(issue_data)

        if last_seen_in_days is not None and last_seen_in_days < max_days_of_inactivity:
            continue

        issue_data["glitchtip_url"] = glitchtip_url
        issue_data["last_seen_in_days"] = last_seen_in_days

        out.append(JiraGlitchtipComposite(issue, issue_data))

    return out


def get_glitchtip_issues_with_no_jira(max_days_of_inactivity: int):
    """Get Glitchtip issues with no associated Jira issues."""
    out = []
    issues = get_glitchtip_issues()
    for issue in issues:
        last_seen_in_days = get_last_seen_in_days(issue)

        if last_seen_in_days >= max_days_of_inactivity:
            continue

        glitchtip_url = f"https://{GLITCHTIP_DOMAIN}/ccx/issues/{issue['id']}"
        jira_issues = get_jira_issues(
            f'project = CCXDEV AND labels = "{glitchtip_url}" AND status != CLOSED'
        )
        if len(jira_issues) == 0:
            out.append({"glitchtip_url": glitchtip_url, "diff": last_seen_in_days})

    return out


def get_glitchtip_issue_from_jira_issue(jira_issue):
    for label in jira_issue.get_field("labels"):
        if "https://glitchtip.devshift.net" in label:
            return get_glitchtip_issue(label.split("/")[-1])

    return None
