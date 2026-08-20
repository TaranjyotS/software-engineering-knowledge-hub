# Coding Questions

This folder contains runnable, interview-focused coding exercises. Compact
questions remain self-contained in one source file. Larger exercises live under
`application_projects/` with separate configuration, API, domain, data-access,
data, and test files.

## Runnable Exercises

|              Exercise               |                 File                  |                              Main Skills                              |
| ----------------------------------- | ------------------------------------- | --------------------------------------------------------------------- |
| Match statistics and head-to-head   | `match_statistics.py`                 | Aggregation, enums, validation, mirrored records                      |
| Priority inventory allocation       | `inventory_bid_allocation.py`         | Sorting, grouped scans, round-robin reasoning                         |
| Top-k frequent paths                | `top_k_frequent_paths.py`             | Frequency maps, heaps, dynamic k, streaming                           |
| Issue creation workflow             | `issue_creation_workflow.py`          | API debugging, persistence, auth, identifiers                         |
| Transaction accounting and fees     | `transaction_accounting.py`           | Dictionaries, sorting, business rules                                 |
| Incident alert routing and backoff  | `incident_alert_router.py`            | Debugging, state, adjacent-pair checks                                |
| Weekly deployment windows           | `weekly_deployment_windows.py`        | Interval processing, boundary handling                                |
| Duplicate merchant detection        | `duplicate_merchant_detection.py`     | Matching, confidence thresholds                                       |
| Commerce support tools              | `commerce_support_tools.py`           | SQLite, refund rules, CLI parsing, tool schemas                       |
| Safe agent orchestrator             | `safe_agent_orchestrator.py`          | Agent loops, guardrails, caching, revalidation                        |
| General Python coding practice      | `python_coding_questions.py`          | General Python coding patterns                                        |
| Progressive algorithm patterns      | `progressive_algorithm_patterns.py`   | Hash maps, windows, heaps, graphs, progressive optimization           |
| Core array, stack & matrix patterns | `core_array_stack_matrix_patterns.py` | Two Sum, stock scan, RPN, matrix rotation, windows, monotonic stack   |
| Concurrent data structures          | `concurrent_data_structures.py`       | LRU, TTL map, blocking queue, rate limiting, locks                    |
| Expiring window map                 | `expiring_window_map.py`              | Lazy expiration, running average, deque, overwrite safety             |
| Kubernetes job reconciliation       | `kubernetes_job_reconciliation.py`    | Value identity, set differences, dependency injection, reconciliation |
| Object-oriented library management  | `library_management.py`               | Classes, state, object-oriented modeling                              |
| General Java coding practice        | `java_coding_questions.java`          | Java coding patterns                                                  |

## Complete Application Projects

|            Project            |                                           Location                                           |                              Main Skills                              |
| ----------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Flask user CRUD application   | [`application_projects/flask_user_crud_app/`](application_projects/flask_user_crud_app/)     | Flask factories, validation, SQLite repositories, HTTP tests          |
| Hotel reservation application | [`application_projects/hotel_reservation_app/`](application_projects/hotel_reservation_app/) | CSV/JSON loading, interval boundaries, sweep-line demand, Flask tests |
| FastAPI task API              | [`application_projects/fastapi_task_api/`](application_projects/fastapi_task_api/)           | FastAPI, Pydantic, SQLAlchemy, dependency injection, Docker           |

## Suggested Workflow

1. Open the runnable source file or application README and read the problem statement.
2. Explain the approach out loud before reading the implementation.
3. Reimplement or modify the solution yourself.
4. Add edge cases and discuss time and space complexity.
5. Run the included sample tests. Application projects have isolated setup and
   test commands in their READMEs.

For broader topic explanations, use the Markdown notes in `docs/`.
