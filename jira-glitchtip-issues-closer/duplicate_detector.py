#!/usr/bin/env python3
"""
Glitchtip Duplicate Issue Detector

This script fetches all issues from a Glitchtip project and groups similar issues
together based on their error messages/titles using text similarity analysis.

The output is a markdown document showing only the groups of potential duplicates.
"""

import os
import re
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

import requests
from glitchtip import (
    GLITCHTIP_API_TOKEN,
    GLITCHTIP_DOMAIN,
    ORG_SLUG,
    get_issues_by_project,
    get_projects,
)

# --- CONFIGURATION ---

# Similarity threshold (0.0 to 1.0). Higher = stricter matching
SIMILARITY_THRESHOLD = float(os.environ.get("SIMILARITY_THRESHOLD", "0.65"))

# Minimum group size to include in output
MIN_GROUP_SIZE = int(os.environ.get("MIN_GROUP_SIZE", "2"))

# Whether to only analyze unresolved issues
UNRESOLVED_ONLY = os.environ.get("UNRESOLVED_ONLY", "true").lower() == "true"
# ---------------------


def fetch_data(url: str, headers: dict) -> list:
    """Fetches data from a paginated API endpoint."""
    all_results = []
    current_url = url

    while current_url:
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()

            all_results.extend(response.json())

            # Check for pagination link in the response headers (Sentry API style)
            link_header = response.headers.get("Link")

            if link_header:
                links = link_header.split(",")
                next_url = None
                for link in links:
                    if 'rel="next"' in link and 'results="true"' in link:
                        next_url = link.split(";")[0].strip("<> ")
                        break
                current_url = next_url
            else:
                current_url = None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {current_url}: {e}")
            break

    return all_results


def normalize_error_message(text: str) -> str:
    """
    Normalize an error message by removing variable parts like:
    - UUIDs
    - IP addresses and ports
    - Timestamps
    - Numeric IDs
    - File paths with specific identifiers
    - Memory addresses
    - Hash values
    """
    if not text:
        return ""

    normalized = text

    # Remove UUIDs (various formats)
    uuid_pattern = (
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    )
    normalized = re.sub(uuid_pattern, "<UUID>", normalized)

    # Remove hex UUIDs without dashes
    hex_uuid_pattern = r"\b[0-9a-fA-F]{32}\b"
    normalized = re.sub(hex_uuid_pattern, "<HEXID>", normalized)

    # Remove IP addresses with optional ports
    ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?\b"
    normalized = re.sub(ip_pattern, "<IP>", normalized)

    # Remove timestamps (various formats)
    # ISO format
    normalized = re.sub(
        r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?([+-]\d{2}:?\d{2}|Z)?",
        "<TIMESTAMP>",
        normalized,
    )
    # Unix timestamps (10-13 digits)
    normalized = re.sub(r"\b\d{10,13}\b", "<TIMESTAMP>", normalized)

    # Remove memory addresses (0x followed by hex)
    normalized = re.sub(r"0x[0-9a-fA-F]+", "<ADDR>", normalized)

    # Remove specific numeric IDs that follow common patterns
    # Organization IDs, user IDs, etc. (sequences of 5+ digits)
    normalized = re.sub(r"\b\d{5,}\b", "<ID>", normalized)

    # Remove port numbers in URLs (but keep the colon)
    normalized = re.sub(r":\d{4,5}/", ":PORT/", normalized)

    # Normalize path segments that look like IDs
    normalized = re.sub(r"/[0-9a-fA-F-]{20,}/", "/<ID>/", normalized)

    # Normalize quoted strings that might be variable values
    # Keep short ones but replace long ones
    def replace_long_quoted(match):
        content = match.group(1) or match.group(2)
        if len(content) > 30:
            return "'<VALUE>'"
        return match.group(0)

    normalized = re.sub(
        r"'([^']{30,})'|\"([^\"]{30,})\"", replace_long_quoted, normalized
    )

    # Collapse multiple spaces and normalize whitespace
    normalized = " ".join(normalized.split())

    return normalized.strip()


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two normalized error messages.
    Returns a score between 0.0 (completely different) and 1.0 (identical).
    """
    if not text1 or not text2:
        return 0.0

    # Use SequenceMatcher for string similarity
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def extract_error_type(title: str) -> str:
    """
    Extract the primary error type from the title.
    This helps with initial categorization before detailed comparison.
    """
    # Common error type patterns
    patterns = [
        r"^(Error|Exception|Warning|Fatal|Panic|ValueError|TypeError|KeyError|AttributeError|RuntimeError|ConnectionError|TimeoutError|IOError|OSError)",
        r"^(\w+Error)",
        r"^(\w+Exception)",
        r":\s*(\w+Error)",
        r":\s*(\w+Exception)",
    ]

    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return match.group(1).lower()

    # If no specific error type, use the first few words
    words = title.split()[:3]
    return " ".join(words).lower() if words else "unknown"


def find_duplicate_groups(
    issues: list, threshold: float = SIMILARITY_THRESHOLD
) -> list:
    """
    Find groups of similar issues based on their titles.

    Uses a two-phase approach:
    1. Quick categorization by error type
    2. Detailed similarity comparison within categories

    Returns a list of groups, where each group is a list of similar issues.
    """
    if not issues:
        return []

    # Pre-process: normalize all titles and extract error types
    processed_issues = []
    for issue in issues:
        normalized = normalize_error_message(issue["title"])
        error_type = extract_error_type(issue["title"])
        processed_issues.append(
            {**issue, "normalized_title": normalized, "error_type": error_type}
        )

    # Phase 1: Group by error type for efficiency
    type_groups = defaultdict(list)
    for issue in processed_issues:
        type_groups[issue["error_type"]].append(issue)

    # Phase 2: Find similar issues within each type group
    all_groups = []
    processed_ids = set()

    for type_issues in type_groups.values():
        # Compare issues within the same error type
        for i, issue1 in enumerate(type_issues):
            if issue1["id"] in processed_ids:
                continue

            group = [issue1]
            processed_ids.add(issue1["id"])

            for _, issue2 in enumerate(type_issues[i + 1 :], start=i + 1):
                if issue2["id"] in processed_ids:
                    continue

                similarity = calculate_similarity(
                    issue1["normalized_title"], issue2["normalized_title"]
                )

                if similarity >= threshold:
                    group.append(issue2)
                    processed_ids.add(issue2["id"])

            if len(group) >= MIN_GROUP_SIZE:
                all_groups.append(group)

    # Also check for cross-type similarities (less common but possible)
    # This catches cases where the error type extraction might differ
    ungrouped = [i for i in processed_issues if i["id"] not in processed_ids]

    for i, issue1 in enumerate(ungrouped):
        if issue1["id"] in processed_ids:
            continue

        group = [issue1]
        processed_ids.add(issue1["id"])

        for issue2 in ungrouped[i + 1 :]:
            if issue2["id"] in processed_ids:
                continue

            similarity = calculate_similarity(
                issue1["normalized_title"], issue2["normalized_title"]
            )

            if similarity >= threshold:
                group.append(issue2)
                processed_ids.add(issue2["id"])

        if len(group) >= MIN_GROUP_SIZE:
            all_groups.append(group)

    # Sort groups by total event count (descending)
    all_groups.sort(key=lambda g: sum(i.get("events", 0) for i in g), reverse=True)

    return all_groups


def get_priority_level(total_events: int) -> tuple:
    """Return priority emoji and label based on event count."""
    if total_events >= 10000:
        return "🔴", "CRITICAL"
    elif total_events >= 1000:
        return "🟠", "HIGH"
    elif total_events >= 100:
        return "🟡", "MEDIUM"
    else:
        return "🟢", "LOW"


def generate_group_title(group: list) -> str:
    """
    Generate a descriptive title for a group of similar issues.
    Uses the most common words/phrases from the normalized titles.
    """
    if not group:
        return "Unknown Error Group"

    # Find the shortest normalized title as it's likely the most general
    titles = [issue.get("normalized_title", issue["title"]) for issue in group]
    base_title = min(titles, key=len)

    # Clean up placeholder tokens for display
    display_title = base_title
    display_title = re.sub(
        r"<UUID>|<HEXID>|<IP>|<TIMESTAMP>|<ADDR>|<ID>|<VALUE>|:PORT",
        "...",
        display_title,
    )
    display_title = re.sub(r"\.\.\.+", "...", display_title)

    # Truncate if too long
    if len(display_title) > 80:
        display_title = display_title[:77] + "..."

    return display_title or "Error Group"


def generate_markdown_report(groups_by_project: dict) -> str:
    """Generate a markdown report of duplicate groups."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# Potential Duplicate Issues Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Glitchtip Instance:** {GLITCHTIP_DOMAIN}",
        f"**Organization:** {ORG_SLUG}",
        f"**Similarity Threshold:** {SIMILARITY_THRESHOLD * 100:.0f}%",
        f"**Analysis Scope:** {'Unresolved issues only' if UNRESOLVED_ONLY else 'All issues'}",
        "",
        "---",
        "",
    ]

    # Calculate summary statistics
    total_groups = sum(len(groups) for groups in groups_by_project.values())
    total_duplicate_issues = sum(
        sum(len(g) for g in groups) for groups in groups_by_project.values()
    )
    total_events_in_duplicates = sum(
        sum(sum(i.get("events", 0) for i in g) for g in groups)
        for groups in groups_by_project.values()
    )

    # Executive Summary
    lines.extend(
        [
            "## Executive Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Projects with duplicates | {len(groups_by_project)} |",
            f"| Total duplicate groups | {total_groups} |",
            f"| Total issues in groups | {total_duplicate_issues} |",
            f"| Total events affected | {total_events_in_duplicates:,} |",
            "",
            "---",
            "",
        ]
    )

    # Table of Contents
    lines.extend(
        [
            "## Table of Contents",
            "",
        ]
    )

    for project_name in sorted(groups_by_project.keys()):
        groups = groups_by_project[project_name]
        total_issues = sum(len(g) for g in groups)
        anchor = project_name.lower().replace(" ", "-").replace("_", "-")
        lines.append(
            f"- [{project_name}](#{anchor}) - {len(groups)} groups, {total_issues} issues"
        )

    lines.extend(["", "---", ""])

    # Project sections
    for project_name in sorted(groups_by_project.keys()):
        groups = groups_by_project[project_name]

        total_issues = sum(len(g) for g in groups)
        total_events = sum(sum(i.get("events", 0) for i in g) for g in groups)

        lines.extend(
            [
                f"## {project_name}",
                "",
                f"**Duplicate Groups:** {len(groups)}  ",
                f"**Issues in Groups:** {total_issues}  ",
                f"**Total Events:** {total_events:,}",
                "",
            ]
        )

        for _, group in enumerate(groups, 1):
            group_events = sum(i.get("events", 0) for i in group)
            priority_emoji, priority_label = get_priority_level(group_events)
            group_title = generate_group_title(group)

            lines.extend(
                [
                    f"### {priority_emoji} {priority_label}: {group_title}",
                    "",
                    f"**Issues:** {len(group)} | **Total Events:** {group_events:,}",
                    "",
                    "| Issue ID | Events | Title | Link |",
                    "|----------|--------|-------|------|",
                ]
            )

            # Sort by events descending
            sorted_group = sorted(group, key=lambda x: x.get("events", 0), reverse=True)

            for issue in sorted_group:
                issue_id = issue.get("id", "N/A")
                events = int(issue.get("count", 0))
                title = issue.get("title", "N/A")
                url = issue.get("permalink", "#")

                # Escape pipes and truncate title
                safe_title = title.replace("|", "\\|")
                if len(safe_title) > 60:
                    safe_title = safe_title[:57] + "..."

                lines.append(
                    f"| #{issue_id} | {events:,} | {safe_title} | [View]({url}) |"
                )

            # Recommendation
            if sorted_group:
                primary_issue = sorted_group[0]
                lines.extend(
                    [
                        "",
                        f"**Recommendation:** Consider merging into [#{primary_issue['id']}]"
                        f"({primary_issue.get('permalink', '#')}) (highest event count)",
                        "",
                        "---",
                        "",
                    ]
                )

    return "\n".join(lines)


def main():
    """Main function to run the duplicate detector."""

    if not GLITCHTIP_API_TOKEN:
        print("Error: GLITCHTIP_API_TOKEN environment variable is not set.")
        print("Please set it with: export GLITCHTIP_API_TOKEN='your_token_here'")
        return

    # headers = {
    #     "Authorization": f"Bearer {GLITCHTIP_API_TOKEN}",
    #     "Accept": "application/json"
    # }

    print("=== Glitchtip Duplicate Issue Detector ===")
    print(f"Instance: {GLITCHTIP_DOMAIN}")
    print(f"Organization: {ORG_SLUG}")
    print(f"Similarity Threshold: {SIMILARITY_THRESHOLD * 100:.0f}%")
    print(f"Analyzing: {'Unresolved issues only' if UNRESOLVED_ONLY else 'All issues'}")
    print()

    # Fetch all projects
    print("Fetching projects...")
    projects = get_projects(ORG_SLUG)

    if not projects:
        print("Error: Could not retrieve projects. Check your configuration.")
        return

    print(f"Found {len(projects)} projects.")
    print()

    # Collect issues from all projects
    all_issues_by_project = {}

    for project in projects:
        project_slug = project.get("slug")
        project_name = project.get("name")

        print(f"  → Fetching issues for: {project_name}...")

        # Build query
        query_param = "?query=is:unresolved" if UNRESOLVED_ONLY else ""
        issues = get_issues_by_project(project_slug, query_param)
        if issues:
            all_issues_by_project[project_name] = issues
            print(f"    Found {len(issues)} issues")

    print()
    print("Analyzing issues for duplicates...")

    # Find duplicate groups for each project
    groups_by_project = {}
    total_duplicates = 0

    for project_name, issues in all_issues_by_project.items():
        groups = find_duplicate_groups(issues)
        if groups:
            groups_by_project[project_name] = groups
            duplicate_count = sum(len(g) for g in groups)
            total_duplicates += duplicate_count
            print(
                f"  → {project_name}: Found {len(groups)} groups "
                f"with {duplicate_count} duplicate issues"
            )

    print()
    print(
        f"Total duplicate groups found: {sum(len(g) for g in groups_by_project.values())}"
    )
    print(f"Total issues in groups: {total_duplicates}")

    if not groups_by_project:
        print("\nNo duplicate groups found with the current threshold.")
        print(f"Try lowering SIMILARITY_THRESHOLD (currently {SIMILARITY_THRESHOLD})")
        return

    # Generate report
    print()
    print("Generating report...")

    report = generate_markdown_report(groups_by_project)

    # Save to file
    output_filename = "duplicate_issues_report.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {output_filename}")
    except Exception as e:
        print(f"Error saving report: {e}")
        print("\n--- Report Content ---\n")
        print(report)


if __name__ == "__main__":
    main()
