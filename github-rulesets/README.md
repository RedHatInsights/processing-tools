# GitHub rulesets

The branch protection in our repositories is performed using the "rulesets".

The configuration can be found on repository Settings -> Rules -> Rulesets.

## Configuration files

Each JSON file is an export of a ruleset (same repository: `RedHatInsights/processing-tools`).
All three target **branches** and apply to the **default branch** (`~DEFAULT_BRANCH`) only, with
**active** enforcement.

### `prodsec_branch_protection.json` — [PRODSEC] Branch Protection

This ruleset ensures that the requirements from ProdSec are fulfilled.

It has a bypass for both RedHat Konflux and our own bots in order to allow the auto-merge for
version bumps, rule releases or synchronisation PRs.

- **Branch deletion** and **non–fast-forward** (force-push) updates are blocked.
- **Pull request:** 1 approving review required; **code owner review** required.
- Stale reviews **are** dismissed when new commits are pushed.
- **Last-push approval** is required (new commits need another approval).
- Resolved review threads are **not** required before merge.
- **Merge methods:** merge, squash, or rebase.
- **Bypass:** Red Hat Konflux application and obsint-processing-app integrations, in "exempt" mode.

### `min_obsint_reviewers.json` — [OBSINT-Proc] 2 reviewers

This ruleset enforces the team's policy of at least 2 reviewers.

It has a bypass for both RedHat Konflux and our own bots in order to allow the auto-merge for
version bumps, rule releases or synchronisation PRs.

- **Pull request:** 2 approving reviews required; **code owner review** required.
- Stale reviews are **not** dismissed when new commits are pushed.
- **Last-push approval** is not required.
- Resolved review threads are **not** required before merge.
- **Merge methods:** merge, squash, or rebase.
- **Bypass:** Red Hat Konflux application and obsint-processing-app integrations, in "exempt" mode.

### `status_checks.json` — Status checks

This ruleset enforces that the status checks are passing for every PR. This ruleset doesn't have
any bypass, so it is enforced for every pull request, including bot ones.

**IMPORTANT NOTE**: even if it can be imported without any warning in a repository, the status
checks to be enforced are different on each one. Please, import this ruleset with caution in
other repositories or you can break your PR ruleset.

- **Required status checks:** the **Linters** check must pass (`integration_id` 15368). Branch
    protection does **not** require branches to be up to date before merging. Checks **are**
    enforced on new branches.
- **Pull request:** 0 approvals in this ruleset (reviews are covered by other rulesets);
    merge/squash/rebase allowed.
- **Bypass:** none.

## Note about actor identifiers

In the configuration files, the bypasses are shown using the `actor_id` attribute, not its name.
The currently used actors are:

- "296509": Red Hat Konflux
- "3331057": obsint-processing-app
