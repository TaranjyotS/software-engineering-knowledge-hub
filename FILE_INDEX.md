# Software Engineering Knowledge Hub

This repository contains topic-wise notes for software engineering, backend development, AI engineering, data, DevOps, and interview preparation.

---

## Repository Map

|             Category             |                   File                   |                                         What It Covers                                          |
| -------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Professional Profile Guide       | `docs/my_profile.md`                     | Generic positioning, evidence inventory, project explanation, and privacy guidance              |
| Behavioral Interview Playbook    | `docs/interview_questions.md`            | Company-neutral behavioral answers, STAR stories, and interview delivery                        |
| Project Deep-Dive Guide          | `docs/project_deep_dive.md`              | Backend, data, AI, CI/CD, security, compatibility, and production scenarios                     |
| Coding Interview Patterns        | `docs/coding_interview_patterns.md`      | Progressive algorithms, complexity reasoning, DSA patterns, testing, follow-up constraints      |
| Python                           | `docs/python.md`                         | OOP, data structures, decorators, generators, context managers, metaclasses, coding patterns    |
| REST / Backend APIs              | `docs/rest_api.md`                       | REST, FastAPI, Flask, API design, validation, production-style AI-enabled backend architecture  |
| SQL / Databases                  | `docs/sql.md`                            | SQL basics, joins, window functions, ORM, transactions, caching, idempotency, consistency       |
| System Design                    | `docs/system_design.md`                  | Scalability, microservices, queues, distributed systems, AI-enabled versus agentic architecture |
| Software Design Patterns         | `docs/software_design_patterns.md`       | GoF patterns, modern backend patterns, Python examples, LLD selection and trade-offs            |
| GenAI / LLMs                     | `docs/genai_llm_rag.md`                  | LLMs, prompt engineering, RAG, agents, tool calling, evaluation, AI product engineering         |
| Machine Learning                 | `docs/machine_learning.md`               | ML fundamentals, model building, validation, deep learning, PyTorch, TensorFlow, MLOps          |
| Data Engineering                 | `docs/data_engineering.md`               | ETL, data quality, batch/streaming, data lineage, S3/lakehouse, PySpark, analytics pipelines    |
| Cloud / DevOps                   | `docs/cloud_devops.md`                   | AWS, Docker, Kubernetes, Terraform, Jenkins, GitHub Actions, CI/CD, deployment patterns         |
| Testing / Security / Reliability | `docs/testing_security_observability.md` | Pytest, QA, security, observability, incidents, alert routing, runbooks, reliability            |
| Frontend / Product               | `docs/frontend_react_typescript.md`      | React, TypeScript, API integration, full-stack and product engineering concepts                 |
| Excel                            | `docs/excel.md`                          | Excel formulas, lookups, pivot tables, conditional formatting, analysis interview questions     |
| Power BI                         | `docs/power_bi.md`                       | DAX, slicers, filters, relationships, RLS, dashboard performance                                |
| Tableau                          | `docs/tableau.md`                        | Calculated fields, parameters, dual-axis charts, filters, dashboard optimization                |
| Unix                             | `docs/unix.md`                           | Linux/Unix commands, permissions, text processing, process/networking commands                  |

## Owner-Specific Material

|              File              |                          Purpose                          |
| ------------------------------ | --------------------------------------------------------- |
| `owner/my_profile.md`          | Anonymized resume-aligned profile and personal story bank |
| `owner/interview_questions.md` | Anonymized tailored answers and dated company research    |
| `owner/README.md`              | Privacy boundary and safe-tailoring guidance              |

---

## Generated Interview PDFs

|                                File                                |                 Source Scope                  |
| ------------------------------------------------------------------ | --------------------------------------------- |
| `interview_questions/Behavioral_Interview_Playbook.pdf`            | Generic behavioral question bank              |
| `interview_questions/Backend_Data_AI_Project_Deep_Dive.pdf`        | Backend, data, AI, and production scenarios   |
| `interview_questions/Software_Design_Patterns_Interview_Guide.pdf` | Generic design-pattern guide                  |
| `interview_questions/Python_Backend_AI_Interview_Master_Guide.pdf` | Combined public interview-preparation sources |

The PDFs are reproducible with `python utils/build_interview_pdfs.py`; the
generator rejects known personal and company-specific terms before publishing.

---

## Repository Quality Tools

|              File               |                  Purpose                   |
| ------------------------------- | ------------------------------------------ |
| `pyproject.toml`                | Ruff lint and format policy                |
| `.pymarkdown`                   | PyMarkdown lint policy                     |
| `.markdownlint.jsonc`           | VS Code and markdownlint policy            |
| `requirements-dev.txt`          | Reproducible lint-tool versions            |
| `utils/build_interview_pdfs.py` | Generic PDF generation with privacy checks |

---

## Coding Exercise Map

|              Exercise               |                          File                          |                               What It Covers                                |
| ----------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------- |
| Match statistics and head-to-head   | `coding_questions/match_statistics.py`                 | Aggregation, validation, mirrored match records                             |
| Priority inventory allocation       | `coding_questions/inventory_bid_allocation.py`         | Priority groups, round-robin allocation, complexity                         |
| Top-k frequent paths                | `coding_questions/top_k_frequent_paths.py`             | Heaps, frequency ranking, dynamic-k and streaming                           |
| Issue creation workflow             | `coding_questions/issue_creation_workflow.py`          | Create-endpoint debugging, auth, nested persistence                         |
| Transaction accounting and fees     | `coding_questions/transaction_accounting.py`           | Balances, grouped averages, chronological fee rules                         |
| Incident alert routing and backoff  | `coding_questions/incident_alert_router.py`            | Open-alert debugging, attempt state, retry cooldown                         |
| Weekly deployment windows           | `coding_questions/weekly_deployment_windows.py`        | Weekly interval and boundary processing                                     |
| Duplicate merchant detection        | `coding_questions/duplicate_merchant_detection.py`     | Merchant matching and confidence thresholds                                 |
| Commerce support tools              | `coding_questions/commerce_support_tools.py`           | SQLite tools, refund rules, CLI parsing, schemas                            |
| Safe agent orchestrator             | `coding_questions/safe_agent_orchestrator.py`          | Bounded agent loop, cache, guardrails, revalidation                         |
| General Python coding practice      | `coding_questions/python_coding_questions.py`          | General Python coding patterns                                              |
| Progressive algorithm patterns      | `coding_questions/progressive_algorithm_patterns.py`   | Hash maps, windows, heaps, graphs, k-way merge                              |
| Core array, stack & matrix patterns | `coding_questions/core_array_stack_matrix_patterns.py` | Two Sum, stock scan, RPN, matrix rotation, sliding windows, monotonic stack |
| Concurrent data structures          | `coding_questions/concurrent_data_structures.py`       | LRU, TTL map, blocking queue, rate limiting, locks                          |
| Expiring window map                 | `coding_questions/expiring_window_map.py`              | Lazy expiration, O(1) average, overwrite-safe cleanup                       |
| Library management                  | `coding_questions/library_management.py`               | Object-oriented modeling                                                    |
| General Java coding practice        | `coding_questions/java_coding_questions.java`          | General Java coding patterns                                                |
