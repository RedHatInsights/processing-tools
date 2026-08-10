---
name: create-agents-md
description: >-
  Create or update AGENTS.md for an ObsInt Processing repository. Use when the
  user asks to add AGENTS.md, refresh agent docs, sync AGENTS.md with Makefile
  or recent commits, or bootstrap agent guidance for a team service.
---

# Create or update AGENTS.md

Write a **repo-specific** `AGENTS.md` from evidence in **that repository**.
Shared team rules live in **team-info** — link them; do not copy.

Keep guidance **generic**: discover what *this* repo actually has. Do not assume
Kafka consumers, REST handlers, migrations, or DLQs exist.

## Source of truth (required)

Every factual claim in `AGENTS.md` must come from the **target repo** itself:

- `README*` / `CONTRIBUTING.md` / other top-level docs
- Architecture / design / implementation / configuration docs (`docs/**`, `architecture.md`, Pages sources, …)
- Other in-repo files: Makefile, lockfiles, `deploy/`, config samples, CI, and the code

Do **not** invent behavior, flags, tables, env vars, deploy defaults, or tasks.
Do **not** import “how it works in prod” from memory or other repos unless the target repo (or team-info for team-wide process only) states it.
If something is unclear or conflicting, omit it or mark `TODO (verify)` — never guess.
Do not add a preamble in `AGENTS.md` about sources; just write accurate content.

Exception: the required **Team context** block (and team-info links for Shared Standards / deployment flow) comes from team-info, not from the service repo.

## Before you start

1. Read [`skills/team-info/SKILL.md`](../team-info/SKILL.md).
2. Confirm the target repo (team-info tables or user-named).
3. **Create** (no/stub AGENTS.md) or **Update** (full file exists).
4. Feature branch + human PR; never auto-merge.
5. **Create mode: do not use an existing AGENTS.md as a source.**

## Quality bar

An agent new to the repo should be able to:

- Set up and run the documented lint/test/build commands
- Understand what the repo does and how the main pieces connect (from docs + code)
- Find important entrypoints **that exist** (CLI, main package, config)
- Open deeper docs via External References

Optional but valuable when the layout clearly supports it: a short **Common Tasks**
section for the real extension points you found — never invent ones that do not exist.

## Mode A — Create

```text
- [ ] Loaded team-info; AGENTS.md missing/ignored
- [ ] Surface facts (Makefile, README, deps, tree, deploy/CI if any)
- [ ] Docs/Pages + light code pass for architecture
- [ ] Wrote AGENTS.md from [TEMPLATE.md](TEMPLATE.md); drop N/A sections
- [ ] Team context → team-info
- [ ] Sanity checks (venv if Python; commands timeboxed)
- [ ] Offered PR / review
```

## Mode B — Update

Goal: **surgical sync**, not a rewrite. Prefer fixing what drifted since AGENTS.md
last changed; do not re-invent sections that are still true.

```text
- [ ] Read existing AGENTS.md
- [ ] Find last AGENTS.md change timestamp / commit (see below)
- [ ] Review repo history since then for breaking / doc-relevant changes
- [ ] Spot-check that cited commands/paths/flags still exist (light validity)
- [ ] Patch only facts that changed or are now wrong
- [ ] Add Team context if missing; strip duplicated Shared Standards
- [ ] Sanity checks on touched commands if any; summarize edits
```

### History window (primary signal)

1. Resolve when `AGENTS.md` was last updated, e.g.:
   - `git log -1 --format='%H %cI' -- AGENTS.md`
   - Or the commit that last touched it: `AGENTS_COMMIT=$(git log -1 --format='%H' -- AGENTS.md)`
2. Inspect changes **since that commit** (not the whole repo history):
   - `git log --oneline ${AGENTS_COMMIT}..HEAD`
   - `git diff ${AGENTS_COMMIT}..HEAD --stat`
   - Then dig into diffs that can break AGENTS guidance, especially:
     - `README*`, `docs/**`, architecture/design/config markdown
     - `Makefile`, scripts, CI (`.github`, `.tekton`, pre-commit)
     - Lockfiles / Dockerfile (toolchain, major deps)
     - `deploy/`, config samples (`*.toml`, env examples)
     - Public entrypoints / CLI flags / package layout in code
3. Map each relevant change to an AGENTS section and **update only those lines**.
4. Ignore noise that does not affect agent guidance (chore dependency bumps with no command/API change, typo-only commits, etc.) unless AGENTS names a version that is now wrong.

### Validity check (secondary)

Quickly confirm existing AGENTS claims are still true **when cheap**:

- Documented `make` / script targets still exist
- Paths and flag names still present
- Linked docs still exist

Do **not** re-run full Mode A discovery. If history is empty and spot-checks pass, report “no AGENTS updates needed.”

### When to widen scope

- AGENTS.md is a stub / clearly incomplete → ask before full Create-style rewrite
- History shows a large redesign (new layout, new primary entrypoint, removed deploy) → update the affected architecture / structure / Common Tasks sections thoroughly, still without inventing unrelated content
- Conflict between AGENTS and current docs/code → trust the repo; patch AGENTS; `TODO (verify)` only if docs and code disagree with each other

## Gather facts

### Surface (always)

| Source | Extract |
|--------|---------|
| team-info row | Purpose, related repos, language |
| `README*`, `CONTRIBUTING.md` | Overview, setup, local conventions |
| Published GitHub Pages / real `docs/**` | Prefer badge URL over stub `docs/index.md` |
| `deploy/README*` | Only if `deploy/` exists |
| Makefile **body** + `make help` | Real targets (`help` may omit some) |
| Lockfiles (`go.mod`, `pyproject.toml`, `package.json`, `requirements*`) | Versions, pins, caps |
| Top-level tree, `Dockerfile`, `.github`, `.tekton`, `.pre-commit-config.yaml` | Layout / CI / hooks **when present** |

### Architecture (when docs or an obvious main package exist)

1. Read architecture / design / implementation / configuration / overview docs if present; else README + main package entrypoints.
2. Summarize **input → work → output** in a few numbered steps **as this repo works** (library, API, batch job, UI, config-only, …).
3. List main packages/modules with one-line roles.
4. Note important config/env only if documented or clearly used.
5. Cross-check names in code lightly; `TODO (verify)` on conflicts.

Skip elaborate architecture if the repo is tiny (scripts, thin config) — a short overview is enough.

### Notable APIs / behaviors (only what you find)

Search the **main package(s)** in a language-appropriate way for:

- Public entrypoints (main, exported types/functions, CLI)
- Validation / parsing helpers **if any**
- Failure / retry / dead-letter behavior **if any**
- Unusual dependency constraints (git pins, upper bounds)

Document exact names when found. If a search finds nothing (e.g. no DLQ), write nothing — do not pad with N/A lists unless useful.

### Common Tasks (optional)

Add **Common Tasks** only when the tree shows clear ways to extend or operate the repo.

- Look at top-level packages and pick **whatever is actually there** (tests, `deploy/`, migrations, handlers, components, …).
- For each task: short numbered steps with **real paths**, copying an existing example in-tree.
- **0 tasks is fine** for docs-only, data-only, or trivial repos.
- Prefer 1–3 honest tasks over a fake “add a consumer” in a repo with none.

### README / Pages → AGENTS.md

| Content | Treatment |
|---------|-----------|
| Long tutorials | Link + brief pointer |
| Install / test / build | Include verified commands |
| Architecture | Short summary + link |
| Gotchas | Include |

## Team context (required)

```markdown
## Team context

This repository is owned by **ObsInt Processing**.

Before working here, **load and follow the team-info skill** (Shared Standards, PR rules, Go/Python conventions, testing norms, related services):

- Skill source: https://github.com/RedHatInsights/processing-tools/blob/master/skills/team-info/SKILL.md
- Install (example): `npx skills add RedHatInsights/processing-tools --skill team-info -g -a cursor -y`

Do **not** duplicate team-wide rules in this file. Keep this AGENTS.md limited to **this repository**.
```

## Completeness checklist

- [ ] Team context → team-info
- [ ] Tech stack matches lockfiles / Dockerfile when those exist
- [ ] Structure tree matches the repo (only dirs that exist)
- [ ] Documented commands exist in Makefile/scripts
- [ ] Overview / architecture appropriate to repo size
- [ ] External References: README (+ Pages if any) + related repos
- [ ] No invented components, tasks, or failure modes — every fact traceable to this repo’s docs/code (or team-info for Team context / team-wide flow only)
- [ ] No pasted team-wide PR/style policy
- [ ] No “sources” preamble in the AGENTS.md body

## Sanity check — run commands

1. Python: `.venv` + install per README. Go: toolchain from `go.mod`. Other: follow README.
2. Build + lint when available.
3. Unit tests if a fast target exists; **timebox ~3–5 minutes**. On hang: kill, keep the command, `TODO (verify)`.
4. Fix AGENTS.md if commands were wrong; keep broken-repo failures as `TODO (verify)`.

## Deliver

1. Write/patch root `AGENTS.md` from [TEMPLATE.md](TEMPLATE.md) on **Create**; on **Update**, patch in place (history-driven).
2. Summarize: Create → sources used; Update → `AGENTS.md` last-commit window, diffs reviewed, lines changed. Include command results / TODOs.
3. Ask before commit/PR unless already requested.

## Additional resources

- [TEMPLATE.md](TEMPLATE.md)
- [`../team-info/SKILL.md`](../team-info/SKILL.md)
