from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from utils.format_markdown_tables import format_markdown_text

DOCS_DIR = REPO_ROOT / "docs"
DOCS_README = DOCS_DIR / "README.md"

TOPIC_FOCUS = {
    "my_profile.md": "Resume-aligned profile, experience, positioning, and knowledge summary",
    "interview_questions.md": "Behavioral, HR, resume-based, and general interview questions",
    "python.md": "Core Python, advanced Python, concurrency, OOP, coding patterns",
    "rest_api.md": "REST, FastAPI, Flask, API contracts, security, pagination, idempotency",
    "sql.md": "SQL fundamentals, joins, indexes, transactions, window functions, optimization",
    "system_design.md": "Scalability, microservices, distributed systems, queues, caching, consistency",
    "genai_llm_rag.md": "LLMs, prompt engineering, RAG, AI agents, tool calling, evaluation",
    "machine_learning.md": "ML fundamentals, model lifecycle, validation, drift, deployment, monitoring",
    "data_engineering.md": "ETL, data quality, batch/streaming, S3 pipelines, lineage, lakehouse concepts",
    "cloud_devops.md": "AWS, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, CI/CD",
    "testing_security_observability.md": "Pytest, AI QA, API security, PII, logs, metrics, tracing, reliability",
    "frontend_react_typescript.md": "React, hooks, TypeScript, API integration, product engineering",
    "excel.md": "Excel formulas, pivot tables, lookups, conditional formatting",
    "power_bi.md": "DAX, relationships, slicers, RLS, dashboard concepts",
    "tableau.md": "Calculated fields, parameters, dual-axis charts, dashboard optimization",
    "unix.md": "Common shell commands, files, permissions, processes, networking",
}

ORDER = list(TOPIC_FOCUS)


def title_from_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").title()


def generate() -> str:
    rows = []
    seen = set()
    for file_name in ORDER:
        path = DOCS_DIR / file_name
        if path.exists():
            rows.append((title_from_file(path), file_name, TOPIC_FOCUS[file_name]))
            seen.add(file_name)

    for path in sorted(DOCS_DIR.glob("*.md")):
        if path.name == "README.md" or path.name in seen:
            continue
        rows.append((title_from_file(path), path.name, "Additional engineering note"))

    table = "\n".join(f"| {title} | `{file_name}` | {focus} |" for title, file_name, focus in rows)

    return f"""# Documentation Index

This folder contains topic-wise notes used for technical interview preparation and engineering reference.

| Topic | File | Focus |
|-------|------|-------|
{table}

---

## Recommended structure for future notes

```md
# Topic

> **Purpose:** What this note is for.
> **Best for:** Interviews, revision, project reference, or implementation.

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
"""


def main() -> None:
    DOCS_README.write_text(format_markdown_text(generate()), encoding="utf-8")
    print(f"Updated {DOCS_README}")


if __name__ == "__main__":
    main()
