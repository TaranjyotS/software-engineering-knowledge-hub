# Confluence Sync Automation

This folder contains scripts for syncing Markdown notes in `docs/` with Confluence.

## Scripts

|           Script           |                                                     Purpose                                                      |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `health_check.py`          | Validates Confluence credentials and optional space access.                                                      |
| `build_page_map.py`        | Fetches existing Confluence pages, creates missing pages for every `docs/*.md` file, and writes `page_map.json`. |
| `push_to_confluence.py`    | Pushes one Markdown file to its mapped Confluence page, creating the page if needed.                             |
| `fetch_from_confluence.py` | Pulls pages from Confluence and writes them back into matching local Markdown files.                             |

## Required environment variables

Create a local `.env` file from `.env.example` or configure GitHub Secrets:

```env
CONFLUENCE_API_URL=https://your-domain.atlassian.net/wiki/rest/api
CONFLUENCE_USER=your-email@example.com
CONFLUENCE_TOKEN=your-api-token
CONFLUENCE_SPACE_KEY=YOURSPACE
CONFLUENCE_SPACE_NAME=Software Engineering Knowledge Hub
```

## Commands

```bash
python confluence_sync/health_check.py
python confluence_sync/build_page_map.py
python confluence_sync/push_to_confluence.py docs/python.md
python confluence_sync/fetch_from_confluence.py
```

## Notes

- `build_page_map.py`creates missing Confluence pages whenever new Markdown files are added under `docs/`.
- Markdown conversion enables tables and fenced code blocks through Python Markdown extensions.
