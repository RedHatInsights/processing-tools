import os

import requests

JIRA_DOMAIN = "issues.redhat.com"


def get_issues(
    query="project=CCXDEV AND labels=Glitchtip AND status!=CLOSED",
    timeout=60,
    max_results="200",
):
    # Define constants
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    # Define the request headers
    headers = {
        "Authorization": f"Bearer {jira_api_token}",
        "Accept": "application/json",
    }

    # Send the GET request to Jira API
    response = requests.get(
        f"https://{JIRA_DOMAIN}/rest/api/latest/search",
        headers=headers,
        params={
            "jql": query,
            "maxResults": max_results,
        },
        timeout=timeout,
    )

    # TODO: This response is paginated. If there are more than 50 results it
    # won't contain all the issues.
    if response.status_code != 200:
        raise ConnectionError(
            f"{response.status_code} - Error getting issues: {response.text}"
        )
    return response.json()


def close_issue(
    issue_id,
    comment="This issue is a duplicate.",
    transition="51",
    resolution="Duplicate",
    timeout=5,
):
    headers = {
        "Authorization": f"Bearer {os.getenv('JIRA_API_TOKEN')}",
        "Accept": "application/json",
    }
    body = {
        "update": {"comment": [{"add": {"body": comment}}]},
        "transition": {"id": transition},
        "fields": {"resolution": {"name": resolution}},
    }
    response = requests.post(
        f"https://{JIRA_DOMAIN}/rest/api/latest/issue/{issue_id}/transitions?expand=transitions.fields",
        headers=headers,
        json=body,
        timeout=timeout,
    )

    if response.status_code != 204:
        raise ConnectionError(
            f"{response.status_code} - Error closing issue: {response.text}"
        )

    return response.text
