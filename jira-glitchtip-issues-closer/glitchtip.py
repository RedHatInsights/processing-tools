import os
from datetime import datetime, timezone
from functools import lru_cache

import requests

# Define constants
GLITCHTIP_API_TOKEN = os.getenv("GLITCHTIP_API_TOKEN")
GLITCHTIP_DOMAIN = "glitchtip.devshift.net"
GLITCHTIP_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Your Organization Slug (found in the URL when viewing your organization)
ORG_SLUG = os.getenv("GLITCHTIP_ORG", "ccx")


# Define the request headers
glitchtip_headers = {
    "Authorization": f"Bearer {GLITCHTIP_API_TOKEN}",
    "accept": "application/json",
    "content-type": "application/json",
}


def get_issue_url(issue_id, org=ORG_SLUG):
    """Build the correct web URL for a Glitchtip issue.

    The API permalink uses the project name in the path; the UI expects the
    organization slug instead (e.g. /ccx/issues/123, not /ccx-data-pipeline/...).
    """
    return f"https://{GLITCHTIP_DOMAIN}/{org}/issues/{issue_id}"


def _normalize_issue(issue):
    issue_id = issue.get("id")
    if issue_id is not None:
        issue["permalink"] = get_issue_url(issue_id)
    return issue


def get_issue(issue_id):
    # Send the GET request to Glitchtip API
    response = requests.get(
        f"https://{GLITCHTIP_DOMAIN}/api/0/issues/{issue_id}/",
        headers=glitchtip_headers,
    )

    if response.status_code == 404:
        return None

    return _normalize_issue(response.json())


@lru_cache
def get_issues():
    # Send the GET request to Glitchtip API
    response = requests.get(
        f"https://{GLITCHTIP_DOMAIN}/api/0/organizations/{ORG_SLUG}/issues/",
        headers=glitchtip_headers,
    )
    return [_normalize_issue(issue) for issue in response.json()]


@lru_cache
def get_issues_by_project(project_slug, query_param=""):
    url = f"https://{GLITCHTIP_DOMAIN}/api/0/projects/{ORG_SLUG}/{project_slug}/issues/{query_param}"
    return [_normalize_issue(issue) for issue in _fetch_paginated(url)]


def get_last_seen_in_days(issue):
    last_seen_in_issue = issue.get("lastSeen", None)

    if last_seen_in_issue is None:
        return None

    last_seen = datetime.strptime(last_seen_in_issue, GLITCHTIP_DATE_FORMAT)
    diff = datetime.now(timezone.utc) - last_seen
    return diff.days


def _fetch_paginated(url: str) -> list:
    """Fetches all pages from a paginated Glitchtip API endpoint."""
    all_results = []
    current_url = url

    while current_url:
        response = requests.get(current_url, headers=glitchtip_headers)
        response.raise_for_status()
        all_results.extend(response.json())

        link_header = response.headers.get("Link")
        current_url = None
        if link_header:
            for link in link_header.split(","):
                if 'rel="next"' in link and 'results="true"' in link:
                    current_url = link.split(";")[0].strip("<> ")
                    break

    return all_results


def get_projects(org: str) -> list:
    """Return all projects for the given organization slug."""
    url = f"https://{GLITCHTIP_DOMAIN}/api/0/organizations/{org}/projects/"
    return _fetch_paginated(url)