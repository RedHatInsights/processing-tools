# Potential Duplicate Issues Report

**Generated:** 2026-09-17 04:21:28
**Glitchtip Instance:** glitchtip.devshift.net
**Organization:** ccx
**Similarity Threshold:** 65%
**Analysis Scope:** Unresolved issues only

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Projects with duplicates | 10 |
| Total duplicate groups | 18 |
| Total issues in groups | 42 |
| Total events affected | 0 |

---

## Table of Contents

- [archive-sync](#archive-sync) - 1 groups, 3 issues
- [ccx-data-pipeline](#ccx-data-pipeline) - 1 groups, 3 issues
- [ccx-notification-service](#ccx-notification-service) - 2 groups, 4 issues
- [ccx-notification-writer](#ccx-notification-writer) - 2 groups, 4 issues
- [ccx-upgrades-data-eng](#ccx-upgrades-data-eng) - 1 groups, 2 issues
- [dvo-writer](#dvo-writer) - 3 groups, 6 issues
- [insights-results-aggregator-db-writer](#insights-results-aggregator-db-writer) - 3 groups, 8 issues
- [parquet-factory](#parquet-factory) - 1 groups, 2 issues
- [rules-processing](#rules-processing) - 3 groups, 8 issues
- [valkey-writer](#valkey-writer) - 1 groups, 2 issues

---

## archive-sync

**Duplicate Groups:** 1
**Issues in Groups:** 3
**Total Events:** 0

### 🟢 LOW: error: Error -3 while decompressing data: invalid block type

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4604390 | 1 | error: Error -3 while decompressing data: invalid literal... | [View](https://glitchtip.devshift.net/ccx/issues/4604390) |
| #4582128 | 1 | error: Error -3 while decompressing data: invalid distanc... | [View](https://glitchtip.devshift.net/ccx/issues/4582128) |
| #4582018 | 2 | error: Error -3 while decompressing data: invalid block type | [View](https://glitchtip.devshift.net/ccx/issues/4582018) |

**Recommendation:** Consider merging into [#4604390](https://glitchtip.devshift.net/ccx/issues/4604390) (highest event count)

---

## ccx-data-pipeline

**Duplicate Groups:** 1
**Issues in Groups:** 3
**Total Events:** 0

### 🟢 LOW: AttributeError: 'str' object has no attribute 'parent'

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3852013 | 6,375 | AttributeError: 'NoneType' object has no attribute 'start... | [View](https://glitchtip.devshift.net/ccx/issues/3852013) |
| #3852210 | 4,513 | AttributeError: 'str' object has no attribute 'parent' | [View](https://glitchtip.devshift.net/ccx/issues/3852210) |
| #4580828 | 237,551 | AttributeError: 'NoneType' object has no attribute 'group' | [View](https://glitchtip.devshift.net/ccx/issues/4580828) |

**Recommendation:** Consider merging into [#3852013](https://glitchtip.devshift.net/ccx/issues/3852013) (highest event count)

---

## ccx-notification-service

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: Post \'...': readfrom tc…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3997223 | 325 | Error: Post \"http://insights-content-template-renderer-s... | [View](https://glitchtip.devshift.net/ccx/issues/3997223) |
| #4649219 | 1 | Error: Get \"http://ccx-insights-content-service:10000/ap... | [View](https://glitchtip.devshift.net/ccx/issues/4649219) |

**Recommendation:** Consider merging into [#3997223](https://glitchtip.devshift.net/ccx/issues/3997223) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4613971 | 3 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4613971) |
| #4613965 | 3 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4613965) |

**Recommendation:** Consider merging into [#4613971](https://glitchtip.devshift.net/ccx/issues/4613971) (highest event count)

---

## ccx-notification-writer

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: kafka server: Request exceeded the user-specified t…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4491664 | 6 | kafka: error while consuming ccx.ocp.results/0: kafka ser... | [View](https://glitchtip.devshift.net/ccx/issues/4491664) |
| #4580574 | 6 | kafka: error while consuming ccx.ocp.results/0: kafka ser... | [View](https://glitchtip.devshift.net/ccx/issues/4580574) |

**Recommendation:** Consider merging into [#4491664](https://glitchtip.devshift.net/ccx/issues/4491664) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4506737 | 4 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4506737) |
| #4434839 | 16 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4434839) |

**Recommendation:** Consider merging into [#4506737](https://glitchtip.devshift.net/ccx/issues/4506737) (highest event count)

---

## ccx-upgrades-data-eng

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: ConnectionError: HTTPConnectionPool(host='ccx-upgrades-inference-svc', port=8000): Max retries exce…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4693164 | 1 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4693164) |
| #4693160 | 3 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4693160) |

**Recommendation:** Consider merging into [#4693164](https://glitchtip.devshift.net/ccx/issues/4693164) (highest event count)

---

## dvo-writer

**Duplicate Groups:** 3
**Issues in Groups:** 6
**Total Events:** 0

### 🟢 LOW: Error: pq: the database system is shutting down (57P03)

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4572840 | 1,352 | Error: pq: the database system is shutting down (57P03) | [View](https://glitchtip.devshift.net/ccx/issues/4572840) |
| #4572839 | 1,352 | Error: pq: the database system is shutting down (57P03) | [View](https://glitchtip.devshift.net/ccx/issues/4572839) |

**Recommendation:** Consider merging into [#4572840](https://glitchtip.devshift.net/ccx/issues/4572840) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129705 | 183 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129705) |
| #4129707 | 183 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129707) |

**Recommendation:** Consider merging into [#4129705](https://glitchtip.devshift.net/ccx/issues/4129705) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4565631 | 5 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4565631) |
| #4586489 | 5 | kafka: error while consuming ccx.dvo.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4586489) |

**Recommendation:** Consider merging into [#4565631](https://glitchtip.devshift.net/ccx/issues/4565631) (highest event count)

---

## insights-results-aggregator-db-writer

**Duplicate Groups:** 3
**Issues in Groups:** 8
**Total Events:** 0

### 🟢 LOW: Error: write tcp ...->...: write: broken pipe

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4571111 | 4 | Error: write tcp 10.131.26.136:52622->10.0.216.46:5432: w... | [View](https://glitchtip.devshift.net/ccx/issues/4571111) |
| #4571109 | 4 | Error: write tcp 10.131.26.136:52622->10.0.216.46:5432: w... | [View](https://glitchtip.devshift.net/ccx/issues/4571109) |

**Recommendation:** Consider merging into [#4571111](https://glitchtip.devshift.net/ccx/issues/4571111) (highest event count)

---

### 🟢 LOW: Error: sql: database is closed

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4127668 | 1,594 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4127668) |
| #4293672 | 1,473 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4293672) |
| #4486496 | 1,389 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4486496) |
| #4593659 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4593659) |

**Recommendation:** Consider merging into [#4127668](https://glitchtip.devshift.net/ccx/issues/4127668) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129671 | 159 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129671) |
| #4129668 | 159 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129668) |

**Recommendation:** Consider merging into [#4129671](https://glitchtip.devshift.net/ccx/issues/4129671) (highest event count)

---

## parquet-factory

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: Error: unexpected status code 503 while pushing to https://pushgateway.app-sre.devshift.net/metrics…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4081087 | 187 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081087) |
| #4081088 | 141 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081088) |

**Recommendation:** Consider merging into [#4081087](https://glitchtip.devshift.net/ccx/issues/4081087) (highest event count)

---

## rules-processing

**Duplicate Groups:** 3
**Issues in Groups:** 8
**Total Events:** 0

### 🟢 LOW: AttributeError: 'str' object has no attribute 'parent'

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3781153 | 6,805 | AttributeError: 'NoneType' object has no attribute 'start... | [View](https://glitchtip.devshift.net/ccx/issues/3781153) |
| #3791585 | 4,742 | AttributeError: 'str' object has no attribute 'parent' | [View](https://glitchtip.devshift.net/ccx/issues/3791585) |
| #4580829 | 237,443 | AttributeError: 'NoneType' object has no attribute 'group' | [View](https://glitchtip.devshift.net/ccx/issues/4580829) |

**Recommendation:** Consider merging into [#3781153](https://glitchtip.devshift.net/ccx/issues/3781153) (highest event count)

---

### 🟢 LOW: IndexError: list index out of range

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4675824 | 12 | IndexError: list index out of range | [View](https://glitchtip.devshift.net/ccx/issues/4675824) |
| #4594819 | 2 | IndexError: list index out of range | [View](https://glitchtip.devshift.net/ccx/issues/4594819) |

**Recommendation:** Consider merging into [#4675824](https://glitchtip.devshift.net/ccx/issues/4675824) (highest event count)

---

### 🟢 LOW: Rule response make_fail(OPERATOR_ISSUE) exceeds the size limit of ... characters.

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4615774 | 3 | Rule response make_fail(CERTIFICATES_EXPIRING_SOON) excee... | [View](https://glitchtip.devshift.net/ccx/issues/4615774) |
| #4198802 | 298 | Rule response make_fail(OPERATOR_ISSUE) exceeds the size ... | [View](https://glitchtip.devshift.net/ccx/issues/4198802) |
| #4509971 | 44 | Rule response make_fail(NODES_CONTAINER_RUNTIME_VERSION) ... | [View](https://glitchtip.devshift.net/ccx/issues/4509971) |

**Recommendation:** Consider merging into [#4615774](https://glitchtip.devshift.net/ccx/issues/4615774) (highest event count)

---

## valkey-writer

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129669 | 65 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129669) |
| #4129667 | 65 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129667) |

**Recommendation:** Consider merging into [#4129669](https://glitchtip.devshift.net/ccx/issues/4129669) (highest event count)

---
