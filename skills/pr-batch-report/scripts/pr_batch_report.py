#!/usr/bin/env python3
"""Batch PR report via GitHub CLI (`gh`). See skills/pr-batch-report/SKILL.md."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

GH_JSON_FIELDS = ",".join(
    [
        "url",
        "title",
        "body",
        "additions",
        "deletions",
        "changedFiles",
        "statusCheckRollup",
        "mergeable",
        "state",
    ]
)

FAIL_CONCLUSIONS = frozenset(
    {"FAILURE", "ERROR", "TIMED_OUT", "CANCELLED", "ACTION_REQUIRED"}
)
PENDING_STATUSES = frozenset(
    {"IN_PROGRESS", "PENDING", "QUEUED", "WAITING", "REQUESTED"}
)


def normalize_pr_url(raw: str) -> str:
    s = raw.strip()
    if not s or s.startswith("#"):
        return ""
    s = re.sub(r"#.*$", "", s).strip()
    s = re.sub(r"/changes/?$", "", s).strip()
    s = s.rstrip("/")
    return s


def collect_urls(args: argparse.Namespace) -> list[str]:
    urls: list[str] = []
    for u in args.url:
        n = normalize_pr_url(u)
        if n:
            urls.append(n)
    if args.file:
        with open(args.file, encoding="utf-8") as f:
            for line in f:
                n = normalize_pr_url(line)
                if n:
                    urls.append(n)
    if not urls and not sys.stdin.isatty():
        for line in sys.stdin:
            n = normalize_pr_url(line)
            if n:
                urls.append(n)
    # de-dupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def _gh_json(url: str) -> dict[str, Any]:
    r = subprocess.run(
        ["gh", "pr", "view", url, "--json", GH_JSON_FIELDS],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        err = (r.stderr or r.stdout or "").strip()
        return {"url": url, "error": err or f"gh exit {r.returncode}"}
    return json.loads(r.stdout)


def _gh_diff(url: str) -> str:
    r = subprocess.run(
        ["gh", "pr", "diff", url],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        return f"(gh pr diff failed: {(r.stderr or '').strip()})"
    return r.stdout


def summarize_checks(rollup: list[dict[str, Any]] | None) -> tuple[str, str]:
    """Return (short label, detail line)."""
    if not rollup:
        return "unknown", "No status check data."

    failing: list[str] = []
    pending: list[str] = []
    for c in rollup:
        tn = c.get("__typename")
        if tn == "CheckRun":
            name = c.get("name") or "check"
            st = (c.get("status") or "").upper()
            con = (c.get("conclusion") or "").upper()
            if st in PENDING_STATUSES:
                pending.append(f"{name} ({st})")
            elif con in FAIL_CONCLUSIONS:
                failing.append(f"{name} ({con})")
        elif tn == "StatusContext":
            ctx = c.get("context") or "status"
            state = (c.get("state") or "").upper()
            if state == "FAILURE":
                failing.append(f"{ctx} ({state})")
            elif state == "PENDING":
                pending.append(f"{ctx} ({state})")

    if failing:
        return "failing", "; ".join(failing[:8]) + ("…" if len(failing) > 8 else "")
    if pending:
        return "pending", "; ".join(pending[:8]) + ("…" if len(pending) > 8 else "")
    return "passing", "No failed or in-progress checks in rollup."


def diff_paths(diff_text: str) -> str:
    paths: list[str] = []
    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            m = re.match(r"diff --git a/(.+?) b/", line)
            if m:
                paths.append(m.group(1))
    if not paths:
        return "—"
    if len(paths) <= 3:
        return ", ".join(f"`{p}`" for p in paths)
    return ", ".join(f"`{p}`" for p in paths[:3]) + f", +{len(paths) - 3} more"


def _pr_link_label(url: str) -> str:
    parts = [p for p in urlparse(url).path.split("/") if p]
    if len(parts) >= 4 and parts[2] == "pull":
        return f"{parts[1]}#{parts[3]}"
    return parts[-1] if parts else url


def esc_cell(s: str, max_len: int) -> str:
    t = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    t = re.sub(r"\s+", " ", t)
    if len(t) > max_len:
        t = t[: max_len - 1] + "…"
    return t.replace("|", "\\|")


@dataclass
class Row:
    url: str
    title: str
    summary: str
    ci: str
    ci_detail: str
    additions: int
    deletions: int
    changed_files: int
    diff_paths: str
    diff_text: str
    error: str | None = None


def fetch_row(url: str, include_diff: bool) -> Row:
    data = _gh_json(url)
    if "error" in data:
        return Row(
            url=url,
            title="",
            summary="",
            ci="",
            ci_detail="",
            additions=0,
            deletions=0,
            changed_files=0,
            diff_paths="",
            diff_text="",
            error=data["error"],
        )
    body = data.get("body") or ""
    first_lines = "\n".join(body.splitlines()[:4]).strip()
    summary = first_lines if first_lines else "(no body)"
    ci, ci_detail = summarize_checks(data.get("statusCheckRollup"))
    diff_text = _gh_diff(url) if include_diff else ""
    paths = diff_paths(diff_text) if include_diff else "—"
    return Row(
        url=data.get("url", url),
        title=data.get("title") or "",
        summary=summary,
        ci=ci,
        ci_detail=ci_detail,
        additions=int(data.get("additions") or 0),
        deletions=int(data.get("deletions") or 0),
        changed_files=int(data.get("changedFiles") or 0),
        diff_paths=paths if include_diff else "—",
        diff_text=diff_text,
        error=None,
    )


def emit_markdown(rows: list[Row], diff_mode: str, desc_max: int) -> None:
    print("## PR batch report\n")
    print(
        "| PR | Title | Description (excerpt) | CI | +/− / Σ | Files | Paths (from diff) |\n"
        "|---|---|---|---|---:|---:|---|"
    )
    for r in rows:
        if r.error:
            print(
                f"| {r.url} | **error** | `{esc_cell(r.error, desc_max)}` | — | — | — | — |"
            )
            continue
        total = r.additions + r.deletions
        desc = esc_cell(r.summary, desc_max)
        pr_label = _pr_link_label(r.url)
        print(
            f"| [{pr_label}]({r.url}) "
            f"| {esc_cell(r.title, 80)} | {desc} | **{r.ci}** | "
            f"+{r.additions} / −{r.deletions} ({total}) | {r.changed_files} | {r.diff_paths} |"
        )

    print("\n### CI notes\n")
    for r in rows:
        if r.error:
            continue
        print(f"- **{r.url}**: {r.ci} — {r.ci_detail}")

    if diff_mode == "none":
        return

    print("\n### Unified diffs (`gh pr diff`)\n")
    for r in rows:
        if r.error or not r.diff_text.strip():
            continue
        if diff_mode == "collapse":
            title = esc_cell(r.title, 100) or r.url
            print(f"<details>\n<summary><strong>{r.url}</strong> — {title}</summary>\n")
            print("\n```diff")
            print(r.diff_text.rstrip())
            print("```\n</details>\n")
        else:
            print(f"#### `{r.url}`\n")
            print("```diff")
            print(r.diff_text.rstrip())
            print("```\n")


def emit_json(rows: list[Row]) -> None:
    out = []
    for r in rows:
        item: dict[str, Any] = {
            "url": r.url,
            "title": r.title,
            "description_excerpt": r.summary,
            "ci": r.ci,
            "ci_detail": r.ci_detail,
            "additions": r.additions,
            "deletions": r.deletions,
            "lines_changed_total": r.additions + r.deletions,
            "changed_files": r.changed_files,
            "diff_paths": r.diff_paths,
            "error": r.error,
        }
        if r.diff_text:
            item["diff"] = r.diff_text
        out.append(item)
    json.dump(out, sys.stdout, indent=2)
    print()


def main() -> int:
    p = argparse.ArgumentParser(
        description="Markdown (or JSON) report for a list of PR URLs."
    )
    p.add_argument(
        "url", nargs="*", help="PR URLs (https://github.com/org/repo/pull/N)"
    )
    p.add_argument(
        "-f",
        "--file",
        metavar="PATH",
        help="Text file with one URL per line (comments with # allowed)",
    )
    p.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    p.add_argument(
        "--no-diff",
        action="store_true",
        help="Do not run gh pr diff (faster; paths column will be empty)",
    )
    p.add_argument(
        "--diff-mode",
        choices=("inline", "collapse", "none"),
        default="inline",
        help="How to print diffs in md: inline blocks, HTML details, or none (default: inline)",
    )
    p.add_argument(
        "--max-desc",
        type=int,
        default=240,
        metavar="N",
        help="Max length for description excerpt in table cells (default: 240)",
    )
    p.add_argument(
        "-j",
        "--jobs",
        type=int,
        default=8,
        metavar="N",
        help="Parallel gh invocations (default: 8)",
    )
    args = p.parse_args()
    urls = collect_urls(args)
    if not urls:
        print(
            "No PR URLs. Pass URLs as args, use --file, or pipe one URL per line.",
            file=sys.stderr,
        )
        return 2

    include_diff = not args.no_diff
    rows: list[Row | None] = [None] * len(urls)
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        futs = {ex.submit(fetch_row, u, include_diff): i for i, u in enumerate(urls)}
        for fut in as_completed(futs):
            rows[futs[fut]] = fut.result()

    ordered = [r for r in rows if r is not None]
    if args.format == "json":
        emit_json(ordered)
    else:
        emit_markdown(
            ordered, "none" if args.no_diff else args.diff_mode, args.max_desc
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
