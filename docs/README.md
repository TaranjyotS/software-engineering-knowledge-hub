# Documentation Index

> **Purpose:** Provide a topic-wise index of the repository documentation.
> **Use this file for:** locating technical interview notes and engineering reference material under `docs/`.

---

|                                 Topic                                 |                File                 |                                       Focus                                       |
| --------------------------------------------------------------------- | ----------------------------------- | --------------------------------------------------------------------------------- |
| My Profile                                                            | `my_profile.md`                     | Resume-aligned profile, experience, positioning, and knowledge summary            |
| Interview Questions                                                   | `interview_questions.md`            | Behavioral, HR, resume-based, senior engineering, and general interview questions |
| Coding Interview Patterns, Data Structures & Progressive Optimization | `coding_interview_patterns.md`      | Progressive coding interviews, DSA patterns, complexity, testing, optimization    |
| Python                                                                | `python.md`                         | Core Python, advanced Python, concurrency, OOP, coding patterns                   |
| REST API & Backend APIs                                               | `rest_api.md`                       | REST, FastAPI, Flask, API contracts, security, pagination, idempotency            |
| SQL, Databases, ORM, Caching & Idempotency                            | `sql.md`                            | SQL fundamentals, joins, indexes, transactions, window functions, optimization    |
| System Design, Microservices & Distributed Systems                    | `system_design.md`                  | Scalability, microservices, distributed systems, queues, caching, consistency     |
| GenAI, LLMs, Prompting, Agents, RAG & Evaluation                      | `genai_llm_rag.md`                  | LLMs, prompt engineering, RAG, AI agents, tool calling, evaluation                |
| Machine Learning, Deep Learning, Modeling & Validation                | `machine_learning.md`               | ML fundamentals, model lifecycle, validation, drift, deployment, monitoring       |
| Data Engineering, ETL, Big Data & Analytics                           | `data_engineering.md`               | ETL, data quality, batch/streaming, S3 pipelines, lineage, lakehouse concepts     |
| Cloud, DevOps, Docker, Kubernetes & CI/CD                             | `cloud_devops.md`                   | AWS, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, CI/CD                |
| Testing, QA, Security, Observability & Reliability                    | `testing_security_observability.md` | Pytest, AI QA, API security, PII, logs, metrics, tracing, reliability             |
| Frontend, React, TypeScript & Product Engineering                     | `frontend_react_typescript.md`      | React, hooks, TypeScript, API integration, product engineering                    |
| Excel                                                                 | `excel.md`                          | Excel formulas, pivot tables, lookups, conditional formatting                     |
| Power BI                                                              | `power_bi.md`                       | DAX, relationships, slicers, RLS, dashboard concepts                              |
| Tableau                                                               | `tableau.md`                        | Calculated fields, parameters, dual-axis charts, dashboard optimization           |
| Unix                                                                  | `unix.md`                           | Common shell commands, files, permissions, processes, networking                  |

---

## Recommended structure for future notes

```md
# Topic

> **Purpose:** What this note is for.
> **Use this file for:** Interviews, revision, project reference, or implementation.

---

## Quick Summary

## Key Concepts

## Interview Questions

## Practical Examples

## Common Mistakes

## Quick Revision Checklist
```

---

## Maintenance Notes

- Keep one topic per Markdown file.
- Prefer reusable interview answers over company-specific content.
- Add code snippets when they clarify implementation.
- Keep personal profile details aligned with the latest resume.
- When adding a new file under `docs/`, run `python confluence_sync/build_page_map.py` before syncing to Confluence.
