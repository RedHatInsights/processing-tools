#!/usr/bin/env python3
"""Fetch open Merge Requests from GitLab repositories and generate reports"""

import json
import os
import ssl
import urllib.error
import urllib.request
from datetime import datetime


class GitLabMRFetcher:
    def __init__(self, gitlab_url, project_path, token=None):
        """
        Args:
            gitlab_url: GitLab instance URL (e.g., "https://gitlab.cee.redhat.com")
            project_path: Project path (e.g., "insights-qe/iqe-ccx-plugin")
            token: GitLab personal access token
        """
        self.gitlab_url = gitlab_url.rstrip("/")
        self.project_path = project_path
        # URL encode the project path (/ becomes %2F)
        self.project_id = project_path.replace("/", "%2F")
        self.api_base = f"{self.gitlab_url}/api/v4"

        self.headers = {"Accept": "application/json"}
        if token:
            self.headers["PRIVATE-TOKEN"] = token

    def _api_request(self, url):
        """Make API request with error handling"""
        req = urllib.request.Request(url, headers=self.headers)
        # Disable SSL verification for internal GitLab with self-signed cert
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            with urllib.request.urlopen(req, context=ctx) as response:
                return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            print(f"❌ HTTP Error {e.code}: {e.reason}")
            print(f"   URL: {url}")
            print(f"   Response: {error_body[:200]}")
            raise
        except urllib.error.URLError as e:
            print(f"❌ URL Error: {e.reason}")
            print(f"   URL: {url}")
            raise

    def get_pipeline_status(self, mr_iid):
        """Get the latest pipeline status for an MR"""
        url = f"{self.api_base}/projects/{self.project_id}/merge_requests/{mr_iid}/pipelines"

        try:
            pipelines = self._api_request(url)
            if pipelines and len(pipelines) > 0:
                # Get the most recent pipeline
                latest = pipelines[0]
                status = latest.get("status", "unknown")
                # Map GitLab statuses to simple ok/failed
                if status in ["success", "manual"]:
                    return "ok"
                elif status in ["failed", "canceled"]:
                    return "failed"
                elif status in ["running", "pending", "created"]:
                    return "running"
                else:
                    return "unknown"
            return "ok"  # No pipeline means ok (like GitHub)
        except Exception:
            return "ok"

    def get_open_mrs(self):
        """Get all open MRs for the project"""
        mrs = []
        page = 1

        while True:
            # GitLab API: Get open MRs ordered by updated time
            url = (
                f"{self.api_base}/projects/{self.project_id}/merge_requests"
                f"?state=opened&order_by=updated_at&sort=desc"
                f"&per_page=100&page={page}"
            )

            try:
                data = self._api_request(url)
            except Exception as e:
                print(f"    ⚠️  Error fetching MRs: {e}")
                break

            if not data:
                break

            for mr in data:
                # Parse dates
                created_at = mr.get("created_at", "")
                updated_at = mr.get("updated_at", "")

                # Get pipeline status
                pipeline_status = self.get_pipeline_status(mr["iid"])

                # Normalize author name for Konflux and CCX bot
                author = mr["author"]["username"]
                if (
                    author == "group_7843_bot_a9ccf2da3fc11b4f888fe6cbaea7c2ee"
                    or author == "ccx-bot"
                ):
                    author = "app/konflux-ci"

                mrs.append(
                    {
                        "iid": mr["iid"],
                        "title": mr["title"],
                        "author": author,
                        "author_name": mr["author"]["name"],
                        "created_at": created_at,
                        "updated_at": updated_at,
                        "web_url": mr["web_url"],
                        "source_branch": mr["source_branch"],
                        "target_branch": mr["target_branch"],
                        "draft": mr.get("draft", False)
                        or mr.get("work_in_progress", False),
                        "labels": mr.get("labels", []),
                        "assignee": mr["assignee"]["username"]
                        if mr.get("assignee")
                        else None,
                        "assignee_name": mr["assignee"]["name"]
                        if mr.get("assignee")
                        else None,
                        "pipeline_status": pipeline_status,
                    }
                )

            page += 1

            # Safety check - if we got less than 100, we're on the last page
            if len(data) < 100:
                break

        return mrs


def main():
    # Configuration
    gitlab_url = "https://gitlab.cee.redhat.com"

    # Project paths to monitor
    project_paths = [
        "insights-qe/iqe-ccx-plugin",
        "ccx/ccx-load-test",
    ]

    # Get token from environment and strip any BOM or whitespace
    token = os.environ.get("GITLAB_TOKEN")
    if token:
        token = token.strip().lstrip("\ufeff")

    if not token:
        print("⚠️ No GITLAB_TOKEN found. Some repos may not be accessible.")

    # Collect all MRs across projects
    all_mrs = []
    project_stats = {}

    print(f"🔍 Fetching open MRs from {len(project_paths)} GitLab projects...")

    for project_path in project_paths:
        print(f"\n  Checking {project_path}...")

        try:
            fetcher = GitLabMRFetcher(gitlab_url, project_path, token)
            mrs = fetcher.get_open_mrs()

            # Add project info to each MR
            for mr in mrs:
                mr["project"] = project_path

            all_mrs.extend(mrs)
            project_stats[project_path] = len(mrs)

            print(f"    Found {len(mrs)} open MR(s)")

        except Exception as e:
            print(f"    ❌ Error: {e}")
            project_stats[project_path] = 0
            continue

    # Sort by created_at (newest first, same as GitHub)
    all_mrs.sort(key=lambda x: x["created_at"], reverse=True)

    print(f"\n📊 Total: {len(all_mrs)} open MRs across all projects")

    # Categorize MRs - Konflux vs Others
    konflux_mrs = [mr for mr in all_mrs if mr["author"] == "app/konflux-ci"]
    other_mrs = [mr for mr in all_mrs if mr["author"] != "app/konflux-ci"]

    # Generate CSV output (all MRs)
    csv_file = "open_mr/open-mrs.csv"
    with open(csv_file, "w") as f:
        f.write("project,mr_id,title,date_created,url,author,ci_status,draft_status\n")
        for mr in all_mrs:
            # Escape commas and quotes in title
            title = mr["title"].replace('"', '""')
            if "," in title or '"' in title:
                title = f'"{title}"'
            draft_status = "draft" if mr["draft"] else "no"

            f.write(
                f"{mr['project']},{mr['iid']},{title},{mr['created_at']},{mr['web_url']},{mr['author']},{mr['pipeline_status']},{draft_status}\n"
            )

    print(f"💾 CSV report saved to: {csv_file}")

    # Generate Konflux Markdown file
    konflux_md_file = "open_mr/open-mrs-konflux.md"
    with open(konflux_md_file, "w") as f:
        f.write("# Open Merge Requests (Konflux)\n\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"**Total Konflux MRs: {len(konflux_mrs)}**\n\n")

        # Table header
        f.write("| Project | MR | Title | Created | Author | CI Status | Draft |\n")
        f.write("|---------|-------|-------|---------|--------|-----------|-------|\n")

        # Table rows
        for mr in konflux_mrs:
            ci_status = (
                "✅ ok"
                if mr["pipeline_status"] == "ok"
                else "❌ failed"
                if mr["pipeline_status"] == "failed"
                else f"🔄 {mr['pipeline_status']}"
            )
            draft_status = "draft" if mr["draft"] else "no"
            date = mr["created_at"][:10]  # Just the date part
            f.write(
                f"| {mr['project']} | [!{mr['iid']}]({mr['web_url']}) | {mr['title']} | {date} | "
                f"{mr['author']} | {ci_status} | {draft_status} |\n"
            )

    print(f"💾 Markdown report (Konflux) saved to: {konflux_md_file}")

    # Generate Others Markdown file
    others_md_file = "open_mr/open-mrs-others.md"
    with open(others_md_file, "w") as f:
        f.write("# Open Merge Requests (Others)\n\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"**Total MRs: {len(other_mrs)}**\n\n")

        # Table header
        f.write("| Project | MR | Title | Created | Author | CI Status | Draft |\n")
        f.write("|---------|-------|-------|---------|--------|-----------|-------|\n")

        # Table rows
        for mr in other_mrs:
            ci_status = (
                "✅ ok"
                if mr["pipeline_status"] == "ok"
                else "❌ failed"
                if mr["pipeline_status"] == "failed"
                else f"🔄 {mr['pipeline_status']}"
            )
            draft_status = "draft" if mr["draft"] else "no"
            date = mr["created_at"][:10]  # Just the date part
            f.write(
                f"| {mr['project']} | [!{mr['iid']}]({mr['web_url']}) | {mr['title']} | {date} | "
                f"{mr['author']} | {ci_status} | {draft_status} |\n"
            )

    print(f"💾 Markdown report (Others) saved to: {others_md_file}")
    print("\n✅ Report generation complete!")


if __name__ == "__main__":
    main()
