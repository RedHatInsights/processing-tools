#!/usr/bin/env python3
"""Bump SaaS `ref:` SHAs under ccx-data-pipeline (round-trip YAML, GitHub API).

Expects a local app-interface checkout (updated `master` is your responsibility).
Skips ref: internal, main, master. Only `https://github.com/...` remotes are resolved.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from ruamel.yaml import YAML

BASE = Path("data/services/insights/ccx-data-pipeline")
SKIP = frozenset({"internal", "main", "master"})
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
GITHUB_META = "https://api.github.com/repos/{owner}/{repo}"


def yaml_rt() -> YAML:
    """Build a ruamel YAML instance suitable for app-interface round-trips.

    Preserves quoting and leading ``---`` so diffs stay small and reviewable.

    Returns:
        Configured ``YAML`` loader/dumper (same instance for load + dump).
    """
    y = YAML()
    y.preserve_quotes = True
    y.explicit_start = True
    return y


def github_owner_repo(url: str) -> tuple[str, str] | None:
    """Parse ``owner`` and ``repo`` from a public GitHub HTTPS clone URL.

    Args:
        url: Repository URL (e.g. ``https://github.com/o/r`` or ``.../r.git``).

    Returns:
        ``(owner, repo)`` for ``api.github.com``, or ``None`` if the host is not
        ``github.com`` or the path does not look like ``/owner/repo``.
    """
    p = urlparse(url)
    if p.scheme != "https" or p.netloc.removeprefix("www.") != "github.com":
        return None
    parts = [x for x in p.path.split("/") if x]
    if len(parts) < 2:
        return None
    owner, name = parts[0], parts[1]
    return owner, name.removesuffix(".git")


def http_json(url: str) -> dict:
    """GET a URL and decode the body as JSON (GitHub REST).

    Args:
        url: Full HTTPS URL to fetch.

    Returns:
        Parsed JSON object (typically a dict).

    Raises:
        Same as ``urllib.request.urlopen`` / ``json.loads`` on failure.
    """
    req = Request(url, headers={"User-Agent": "processing-tools-update-refs"})
    with urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode())


def tip_sha(url: str, cache: dict[str, str]) -> str | None:
    """Resolve the tip commit SHA for a GitHub repo URL (default branch).

    Uses the GitHub REST API: repo metadata for ``default_branch``, then the
    commit object for that ref. Warns and returns ``None`` for non-GitHub URLs
    or HTTP/JSON errors.

    Args:
        url: HTTPS GitHub repository URL.
        cache: Mutable map ``url -> sha``; updated on success to avoid repeat calls.

    Returns:
        Full 40-char hex SHA, or ``None`` if the URL is unsupported or lookup fails.
    """
    if url in cache:
        return cache[url]
    pair = github_owner_repo(url)
    if not pair:
        print(f"WARNING: only github.com HTTPS remotes are supported, skipping {url}", file=sys.stderr)
        return None
    owner, repo = pair
    try:
        meta = http_json(GITHUB_META.format(owner=owner, repo=repo))
        branch = meta["default_branch"]
        commit = http_json(GITHUB_API.format(owner=owner, repo=repo, ref=branch))
        sha = commit["sha"]
    except (HTTPError, URLError, KeyError, json.JSONDecodeError) as e:
        print(f"WARNING: could not resolve tip for {url}: {e}", file=sys.stderr)
        return None
    cache[url] = sha
    return sha


def repo_matches(url: str, filters: list[str]) -> bool:
    """Return whether ``url`` should be processed given optional CLI filters.

    Args:
        url: Repository URL (https).
        filters: Exact-match strings from ``--repo``; each entry may be the
            full URL or the last path segment (repo name). If empty, all repos match.

    Returns:
        ``True`` if ``filters`` is empty or any filter equals ``url`` or the
        repo tail after the final ``/``.
    """
    if not filters:
        return True
    tail = url.rsplit("/", 1)[-1]
    return any(url == f or tail == f for f in filters)


def gather_updates(
    node,
    filters: list[str],
    cache: dict[str, str],
    out: list,
    url_ctx: str | None = None,
) -> str | None:
    """Walk YAML and collect ``ref`` updates bound to the active repository URL.

    A ``ref`` uses the nearest ancestor ``https://`` ``url`` (same mapping or
    above). For sequences, the URL context advances left-to-right across items
    (similar to the bash script's ``current_url`` line state).

    Args:
        node: Parsed YAML (``dict``/``list``/``CommentedMap``/``CommentedSeq`` from ruamel).
        filters: Repo filter list; passed to ``repo_matches`` for each candidate.
        cache: Passed through to ``tip_sha`` for GitHub lookups.
        out: Appended with ``(node, old_ref, new_sha, repo_url)`` for each change;
            ``node`` is the mapping that owns ``ref`` (often without a ``url`` key).
        url_ctx: Active repo URL from outer scope, or ``None`` before any ``url``.

    Returns:
        The URL context to expose to the caller after this subtree (for list
        folding): the mapping's own ``https`` ``url`` if present, else ``url_ctx``.
    """
    if isinstance(node, Mapping):
        ctx = url_ctx
        u = node.get("url")
        if isinstance(u, str) and u.startswith("https://"):
            ctx = u
        r = node.get("ref")
        if isinstance(r, str) and ctx is not None:
            if r not in SKIP and repo_matches(ctx, filters):
                new = tip_sha(ctx, cache)
                if new and new != r:
                    out.append((node, r, new, ctx))
        for v in node.values():
            if isinstance(v, (Mapping, Sequence)) and not isinstance(v, (str, bytes)):
                gather_updates(v, filters, cache, out, ctx)
        return ctx
    if isinstance(node, Sequence) and not isinstance(node, (str, bytes)):
        last = url_ctx
        for item in node:
            nxt = gather_updates(item, filters, cache, out, last)
            if nxt is not None:
                last = nxt
        return last
    return url_ctx


def main(argv: list[str] | None = None) -> int:
    """CLI entry: scan app-interface YAML under ``BASE``, bump refs, optionally write files.

    Args:
        argv: Argument list (excluding ``sys.argv[0]``). If ``None``, ``parse_args``
            uses ``sys.argv`` as usual.

    Returns:
        Process exit code (``0`` on success, ``1`` if ``--local-folder`` is missing
        or not a directory).
    """
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--repo", action="append", default=None, metavar="NAME_OR_URL")
    ap.add_argument("--local-folder", default="/tmp/app-interface", metavar="PATH")
    args = ap.parse_args(argv)

    root = Path(args.local_folder).expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 1

    if args.dry_run:
        print("=== DRY RUN ===")

    filters = list(args.repo or [])
    if filters:
        print("Filtering repos:", " ".join(filters))

    base = root / BASE
    paths = sorted({*base.rglob("*.yml"), *base.rglob("*.yaml")}, key=str)
    print(f"Collecting YAML files from {base} ...\nFound {len(paths)} files.\n")

    yl = yaml_rt()
    cache: dict[str, str] = {}

    for path in paths:
        try:
            with path.open(encoding="utf-8") as fh:
                data = yl.load(fh)
        except Exception as e:
            print(f"WARNING: skip {path.relative_to(root)}: {e}", file=sys.stderr)
            continue
        if data is None:
            continue
        batch: list = []
        gather_updates(data, filters, cache, batch)
        if not batch:
            continue
        rel = path.relative_to(root)
        print(f"[{rel}] {len(batch)} ref(s) updated")
        for node, old, new, repo_url in batch:
            print(f"  {old[:12]}... -> {new[:12]}... ({repo_url})", file=sys.stderr)
            if not args.dry_run:
                node["ref"] = new
        if not args.dry_run:
            with path.open("w", encoding="utf-8") as fh:
                yl.dump(data, fh)

    print(
        f"\nDone. {len(cache)} unique repo URL(s) successfully resolved via the GitHub API.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
