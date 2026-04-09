import os

import requests

# Define constants
GLITCHTIP_API_TOKEN = os.getenv("GLITCHTIP_API_TOKEN")
GLITCHTIP_DOMAIN = "glitchtip.devshift.net"
GLITCHTIP_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"

# Define the request headers
glitchtip_headers = {
    "Authorization": f"Bearer {GLITCHTIP_API_TOKEN}",
    "accept": "application/json",
    "content-type": "application/json",
}


def get_issue(issue_id):
    # Send the GET request to Glitchtip API
    response = requests.get(
        f"https://{GLITCHTIP_DOMAIN}/api/0/issues/{issue_id}/",
        headers=glitchtip_headers,
    )
    return response.json()


def get_issues():
    # Send the GET request to Glitchtip API
    response = requests.get(
        f"https://{GLITCHTIP_DOMAIN}/api/0/organizations/ccx/issues/",
        headers=glitchtip_headers,
    )
    return response.json()
