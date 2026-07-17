# Potential Duplicate Issues Report

**Generated:** 2026-07-17 05:09:06
**Glitchtip Instance:** glitchtip.devshift.net
**Organization:** ccx
**Similarity Threshold:** 65%
**Analysis Scope:** Unresolved issues only

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Projects with duplicates | 10 |
| Total duplicate groups | 19 |
| Total issues in groups | 170 |
| Total events affected | 0 |

---

## Table of Contents

- [ccx-data-pipeline](#ccx-data-pipeline) - 2 groups, 13 issues
- [ccx-notification-service](#ccx-notification-service) - 1 groups, 2 issues
- [ccx-notification-writer](#ccx-notification-writer) - 1 groups, 3 issues
- [ccx-upgrades-data-eng](#ccx-upgrades-data-eng) - 1 groups, 2 issues
- [dvo-extractor](#dvo-extractor) - 1 groups, 2 issues
- [dvo-writer](#dvo-writer) - 2 groups, 4 issues
- [insights-results-aggregator-db-writer](#insights-results-aggregator-db-writer) - 3 groups, 13 issues
- [parquet-factory](#parquet-factory) - 1 groups, 2 issues
- [rules-processing](#rules-processing) - 5 groups, 123 issues
- [valkey-writer](#valkey-writer) - 2 groups, 6 issues

---

## ccx-data-pipeline

**Duplicate Groups:** 2
**Issues in Groups:** 13
**Total Events:** 0

### 🟢 LOW: AttributeError: 'str' object has no attribute 'parent'

**Issues:** 11 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3852013 | 4,844 | AttributeError: 'NoneType' object has no attribute 'start... | [View](https://glitchtip.devshift.net/ccx/issues/3852013) |
| #3852210 | 3,771 | AttributeError: 'str' object has no attribute 'parent' | [View](https://glitchtip.devshift.net/ccx/issues/3852210) |
| #4520000 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520000) |
| #4519999 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519999) |
| #4519998 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519998) |
| #4519997 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519997) |
| #4519996 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519996) |
| #4519995 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519995) |
| #4519994 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519994) |
| #4519993 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519993) |
| #4519992 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4519992) |

**Recommendation:** Consider merging into [#3852013](https://glitchtip.devshift.net/ccx/issues/3852013) (highest event count)

---

### 🟢 LOW: ParseException: ccx_ocp_core.parsers.insights_operator.core.PodsIO couldn't parse json.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4319957 | 1,056 | ParseException: ccx_ocp_core.parsers.insights_operator.co... | [View](https://glitchtip.devshift.net/ccx/issues/4319957) |
| #4513667 | 1 | ParseException: ccx_ocp_core.parsers.insights_operator_hc... | [View](https://glitchtip.devshift.net/ccx/issues/4513667) |

**Recommendation:** Consider merging into [#4319957](https://glitchtip.devshift.net/ccx/issues/4319957) (highest event count)

---

## ccx-notification-service

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: Error: Post \'...': readfrom tc…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3997223 | 290 | Error: Post \"http://insights-content-template-renderer-s... | [View](https://glitchtip.devshift.net/ccx/issues/3997223) |
| #4519036 | 8 | Error: Get \"http://ccx-insights-content-service:10000/ap... | [View](https://glitchtip.devshift.net/ccx/issues/4519036) |

**Recommendation:** Consider merging into [#3997223](https://glitchtip.devshift.net/ccx/issues/3997223) (highest event count)

---

## ccx-notification-writer

**Duplicate Groups:** 1
**Issues in Groups:** 3
**Total Events:** 0

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4434839 | 15 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4434839) |
| #4506737 | 3 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4506737) |
| #4494281 | 1 | kafka: error while consuming ccx.ocp.results/0: read tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4494281) |

**Recommendation:** Consider merging into [#4434839](https://glitchtip.devshift.net/ccx/issues/4434839) (highest event count)

---

## ccx-upgrades-data-eng

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: ConnectionError: HTTPConnectionPool(host='ccx-upgrades-inference-svc', port=8000): Max retries exce…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4466472 | 33 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4466472) |
| #4466473 | 21 | ConnectionError: HTTPConnectionPool(host='ccx-upgrades-in... | [View](https://glitchtip.devshift.net/ccx/issues/4466473) |

**Recommendation:** Consider merging into [#4466472](https://glitchtip.devshift.net/ccx/issues/4466472) (highest event count)

---

## dvo-extractor

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: ParseException: ccx_ocp_core.parsers.insights_operator.core.PodsIO couldn't parse json.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4319955 | 1,055 | ParseException: ccx_ocp_core.parsers.insights_operator.co... | [View](https://glitchtip.devshift.net/ccx/issues/4319955) |
| #4513668 | 1 | ParseException: ccx_ocp_core.parsers.insights_operator_hc... | [View](https://glitchtip.devshift.net/ccx/issues/4513668) |

**Recommendation:** Consider merging into [#4319955](https://glitchtip.devshift.net/ccx/issues/4319955) (highest event count)

---

## dvo-writer

**Duplicate Groups:** 2
**Issues in Groups:** 4
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129705 | 120 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129705) |
| #4129707 | 120 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129707) |

**Recommendation:** Consider merging into [#4129705](https://glitchtip.devshift.net/ccx/issues/4129705) (highest event count)

---

### 🟢 LOW: Error: sql: database is closed

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4111096 | 172 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4111096) |
| #4111095 | 53 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4111095) |

**Recommendation:** Consider merging into [#4111096](https://glitchtip.devshift.net/ccx/issues/4111096) (highest event count)

---

## insights-results-aggregator-db-writer

**Duplicate Groups:** 3
**Issues in Groups:** 13
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129671 | 98 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129671) |
| #4129668 | 98 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129668) |

**Recommendation:** Consider merging into [#4129671](https://glitchtip.devshift.net/ccx/issues/4129671) (highest event count)

---

### 🟢 LOW: Error: sql: database is closed

**Issues:** 8 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4127668 | 207 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4127668) |
| #4293672 | 86 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4293672) |
| #4427981 | 3 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4427981) |
| #4486496 | 3 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4486496) |
| #4515056 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4515056) |
| #4515055 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4515055) |
| #4515054 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4515054) |
| #4515053 | 1 | Error: sql: database is closed | [View](https://glitchtip.devshift.net/ccx/issues/4515053) |

**Recommendation:** Consider merging into [#4127668](https://glitchtip.devshift.net/ccx/issues/4127668) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 3 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4523197 | 5 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4523197) |
| #4506735 | 1 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4506735) |
| #4367658 | 4 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4367658) |

**Recommendation:** Consider merging into [#4523197](https://glitchtip.devshift.net/ccx/issues/4523197) (highest event count)

---

## parquet-factory

**Duplicate Groups:** 1
**Issues in Groups:** 2
**Total Events:** 0

### 🟢 LOW: Error: unexpected status code 503 while pushing to https://pushgateway.app-sre.devshift.net/metrics…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4081087 | 181 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081087) |
| #4081088 | 138 | Error: unexpected status code 503 while pushing to https:... | [View](https://glitchtip.devshift.net/ccx/issues/4081088) |

**Recommendation:** Consider merging into [#4081087](https://glitchtip.devshift.net/ccx/issues/4081087) (highest event count)

---

## rules-processing

**Duplicate Groups:** 5
**Issues in Groups:** 123
**Total Events:** 0

### 🟢 LOW: AttributeError: 'str' object has no attribute 'parent'

**Issues:** 15 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #3781153 | 5,270 | AttributeError: 'NoneType' object has no attribute 'start... | [View](https://glitchtip.devshift.net/ccx/issues/3781153) |
| #3791585 | 4,000 | AttributeError: 'str' object has no attribute 'parent' | [View](https://glitchtip.devshift.net/ccx/issues/3791585) |
| #4520013 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520013) |
| #4520012 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520012) |
| #4520011 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520011) |
| #4520010 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520010) |
| #4520009 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520009) |
| #4520008 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520008) |
| #4520007 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520007) |
| #4520006 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520006) |
| #4520005 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520005) |
| #4520004 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520004) |
| #4520003 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520003) |
| #4520002 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520002) |
| #4520001 | 1 | AttributeError: 'NoneType' object has no attribute 'lower' | [View](https://glitchtip.devshift.net/ccx/issues/4520001) |

**Recommendation:** Consider merging into [#3781153](https://glitchtip.devshift.net/ccx/issues/3781153) (highest event count)

---

### 🟢 LOW: ParseException: ccx_ocp_core.parsers.insights_operator.core.PodsIO couldn't parse json.

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4319956 | 1,056 | ParseException: ccx_ocp_core.parsers.insights_operator.co... | [View](https://glitchtip.devshift.net/ccx/issues/4319956) |
| #4513669 | 1 | ParseException: ccx_ocp_core.parsers.insights_operator_hc... | [View](https://glitchtip.devshift.net/ccx/issues/4513669) |

**Recommendation:** Consider merging into [#4319956](https://glitchtip.devshift.net/ccx/issues/4319956) (highest event count)

---

### 🟢 LOW: FileExpired: [Errno 16] The remote file corresponding to filename rh-openshift-obs-prod-secure/arch…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4249305 | 102 | FileExpired: [Errno 16] The remote file corresponding to ... | [View](https://glitchtip.devshift.net/ccx/issues/4249305) |
| #4521056 | 7 | FileExpired: [Errno 16] The remote file corresponding to ... | [View](https://glitchtip.devshift.net/ccx/issues/4521056) |

**Recommendation:** Consider merging into [#4249305](https://glitchtip.devshift.net/ccx/issues/4249305) (highest event count)

---

### 🟢 LOW: InvalidArchive: Cannot detect execution context: No files in path: /tmp/insights-717cz68w

**Issues:** 100 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4519922 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519922) |
| #4519859 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519859) |
| #4519840 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519840) |
| #4519823 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519823) |
| #4519804 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519804) |
| #4519786 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519786) |
| #4519762 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519762) |
| #4519747 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519747) |
| #4519731 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519731) |
| #4519708 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519708) |
| #4519696 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519696) |
| #4519669 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519669) |
| #4519650 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519650) |
| #4519619 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519619) |
| #4519569 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519569) |
| #4519532 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519532) |
| #4519484 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519484) |
| #4519426 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519426) |
| #4519404 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519404) |
| #4519358 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519358) |
| #4519323 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519323) |
| #4519305 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519305) |
| #4519258 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519258) |
| #4519129 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519129) |
| #4519087 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519087) |
| #4519047 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4519047) |
| #4518994 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518994) |
| #4518967 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518967) |
| #4518948 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518948) |
| #4518933 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518933) |
| #4518919 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518919) |
| #4518902 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518902) |
| #4518892 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518892) |
| #4518883 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518883) |
| #4518864 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518864) |
| #4518809 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518809) |
| #4518784 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518784) |
| #4518757 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518757) |
| #4518729 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518729) |
| #4518707 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518707) |
| #4518671 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518671) |
| #4518650 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518650) |
| #4518619 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518619) |
| #4518592 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518592) |
| #4518481 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518481) |
| #4518451 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518451) |
| #4518410 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518410) |
| #4518354 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518354) |
| #4518309 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518309) |
| #4518262 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518262) |
| #4518224 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518224) |
| #4518198 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518198) |
| #4518184 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518184) |
| #4518157 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518157) |
| #4518145 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518145) |
| #4518127 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518127) |
| #4518119 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4518119) |
| #4517941 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517941) |
| #4517926 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517926) |
| #4517910 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517910) |
| #4517888 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517888) |
| #4517870 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517870) |
| #4517851 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517851) |
| #4517822 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517822) |
| #4517798 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517798) |
| #4517759 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517759) |
| #4517716 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517716) |
| #4517696 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517696) |
| #4517675 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517675) |
| #4517652 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517652) |
| #4517626 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517626) |
| #4517597 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517597) |
| #4517562 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517562) |
| #4517530 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517530) |
| #4517508 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517508) |
| #4517481 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517481) |
| #4517460 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517460) |
| #4517449 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517449) |
| #4517431 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517431) |
| #4517416 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517416) |
| #4517363 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517363) |
| #4517349 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517349) |
| #4517330 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517330) |
| #4517243 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517243) |
| #4517221 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517221) |
| #4517157 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517157) |
| #4517132 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517132) |
| #4517105 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517105) |
| #4517087 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517087) |
| #4517048 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4517048) |
| #4516984 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516984) |
| #4516911 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516911) |
| #4516886 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516886) |
| #4516859 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516859) |
| #4516806 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516806) |
| #4516770 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516770) |
| #4516704 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4516704) |
| #4508323 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4508323) |
| #4496236 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4496236) |
| #4486324 | 1 | InvalidArchive: Cannot detect execution context: No files... | [View](https://glitchtip.devshift.net/ccx/issues/4486324) |

**Recommendation:** Consider merging into [#4519922](https://glitchtip.devshift.net/ccx/issues/4519922) (highest event count)

---

### 🟢 LOW: Rule response make_fail(OPERATOR_ISSUE) exceeds the size limit of ... characters.

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4198802 | 159 | Rule response make_fail(OPERATOR_ISSUE) exceeds the size ... | [View](https://glitchtip.devshift.net/ccx/issues/4198802) |
| #4526281 | 4 | Rule response make_fail(CERTIFICATES_EXPIRING_SOON) excee... | [View](https://glitchtip.devshift.net/ccx/issues/4526281) |
| #4233800 | 373 | Rule response make_fail(MACHINE_POOL_NOT_OK) exceeds the ... | [View](https://glitchtip.devshift.net/ccx/issues/4233800) |
| #4509971 | 23 | Rule response make_fail(NODES_CONTAINER_RUNTIME_VERSION) ... | [View](https://glitchtip.devshift.net/ccx/issues/4509971) |

**Recommendation:** Consider merging into [#4198802](https://glitchtip.devshift.net/ccx/issues/4198802) (highest event count)

---

## valkey-writer

**Duplicate Groups:** 2
**Issues in Groups:** 6
**Total Events:** 0

### 🟢 LOW: Error: kafka server: Tried to send a message to a replica that is not the leader for some partition…

**Issues:** 2 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4129669 | 51 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129669) |
| #4129667 | 51 | Error: kafka server: Tried to send a message to a replica... | [View](https://glitchtip.devshift.net/ccx/issues/4129667) |

**Recommendation:** Consider merging into [#4129669](https://glitchtip.devshift.net/ccx/issues/4129669) (highest event count)

---

### 🟢 LOW: kafka: error while consuming ccx.ocp.results/0: EOF

**Issues:** 4 | **Total Events:** 0

| Issue ID | Events | Title | Link |
|----------|--------|-------|------|
| #4434850 | 13 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4434850) |
| #4523164 | 1 | kafka: error while consuming ccx.ocp.results/0: EOF | [View](https://glitchtip.devshift.net/ccx/issues/4523164) |
| #4506736 | 1 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4506736) |
| #4491661 | 1 | kafka: error while consuming ccx.ocp.results/0: dial tcp ... | [View](https://glitchtip.devshift.net/ccx/issues/4491661) |

**Recommendation:** Consider merging into [#4434850](https://glitchtip.devshift.net/ccx/issues/4434850) (highest event count)

---
