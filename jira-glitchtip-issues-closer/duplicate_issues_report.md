# Potential Duplicate Issues Report

**Generated:** 2026-11-25 10:52:32
**Glitchtip Instance:** glitchtip.devshift.net
**Organization:** ccx
**Similarity Threshold:** 65%
**Analysis Scope:** Unresolved issues only

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Projects with duplicates | 10 |
| Total duplicate groups | 22 |
| Total issues in groups | 68 |
| Total events affected | 0 |

---

## Table of Contents

- [archive-sync](#archive-sync) - 1 groups, 2 issues
- [ccx-notification-service](#ccx-notification-service) - 4 groups, 11 issues
- [ccx-notification-writer](#ccx-notification-writer) - 2 groups, 5 issues
- [ccx-upgrades-data-eng](#ccx-upgrades-data-eng) - 3 groups, 8 issues
- [dvo-writer](#dvo-writer) - 3 groups, 9 issues
- [insights-results-aggregator](#insights-results-aggregator) - 1 groups, 10 issues
- [insights-results-aggregator-db-writer](#insights-results-aggregator-db-writer) - 3 groups, 11 issues
- [parquet-factory](#parquet-factory) - 2 groups, 4 issues
- [rules-processing](#rules-processing) - 1 groups, 4 issues
- [valkey-writer](#valkey-writer) - 2 groups, 4 issues

---

## archive-sync

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: error: Error -3 while decompressing data: invalid block type

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4696802 | 10 | error: Error -3 while decompressing data: invalid code le... | [View](https://glitchtip.devshift.net/ccx/issues/4696802) |
| #4582018 | 25 | error: Error -3 while decompressing data: invalid block type | [View](https://glitchtip.devshift.net/ccx/issues/4582018) |

**Recommendation:** Consider merging into [#4696802](https://glitchtip.devshift.net/ccx/issues/4696802) (highest event count)

---

## ccx-notification-service

**Duplicate Groups:** 4
**Issues in Groups:** 11
**Total Events:** 0

### 🟢 LOW: Error: Post \'...': readfrom tc…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3997223 | 556 | Error: Post \"http://insights-content-template-renderer-s... | [View](https://glitchtip.devshift.net/ccx/issues/3997223) |
| #4649219 | 3 | Error: Get \"http://ccx-insights-content-service:10000/ap... | [View](https://glitchtip.devshift.net/ccx/issues/4649219) |

**Recommendation:** Consider merging into [#3997223](https://glitchtip.devshift.net/ccx/issues/3997223) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 5 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4408130 | 2,108 | Error: read tcp 10.131.1.230:47006->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4408130) |
| #4852265 | 132 | Error: dial tcp 10.0.216.215:5432: connect: connection ti... | [View](https://glitchtip.devshift.net/ccx/issues/4852265) |
| #4852264 | 1,141 | Error: read tcp 10.129.5.216:41030->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4852264) |
| #4854273 | 1,130 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4854273) |
| #4854274 | 1,125 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4854274) |

**Recommendation:** Consider merging into [#4408130](https://glitchtip.devshift.net/ccx/issues/4408130) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793836 | 2 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793836) |
| #4793833 | 2 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793833) |

**Recommendation:** Consider merging into [#4793836](https://glitchtip.devshift.net/ccx/issues/4793836) (highest event count)

---

### 🟢 LOW: Couldn't initialize Kafka producer with the provided config.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4619510 | 151 | Couldn't initialize Service Log producer with the provide... | [View](https://glitchtip.devshift.net/ccx/issues/4619510) |
| #4933130 | 20 | Couldn't initialize Kafka producer with the provided config. | [View](https://glitchtip.devshift.net/ccx/issues/4933130) |

**Recommendation:** Consider merging into [#4619510](https://glitchtip.devshift.net/ccx/issues/4619510) (highest event count)

---

## ccx-notification-writer

**Duplicate Groups:** 2
**Issues in Groups:** 5
**Total Events:** 0

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4017706 | 36 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4017706) |
| #4852266 | 23 | Error: read tcp 10.129.1.192:42670->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4852266) |

**Recommendation:** Consider merging into [#4017706](https://glitchtip.devshift.net/ccx/issues/4017706) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #5006572 | 1 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/5006572) |
| #4794006 | 9 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4794006) |
| #4881799 | 2 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4881799) |

**Recommendation:** Consider merging into [#5006572](https://glitchtip.devshift.net/ccx/issues/5006572) (highest event count)

---

## ccx-upgrades-data-eng

**Duplicate Groups:** 3
**Issues in Groups:** 8
**Total Events:** 0

### 🟢 LOW: Unable to update SSO token: Error refreshing the token: (unauthorized_client) Invalid client or Inv…

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4989244 | 169 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4989244) |
| #4989245 | 83 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4989245) |
| #4989223 | 261 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4989223) |
| #4989224 | 168 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4989224) |

**Recommendation:** Consider merging into [#4989244](https://glitchtip.devshift.net/ccx/issues/4989244) (highest event count)

---

### 🟢 LOW: TokenError: Error refreshing the token:

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4462503 | 30 | TokenError: Error refreshing the token: | [View](https://glitchtip.devshift.net/ccx/issues/4462503) |
| #4904816 | 1 | TokenError: Error refreshing the token: | [View](https://glitchtip.devshift.net/ccx/issues/4904816) |

**Recommendation:** Consider merging into [#4462503](https://glitchtip.devshift.net/ccx/issues/4462503) (highest event count)

---

### 🟢 LOW: ConnectionError: HTTPConnectionPool(host='ccx-upgrades-inference-svc', port=8000): Max retries exce…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4693164 | 33 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4693164) |
| #4693160 | 20 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4693160) |

**Recommendation:** Consider merging into [#4693164](https://glitchtip.devshift.net/ccx/issues/4693164) (highest event count)

---

## dvo-writer

**Duplicate Groups:** 3
**Issues in Groups:** 9
**Total Events:** 0

### 🟢 LOW: Error: sql: database is closed

**Issues:** 5 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4965657 | 9 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4965657) |
| #4976627 | 2 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4976627) |
| #4965656 | 8 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4965656) |
| #4887263 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4887263) |
| #4887264 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4887264) |

**Recommendation:** Consider merging into [#4965657](https://glitchtip.devshift.net/ccx/issues/4965657) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793109 | 24 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793109) |
| #4793121 | 24 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793121) |

**Recommendation:** Consider merging into [#4793109](https://glitchtip.devshift.net/ccx/issues/4793109) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4730833 | 7 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4730833) |
| #4937434 | 6 | kafka: error while consuming ccx.dvo.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4937434) |

**Recommendation:** Consider merging into [#4730833](https://glitchtip.devshift.net/ccx/issues/4730833) (highest event count)

---

## insights-results-aggregator

**Duplicate Groups:** 1
**Issues in Groups:** 10
**Total Events:** 0

### 🟢 LOW: Error: pq: password authentication failed for user "postgres" (28P01)

**Issues:** 10 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4974959 | 511 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4974959) |
| #4974960 | 192 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4974960) |
| #4974997 | 13 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4974997) |
| #4974998 | 13 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4974998) |
| #4975000 | 2 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4975000) |
| #4974999 | 2 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4974999) |
| #4975051 | 4 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4975051) |
| #4974985 | 4 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4974985) |
| #4975050 | 1 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4975050) |
| #4975049 | 1 | Error: pq: password authentication failed for user "postg... | [View](https://glitchtip.devshift.net/ccx/issues/4975049) |

**Recommendation:** Consider merging into [#4974959](https://glitchtip.devshift.net/ccx/issues/4974959) (highest event count)

---

## insights-results-aggregator-db-writer

**Duplicate Groups:** 3
**Issues in Groups:** 11
**Total Events:** 0

### 🟢 LOW: Error: sql: database is closed

**Issues:** 6 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4127668 | 1,661 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4127668) |
| #4293672 | 1,539 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4293672) |
| #4866428 | 2 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4866428) |
| #4839684 | 60 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4839684) |
| #4768423 | 7 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4768423) |
| #4959747 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4959747) |

**Recommendation:** Consider merging into [#4127668](https://glitchtip.devshift.net/ccx/issues/4127668) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4793116 | 27 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793116) |
| #4793110 | 26 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4793110) |

**Recommendation:** Consider merging into [#4793116](https://glitchtip.devshift.net/ccx/issues/4793116) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #5006573 | 1 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/5006573) |
| #4938005 | 1 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4938005) |
| #4794125 | 10 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4794125) |

**Recommendation:** Consider merging into [#5006573](https://glitchtip.devshift.net/ccx/issues/5006573) (highest event count)

---

## parquet-factory

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Request was for a consumer group that is not coordinated by this broker

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4939109 | 20 | Error: kafka server: Request was for a consumer group tha... | [View](https://glitchtip.devshift.net/ccx/issues/4939109) |
| #4939113 | 20 | Error: kafka server: Request was for a consumer group tha... | [View](https://glitchtip.devshift.net/ccx/issues/4939113) |

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

**Duplicate Groups:** 1
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Rule response make_fail(OPERATOR_ISSUE) exceeds the size limit of ... characters.

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4847319 | 8 | Rule response make_fail(OPERATOR_ISSUE) exceeds the size ... | [View](https://glitchtip.devshift.net/ccx/issues/4847319) |
| #4927785 | 1 | Rule response make_fail(MACHINE_POOL_NOT_OK) exceeds the ... | [View](https://glitchtip.devshift.net/ccx/issues/4927785) |
| #4615774 | 6 | Rule response make_fail(CERTIFICATES_EXPIRING_SOON) excee... | [View](https://glitchtip.devshift.net/ccx/issues/4615774) |
| #4729746 | 36 | Rule response make_fail(NODES_CONTAINER_RUNTIME_VERSION) ... | [View](https://glitchtip.devshift.net/ccx/issues/4729746) |

**Recommendation:** Consider merging into [#4847319](https://glitchtip.devshift.net/ccx/issues/4847319) (highest event count)

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
| #4881803 | 2 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4881803) |
| #4793697 | 2 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4793697) |

**Recommendation:** Consider merging into [#4881803](https://glitchtip.devshift.net/ccx/issues/4881803) (highest event count)

---
