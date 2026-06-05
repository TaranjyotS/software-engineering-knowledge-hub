# Confluence Sync

This folder contains scripts for synchronizing Markdown documentation with Confluence.

## Scripts

|           Script           |                        Purpose                          |
|----------------------------|---------------------------------------------------------|
| `health_check.py`          | Checks Confluence credentials and space access          |
| `build_page_map.py`        | Builds or refreshes the Markdown-to-Confluence page map |
| `fetch_from_confluence.py` | Fetches Confluence pages into local Markdown files      |
| `push_to_confluence.py`    | Pushes a local Markdown file to Confluence              |
| `page_map.json`            | Stores local file to Confluence page ID mapping         |

## Environment variables

Create a local `.env` file from `.env.example` at the repository root.

```bash
cp .env.example .env
```

Required variables:

```bash
CONFLUENCE_API_URL=https://your-domain.atlassian.net/wiki/rest/api
CONFLUENCE_USER=your-email@example.com
CONFLUENCE_TOKEN=your-token
```

Optional variables:

```bash
CONFLUENCE_SPACE_KEY=INTPREP
CONFLUENCE_SPACE_NAME=Interview Prep
```
