from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()

import json
import os
import re
from pathlib import Path
from typing import Dict, Tuple

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

CONFLUENCE_API_URL = os.getenv("CONFLUENCE_API_URL", "").rstrip("/")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER", "")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN", "")

IGNORED_TITLES = {"overview", "getting started in confluence"}

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "docs"
PAGE_MAP_PATH = REPO_ROOT / "confluence_sync" / "page_map.json"
OUT_DIR.mkdir(exist_ok=True)


def _auth() -> Tuple[str, str]:
    if not (CONFLUENCE_API_URL and CONFLUENCE_USER and CONFLUENCE_TOKEN):
        raise RuntimeError(
            "Missing Confluence environment variables. "
            "Please set CONFLUENCE_API_URL, CONFLUENCE_USER, CONFLUENCE_TOKEN."
        )
    return CONFLUENCE_USER, CONFLUENCE_TOKEN


def slugify_title(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    return slug.strip("_") or "untitled"


def local_title_to_filename() -> Dict[str, str]:
    """Use existing docs H1 titles so Confluence fetches update the intended file."""
    mapping: Dict[str, str] = {}
    for md_file in OUT_DIR.glob("*.md"):
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        first_h1 = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), None)
        if first_h1:
            mapping[first_h1.strip().lower()] = md_file.name
    return mapping


def get_page_html(page_id: str) -> Tuple[str, str]:
    url = f"{CONFLUENCE_API_URL}/content/{page_id}?expand=body.storage,title"
    res = requests.get(url, auth=_auth(), timeout=60)
    if res.status_code in (401, 403):
        raise RuntimeError("Confluence authentication failed. Check token/user permissions.")
    res.raise_for_status()
    data = res.json()
    return data["title"], data["body"]["storage"]["value"]


def convert_html_to_md(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for macro in soup.find_all("ac:structured-macro"):
        macro.decompose()
    return md(str(soup), heading_style="ATX")


def export_all() -> None:
    if not PAGE_MAP_PATH.exists():
        raise FileNotFoundError("page_map.json not found. Run build_page_map.py first.")

    page_map = json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8") or "{}")
    title_file_map = local_title_to_filename()

    for title, page_id in page_map.items():
        if title.strip().lower() in IGNORED_TITLES:
            print(f"Skipping ignored page: {title}")
            continue
        try:
            clean_title, html = get_page_html(page_id)
            markdown = convert_html_to_md(html).strip()
            file_name = title_file_map.get(clean_title.strip().lower()) or title_file_map.get(title.strip().lower())
            if not file_name:
                file_name = f"{slugify_title(clean_title or title)}.md"

            (OUT_DIR / file_name).write_text(f"# {clean_title}\n\n{markdown}\n", encoding="utf-8")
            print(f"Exported: {file_name}")
        except Exception as e:
            print(f"Failed: {title} - {e}")


if __name__ == "__main__":
    export_all()
