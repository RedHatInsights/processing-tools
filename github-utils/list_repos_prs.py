#!/usr/bin/env python3
"""
Script to list open pull requests from GitHub repositories.
Generates CSV output with PR details including CI status.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any

import yaml


def load_repos(repos_file: str = None) -> List[str]:
    """Load repository configuration from YAML file."""
    if repos_file is None:
        # Default to repos.yaml in the same directory as this script
        script_dir = Path(__file__).parent
        repos_file = script_dir / "repos.yaml"

    with open(repos_file, 'r') as f:
        config = yaml.safe_load(f)

    return config.get('github_repos', [])


def get_ci_status(status_check_rollup: List[Dict]) -> str:
    """Determine CI status from status check rollup."""
    if not status_check_rollup:
        return "ok"

    for check in status_check_rollup:
        if check.get("conclusion") == "FAILURE" or check.get("state") == "FAILURE":
            return "failed"

    return "ok"


def get_prs_for_repo(repo_path: str) -> List[Dict[str, Any]]:
    """Fetch open PRs for a given repository."""
    cmd = [
        "gh", "pr", "list",
        "--repo", repo_path,
        "--state", "open",
        "--limit", "100",
        "--json", "number,title,createdAt,url,author,statusCheckRollup,isDraft"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        prs = json.loads(result.stdout)

        # Add repo name and CI status to each PR
        repo_name = repo_path.split('/')[-1]
        for pr in prs:
            pr["repo"] = repo_name
            pr["ci_status"] = get_ci_status(pr.get("statusCheckRollup", []))

        return prs
    except subprocess.CalledProcessError as e:
        print(f"Error fetching PRs for {repo_path}: {e}", file=sys.stderr)
        return []


def format_pr_as_csv(pr: Dict[str, Any]) -> str:
    """Format a PR as a CSV row."""
    fields = [
        pr["repo"],
        str(pr["number"]),
        pr["title"],
        pr["createdAt"],
        pr["url"],
        pr["author"]["login"],
        pr["ci_status"],
        "draft" if pr.get("isDraft", False) else "ready"
    ]

    # Properly escape and quote fields for CSV
    escaped_fields = []
    for field in fields:
        # Escape quotes and wrap in quotes if necessary
        if ',' in field or '"' in field or '\n' in field:
            field = '"' + field.replace('"', '""') + '"'
        escaped_fields.append(field)

    return ",".join(escaped_fields)


def format_pr_as_markdown_row(pr: Dict[str, Any]) -> str:
    """Format a PR as a markdown table row."""
    ci_status = "✅ ok" if pr["ci_status"] == "ok" else "❌ failed"
    draft_status = "draft" if pr.get("isDraft", False) else "ready"
    date = pr["createdAt"][:10]  # Just the date part
    return f"| {pr['repo']} | [{pr['number']}]({pr['url']}) | {pr['title']} | {date} | {pr['author']['login']} | {ci_status} | {draft_status} |"


def main():
    """Main function to generate PR report."""
    from datetime import datetime

    # Determine output files
    script_dir = Path(__file__).parent
    csv_file = script_dir / "open-prs.csv"
    md_file = script_dir / "open-prs.md"

    # Load repositories
    try:
        repos = load_repos()
    except Exception as e:
        print(f"Error loading repos: {e}", file=sys.stderr)
        sys.exit(1)

    # Collect all PRs
    all_prs = []

    for repo_path in repos:
        prs = get_prs_for_repo(repo_path)
        all_prs.extend(prs)

    # Sort by creation date (newest first)
    all_prs.sort(key=lambda x: x["createdAt"], reverse=True)

    # Split into Konflux and others
    konflux_prs = [pr for pr in all_prs if pr["author"]["login"] == "app/red-hat-konflux"]
    other_prs = [pr for pr in all_prs if pr["author"]["login"] != "app/red-hat-konflux"]

    # Write CSV file (all PRs)
    with open(csv_file, 'w') as f:
        f.write("repo,pr_id,title,date_created,url,author,ci_status,draft_status\n")
        for pr in all_prs:
            f.write(format_pr_as_csv(pr) + "\n")

    # Write Konflux Markdown file
    konflux_md_file = script_dir / "open-prs-konflux.md"
    with open(konflux_md_file, 'w') as f:
        f.write(f"# Open Pull Requests (Konflux)\n\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"**Total Konflux PRs: {len(konflux_prs)}**\n\n")

        # Table header
        f.write("| Repo | PR | Title | Created | Author | CI Status | Draft |\n")
        f.write("|------|-------|-------|---------|--------|-----------|-------|\n")

        # Table rows
        for pr in konflux_prs:
            f.write(format_pr_as_markdown_row(pr) + "\n")

    # Write Others Markdown file
    others_md_file = script_dir / "open-prs-others.md"
    with open(others_md_file, 'w') as f:
        f.write(f"# Open Pull Requests (Others)\n\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write(f"**Total PRs: {len(other_prs)}**\n\n")

        # Table header
        f.write("| Repo | PR | Title | Created | Author | CI Status | Draft |\n")
        f.write("|------|-------|-------|---------|--------|-----------|-------|\n")

        # Table rows
        for pr in other_prs:
            f.write(format_pr_as_markdown_row(pr) + "\n")

    print(f"✅ Reports saved:")
    print(f"   📄 CSV (all): {csv_file}")
    print(f"   📝 Markdown (Konflux): {konflux_md_file}")
    print(f"   📝 Markdown (Others): {others_md_file}")
    print(f"📊 Found {len(all_prs)} open PRs ({len(konflux_prs)} Konflux, {len(other_prs)} others)")


if __name__ == "__main__":
    main()
