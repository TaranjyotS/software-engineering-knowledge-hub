from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

import requests
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()

CONFLUENCE_API_URL = os.getenv("CONFLUENCE_API_URL", "").rstrip("/")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER", "")
CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN", "")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
MARKDOWN_EXTENSIONS = ["extra", "tables", "fenced_code", "toc", "sane_lists"]

REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_MAP_PATH = REPO_ROOT / "confluence_sync" / "page_map.json"


def _auth() -> Tuple[str, str]:
    if not (CONFLUENCE_API_URL and CONFLUENCE_USER and CONFLUENCE_TOKEN):
        raise RuntimeError(
            "Missing Confluence environment variables. "
            "Please set CONFLUENCE_API_URL, CONFLUENCE_USER, CONFLUENCE_TOKEN."
        )
    return CONFLUENCE_USER, CONFLUENCE_TOKEN


def _request(method: str, url: str, **kwargs) -> requests.Response:
    res = requests.request(method, url, auth=_auth(), timeout=60, **kwargs)
    if res.status_code in (401, 403):
        raise RuntimeError(
            f"Confluence API auth failed ({res.status_code}). "
            "Your token may be expired/revoked or lacks permissions."
        )
    res.raise_for_status()
    return res


def load_page_map() -> Dict[str, str]:
    if not PAGE_MAP_PATH.exists():
        return {}
    try:
        return json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8") or "{}")
    except Exception:
        return {}


def save_page_map(mapping: Dict[str, str]) -> None:
    PAGE_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAGE_MAP_PATH.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")


def fetch_personal_space_key() -> str:
    url = f"{CONFLUENCE_API_URL}/space"
    res = _request("GET", url)
    data = res.json()
    for space in data.get("results", []):
        if space.get("type") == "personal":
            return space["key"]
    raise RuntimeError("Personal space key not found. Set CONFLUENCE_SPACE_KEY explicitly.")


def get_target_space_key() -> str:
    return CONFLUENCE_SPACE_KEY or fetch_personal_space_key()


def get_page_version(page_id: str) -> int:
    res = _request("GET", f"{CONFLUENCE_API_URL}/content/{page_id}?expand=version")
    return res.json()["version"]["number"]


def create_page(space_key: str, title: str, html_body: str) -> str:
    url = f"{CONFLUENCE_API_URL}/content"
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {"storage": {"value": html_body, "representation": "storage"}},
    }
    res = _request("POST", url, json=payload, headers={"Content-Type": "application/json"})
    return res.json()["id"]


def update_page(page_id: str, title: str, html_body: str) -> None:
    version = get_page_version(page_id)
    payload = {
        "version": {"number": version + 1},
        "title": title,
        "type": "page",
        "body": {"storage": {"value": html_body, "representation": "storage"}},
    }
    _request(
        "PUT",
        f"{CONFLUENCE_API_URL}/content/{page_id}",
        json=payload,
        headers={"Content-Type": "application/json"},
    )


def title_from_markdown(md_text: str, md_file: Path) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_file.stem.replace("_", " ").replace("-", " ").title()


def ensure_page_id(mapping: Dict[str, str], title: str, html_body: str) -> str:
    page_id = mapping.get(title)
    if page_id:
        return page_id

    for existing_title, existing_id in mapping.items():
        if existing_title.strip().lower() == title.strip().lower():
            return existing_id

    space_key = get_target_space_key()
    created_id = create_page(space_key, title, html_body)
    mapping[title] = created_id
    save_page_map(mapping)
    print(f"Created missing page '{title}' and updated page_map.json")
    return created_id


def update_confluence_page_from_md(md_path: str) -> None:
    md_file = Path(md_path)
    if not md_file.is_absolute():
        md_file = REPO_ROOT / md_file
    if not md_file.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    md_text = md_file.read_text(encoding="utf-8")
    title = title_from_markdown(md_text, md_file)
    html_body = markdown(md_text, extensions=MARKDOWN_EXTENSIONS)

    mapping = load_page_map()
    page_id = ensure_page_id(mapping, title, html_body)

    update_page(page_id, title, html_body)
    print(f"Synced '{title}' successfully")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python confluence_sync/push_to_confluence.py <path_to_md_file>")
    update_confluence_page_from_md(sys.argv[1])
