#!/usr/bin/env python3
"""Read-only Jira REST helper for Quarterly Connection reports.

The helper uses the authentication already available to `requests` (for example
an existing `.netrc` entry for the Jira host). It does not accept raw tokens on
the command line and does not print credentials.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

import requests

DEFAULT_SITE = "https://redhat.atlassian.net"


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session


def get_json(
    session: requests.Session,
    site: str,
    path: str,
    params: dict[str, str],
    timeout: int,
) -> dict[str, Any]:
    response = session.get(
        f"{site.rstrip('/')}{path}",
        params=params,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def search_jql(
    session: requests.Session,
    site: str,
    jql: str,
    fields: list[str],
    max_results: int,
    timeout: int,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    next_page_token: str | None = None

    while True:
        params = {
            "jql": jql,
            "fields": ",".join(fields),
            "maxResults": str(max_results),
        }
        if next_page_token:
            params["nextPageToken"] = next_page_token

        data = get_json(session, site, "/rest/api/3/search/jql", params, timeout)
        issues.extend(data.get("issues", []))
        next_page_token = data.get("nextPageToken")
        if data.get("isLast", True) or not next_page_token:
            return issues


def issue_comments(
    session: requests.Session,
    site: str,
    key: str,
    max_results: int,
    timeout: int,
) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    start_at = 0

    while True:
        data = get_json(
            session,
            site,
            f"/rest/api/3/issue/{key}/comment",
            {
                "startAt": str(start_at),
                "maxResults": str(max_results),
                "orderBy": "created",
            },
            timeout,
        )
        page = data.get("comments", [])
        comments.extend(page)
        start_at += len(page)
        if start_at >= data.get("total", 0) or not page:
            return comments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default=DEFAULT_SITE, help=f"Jira site URL (default: {DEFAULT_SITE})")
    parser.add_argument("--timeout", type=int, default=60, help="request timeout in seconds")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="run a paginated /search/jql query")
    search_parser.add_argument("--jql", required=True, help="JQL query")
    search_parser.add_argument(
        "--fields",
        required=True,
        help="comma-separated Jira fields to request",
    )
    search_parser.add_argument("--max-results", type=int, default=100)

    comments_parser = subparsers.add_parser("comments", help="fetch all comments for an issue")
    comments_parser.add_argument("key", help="Jira issue key, e.g. CCXDEV-123")
    comments_parser.add_argument("--max-results", type=int, default=100)

    args = parser.parse_args()
    session = build_session()

    try:
        if args.command == "search":
            fields = [field.strip() for field in args.fields.split(",") if field.strip()]
            output: dict[str, Any] = {
                "issues": search_jql(
                    session,
                    args.site,
                    args.jql,
                    fields,
                    args.max_results,
                    args.timeout,
                )
            }
        elif args.command == "comments":
            output = {
                "comments": issue_comments(
                    session,
                    args.site,
                    args.key,
                    args.max_results,
                    args.timeout,
                )
            }
        else:
            parser.error(f"unsupported command: {args.command}")
    except requests.HTTPError as exc:
        print(f"Jira REST request failed: {exc}", file=sys.stderr)
        return 1

    json.dump(output, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
