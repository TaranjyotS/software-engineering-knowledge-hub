<div align="center">

# 📚 Software Engineering Knowledge Hub

### A version-controlled interview preparation and engineering notes repository with Confluence sync automation.

This repository keeps technical notes, coding questions, interview resources, and documentation workflows in one place. It is designed to stay useful as a personal study hub while also being clean enough for other developers, learners, and recruiters to understand quickly.

<br/>

<img src="https://img.shields.io/badge/Docs-Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white" />
<img src="https://img.shields.io/badge/Python-Automation-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Confluence-Sync-172B4D?style=for-the-badge&logo=confluence&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />

</div>

---

## ✨ Overview

This project is a curated software engineering knowledge base built around practical interview preparation. It combines Markdown notes, coding practice, downloadable PDFs, and Confluence automation so the same content can be maintained locally, versioned on GitHub, and synchronized to a documentation workspace.

The original purpose is preserved: **keep notes handy and help others prepare**. The repository is now organized to look more polished, easier to navigate, and more portfolio-friendly.

---

## 📌 What This Repository Covers

<div align="center">

|               Area               |                     What You’ll Find                         |
|----------------------------------|--------------------------------------------------------------|
| 🐍 Python                        | Core concepts, examples, coding questions, interview notes   |
| 🗄️ SQL                           | Query patterns, joins, optimization concepts, interview prep |
| 🧱 System Design                 | Architecture fundamentals, scalability, design trade-offs    |
| 🌐 REST APIs                     | HTTP, endpoints, contracts, authentication, backend concepts |
| 🖥️ Unix                          | Common commands, shell usage, developer productivity notes   |
| 📊 Excel / Tableau / Power BI    | Analytics, reporting, dashboards, BI concepts                |
| 🤖 Machine Learning              | ML fundamentals and interview-oriented summaries             |
| ☕ Java / Spring / Microservices | Downloadable PDFs and related interview resources            |

</div>

---

<details>
<summary><strong>📁 Folder Structure</strong></summary>

```text
software-engineering-knowledge-hub/
├── .github/workflows/              # GitHub Actions for Confluence sync
├── coding_questions/               # Python and Java practice examples
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

|        Topic        |                             Link                           |
|---------------------|------------------------------------------------------------|
| Excel               | [docs/excel.md](docs/excel.md)                             |
| Interview Questions | [docs/interview_questions.md](docs/interview_questions.md) |
| Machine Learning    | [docs/machine_learning.md](docs/machine_learning.md)       |
| My Profile          | [docs/my_profile.md](docs/my_profile.md)                   |
| Power BI            | [docs/power_bi.md](docs/power_bi.md)                       |
| Python              | [docs/python.md](docs/python.md)                           |
| REST API            | [docs/rest_api.md](docs/rest_api.md)                       |
| SQL                 | [docs/sql.md](docs/sql.md)                                 |
| System Design       | [docs/system_design.md](docs/system_design.md)             |
| Tableau             | [docs/tableau.md](docs/tableau.md)                         |
| Unix                | [docs/unix.md](docs/unix.md)                               |

</div>

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

|                  Script                    |                     Purpose                       |
|--------------------------------------------|---------------------------------------------------|
| `confluence_sync/health_check.py`          | Validates Confluence credentials and space access |
| `confluence_sync/build_page_map.py`        | Builds or refreshes the local page mapping file   |
| `confluence_sync/fetch_from_confluence.py` | Pulls pages from Confluence into Markdown         |
| `confluence_sync/push_to_confluence.py`    | Pushes Markdown documentation back to Confluence  |
| `utils/generate_pdf_links.py`              | Regenerates PDF links for the README              |

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/TaranjyotS/interview-prep.git
cd interview-prep
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

The following interview resources are included in the repository:

- [Java-1 Interview Questions](interview_questions/Java-1%20Interview%20Questions.pdf)
- [Java-2 Interview Questions](interview_questions/Java-2%20Interview%20Questions.pdf)
- [Microservices Interview Questions](interview_questions/Microservices%20Interview%20Questions.pdf)
- [REST API Interview Questions](interview_questions/REST%20API%20Interview%20Questions.pdf)
- [Spring Boot Interview Questions](interview_questions/Spring%20Boot%20Interview%20Questions.pdf)

---

## 📝 Helpful Reference Links

|                                     Resource                                                 |             Use Case             |
|----------------------------------------------------------------------------------------------|----------------------------------|
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
- The original uploaded ZIP contained a local `.env` file and `.git/` directory; both were removed from this revised version.

If a real Confluence token was ever committed or shared publicly, revoke it and generate a new one.

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
