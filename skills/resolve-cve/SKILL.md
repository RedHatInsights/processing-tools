---
name: resolve-cve
description: >-
  Resolve a CVE vulnerability issue from Jira. Reads the
  CVE details, assesses impact, and either marks "not
  affected" with a Jira comment and transition, bumps the
  affected dependency, or implements a code fix. Use when
  the user says "cve", "resolve CVE", or provides a CVE
  Jira issue.
---

# resolve-cve

The user provides a Jira key (e.g., `CCXDEV-12345`) or a Jira
URL. If no specific issue is given, find CVEs to triage by
searching the current sprint in the **CCX Core - Processing**
(CCXDEV) project.

## Pre-requisites

The user should have installed the `acli` tool:
https://developer.atlassian.com/cloud/acli/guides/install-acli/

You can check if it's installed by running:
`acli --version`

The authentication should be set up. If you ever find any issues with
the authentication, tell the user to follow
https://docs.google.com/document/d/1ilv5NgMS06SK7kS6jXtaELdxE9Nbh_8-nZcEeC9bXPI.

Full documentation for the CLI can be found in https://developer.atlassian.com/cloud/acli/.

The user also needs `syft` installed to be able to inspect the images. Please
ask the user to follow https://github.com/anchore/syft if they don't have it installed.

## Step 0: Find CVEs to triage

Use `acli` to find the CVEs to triage:
```
acli jira workitem search --jql 'project = CCXDEV
  AND type = Vulnerability
  AND sprint in openSprints()
  AND statusCategory = "To Do"
  AND assignee = currentUser()
  ORDER BY priority DESC' --fields key,summary
```

## Step 1: Read the CVE Issue

Now, for each CVE, fetch the issue via
`acli jira workitem view {Jira Key}`

and parse the data from these fields:

- **CVE ID** — embedded in the `summary` field, with this format
  `CVE-YYYY-NNNNN {Component}: {Package}: {Title} [services-ccx-default]` e.g.,
  `CVE-2026-32285 parquet-factory: github.com/buger/jsonparser: Denial of Service via malformed JSON input [services-ccx-default]`
- **Affected package** — mentioned in the description's
  `Flaw:` section (the description starts with boilerplate
  "Security Tracking Issue", "Do not make this issue
  public" — skip to the flaw text). The description stops at the `~~~` separator.

Then look up severity and fix details externally:

- **CVSS score** — use `WebSearch` for the CVE ID on NVD
  (e.g., `CVE-2026-32285 NVD`) to get the severity rating
- **Fixed version and references** — from the search results,
  collect and record these links for later use in the Jira comment:
  - NVD entry URL (e.g., `https://nvd.nist.gov/vuln/detail/CVE-YYYY-NNNNN`)
  - Language-specific advisory (e.g., Go: `https://pkg.go.dev/vuln/GO-YYYY-NNNN`,
    Python: the relevant GitHub Security Advisory)
  - Upstream fix (PR or commit URL)

  These links are the **proof** for the vulnerable version range
  and the fixed version. Always verify the fixed version from
  an authoritative source (NVD, language advisory DB, or the
  upstream PR/release notes) — do not rely solely on web search
  summaries.

If the issue is missing a CVE ID or the affected package
is unclear from the flaw text, ask the user to clarify.

## Step 2: Assess Impact

Determine whether this project is affected:

1. **Check if the package is a dependency** — Use @reference/repos.yaml
   to find the repository for this component. If the component name is not
   among the repositories, ask the user to clarify.
   Match case-insensitively (Jira may say `NLTK`, lock
   file has `nltk`). If not present at all, the project
   may not be affected. However, it can be installed at build time, so please
   check also in @reference/images.yaml.
2. **Check the installed version** — if found, compare the installed version
   with the vulnerable version range.
3. **Check if the vulnerable code path is reachable** — if
   the CVE targets a specific feature or module of the
   package, search the codebase for imports and usage of
   that feature. If the project never calls the affected
   API, it may be installed at build time.
4. **Check transitive dependencies** — if the package isn't
   a direct dependency, check whether it appears as a
   transitive dependency in the dependency tree. Trace which direct
   dependency pulls it in. Check things like `uv.lock` or `go.sum`.
5. **Check if the vulnerability is introduced at build time** — find the
   exact version using `syft`. For example:
   ```
   syft quay.io/redhat-services-prod/obsint-processing-tenant/parquet-factory/parquet-factory:latest
   ```
   or appending `-o json` if that makes it easier to parse.
   Please make sure to use `--from registry`, otherwise it won't pull the latest
   version.
   If the package is there, it means it is installed at build time and may need
   to be fixed by a rebuilt or enforcing a newer version in the Dockerfile.
   Otherwise, the component is not affected.

## Step 3: Present Assessment

Present the finding to the user clearly:

```
CVE Assessment: {CVE-ID}

Package: {package name}
Vulnerable versions: {range}
Installed version: {version}
Direct dependency: {yes/no — if no, pulled in by {parent}}

Verdict: {NOT AFFECTED / AFFECTED — bump needed / AFFECTED — code change needed}

Reasoning:
- {why this verdict — e.g., "package not in dependency tree",
  "installed version is outside vulnerable range",
  "vulnerable API is not used by this project",
  "project uses the affected code path in module X"}
```

**GATE — do not proceed without user acknowledgment.**
The user may have context that changes the verdict
(e.g., the package is used indirectly, or the feature
is enabled in production but not in tests). Present the
assessment and stop. Only continue after explicit "go".

## Step 4: Resolve

Based on the verdict and user acknowledgment:

### Path A: Not Affected

1. Add a comment to the Jira issue via `acli`:

   ```
   acli jira workitem comment create --key {Jira Key} --body '{comment text}'
   ```

   Comment text:

   ```
   **Assessment: Not Affected**

   {CVE-ID} targets {package} versions {range}.

   {Reason — one of:}
   - Package is not in the dependency tree.
   - Installed version ({version}) is outside the
     vulnerable range.
   - The vulnerable code path ({specific API/module}) is
     not used by this project.

   References:
   - {NVD URL}
   - {Language advisory URL}
   - {Upstream fix PR/commit URL}

   No action required.
   ```

2. Transition the issue to **Closed**:

   ```
   acli jira workitem transition --key {Jira Key} --status "Closed" --yes
   ```

   If "Closed" fails, try "Done" or "Won't Do" as the
   status value. Use `--yes` to skip the confirmation prompt.

### Path B: Dependency Bump

Check in the repository pull requests when was the last time the package was bumped.
If it was more than 30 days ago, ask the user if they want to bump the package.
If they do, please help them with the process.

After the bump, verify the new version installed in the `latest` image is
outside the vulnerable range. You may need to wait for the user to merge
the PR.

If the latest release is still vulnerable, stop and tell the user — no fix is
available upstream yet.

Then add a Jira comment via `acli`:

```
acli jira workitem comment create --key {Jira Key} --body '{comment text}'
```

Comment text:

```
**Resolution: Dependency bumped**

{CVE-ID} targets {package} versions {range}.
Bumped {package} from {old version} to {new version}.

References:
- {NVD URL}
- {Language advisory URL}
- {Upstream fix PR/commit URL}

Lint/types/tests: passing.
```

Please add any links or even terminal output, both command and stdout, that would proof your statement is true.

Ask user about Jira transition (same `acli jira workitem transition` command as Path A step 2).

### Path C: Code Change (Rare)

1. Explain to the user what code change is needed and why.
   This is unusual — confirm the approach before
   implementing.
2. Add a Jira comment summarizing the code change
   (`acli jira workitem comment create`).
3. Ask user about Jira transition
   (`acli jira workitem transition`).

## Step 5: Report

```
CVE {CVE-ID} resolved for {story_id}.

Verdict: {Not Affected / Bumped {package} to {version} / Code fix applied}
Jira: {commented / commented + transitioned to {status}}

{If files changed:}
Files changed:
  - {list files}

Ready to commit.
{End if}
```

If the user wants a commit (Path B or C), use message:

```
fix: resolve {CVE-ID} — bump {package} to {version}
```

or for code changes:

```
fix: resolve {CVE-ID} — {brief description}
```

## Constraints

- **User acknowledgment required** — never act on the
  verdict without the user confirming the assessment.
  They may know things the codebase analysis cannot reveal.
- **Jira transitions** — Path A (Not Affected) transitions
  automatically to Done/Closed with resolution "Won't Do".
  For Paths B and C, ask the user which transition to use.
- **Minimal changes** — bump only the affected package,
  not all dependencies.
- **Verify after every change** — lint, types, and unit
  tests must pass before declaring done.
- **Do not downplay severity** — if the project is
  affected, say so clearly. Do not stretch "not affected"
  reasoning to avoid work.
