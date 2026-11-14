# Potential Duplicate Issues Report

**Generated:** 2026-11-14 04:12:25
**Glitchtip Instance:** glitchtip.devshift.net
**Organization:** ccx
**Similarity Threshold:** 65%
**Analysis Scope:** Unresolved issues only

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Projects with duplicates | 11 |
| Total duplicate groups | 23 |
| Total issues in groups | 62 |
| Total events affected | 0 |

---

## Table of Contents

- [archive-sync](#archive-sync) - 1 groups, 5 issues
- [ccx-data-pipeline](#ccx-data-pipeline) - 1 groups, 2 issues
- [ccx-notification-service](#ccx-notification-service) - 4 groups, 11 issues
- [ccx-notification-writer](#ccx-notification-writer) - 2 groups, 4 issues
- [ccx-upgrades-data-eng](#ccx-upgrades-data-eng) - 2 groups, 4 issues
- [dvo-extractor](#dvo-extractor) - 1 groups, 2 issues
- [dvo-writer](#dvo-writer) - 3 groups, 7 issues
- [insights-results-aggregator-db-writer](#insights-results-aggregator-db-writer) - 3 groups, 13 issues
- [parquet-factory](#parquet-factory) - 2 groups, 4 issues
- [rules-processing](#rules-processing) - 2 groups, 6 issues
- [valkey-writer](#valkey-writer) - 2 groups, 4 issues

---

## archive-sync

**Duplicate Groups:** 1
**Issues in Groups:** 5
**Total Events:** 0

### 🟢 LOW: error: Error -3 while decompressing data: invalid block type

**Issues:** 5 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4696802 | 10 | error: Error -3 while decompressing data: invalid code le... | [View](https://glitchtip.devshift.net/ccx/issues/4696802) |
| #4582018 | 25 | error: Error -3 while decompressing data: invalid block type | [View](https://glitchtip.devshift.net/ccx/issues/4582018) |
| #4768590 | 7 | error: Error -3 while decompressing data: invalid distanc... | [View](https://glitchtip.devshift.net/ccx/issues/4768590) |
| #4729727 | 11 | error: Error -3 while decompressing data: invalid stored ... | [View](https://glitchtip.devshift.net/ccx/issues/4729727) |
| #4782079 | 2 | error: Error -3 while decompressing data: invalid literal... | [View](https://glitchtip.devshift.net/ccx/issues/4782079) |

**Recommendation:** Consider merging into [#4696802](https://glitchtip.devshift.net/ccx/issues/4696802) (highest event count)

---

## ccx-data-pipeline

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: ParseException: ccx_ocp_core.parsers.insights_operator.core.PodsIO couldn't parse json.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4901599 | 1 | ParseException: ccx_ocp_core.parsers.insights_operator.op... | [View](https://glitchtip.devshift.net/ccx/issues/4901599) |
| #4319957 | 2,017 | ParseException: ccx_ocp_core.parsers.insights_operator.co... | [View](https://glitchtip.devshift.net/ccx/issues/4319957) |

**Recommendation:** Consider merging into [#4901599](https://glitchtip.devshift.net/ccx/issues/4901599) (highest event count)

---

## ccx-notification-service

**Duplicate Groups:** 4
**Issues in Groups:** 11
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793836 | 2 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793836) |
| #4793833 | 2 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793833) |

**Recommendation:** Consider merging into [#4793836](https://glitchtip.devshift.net/ccx/issues/4793836) (highest event count)

---

### 🟢 LOW: Error: Post \'...': readfrom tc…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3997223 | 539 | Error: Post \"http://insights-content-template-renderer-s... | [View](https://glitchtip.devshift.net/ccx/issues/3997223) |
| #4649219 | 3 | Error: Get \"http://ccx-insights-content-service:10000/ap... | [View](https://glitchtip.devshift.net/ccx/issues/4649219) |

**Recommendation:** Consider merging into [#3997223](https://glitchtip.devshift.net/ccx/issues/3997223) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 5 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4408130 | 1,636 | Error: read tcp 10.131.1.230:47006->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4408130) |
| #4852265 | 15 | Error: dial tcp 10.0.216.215:5432: connect: connection ti... | [View](https://glitchtip.devshift.net/ccx/issues/4852265) |
| #4852264 | 1,141 | Error: read tcp 10.129.5.216:41030->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4852264) |
| #4854273 | 1,130 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4854273) |
| #4854274 | 1,125 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4854274) |

**Recommendation:** Consider merging into [#4408130](https://glitchtip.devshift.net/ccx/issues/4408130) (highest event count)

---

### 🟢 LOW: Couldn't initialize Kafka producer with the provided config.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4933130 | 14 | Couldn't initialize Kafka producer with the provided config. | [View](https://glitchtip.devshift.net/ccx/issues/4933130) |
| #4619510 | 114 | Couldn't initialize Service Log producer with the provide... | [View](https://glitchtip.devshift.net/ccx/issues/4619510) |

**Recommendation:** Consider merging into [#4933130](https://glitchtip.devshift.net/ccx/issues/4933130) (highest event count)

---

## ccx-notification-writer

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4017706 | 35 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4017706) |
| #4852266 | 23 | Error: read tcp 10.129.1.192:42670->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4852266) |

**Recommendation:** Consider merging into [#4017706](https://glitchtip.devshift.net/ccx/issues/4017706) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4794006 | 9 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4794006) |
| #4881799 | 2 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4881799) |

**Recommendation:** Consider merging into [#4794006](https://glitchtip.devshift.net/ccx/issues/4794006) (highest event count)

---

## ccx-upgrades-data-eng

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: TokenError: Error refreshing the token:

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4462503 | 29 | TokenError: Error refreshing the token: | [View](https://glitchtip.devshift.net/ccx/issues/4462503) |
| #4904816 | 1 | TokenError: Error refreshing the token: | [View](https://glitchtip.devshift.net/ccx/issues/4904816) |

**Recommendation:** Consider merging into [#4462503](https://glitchtip.devshift.net/ccx/issues/4462503) (highest event count)

---

### 🟢 LOW: ConnectionError: HTTPConnectionPool(host='ccx-upgrades-inference-svc', port=8000): Max retries exce…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4693164 | 17 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4693164) |
| #4693160 | 18 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4693160) |

**Recommendation:** Consider merging into [#4693164](https://glitchtip.devshift.net/ccx/issues/4693164) (highest event count)

---

## dvo-extractor

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: ParseException: ccx_ocp_core.parsers.insights_operator.core.PodsIO couldn't parse json.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4901601 | 1 | ParseException: ccx_ocp_core.parsers.insights_operator.op... | [View](https://glitchtip.devshift.net/ccx/issues/4901601) |
| #4319955 | 2,016 | ParseException: ccx_ocp_core.parsers.insights_operator.co... | [View](https://glitchtip.devshift.net/ccx/issues/4319955) |

**Recommendation:** Consider merging into [#4901601](https://glitchtip.devshift.net/ccx/issues/4901601) (highest event count)

---

## dvo-writer

**Duplicate Groups:** 3
**Issues in Groups:** 7
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793109 | 24 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793109) |
| #4793121 | 24 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793121) |

**Recommendation:** Consider merging into [#4793109](https://glitchtip.devshift.net/ccx/issues/4793109) (highest event count)

---

### 🟢 LOW: Error: sql: database is closed

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4887263 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4887263) |
| #4887264 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4887264) |

**Recommendation:** Consider merging into [#4887263](https://glitchtip.devshift.net/ccx/issues/4887263) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.dvo.results/0: write tcp ...->...: w…

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4937434 | 6 | kafka: error while consuming ccx.dvo.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4937434) |
| #4794206 | 1 | kafka: error while consuming ccx.dvo.results/0: write tcp... | [View](https://glitchtip.devshift.net/ccx/issues/4794206) |
| #4794179 | 1 | kafka: error while consuming ccx.dvo.results/0: kafka: br... | [View](https://glitchtip.devshift.net/ccx/issues/4794179) |

**Recommendation:** Consider merging into [#4937434](https://glitchtip.devshift.net/ccx/issues/4937434) (highest event count)

---

## insights-results-aggregator-db-writer

**Duplicate Groups:** 3
**Issues in Groups:** 13
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793110 | 26 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793110) |
| #4793116 | 26 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793116) |

**Recommendation:** Consider merging into [#4793110](https://glitchtip.devshift.net/ccx/issues/4793110) (highest event count)

---

### 🟢 LOW: Error: sql: database is closed

**Issues:** 8 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4127668 | 1,598 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4127668) |
| #4293672 | 1,477 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4293672) |
| #4866428 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4866428) |
| #4839684 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4839684) |
| #4768423 | 2 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4768423) |
| #4802967 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4802967) |
| #4802965 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4802965) |
| #4802966 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4802966) |

**Recommendation:** Consider merging into [#4127668](https://glitchtip.devshift.net/ccx/issues/4127668) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4938005 | 1 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4938005) |
| #4794125 | 10 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4794125) |
| #4793238 | 1 | kafka: error while consuming ccx.ocp.results/0: kafka ser... | [View](https://glitchtip.devshift.net/ccx/issues/4793238) |

**Recommendation:** Consider merging into [#4938005](https://glitchtip.devshift.net/ccx/issues/4938005) (highest event count)

---

## parquet-factory

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Request was for a consumer group that is not coordinated by this broker

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4939109 | 7 | Error: kafka server: Request was for a consumer group tha... | [View](https://glitchtip.devshift.net/ccx/issues/4939109) |
| #4939113 | 7 | Error: kafka server: Request was for a consumer group tha... | [View](https://glitchtip.devshift.net/ccx/issues/4939113) |

**Recommendation:** Consider merging into [#4939109](https://glitchtip.devshift.net/ccx/issues/4939109) (highest event count)

---

### 🟢 LOW: Error: unexpected status code 503 while pushing to https://pushgateway.app-sre.devshift.net/metrics…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4781142 | 3 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4781142) |
| #4081087 | 190 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081087) |

**Recommendation:** Consider merging into [#4781142](https://glitchtip.devshift.net/ccx/issues/4781142) (highest event count)

---

## rules-processing

**Duplicate Groups:** 2
**Issues in Groups:** 6
**Total Events:** 0

### 🟢 LOW: ParseException: ccx_ocp_core.parsers.insights_operator.core.PodsIO couldn't parse json.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4901600 | 1 | ParseException: ccx_ocp_core.parsers.insights_operator.op... | [View](https://glitchtip.devshift.net/ccx/issues/4901600) |
| #4319956 | 2,016 | ParseException: ccx_ocp_core.parsers.insights_operator.co... | [View](https://glitchtip.devshift.net/ccx/issues/4319956) |

**Recommendation:** Consider merging into [#4901600](https://glitchtip.devshift.net/ccx/issues/4901600) (highest event count)

---

### 🟢 LOW: Rule response make_fail(OPERATOR_ISSUE) exceeds the size limit of ... characters.

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4927785 | 1 | Rule response make_fail(MACHINE_POOL_NOT_OK) exceeds the ... | [View](https://glitchtip.devshift.net/ccx/issues/4927785) |
| #4615774 | 6 | Rule response make_fail(CERTIFICATES_EXPIRING_SOON) excee... | [View](https://glitchtip.devshift.net/ccx/issues/4615774) |
| #4847319 | 3 | Rule response make_fail(OPERATOR_ISSUE) exceeds the size ... | [View](https://glitchtip.devshift.net/ccx/issues/4847319) |
| #4729746 | 36 | Rule response make_fail(NODES_CONTAINER_RUNTIME_VERSION) ... | [View](https://glitchtip.devshift.net/ccx/issues/4729746) |

**Recommendation:** Consider merging into [#4927785](https://glitchtip.devshift.net/ccx/issues/4927785) (highest event count)

---

## valkey-writer

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793832 | 19 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793832) |
| #4793834 | 19 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793834) |

**Recommendation:** Consider merging into [#4793832](https://glitchtip.devshift.net/ccx/issues/4793832) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: dial tcp ...: connect: connection ref…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793697 | 2 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4793697) |
| #4881803 | 1 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4881803) |

**Recommendation:** Consider merging into [#4793697](https://glitchtip.devshift.net/ccx/issues/4793697) (highest event count)

---
