# AGENTS.md template (ObsInt Processing)

Fill with **repo-specific** facts. **Omit any section that does not apply** (no fake consumers, DLQ, migrations, etc.). Keep Shared Standards out — link team-info.

```markdown
# AGENTS.md

## Project Overview

<One short paragraph: what this repo does.>

**Tech Stack**: <languages and major deps actually used>

## Team context

This repository is owned by **ObsInt Processing**.

Before working here, **load and follow the team-info skill** (Shared Standards, PR rules, Go/Python conventions, testing norms, related services):

- Skill source: https://github.com/RedHatInsights/processing-tools/blob/master/skills/team-info/SKILL.md
- Install (example): `npx skills add RedHatInsights/processing-tools --skill team-info -g -a cursor -y`

Do **not** duplicate team-wide rules in this file. Keep this AGENTS.md limited to **this repository**.

**Related repos** (from team-info): <list with links>

## Repository Structure

\`\`\`text
<only real top-level dirs / important files, one-line comments>
\`\`\`

## Development Workflow

### Setup
- <runtime / install from README or lockfiles>

### Running Tests
- <make/pytest/go test targets that exist>

### Code Quality
- <lint/format/pre-commit targets that exist>

### Building and Running
- <build/run/CLI only if they exist>

## Key Architectural Patterns

### Data flow
1. <how work enters>
2. <what this repo does>
3. <what it produces / where it goes>

### Components
- <package or module>: <role>

### Configuration
- <important knobs / env / config files — only if relevant>
- Details: <link to docs/Pages if any>

## Working with this Repository

**As an agent, you should create a TODO list** when working on tasks to track progress and ensure all steps are completed systematically.

## Code Conventions

- Follow team-info language standards unless this repo differs:
- <deltas only: linters, naming, forbidden libs, …>

## Important Notes

### Dependencies
- <unusual pins, git deps, upper bounds — if any>

### Testing
- <how tests are organized; external BDD repo only if used>

### Monitoring
- <metrics/health — only if the repo exposes them>

## Common Tasks

<!-- Optional: omit entire section if nothing clear to extend -->

### <Task named after something that exists in this repo>
1. <real path>
2. <copy existing example>
3. <tests / config touchpoints>

## Pull Request Guidelines

### Before Creating a PR
- Run <repo pre-push / test / lint targets that exist>
- Also follow team-info Pull Request Requirements and Testing

### Repo-specific checklist
- <extras only>

## Deployment Information

<!-- Omit if no deploy/ -->
- Configs: <deploy/ paths>
- Environments and promotion: see team-info Deployment Flow

## Security Considerations

- Follow team-info Security
- <repo-specific notes only if any>

## Debugging Tips

- <commands / docs that help in *this* repo>

## External References

- [README](./README.md) — <one line>
- <Pages / architecture docs if any>
- <related repos / upstream libs>
```
