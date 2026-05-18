# Known Service-to-Repository Mapping

When step 4d needs to find a source repo, check this table first before trying naming patterns or app-interface.

| Glitchtip `project:*` label | Repository URL (SSH) | Language | Notes |
|------------------------------|----------------------|----------|-------|
| insights-results-smart-proxy | `git@github.com:RedHatInsights/insights-results-smart-proxy.git` | Go | |
| insights-results-aggregator | `git@github.com:RedHatInsights/insights-results-aggregator.git` | Go | |
| archive-sync | `git@github.com:RedHatInsights/insights-ccx-messaging.git` | Python | Package name is `ccx_messaging`, not `archive-sync` |
| ccx-data-pipeline | `git@gitlab.cee.redhat.com:ccx/ccx-rules-ocp.git` | Python | Errors in rules come from this repo; the pipeline itself is `insights-ccx-messaging` |
| ccx-notification-service | `git@github.com:RedHatInsights/ccx-notification-service.git` | Go | |
| ccx-notification-writer | `git@github.com:RedHatInsights/ccx-notification-writer.git` | Go | |
| dvo-extractor | `git@github.com:RedHatInsights/insights-ccx-messaging.git` | Python | Same codebase as archive-sync |
| dvo-writer | `git@github.com:RedHatInsights/ccx-notification-writer.git` | Go | Shares repo with notification-writer |
| valkey-writer | `git@github.com:RedHatInsights/ccx-notification-writer.git` | Go | Shares repo with notification-writer |
| insights-content-service | `git@github.com:RedHatInsights/insights-content-service.git` | Go | |
| rules-processing | `git@github.com:RedHatInsights/insights-ccx-messaging.git` | Python | |
| parquet-factory | `git@github.com:RedHatInsights/insights-ccx-messaging.git` | Python | |
| ccx-upgrades-data-eng | `git@github.com:RedHatInsights/ccx-upgrades-data-eng.git` | Python | |
| rules-uploader | `git@github.com:RedHatInsights/insights-ccx-messaging.git` | Python | |

## Updating this table

When you discover a new service-to-repo mapping during triage, add it here so future runs benefit. If a mapping turns out to be wrong (repo moved, service renamed), update it.

## Common patterns

- Many Python services (`archive-sync`, `dvo-extractor`, `rules-processing`, `parquet-factory`, `rules-uploader`) share the `insights-ccx-messaging` repo — they are different deployments of the same codebase.
- The `ccx-data-pipeline` service runs rules from `ccx-rules-ocp`. When the error originates in a rule file (path like `ccx_rules_ocp/...`), clone `ccx-rules-ocp`. When it originates in messaging code (path like `ccx_messaging/...`), clone `insights-ccx-messaging`.
- Several Go writers (`dvo-writer`, `valkey-writer`, `ccx-notification-writer`) share the `ccx-notification-writer` repo.
