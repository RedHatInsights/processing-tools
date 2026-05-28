import os
from functools import lru_cache

from jira import JIRA

JIRA_DOMAIN = "redhat.atlassian.net"


@lru_cache
def get_issues(
    query="project=CCXDEV AND labels=Glitchtip AND status!=CLOSED",
    timeout=60,
):
    # Define constants
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_email = os.getenv("JIRA_EMAIL")

    client = JIRA(f"https://{JIRA_DOMAIN}", basic_auth=(jira_email, jira_api_token))

    results = client.enhanced_search_issues(query)

    while results.nextPageToken is not None:
        new_result = client.enhanced_search_issues(
            query, nextPageToken=results.nextPageToken
        )
        results.extend(new_result)
        results.nextPageToken = new_result.nextPageToken

    return results


def close_issue(
    issue_id,
    comment="This issue is a duplicate.",
    transition="Closed",
    resolution="Duplicate",
    timeout=5,
):
    # Define constants
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    jira_email = os.getenv("JIRA_EMAIL")

    client = JIRA(f"https://{JIRA_DOMAIN}", basic_auth=(jira_email, jira_api_token))

    client.transition_issue(
        issue_id, transition, fields={"resolution": {"name": resolution}}
    )
    client.add_comment(issue_id, comment)
