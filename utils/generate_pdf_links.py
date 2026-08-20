from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = REPO_ROOT / "interview_questions"
README_FILE = REPO_ROOT / "README.md"
SECTION_HEADER = "## 📥 Downloadable PDFs"
GITHUB_REPO_RAW = (
    "https://github.com/YOUR_USERNAME/software-engineering-knowledge-hub/raw/main/"
    "interview_questions"
)


def _title_from_pdf(file_name: str) -> str:
    words = Path(file_name).stem.replace("_", " ").replace("-", " ").split()
    acronyms = {"ai": "AI", "api": "API", "qa": "QA", "rest": "REST"}
    return " ".join(acronyms.get(word.lower(), word.title()) for word in words)


def generate_pdf_section(use_relative_links: bool = True) -> str:
    """Generate the README PDF section from PDFs in interview_questions/."""
    pdf_files = sorted(path.name for path in PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        return ""

    lines = [
        SECTION_HEADER,
        "",
        "The following interview resources are included in the repository:",
        "",
    ]
    for file_name in pdf_files:
        title = _title_from_pdf(file_name)
        if use_relative_links:
            url = f"interview_questions/{quote(file_name)}"
        else:
            url = f"{GITHUB_REPO_RAW}/{quote(file_name)}"
        lines.append(f"- [{title}]({url})")

    return "\n".join(lines)


def update_readme() -> None:
    if not README_FILE.exists():
        raise FileNotFoundError(f"README.md not found at {README_FILE}")

    content = README_FILE.read_text(encoding="utf-8")
    new_section = generate_pdf_section(use_relative_links=True)
    if not new_section:
        print("No PDF files found. Skipping update.")
        return

    pattern = re.compile(rf"{re.escape(SECTION_HEADER)}.*?(?=\n---\n\n## |\n## |\Z)", re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_section + "\n", content)
    else:
        content = content.rstrip() + "\n\n---\n\n" + new_section

    README_FILE.write_text(content.rstrip() + "\n", encoding="utf-8")
    print("README.md updated with PDF links.")


if __name__ == "__main__":
    update_readme()
