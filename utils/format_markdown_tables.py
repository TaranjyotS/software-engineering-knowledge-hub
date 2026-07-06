"""Format Markdown pipe tables in-place.

This utility scans Markdown files and aligns pipe-table columns so header,
separator dashes, and row cells line up consistently in VS Code/GitHub.

Examples:
    python utils/format_markdown_tables.py docs
    python utils/format_markdown_tables.py README.md docs --check
    python utils/format_markdown_tables.py docs --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Sequence

MARKDOWN_EXTENSIONS = {".md", ".markdown"}
IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
}

FENCE_RE = re.compile(r"^\s*(```|~~~)")


class MarkdownTableFormatterError(Exception):
    """Raised for expected CLI/input errors."""


def is_probable_pipe_row(line: str) -> bool:
    """Return True if a line looks like a Markdown pipe-table row."""
    stripped = line.strip()
    if not stripped or "|" not in stripped:
        return False

    # A table row needs at least two unescaped pipe separators.
    return len(split_markdown_row(stripped)) >= 2


def split_markdown_row(line: str) -> list[str]:
    """Split a Markdown pipe row on unescaped pipes.

    This intentionally handles common Markdown tables, including escaped pipes
    like ``\\|`` inside a cell. It does not attempt to parse every possible
    inline Markdown construct, but it is safe and idempotent for normal notes.
    """
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False

    for char in stripped:
        if char == "\\" and not escaped:
            current.append(char)
            escaped = True
            continue
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = False

    cells.append("".join(current).strip())
    return cells


def is_separator_cell(cell: str) -> bool:
    """Return True if a table separator cell is valid Markdown syntax."""
    normalized = cell.strip().replace(" ", "")
    return bool(re.fullmatch(r":?-{3,}:?", normalized))


def is_separator_row(line: str) -> bool:
    cells = split_markdown_row(line)
    return len(cells) >= 2 and all(is_separator_cell(cell) for cell in cells)


def get_alignment(separator_cell: str) -> str:
    """Return left, right, center, or default alignment from a separator cell."""
    normalized = separator_cell.strip().replace(" ", "")
    starts = normalized.startswith(":")
    ends = normalized.endswith(":")

    if starts and ends:
        return "center"
    if ends:
        return "right"
    if starts:
        return "left"
    return "default"


def pad_cells(cells: Sequence[str], count: int) -> list[str]:
    padded = list(cells)
    if len(padded) < count:
        padded.extend("" for _ in range(count - len(padded)))
    return padded[:count]


def align_text(text: str, width: int, alignment: str) -> str:
    if alignment == "right":
        return text.rjust(width)
    if alignment == "center":
        return text.center(width)
    return text.ljust(width)


def separator_text(width: int, alignment: str) -> str:
    width = max(width, 3)

    if alignment == "right":
        return "-" * (width - 1) + ":"
    if alignment == "center":
        if width < 4:
            width = 4
        return ":" + "-" * (width - 2) + ":"
    if alignment == "left":
        return ":" + "-" * (width - 1)
    return "-" * width


def format_row(cells: Sequence[str], widths: Sequence[int], alignments: Sequence[str]) -> str:
    formatted = [align_text(cell, widths[index], alignments[index]) for index, cell in enumerate(cells)]
    return "| " + " | ".join(formatted) + " |"


def format_separator(widths: Sequence[int], alignments: Sequence[str]) -> str:
    cells = [separator_text(widths[index], alignments[index]) for index in range(len(widths))]
    return "| " + " | ".join(cells) + " |"


def format_table_block(lines: Sequence[str]) -> list[str]:
    """Format a contiguous Markdown pipe-table block."""
    rows = [split_markdown_row(line) for line in lines]

    separator_index = next(
        (index for index, line in enumerate(lines) if is_separator_row(line)),
        None,
    )
    if separator_index is None or separator_index == 0:
        return list(lines)

    column_count = max(len(row) for row in rows)
    rows = [pad_cells(row, column_count) for row in rows]

    separator_cells = rows[separator_index]
    alignments = [get_alignment(cell) for cell in separator_cells]

    widths: list[int] = []
    for column in range(column_count):
        content_width = max(
            len(row[column])
            for index, row in enumerate(rows)
            if index != separator_index
        )
        widths.append(max(content_width, 3))

    formatted_lines: list[str] = []
    for index, row in enumerate(rows):
        if index == separator_index:
            formatted_lines.append(format_separator(widths, alignments))
        else:
            formatted_lines.append(format_row(row, widths, alignments))

    return formatted_lines


def find_table_end(lines: Sequence[str], start: int) -> int:
    """Return the first index after a contiguous table block."""
    end = start
    while end < len(lines) and is_probable_pipe_row(lines[end]):
        end += 1
    return end


def format_markdown_text(text: str) -> str:
    """Format all Markdown pipe tables outside fenced code blocks."""
    has_trailing_newline = text.endswith("\n")
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    in_fence = False

    while index < len(lines):
        line = lines[index]

        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            index += 1
            continue

        if (
            not in_fence
            and index + 1 < len(lines)
            and is_probable_pipe_row(lines[index])
            and is_separator_row(lines[index + 1])
        ):
            end = find_table_end(lines, index)
            output.extend(format_table_block(lines[index:end]))
            index = end
            continue

        output.append(line)
        index += 1

    formatted = "\n".join(output)
    if has_trailing_newline:
        formatted += "\n"
    return formatted


def iter_markdown_files(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if not path.exists():
            raise MarkdownTableFormatterError(f"Path does not exist: {path}")

        if path.is_file():
            if path.suffix.lower() in MARKDOWN_EXTENSIONS:
                yield path
            continue

        for child in sorted(path.rglob("*")):
            if child.is_dir():
                continue
            if any(part in IGNORED_DIRS for part in child.parts):
                continue
            if child.suffix.lower() in MARKDOWN_EXTENSIONS:
                yield child


def process_file(path: Path, *, check: bool, dry_run: bool, backup: bool) -> bool:
    original = path.read_text(encoding="utf-8", errors="ignore")
    formatted = format_markdown_text(original)

    if formatted == original:
        return False

    if not check and not dry_run:
        if backup:
            backup_path = path.with_suffix(path.suffix + ".bak")
            backup_path.write_text(original, encoding="utf-8")
        path.write_text(formatted, encoding="utf-8")

    return True


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Align Markdown pipe tables across Markdown files.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Markdown files or directories to scan recursively.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write files. Exit with code 1 if any file would change.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would change without writing them.",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create .bak files before writing changes.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = [Path(path).resolve() for path in args.paths]

    try:
        files = list(dict.fromkeys(iter_markdown_files(paths)))
    except MarkdownTableFormatterError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    changed: list[Path] = []
    for path in files:
        if process_file(path, check=args.check, dry_run=args.dry_run, backup=args.backup):
            changed.append(path)

    if changed:
        action = "would change" if args.check or args.dry_run else "formatted"
        for path in changed:
            print(f"{action}: {path}")
    else:
        print("All Markdown tables are already aligned.")

    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
