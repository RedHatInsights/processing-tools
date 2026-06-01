---
name: team-info
description: ObsInt Processing team reference — repos, services, app-interface deployment, clusters, and related skills. Loaded by default for all work in team repositories.
---

# ObsInt Processing — Team Info

## Data Flow

### Internal Pipeline

Insights Operator archives arrive on the `platform.upload.announce` Kafka topic. **archive-sync** (an insights-ccx-messaging consumer) downloads the archive to S3 (`rh-openshift-obs-stage` / `rh-openshift-obs-prod-secure`) and publishes to `ccx.archive.synced`. **rules-processing** (a data-pipeline consumer) picks up from `ccx.archive.synced`, downloads the archive from S3, runs OCP rules, and publishes results to `ccx.insights.rules.results`. **rules-uploader** writes each result back to S3. **parquet-factory** also reads from `ccx.insights.rules.results` and aggregates rule-hit and cluster-info data into Parquet files on S3 (hourly).

### External Pipeline

**ccx-data-pipeline** (`data-pipeline` repo) consumes new archive events from Kafka, reads the archive from S3, runs OCP rules, and publishes results to `ccx.ocp.results`. **insights-results-db-writer** (same codebase as aggregator, different deployment params) consumes from `ccx.ocp.results` and writes to PostgreSQL. **insights-results-aggregator** reads from that DB and serves results via REST API. **insights-results-smart-proxy** is the API gateway — external clients (UI, integrations, notifications) go through it to reach the aggregator and **content-service** (rule metadata: titles, remediations, tags). **ocp-advisor-frontend** is the React UI on console.redhat.com.

**ccx-notification-writer** also consumes from `ccx.ocp.results` and writes new/changed hits into a notification DB. **ccx-notification-service** reads that DB and sends email/webhook notifications.

**ccx-upgrades-data-eng** queries RHOBS for cluster metrics and calls **ccx-upgrades-inference** (ML model) to predict upgrade failure risk.

### Kafka

AWS MSK cluster managed by AppSRE, shared across tenants. Topics are configured via PRs to [platform-mq](https://github.com/RedHatInsights/platform-mq). Used topics: `platform.upload.announce`, `ccx.archive.synced`, `ccx.insights.rules.results`, `ccx.ocp.results`.

## Tech Stack

| Area | Technologies |
|------|-------------|
| Backend services | Go (aggregator, smart-proxy, notification-*, content-service, cleaner, exporter, gathering-conditions-service),  Python (data-pipeline, parquet-factory, insights-ccx-messaging, upgrades-data-eng, upgrades-inference, template-renderer) |
| Frontend | React, PatternFly (ocp-advisor-frontend) |
| Messaging | Kafka (all inter-service communication) |
| Storage | PostgreSQL (aggregator DB, notification DB), S3 (Parquet files) |
| Deployment | [Clowder](https://github.com/RedHatInsights/clowder)/ClowdApp on OpenShift, managed via app-interface SaaS files |
| CI/CD | Konflux (Tekton), GitHub Actions, Jenkins |
| Testing | BDD with Behave (insights-behavioral-spec), IQE (iqe-ccx-plugin), pytest (Python services), Go standard testing |

All new code requires tests and coverage. See each repo's AGENTS.md or documentation for testing standards, frameworks, and how to run locally / in ephemeral.

## Deployment

### app-interface

app-interface controls service definitions, deployments, namespaces, cluster config, Grafana dashboards, and SaaS promotions. Our services live under `data/services/insights/ccx-data-pipeline/`.

Browse: https://gitlab.cee.redhat.com/service/app-interface/-/tree/master/data/services/insights/ccx-data-pipeline

App-interface GraphQL API: https://app-interface.apps.rosa.appsrep09ue1.03r5.p3.openshiftapps.com/graphql

Visual app-interface: https://visual-app-interface.devshift.net

Available app-interface [skills](https://gitlab.cee.redhat.com/service/app-interface/-/tree/master/.claude/skills).

## Repositories

### External Data Pipeline (EDP)

| Repo | What it does | Related Repos | AGENTS.md |
|------|-------------|---------|-----------|
| [data-pipeline](https://github.com/RedHatInsights/data-pipeline) | Consumes archives from Kafka, runs OCP rules, publishes results. | insights-ccx-messaging, parquet-factory | [AGENTS.md](https://github.com/RedHatInsights/data-pipeline/blob/main/AGENTS.md) |
| [insights-results-aggregator](https://github.com/RedHatInsights/insights-results-aggregator) | Stores OCP rule hits in PostgreSQL, serves them via REST API to smart-proxy. Also deployed as **insights-results-db-writer** (same code, different params — writer consumes Kafka, aggregator serves RESTAPI). | insights-results-smart-proxy, aggregator-cleaner, aggregator-exporter | [AGENTS.md](https://github.com/RedHatInsights/insights-results-aggregator/blob/master/AGENTS.md) |
| [insights-results-smart-proxy](https://github.com/RedHatInsights/insights-results-smart-proxy) | API gateway between external clients (UI, integrations) and backend pipeline services. | insights-results-aggregator, content-service, ocp-advisor-frontend | [AGENTS.md](https://github.com/RedHatInsights/insights-results-smart-proxy/blob/master/AGENTS.md) |
| [ccx-notification-service](https://github.com/RedHatInsights/ccx-notification-service) | Reads new / changed rule hits and sends notifications to customers. | ccx-notification-writer, insights-results-aggregator | — |
| [ccx-notification-writer](https://github.com/RedHatInsights/ccx-notification-writer) | Consumes rule-hit from Kafka and writes them into the notification DB. | ccx-notification-service | — |
| [ccx-upgrades-data-eng](https://github.com/RedHatInsights/ccx-upgrades-data-eng) | Queries RHOBS for cluster metrics and calls the inference model to predict upgrade risk. | ccx-upgrades-inference, obsint-mocks | — |
| [ccx-upgrades-inference](https://github.com/RedHatInsights/ccx-upgrades-inference) | REST API serving the ML model that predicts upgrade failure likelihood from cluster metrics. | ccx-upgrades-data-eng | — |
| [content-service](https://github.com/RedHatInsights/content-service) | Serves rule metadata (titles, descriptions, remediations, tags, groups) to smart-proxy. | insights-results-smart-proxy, ocp-advisor-frontend | — |
| [insights-content-template-renderer](https://github.com/RedHatInsights/insights-content-template-renderer) | Renders report messages from DoT.js templates using content data and report details. | content-service | — |
| [insights-results-aggregator-cleaner](https://github.com/RedHatInsights/insights-results-aggregator-cleaner) | Periodic job that deletes old/obsolete records from the aggregator database. | insights-results-aggregator | — |
| [insights-results-aggregator-exporter](https://github.com/RedHatInsights/insights-results-aggregator-exporter) | Exports aggregator PostgreSQL data to S3 as CSV for offline analysis. | insights-results-aggregator | — |
| [insights-operator-gathering-conditions](https://github.com/RedHatInsights/insights-operator-gathering-conditions) | Remote configuration data (conditional gathering rules, rapid recommendations) for Insights Operator. | insights-operator-gathering-conditions-service | — |
| [insights-operator-gathering-conditions-service](https://github.com/RedHatInsights/insights-operator-gathering-conditions-service) | Serves gathering conditions and rapid recommendations to Insights Operator on clusters. | insights-operator-gathering-conditions | — |

#### Frontend

| [ocp-advisor-frontend](https://github.com/RedHatInsights/ocp-advisor-frontend) | React UI for OCP Advisor on console.redhat.com — displays rule hits per cluster. | insights-results-smart-proxy, content-service | — |

### Internal Data Pipeline (IDP)

| Repo | What it does | Related Repos | AGENTS.md |
|------|-------------|---------|-----------|
| [insights-ccx-messaging](https://github.com/RedHatInsights/insights-ccx-messaging) | Python framework (on top of insights-core-messaging) that all CCX Kafka consumers inherit from. | data-pipeline, parquet-factory | [AGENTS.md](https://github.com/RedHatInsights/insights-ccx-messaging/blob/main/AGENTS.md) |
| [parquet-factory](https://github.com/RedHatInsights/parquet-factory) | Aggregates rule-hit events from Kafka into Parquet files and uploads them to S3. | data-pipeline, insights-ccx-messaging | — |

### Insights on Prem

| Repo | What it does | Related Repos | AGENTS.md |
|------|-------------|---------|-----------|
| [insights-on-prem](https://github.com/RedHatInsights/insights-on-prem) | Deployment files and code for running Insights on Prem. | all EDP ones | [AGENTS.md](https://github.com/RedHatInsights/insights-on-prem/blob/master/AGENTS.md) |

### Shared Tooling and Testing

| Repo | What it does | Related Repos | AGENTS.md |
|------|-------------|---------|-----------|
| [processing-tools](https://github.com/RedHatInsights/processing-tools) | Scripts, CI workflows, skills, and automations shared across all team repos. | all repos | — |
| [ccx-docs](https://gitlab.cee.redhat.com/ccx/ccx-docs) | Internal documentation for the team. | all repos | [AGENTS.md](https://gitlab.cee.redhat.com/ccx/ccx-docs/-/blob/master/AGENTS.md) |
| [insights-operator-utils](https://github.com/RedHatInsights/insights-operator-utils) | Shared Go library used by multiple insights-operator-* and pipeline services. | insights-results-aggregator, smart-proxy, gathering-conditions-service | — |

| [insights-behavioral-spec](https://github.com/RedHatInsights/insights-behavioral-spec) | BDD test suite (Gherkin + Python) covering the full pipeline, OCM, notifications, and ServiceLog. | all pipeline services | [AGENTS.md](https://github.com/RedHatInsights/insights-behavioral-spec/blob/main/AGENTS.md) |
| [iqe-ccx-plugin](https://gitlab.cee.redhat.com/insights-qe/iqe-ccx-plugin) | IQE test plugin for CCX integration tests in ephemeral environments. | insights-behavioral-spec | [AGENTS.md](https://gitlab.cee.redhat.com/insights-qe/iqe-ccx-plugin/-/blob/master/AGENTS.md) |
| [obsint-mocks](https://github.com/RedHatInsights/obsint-mocks) | Mock AMS and RHOBS endpoints used for local dev and BDD testing. | ccx-upgrades-data-eng | — |
| [insights-results-aggregator-mock](https://github.com/RedHatInsights/insights-results-aggregator-mock) | Mock aggregator/smart-proxy API for local frontend and BDD development. | insights-results-aggregator, ocp-advisor-frontend | — |
| [insights-results-mcp](https://github.com/RedHatInsights/insights-results-mcp) | MCP server exposing Insights results to LLMs via the Model Context Protocol. | - | — |
| [insights-results-aggregator-utils](https://github.com/RedHatInsights/insights-results-aggregator-utils) | Utility scripts (Python/Go) for testing and interacting with pipeline REST APIs. | insights-results-aggregator, insights-results-smart-proxy | — |


## Deployment Flow

All services are deployed via **app-interface** SaaS files:

1. **Stage** — SaaS target uses `ref: master` (or `main`). Merging to the default branch auto-deploys to stage.
2. **Prod** — SaaS target uses `ref: <pinned-sha>` with `promotion: auto: false`. Promoting requires an app-interface MR that updates the sha (use `/promote-hypershift` in app-interface).
3. **Ephemeral** — short-lived environments for testing, deployed via [Bonfire](https://github.com/RedHatInsights/bonfire). See [Playing with ephemeral](https://ccx.pages.redhat.com/ccx-docs/docs/processing/howto/ephemeral_env/) for setup or example config.

Each SaaS file publishes/subscribes to promotion channels (e.g. `commit-lag-exporter-*`).

### Where to update things in app-interface

Under `data/services/insights/ccx-data-pipeline/`:

| What | Path |
|------|------|
| **External SaaS files** | `external-data-pipeline/<service>.yml` |
| **Internal SaaS files** | `internal-data-pipeline/<service>.yml` |
| **Stage namespace** | `namespaces/stage-ccx-data-pipeline-stage.yml` |
| **Prod namespace** | `namespaces/ccx-data-pipeline-prod.yml` |
| **Pipelines namespace** | `namespaces/ccx-data-pipeline-pipelines.appsrep09ue1.yaml` |
| **Grafana dashboards** | `provider: directory` resourceTemplates in each SaaS file, path `/dashboards` |
| **SLO document** | `slo-documents/ccx-data-pipeline.yml` |
| **Post-deploy jobs** | `jobs/post-deploy-jobs.yml` |

## Clusters & Environments

| Environment | Cluster | Namespace |
|-------------|---------|-----------|
| Stage | crcs02ue1 | ccx-data-pipeline-stage |
| Production | crcp01ue1 | ccx-data-pipeline-prod |
| Pipelines (Konflux) | appsrep09ue1 | ccx-data-pipeline-pipelines |

## IC Schedule

It may be relevant to know who is currently on [watch duty](https://ccx.pages.redhat.com/ccx-docs/docs/processing/on_call_duty/). The rotation: `data/teams/insights/schedules/ccx-processing-ic.yml` in app-interface — [browse](https://gitlab.cee.redhat.com/service/app-interface/-/blob/master/data/teams/insights/schedules/ccx-processing-ic.yml)

## Related Skills (processing-tools)

The [processing-tools](https://github.com/RedHatInsights/processing-tools) repo hosts shared skills that can be installed into any agent:

| Skill | What it does |
|-------|-------------|
| `konflux-dep-bumps` | Triage and fix failing Konflux/MintMaker dependency bump PRs. |
| `resolve-cve` | Resolve CVE vulnerability issues from Jira — assess, bump, or mark not-affected. |
| `update-refs` | Update refs of deployments to the latest commit SHA |

To install a skill from processing-tools (Claude-specific):

```bash
# Via npx (works with any agent — replace claude-code with agent name)
npx skills add RedHatInsights/processing-tools --skill <skill-name> -g -a claude-code -y

# Via the plugin system (Claude Code only)
claude plugin marketplace add https://github.com/RedHatInsights/processing-tools
claude plugin install <skill-name>

# Or via curl into your skills directory
curl -sL https://raw.githubusercontent.com/RedHatInsights/processing-tools/master/skills/<skill-name>/SKILL.md \
  -o ~/.claude/skills/<skill-name>/SKILL.md --create-dirs
```
