# Potential Duplicate Issues Report

**Generated:** 2026-08-19 04:17:02
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
| Total issues in groups | 66 |
| Total events affected | 0 |

---

## Table of Contents

- [archive-sync](#archive-sync) - 1 groups, 3 issues
- [ccx-data-pipeline](#ccx-data-pipeline) - 1 groups, 3 issues
- [ccx-notification-service](#ccx-notification-service) - 1 groups, 5 issues
- [ccx-notification-writer](#ccx-notification-writer) - 3 groups, 6 issues
- [ccx-upgrades-data-eng](#ccx-upgrades-data-eng) - 2 groups, 5 issues
- [dvo-writer](#dvo-writer) - 5 groups, 11 issues
- [insights-results-aggregator](#insights-results-aggregator) - 1 groups, 9 issues
- [insights-results-aggregator-db-writer](#insights-results-aggregator-db-writer) - 4 groups, 11 issues
- [parquet-factory](#parquet-factory) - 1 groups, 2 issues
- [rules-processing](#rules-processing) - 2 groups, 7 issues
- [valkey-writer](#valkey-writer) - 2 groups, 4 issues

---

## archive-sync

**Duplicate Groups:** 1
**Issues in Groups:** 3
**Total Events:** 0

### 🟢 LOW: error: Error -3 while decompressing data: invalid block type

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4582128 | 1 | error: Error -3 while decompressing data: invalid distanc... | [View](https://glitchtip.devshift.net/ccx/issues/4582128) |
| #4582018 | 2 | error: Error -3 while decompressing data: invalid block type | [View](https://glitchtip.devshift.net/ccx/issues/4582018) |
| #4538382 | 1 | error: Error -3 while decompressing data: invalid code le... | [View](https://glitchtip.devshift.net/ccx/issues/4538382) |

**Recommendation:** Consider merging into [#4582128](https://glitchtip.devshift.net/ccx/issues/4582128) (highest event count)

---

## ccx-data-pipeline

**Duplicate Groups:** 1
**Issues in Groups:** 3
**Total Events:** 0

### 🟢 LOW: AttributeError: 'str' object has no attribute 'parent'

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3852013 | 5,643 | AttributeError: 'NoneType' object has no attribute 'start... | [View](https://glitchtip.devshift.net/ccx/issues/3852013) |
| #3852210 | 4,165 | AttributeError: 'str' object has no attribute 'parent' | [View](https://glitchtip.devshift.net/ccx/issues/3852210) |
| #4580828 | 237,551 | AttributeError: 'NoneType' object has no attribute 'group' | [View](https://glitchtip.devshift.net/ccx/issues/4580828) |

**Recommendation:** Consider merging into [#3852013](https://glitchtip.devshift.net/ccx/issues/3852013) (highest event count)

---

## ccx-notification-service

**Duplicate Groups:** 1
**Issues in Groups:** 5
**Total Events:** 0

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 5 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4408130 | 785 | Error: read tcp 10.131.1.230:47006->10.0.216.215:5432: re... | [View](https://glitchtip.devshift.net/ccx/issues/4408130) |
| #4571411 | 5,362 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4571411) |
| #4571289 | 1,772 | Error: read tcp 10.129.23.117:49636->10.0.216.215:5432: r... | [View](https://glitchtip.devshift.net/ccx/issues/4571289) |
| #4571410 | 8,178 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4571410) |
| #4571134 | 13 | Error: dial tcp 10.0.216.215:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4571134) |

**Recommendation:** Consider merging into [#4408130](https://glitchtip.devshift.net/ccx/issues/4408130) (highest event count)

---

## ccx-notification-writer

**Duplicate Groups:** 3
**Issues in Groups:** 6
**Total Events:** 0

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4017706 | 26 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4017706) |
| #4571290 | 1,519 | Error: read tcp 10.131.0.86:56666->10.0.216.215:5432: rea... | [View](https://glitchtip.devshift.net/ccx/issues/4571290) |

**Recommendation:** Consider merging into [#4017706](https://glitchtip.devshift.net/ccx/issues/4017706) (highest event count)

---

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

**Duplicate Groups:** 2
**Issues in Groups:** 5
**Total Events:** 0

### 🟢 LOW: ConnectionError: HTTPConnectionPool(host='ccx-upgrades-inference-svc', port=8000): Max retries exce…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4466473 | 22 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4466473) |
| #4466472 | 33 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4466472) |

**Recommendation:** Consider merging into [#4466473](https://glitchtip.devshift.net/ccx/issues/4466473) (highest event count)

---

### 🟢 LOW: Unable to update SSO token: Error refreshing the token: (missing_token) Missing access token parame…

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4531944 | 1 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4531944) |
| #4531940 | 1 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4531940) |
| #4531938 | 1 | Unable to update SSO token: Error refreshing the token:
(... | [View](https://glitchtip.devshift.net/ccx/issues/4531938) |

**Recommendation:** Consider merging into [#4531944](https://glitchtip.devshift.net/ccx/issues/4531944) (highest event count)

---

## dvo-writer

**Duplicate Groups:** 5
**Issues in Groups:** 11
**Total Events:** 0

### 🟢 LOW: Error: pq: the database system is shutting down (57P03)

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4572840 | 1,351 | Error: pq: the database system is shutting down (57P03) | [View](https://glitchtip.devshift.net/ccx/issues/4572840) |
| #4572839 | 1,351 | Error: pq: the database system is shutting down (57P03) | [View](https://glitchtip.devshift.net/ccx/issues/4572839) |

**Recommendation:** Consider merging into [#4572840](https://glitchtip.devshift.net/ccx/issues/4572840) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129705 | 132 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129705) |
| #4129707 | 132 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129707) |

**Recommendation:** Consider merging into [#4129705](https://glitchtip.devshift.net/ccx/issues/4129705) (highest event count)

---

### 🟢 LOW: Error: driver: bad connection

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4572838 | 1 | Error: driver: bad connection | [View](https://glitchtip.devshift.net/ccx/issues/4572838) |
| #4572841 | 1 | Error: driver: bad connection | [View](https://glitchtip.devshift.net/ccx/issues/4572841) |
| #4572837 | 1 | Error: driver: bad connection | [View](https://glitchtip.devshift.net/ccx/issues/4572837) |

**Recommendation:** Consider merging into [#4572838](https://glitchtip.devshift.net/ccx/issues/4572838) (highest event count)

---

### 🟢 LOW: Error: write tcp ...->...: write: broken pipe

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4571108 | 1 | Error: write tcp 10.128.29.91:38490->10.0.216.46:5432: wr... | [View](https://glitchtip.devshift.net/ccx/issues/4571108) |
| #4571110 | 1 | Error: write tcp 10.128.29.91:38490->10.0.216.46:5432: wr... | [View](https://glitchtip.devshift.net/ccx/issues/4571110) |

**Recommendation:** Consider merging into [#4571108](https://glitchtip.devshift.net/ccx/issues/4571108) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4565631 | 5 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4565631) |
| #4586489 | 5 | kafka: error while consuming ccx.dvo.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4586489) |

**Recommendation:** Consider merging into [#4565631](https://glitchtip.devshift.net/ccx/issues/4565631) (highest event count)

---

## insights-results-aggregator

**Duplicate Groups:** 1
**Issues in Groups:** 9
**Total Events:** 0

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 9 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4571092 | 2,880 | Error: dial tcp 10.0.216.46:5432: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4571092) |
| #4572842 | 153 | Error: dial tcp 10.0.217.160:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4572842) |
| #4572843 | 153 | Error: dial tcp 10.0.217.160:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4572843) |
| #4572844 | 153 | Error: dial tcp 10.0.217.160:5432: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4572844) |
| #4571096 | 154 | Error: dial tcp 10.0.216.46:5432: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4571096) |
| #4571097 | 9 | Error: dial tcp 10.0.216.46:5432: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4571097) |
| #4571095 | 9 | Error: dial tcp 10.0.216.46:5432: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4571095) |
| #4571093 | 3 | Error: dial tcp 10.0.216.46:5432: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4571093) |
| #4571094 | 1 | Error: dial tcp 10.0.216.46:5432: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4571094) |

**Recommendation:** Consider merging into [#4571092](https://glitchtip.devshift.net/ccx/issues/4571092) (highest event count)

---

## insights-results-aggregator-db-writer

**Duplicate Groups:** 4
**Issues in Groups:** 11
**Total Events:** 0

### 🟢 LOW: Error: sql: database is closed

**Issues:** 5 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4127668 | 1,593 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4127668) |
| #4293672 | 1,472 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4293672) |
| #4593659 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4593659) |
| #4486496 | 1,388 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4486496) |
| #4574517 | 2 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4574517) |

**Recommendation:** Consider merging into [#4127668](https://glitchtip.devshift.net/ccx/issues/4127668) (highest event count)

---

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129671 | 109 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129671) |
| #4129668 | 109 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129668) |

**Recommendation:** Consider merging into [#4129671](https://glitchtip.devshift.net/ccx/issues/4129671) (highest event count)

---

### 🟢 LOW: Error: write tcp ...->...: write: broken pipe

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4571111 | 2 | Error: write tcp 10.131.26.136:52622->10.0.216.46:5432: w... | [View](https://glitchtip.devshift.net/ccx/issues/4571111) |
| #4571109 | 2 | Error: write tcp 10.131.26.136:52622->10.0.216.46:5432: w... | [View](https://glitchtip.devshift.net/ccx/issues/4571109) |

**Recommendation:** Consider merging into [#4571111](https://glitchtip.devshift.net/ccx/issues/4571111) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4017705 | 71 | Error: dial tcp 10.0.184.48:9096: connect: connection ref... | [View](https://glitchtip.devshift.net/ccx/issues/4017705) |
| #4506735 | 2 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4506735) |

**Recommendation:** Consider merging into [#4017705](https://glitchtip.devshift.net/ccx/issues/4017705) (highest event count)

---

## parquet-factory

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: Error: unexpected status code 503 while pushing to https://pushgateway.app-sre.devshift.net/metrics…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4081088 | 141 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081088) |
| #4081087 | 185 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081087) |

**Recommendation:** Consider merging into [#4081088](https://glitchtip.devshift.net/ccx/issues/4081088) (highest event count)

---

## rules-processing

**Duplicate Groups:** 2
**Issues in Groups:** 7
**Total Events:** 0

### 🟢 LOW: AttributeError: 'str' object has no attribute 'parent'

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3781153 | 6,071 | AttributeError: 'NoneType' object has no attribute 'start... | [View](https://glitchtip.devshift.net/ccx/issues/3781153) |
| #3791585 | 4,394 | AttributeError: 'str' object has no attribute 'parent' | [View](https://glitchtip.devshift.net/ccx/issues/3791585) |
| #4580829 | 237,443 | AttributeError: 'NoneType' object has no attribute 'group' | [View](https://glitchtip.devshift.net/ccx/issues/4580829) |

**Recommendation:** Consider merging into [#3781153](https://glitchtip.devshift.net/ccx/issues/3781153) (highest event count)

---

### 🟢 LOW: Rule response make_fail(OPERATOR_ISSUE) exceeds the size limit of ... characters.

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4198802 | 230 | Rule response make_fail(OPERATOR_ISSUE) exceeds the size ... | [View](https://glitchtip.devshift.net/ccx/issues/4198802) |
| #4509971 | 44 | Rule response make_fail(NODES_CONTAINER_RUNTIME_VERSION) ... | [View](https://glitchtip.devshift.net/ccx/issues/4509971) |
| #4526281 | 4 | Rule response make_fail(CERTIFICATES_EXPIRING_SOON) excee... | [View](https://glitchtip.devshift.net/ccx/issues/4526281) |
| #4233800 | 373 | Rule response make_fail(MACHINE_POOL_NOT_OK) exceeds the ... | [View](https://glitchtip.devshift.net/ccx/issues/4233800) |

**Recommendation:** Consider merging into [#4198802](https://glitchtip.devshift.net/ccx/issues/4198802) (highest event count)

---

## valkey-writer

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129669 | 56 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129669) |
| #4129667 | 56 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129667) |

**Recommendation:** Consider merging into [#4129669](https://glitchtip.devshift.net/ccx/issues/4129669) (highest event count)

---

### 🟢 LOW: Error: dial tcp ...: connect: connection refused

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4017718 | 25 | Error: dial tcp 10.0.186.167:9096: connect: connection re... | [View](https://glitchtip.devshift.net/ccx/issues/4017718) |
| #4506736 | 2 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4506736) |

**Recommendation:** Consider merging into [#4017718](https://glitchtip.devshift.net/ccx/issues/4017718) (highest event count)

---
