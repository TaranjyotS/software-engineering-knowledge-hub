<div align="center">

# 📚 Software Engineering Knowledge Hub

## A version-controlled software engineering, AI engineering, and interview preparation knowledge base with Confluence sync automation.

This repository keeps technical notes, coding questions, interview resources, downloadable PDFs, and documentation automation in one place. It is designed as a personal learning hub, recruiter-friendly portfolio resource, and docs-as-code workflow for keeping Markdown and Confluence aligned.

<br/>

<img src="https://img.shields.io/badge/Docs-Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" />
<img src="https://img.shields.io/badge/Python-Automation-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/GenAI-LLM%20%7C%20RAG%20%7C%20Agents-7B61FF?style=for-the-badge" />
<img src="https://img.shields.io/badge/Confluence-Sync-172B4D?style=for-the-badge&logo=confluence&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

</div>

---

## ✨ Overview

This project is a curated software engineering knowledge base built around practical interview preparation and engineering reference notes. It combines Markdown notes, coding practice, downloadable PDFs, and Confluence automation so the same content can be maintained locally, versioned on GitHub, and synchronized to a documentation workspace.

The repository now includes both traditional software engineering topics and updated AI engineering topics, including Python, REST APIs, SQL, system design, cloud/DevOps, testing, observability, GenAI, RAG, LLM evaluation, AI agents, data engineering, ML/MLOps, and behavioral interview preparation.

---

## 📌 What This Repository Covers

<div align="center">

|                 Area                  |                                   What You’ll Find                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------- |
| 🐍 Python                             | Core concepts, advanced Python, concurrency, decorators, generators, coding patterns  |
| 🧠 Coding Interviews                  | Progressive optimization, DSA patterns, complexity analysis, concurrency follow-ups   |
| 🌐 Backend APIs                       | REST, FastAPI, Flask, gRPC, GraphQL, validation, versioning, idempotency              |
| 🗄️ SQL & Databases                    | Joins, indexes, transactions, ORM, caching, query optimization, data modeling         |
| 🧱 System Design                      | Scalability, microservices, distributed systems, queues, consistency, caching         |
| 🤖 GenAI / LLMs                       | RAG, AI agents, prompt engineering, tool calling, hallucination reduction, evaluation |
| 📈 ML / MLOps                         | ML lifecycle, model validation, drift, model registry, deployment, monitoring         |
| 🔁 Data Engineering                   | ETL, batch/streaming, data quality, lineage, cloud data architecture                  |
| ☁️ Cloud / DevOps                     | AWS, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, CI/CD                    |
| 🧪 Testing / Security / Observability | Pytest, AI QA, API security, PII handling, logs, metrics, tracing, runbooks           |
| ⚛️ Frontend                           | React, TypeScript, API integration, product engineering basics                        |
| 📊 BI Tools                           | Excel, Power BI, Tableau analytics and interview notes                                |
| 🖥️ Unix                               | Commands, shell usage, permissions, process and file management                       |
| ☕ PDF Resources                      | Java, Spring Boot, Microservices, and REST API interview PDFs                         |

</div>

---

<details>
<summary><strong>📁 Folder Structure</strong></summary>

```text
software-engineering-knowledge-hub/
├── .github/workflows/              # GitHub Actions for Confluence sync
├── coding_questions/               # Runnable solutions and problem explanations
├── confluence_sync/                # Docs-as-code automation scripts
├── docs/                           # Markdown notes by topic
├── interview_questions/            # PDF interview resources
├── utils/                          # Helper utilities
├── .env.example                    # Safe environment variable template
├── .gitignore
├── requirements.txt
└── README.md
```

</details>

---

## 📂 Documentation Index

<div align="center">

|                Topic                 |                                       Link                                       |
| ------------------------------------ | -------------------------------------------------------------------------------- |
| My Profile                           | [docs/my_profile.md](docs/my_profile.md)                                         |
| Interview Questions                  | [docs/interview_questions.md](docs/interview_questions.md)                       |
| Coding Interview Patterns            | [docs/coding_interview_patterns.md](docs/coding_interview_patterns.md)           |
| Python                               | [docs/python.md](docs/python.md)                                                 |
| REST API / Backend APIs              | [docs/rest_api.md](docs/rest_api.md)                                             |
| SQL / Databases                      | [docs/sql.md](docs/sql.md)                                                       |
| System Design                        | [docs/system_design.md](docs/system_design.md)                                   |
| GenAI, LLMs, RAG & Agents            | [docs/genai_llm_rag.md](docs/genai_llm_rag.md)                                   |
| Machine Learning / MLOps             | [docs/machine_learning.md](docs/machine_learning.md)                             |
| Data Engineering                     | [docs/data_engineering.md](docs/data_engineering.md)                             |
| Cloud / DevOps / Docker / Kubernetes | [docs/cloud_devops.md](docs/cloud_devops.md)                                     |
| Testing / Security / Observability   | [docs/testing_security_observability.md](docs/testing_security_observability.md) |
| Frontend React / TypeScript          | [docs/frontend_react_typescript.md](docs/frontend_react_typescript.md)           |
| Excel                                | [docs/excel.md](docs/excel.md)                                                   |
| Power BI                             | [docs/power_bi.md](docs/power_bi.md)                                             |
| Tableau                              | [docs/tableau.md](docs/tableau.md)                                               |
| Unix                                 | [docs/unix.md](docs/unix.md)                                                     |
| Coding Practice                      | [coding_questions/README.md](coding_questions/README.md)                         |

</div>

---

## 💻 Coding Exercise Index

|              Exercise              |                       Runnable Source                        |
| ---------------------------------- | ------------------------------------------------------------ |
| Match statistics and head-to-head  | [Python](coding_questions/match_statistics.py)               |
| Priority inventory allocation      | [Python](coding_questions/inventory_bid_allocation.py)       |
| Top-k frequent paths               | [Python](coding_questions/top_k_frequent_paths.py)           |
| Issue creation workflow            | [Python](coding_questions/issue_creation_workflow.py)        |
| Transaction accounting and fees    | [Python](coding_questions/transaction_accounting.py)         |
| Incident alert routing and backoff | [Python](coding_questions/incident_alert_router.py)          |
| Weekly deployment windows          | [Python](coding_questions/weekly_deployment_windows.py)      |
| Duplicate merchant detection       | [Python](coding_questions/duplicate_merchant_detection.py)   |
| Commerce support tools             | [Python](coding_questions/commerce_support_tools.py)         |
| Safe agent orchestrator            | [Python](coding_questions/safe_agent_orchestrator.py)        |
| General Python coding practice     | [Python](coding_questions/python_coding_questions.py)        |
| Progressive algorithm patterns     | [Python](coding_questions/progressive_algorithm_patterns.py) |
| Concurrent data structures         | [Python](coding_questions/concurrent_data_structures.py)     |
| Expiring window map                | [Python](coding_questions/expiring_window_map.py)            |
| Object-oriented library management | [Python](coding_questions/library_management.py)             |
| General Java coding practice       | [Java](coding_questions/java_coding_questions.java)          |

> Coding-exercise documentation is intentionally kept inside the runnable source files as question and explanation blocks, so each exercise can be reviewed and executed from one file.

---

## 🔄 Confluence Documentation Automation

This repository includes a lightweight **Docs-as-Code** workflow for keeping Markdown notes and Confluence pages aligned.

```text
Markdown Docs
     │
     ▼
Confluence Sync Scripts
     │
     ▼
Confluence Knowledge Space
     │
     ▼
Versioned Engineering Notes
```

### Included automation scripts

|                   Script                   |                                          Purpose                                           |
| ------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `confluence_sync/health_check.py`          | Validates Confluence credentials and space access                                          |
| `confluence_sync/build_page_map.py`        | Builds or refreshes the local page mapping file and creates missing pages from `docs/*.md` |
| `confluence_sync/fetch_from_confluence.py` | Pulls pages from Confluence into matching Markdown files                                   |
| `confluence_sync/push_to_confluence.py`    | Pushes Markdown documentation back to Confluence                                           |
| `utils/generate_pdf_links.py`              | Regenerates PDF links for the README                                                       |
| `utils/generate_docs_index.py`             | Regenerates `docs/README.md` from the current `docs/*.md` files                            |
| `utils/format_markdown_tables.py`          | Centers table headers and aligns Markdown pipe tables across files or folders              |

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/TaranjyotS/software-engineering-knowledge-hub.git
cd software-engineering-knowledge-hub
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure local environment variables

```bash
cp .env.example .env
```

Then update `.env` with your own Confluence details.

> ⚠️ Never commit `.env` or real API tokens. Use GitHub Secrets for CI/CD.

---

## 🚀 Confluence Sync Workflow

### Validate credentials

```bash
python confluence_sync/health_check.py
```

### Build or refresh page mapping

```bash
python confluence_sync/build_page_map.py
```

### Format Markdown tables

```bash
python utils/format_markdown_tables.py README.md FILE_INDEX.md docs confluence_sync coding_questions
```

Check table alignment without writing files:

```bash
python utils/format_markdown_tables.py docs --check
```

### Push a Markdown file to Confluence

```bash
python confluence_sync/push_to_confluence.py docs/python.md
```

### Fetch Confluence pages into local Markdown

```bash
python confluence_sync/fetch_from_confluence.py
```

---

## 📥 Downloadable PDFs

The following interview resources/cheat sheets are included in the repository:

- [Java 1 Interview Questions](interview_questions/Java-1%20Interview%20Questions.pdf)
- [Java 2 Interview Questions](interview_questions/Java-2%20Interview%20Questions.pdf)
- [Microservices Interview Questions](interview_questions/Microservices%20Interview%20Questions.pdf)
- [Rest Api Interview Questions](interview_questions/REST%20API%20Interview%20Questions.pdf)
- [Spring Boot Interview Questions](interview_questions/Spring%20Boot%20Interview%20Questions.pdf)
- [Git Cheat Sheet](interview_questions/Git%20Cheat%20Sheet.pdf)
- [Python Cheat Sheet](interview_questions/Python%20Cheat%20Sheet.pdf)

---

## 📝 Helpful Reference Links

|                                           Resource                                           |             Use Case             |
| -------------------------------------------------------------------------------------------- | -------------------------------- |
| [QuickRef](https://quickref.me/)                                                             | Fast syntax references           |
| [Python Guides](https://pythonguides.com/python-interview-questions-and-answers/)            | Python interview preparation     |
| [InterviewBit](https://www.interviewbit.com/technical-interview-questions/)                  | Multi-topic interview prep       |
| [Baeldung Ops](https://www.baeldung.com/ops/)                                                | Docker, Kubernetes, Jenkins, Git |
| [Refactoring Guru](https://refactoring.guru/design-patterns)                                 | Design patterns                  |
| [Spring REST Guide](https://spring.io/guides/gs/rest-service)                                | Spring Boot REST services        |
| [System Design Reference](https://github.com/coding-parrot/system_design?tab=readme-ov-file) | Architecture and system design   |

---

## 🔐 Security Notes

This repository is intended to be safe for public GitHub use.

- Real `.env` files are ignored.
- `.env.example` is included as a safe template.
- API tokens should be stored in GitHub Secrets.

---

## 🤝 Contribution Ideas

Contributions can improve the repository by adding:

- More coding questions with explanations
- System design diagrams
- SQL query examples
- Cloud and DevOps notes
- Interview checklists
- Cleaner topic summaries
- Additional Confluence automation improvements

---

## 🎯 Project Purpose

This project is not meant to be a complex production application. Its value is in being a practical, searchable, version-controlled engineering knowledge base that supports interview preparation, documentation habits, and reusable learning resources.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## ⚠️ Disclaimer

This repository is maintained as a personal learning and interview preparation knowledge base. The notes, examples, and explanations are intended for educational purposes only and may evolve over time as new concepts, tools, and best practices are learned.

Some content may be summarized from personal study, documentation, practice problems, and interview preparation resources. Users are encouraged to verify technical details from official documentation when applying them in production or interview settings.
