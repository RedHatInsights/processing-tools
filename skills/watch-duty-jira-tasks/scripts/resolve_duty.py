#!/usr/bin/env python3
"""Resolve who is on watch duty for given dates from the CCX processing IC schedule.

Reads the schedule YAML (from stdin, or fetched via fetch_schedule.sh when no
stdin is piped) and, for each date the user asks about, finds the schedule entry
whose [start, end) interval contains that date and reports the assigned
engineer(s).

The schedule YAML has the shape::

    schedule:
    - start: '2023-07-10 06:00'
      end: '2023-07-17 06:00'
      users:
      - $ref: /teams/insights/users/ccx/jsegural.yml

The org_username is taken from the last path segment of the $ref (``jsegural``),
and the Jira assignee email is derived as ``<org_username>@redhat.com``.

Usage::

    # explicit dates (YYYY-MM-DD), read schedule from stdin
    ./fetch_schedule.sh | ./resolve_duty.py 2026-09-03 2026-09-10

    # a date range expands to every ISO week start (Friday 06:00 boundaries vary,
    # so we sample the given dates only — pass the dates you care about)
    ./fetch_schedule.sh | ./resolve_duty.py --json 2026-09-03

Output: human-readable by default, or JSON with --json for the Jira step to
consume.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml (or dnf install python3-pyyaml)")


DATE_FORMATS = ("%Y-%m-%d %H:%M", "%Y-%m-%d")


def _parse_dt(value: str) -> datetime:
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognized date/time: {value!r}")


def _org_username(ref: str) -> str:
    """Extract org_username from a $ref like /teams/insights/users/ccx/jsegural.yml."""
    return Path(ref).stem


def load_schedule(text: str) -> list[dict]:
    data = yaml.safe_load(text)
    if not data or "schedule" not in data:
        raise ValueError("YAML has no 'schedule' key")
    return data["schedule"]


def read_schedule_from_stdin_or_fetch() -> str:
    if not sys.stdin.isatty():
        piped = sys.stdin.read()
        if piped.strip():
            return piped
    # Fall back to the sibling fetch script.
    fetch = Path(__file__).with_name("fetch_schedule.sh")
    result = subprocess.run(
        ["bash", str(fetch)], capture_output=True, text=True, check=True
    )
    return result.stdout


def find_duty(schedule: list[dict], target: date) -> dict | None:
    """Return the schedule entry whose [start, end) contains target, else None."""
    for entry in schedule:
        start = _parse_dt(str(entry["start"])).date()
        end = _parse_dt(str(entry["end"])).date()
        # Interval is [start, end): start inclusive, end exclusive.
        if start <= target < end:
            return entry
    return None


def resolve(schedule: list[dict], target: date) -> dict:
    entry = find_duty(schedule, target)
    if entry is None:
        return {"date": target.isoformat(), "found": False, "engineers": []}
    engineers = []
    for user in entry.get("users", []):
        org = _org_username(user["$ref"])
        engineers.append({"org_username": org, "email": f"{org}@redhat.com"})
    return {
        "date": target.isoformat(),
        "found": True,
        "start": str(entry["start"]),
        "end": str(entry["end"]),
        "engineers": engineers,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dates", nargs="+", help="dates in YYYY-MM-DD to look up")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    try:
        targets = [datetime.strptime(d, "%Y-%m-%d").date() for d in args.dates]
    except ValueError as exc:
        ap.error(f"dates must be YYYY-MM-DD: {exc}")

    schedule = load_schedule(read_schedule_from_stdin_or_fetch())
    results = [resolve(schedule, t) for t in targets]

    if args.json:
        json.dump(results, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    for r in results:
        if not r["found"]:
            print(f"{r['date']}: no schedule entry found")
            continue
        who = ", ".join(f"{e['org_username']} <{e['email']}>" for e in r["engineers"])
        print(f"{r['date']}: {who}  (week {r['start']} → {r['end']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
