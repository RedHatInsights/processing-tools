#!/usr/bin/env python3
"""Bootstrap a minimal AGENTS.md into ObsInt repos that do not have one.

Reads target repos from processing-tools `.github/sync.yml` (same fleet as
CODEOWNERS / CI workflow sync). Skips any repo that already has a root
AGENTS.md. Opens draft PRs via the GitHub CLI (`gh`) using GITHUB_TOKEN /
GH_TOKEN when provided (e.g. obsint-processing-app in Actions).

Examples:
  # Dry-run against the full sync.yml list
  python3 agents_bootstrap/bootstrap.py --dry-run

  # Only one repo, actually open a draft PR
  python3 agents_bootstrap/bootstrap.py --repo RedHatInsights/insights-results-aggregator-exporter

  # Custom sync file / template
  python3 agents_bootstrap/bootstrap.py --sync-yml .github/sync.yml --dry-run
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_SYNC_YML = REPO_ROOT / ".github" / "sync.yml"
DEFAULT_TEMPLATE = SCRIPT_DIR / "AGENTS.md.tmpl"
BRANCH_NAME = "obsint-processing-app/bootstrap-agents-md"
PAGES_BASE = "https://redhatinsights.github.io"


def run_gh(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["gh", *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def load_repos_from_sync_yml(path: Path) -> list[str]:
    with path.open() as f:
        data = yaml.safe_load(f) or {}
    repos: list[str] = []
    for key in data:
        if not isinstance(key, str):
            continue
        # sync.yml keys are "Owner/repo"
        if "/" in key and not key.startswith("."):
            repos.append(key)
    return sorted(set(repos))


def render_template(template: str, owner: str, repo_name: str) -> str:
    return (
        template.replace("{{ repo_name }}", repo_name)
        .replace("{{ owner }}", owner)
        .replace("{{ full_name }}", f"{owner}/{repo_name}")
    )


def agents_md_exists(full_name: str) -> bool:
    result = run_gh(
        ["api", f"repos/{full_name}/contents/AGENTS.md", "--jq", ".path"],
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return True
    # 404 or other — treat non-0 as missing unless stderr suggests auth failure
    stderr = (result.stderr or "").lower()
    if "401" in stderr or "403" in stderr or "bad credentials" in stderr:
        raise RuntimeError(f"Auth error checking AGENTS.md in {full_name}: {result.stderr}")
    return False


def default_branch(full_name: str) -> str:
    result = run_gh(["api", f"repos/{full_name}", "--jq", ".default_branch"])
    return result.stdout.strip()


def branch_exists(full_name: str, branch: str) -> bool:
    result = run_gh(
        ["api", f"repos/{full_name}/git/ref/heads/{branch}"],
        check=False,
    )
    return result.returncode == 0


def ensure_branch(full_name: str, base: str, branch: str) -> None:
    if branch_exists(full_name, branch):
        return
    sha = run_gh(
        ["api", f"repos/{full_name}/git/ref/heads/{base}", "--jq", ".object.sha"]
    ).stdout.strip()
    run_gh(
        [
            "api",
            "--method",
            "POST",
            f"repos/{full_name}/git/refs",
            "-f",
            f"ref=refs/heads/{branch}",
            "-f",
            f"sha={sha}",
        ]
    )


def put_agents_md(full_name: str, branch: str, content: str) -> None:
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    payload: dict[str, str] = {
        "message": "docs: bootstrap minimal AGENTS.md",
        "content": encoded,
        "branch": branch,
    }
    # Updating an existing file on the bootstrap branch requires the blob sha
    meta = run_gh(
        [
            "api",
            f"repos/{full_name}/contents/AGENTS.md?ref={branch}",
            "--jq",
            ".sha",
        ],
        check=False,
    )
    if meta.returncode == 0 and meta.stdout.strip():
        payload["sha"] = meta.stdout.strip()

    proc = subprocess.run(
        [
            "gh",
            "api",
            "--method",
            "PUT",
            f"repos/{full_name}/contents/AGENTS.md",
            "--input",
            "-",
        ],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Failed to create AGENTS.md on {full_name}@{branch}: {proc.stderr}"
        )


def open_draft_pr(full_name: str, base: str, branch: str, repo_name: str) -> str:
    body = f"""## Summary
- Bootstrap a **minimal** root `AGENTS.md` for agent onboarding.
- Includes ObsInt Processing **Team context** (team-info links) plus stable links to `./README.md` and GitHub Pages (`{PAGES_BASE}/{repo_name}/`).

## Notes
- This is an intentional thin stub — not a full architecture / Common Tasks doc.
- Enrich later by hand, or use the `create-agents-md` skill in processing-tools for a deeper pass.
- Pages URL follows the conventional `redhatinsights.github.io/<repo>/` pattern; it may 404 until Pages are enabled.

## Test plan
- [ ] Skim AGENTS.md Team context + External References
- [ ] Confirm README / Pages links are acceptable for this repo
"""
    # If an open PR from this head already exists, report it
    existing = run_gh(
        [
            "pr",
            "list",
            "--repo",
            full_name,
            "--head",
            branch,
            "--state",
            "open",
            "--json",
            "url",
            "--jq",
            ".[0].url",
        ],
        check=False,
    )
    if existing.returncode == 0 and existing.stdout.strip():
        return existing.stdout.strip()

    result = run_gh(
        [
            "pr",
            "create",
            "--repo",
            full_name,
            "--draft",
            "--base",
            base,
            "--head",
            branch,
            "--title",
            "docs: bootstrap minimal AGENTS.md",
            "--body",
            body,
        ]
    )
    return result.stdout.strip()


def process_repo(
    full_name: str,
    template: str,
    *,
    dry_run: bool,
) -> str:
    owner, repo_name = full_name.split("/", 1)
    if agents_md_exists(full_name):
        return f"SKIP {full_name}: AGENTS.md already present"

    content = render_template(template, owner, repo_name)
    if dry_run:
        pages = f"{PAGES_BASE}/{repo_name}/"
        return (
            f"DRY-RUN {full_name}: would open draft PR adding AGENTS.md "
            f"(Pages → {pages})"
        )

    base = default_branch(full_name)
    ensure_branch(full_name, base, BRANCH_NAME)
    put_agents_md(full_name, BRANCH_NAME, content)
    url = open_draft_pr(full_name, base, BRANCH_NAME, repo_name)
    return f"PR {full_name}: {url}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--sync-yml",
        type=Path,
        default=DEFAULT_SYNC_YML,
        help="Path to processing-tools .github/sync.yml",
    )
    p.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Path to AGENTS.md.tmpl",
    )
    p.add_argument(
        "--repo",
        action="append",
        dest="repos",
        help="Limit to one or more Owner/repo (repeatable). Default: all sync.yml keys.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print what would happen; do not create branches/PRs",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.sync_yml.is_file():
        print(f"sync.yml not found: {args.sync_yml}", file=sys.stderr)
        return 1
    if not args.template.is_file():
        print(f"template not found: {args.template}", file=sys.stderr)
        return 1

    template = args.template.read_text()
    repos = args.repos or load_repos_from_sync_yml(args.sync_yml)
    if not repos:
        print("No target repos", file=sys.stderr)
        return 1

    print(f"Targets: {len(repos)} repo(s); dry_run={args.dry_run}")
    failures = 0
    for full_name in repos:
        try:
            msg = process_repo(full_name, template, dry_run=args.dry_run)
            print(msg)
        except Exception as exc:  # noqa: BLE001 — report and continue fleet-wide
            failures += 1
            print(f"ERROR {full_name}: {exc}", file=sys.stderr)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
