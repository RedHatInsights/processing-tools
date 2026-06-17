#!/usr/bin/env python3
"""Fetch CCX rule release pipeline data from GitLab for triage.

Usage:
    python3 triage_rule_release.py                       # Latest pipeline
    python3 triage_rule_release.py <pipeline-id>         # Specific pipeline
    python3 triage_rule_release.py <full-gitlab-url>     # Parse pipeline ID from URL

Output is JSON to stdout.
Requires: GITLAB_TOKEN or GL_TOKEN env var, Red Hat VPN.

macOS SSL setup:
    Python's OpenSSL doesn't read from the macOS Keychain where the Red Hat
    internal CA is installed. Export your keychain certs to a PEM file and
    point SSL_CERT_FILE at it:

        security find-certificate -a -p > ~/.ssl/certs.pem
        export SSL_CERT_FILE=~/.ssl/certs.pem

    On Linux this is usually not needed — the system CA bundle includes
    corporate certs if they were installed.
"""

import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

GITLAB = "https://gitlab.cee.redhat.com"
API = f"{GITLAB}/api/v4"
PROJECT_ID = 61075
LOG_TAIL = 80


def _token():
    """Return the GitLab personal access token from env vars."""
    for var in ("GITLAB_TOKEN", "GL_TOKEN"):
        val = os.environ.get(var, "").strip()
        if val:
            return val
    return ""


def _ssl_context():
    """Build an SSL context that trusts the system CA bundle.

    On macOS, Python's OpenSSL doesn't read from the Keychain. If
    SSL_CERT_FILE is set (e.g. to an exported keychain PEM), it will
    be picked up automatically by ssl.create_default_context().
    Otherwise this will fail on internal Red Hat hosts — see the
    module docstring for setup instructions.
    """
    return ssl.create_default_context()


def fetch(url, timeout=15):
    """Fetch a URL with GitLab auth. Returns (body, error)."""
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": _token()})
    try:
        with urllib.request.urlopen(
            req, timeout=timeout, context=_ssl_context()
        ) as resp:
            return resp.read().decode("utf-8"), None
    except urllib.error.HTTPError as e:
        return None, f"http:{e.code}"
    except urllib.error.URLError as e:
        return None, f"url:{e.reason}"


def api(url, timeout=15):
    """Fetch a URL and parse JSON. Returns (data, error)."""
    body, err = fetch(url, timeout)
    if err:
        return None, err
    try:
        return json.loads(body), None
    except json.JSONDecodeError:
        return None, "json_error"


def get_pipelines(count=1):
    """Get recent release pipelines. Returns (pipelines, errors)."""
    results = []
    errs = []
    for source in ("trigger", "web", "pipeline"):
        data, err = api(
            f"{API}/projects/{PROJECT_ID}/pipelines"
            f"?ref=master&source={source}&per_page={count}"
        )
        if err:
            errs.append(err)
            continue
        if data:
            results.extend(data)
    seen = set()
    pipelines = [
        p
        for p in sorted(results, key=lambda x: x.get("id", 0), reverse=True)
        if p["id"] not in seen and not seen.add(p["id"])
    ][:count]
    return pipelines, errs


def get_jobs(pipeline_id):
    """Get all jobs for a pipeline, paginated. Returns (jobs, errors)."""
    all_jobs = []
    errs = []
    page = 1
    while True:
        data, err = api(
            f"{API}/projects/{PROJECT_ID}/pipelines/{pipeline_id}"
            f"/jobs?per_page=100&page={page}"
        )
        if err:
            errs.append(err)
            break
        if not data:
            break
        all_jobs.extend(data)
        if len(data) < 100:
            break
        page += 1
    return all_jobs, errs


def triage(pipeline_id):
    """Fetch pipeline, jobs, and failed job logs. Returns a dict."""
    errs = []

    pipeline, err = api(f"{API}/projects/{PROJECT_ID}/pipelines/{pipeline_id}")
    if err:
        return {"error": f"Could not fetch pipeline {pipeline_id}", "errors": [err]}

    jobs_data, job_errs = get_jobs(pipeline_id)
    errs.extend(job_errs)

    tag = None
    variables, _ = api(f"{API}/projects/{PROJECT_ID}/pipelines/{pipeline_id}/variables")
    if variables:
        for v in variables:
            if v.get("key") == "CCX_RULES_TAG":
                tag = v["value"]
                break

    jobs = []
    failed = []
    for j in jobs_data:
        job = {
            "id": j["id"],
            "name": j["name"],
            "stage": j["stage"],
            "status": j["status"],
            "duration": j.get("duration"),
            "failure_reason": j.get("failure_reason"),
            "web_url": j.get("web_url"),
            "allow_failure": j.get("allow_failure", False),
        }
        jobs.append(job)

        if j["status"] == "failed" and not j.get("allow_failure"):
            log_body, _ = fetch(
                f"{API}/projects/{PROJECT_ID}/jobs/{j['id']}/trace",
                timeout=20,
            )
            if log_body:
                job["log_tail"] = "\n".join(log_body.strip().splitlines()[-LOG_TAIL:])
            failed.append(job)

    result = {
        "pipeline": {
            "id": pipeline["id"],
            "status": pipeline["status"],
            "source": pipeline.get("source"),
            "ref": pipeline.get("ref"),
            "created_at": pipeline.get("created_at"),
            "duration": pipeline.get("duration"),
            "web_url": pipeline.get("web_url"),
        },
        "tag": tag,
        "jobs": jobs,
        "failed_jobs": failed,
    }
    if errs:
        result["errors"] = errs
    return result


def main():
    """Entry point — parse args, fetch pipeline data, output JSON."""
    if not _token():
        json.dump(
            {
                "error": (
                    "No GitLab token found. Set GITLAB_TOKEN or GL_TOKEN env var."
                ),
            },
            sys.stdout,
            indent=2,
        )
        print()
        sys.exit(1)

    target = sys.argv[1] if len(sys.argv) > 1 else None

    if target:
        m = re.search(r"/pipelines/(\d+)", target)
        pipeline_id = int(m.group(1)) if m else None
        if not pipeline_id:
            try:
                pipeline_id = int(target)
            except ValueError:
                json.dump(
                    {"error": f"Could not parse pipeline ID from: {target}"},
                    sys.stdout,
                )
                print()
                sys.exit(1)
    else:
        pipelines, errs = get_pipelines()
        if not pipelines:
            json.dump(
                {"error": "No pipelines found. VPN connected?", "errors": errs},
                sys.stdout,
                indent=2,
            )
            print()
            sys.exit(1)
        pipeline_id = pipelines[0]["id"]

    result = triage(pipeline_id)
    json.dump(result, sys.stdout, indent=2)
    print()
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()
