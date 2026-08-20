"""Normalize Markdown headings and format pipe tables in-place.

This utility scans Markdown files, centers header labels in the source and aligns separator dashes and row cells consistently in VS Code/GitHub.

Examples:
    python utils/format_markdown_tables.py docs
    python utils/format_markdown_tables.py README.md docs --check
    python utils/format_markdown_tables.py docs --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
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
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:\s+|$)")


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


def _codepoint_width(char: str) -> int:
    """Return an approximate terminal/editor cell width for one code point.

    Markdown tables in this repository contain emoji and other wide Unicode
    symbols. ``len()`` counts code points, not visual columns, so using it for
    padding makes separator pipes appear shifted in monospaced editors such as
    VS Code. This helper keeps the formatter dependency-free while following
    the width rules that matter for the symbols used in the notes.
    """
    codepoint = ord(char)

    if (
        unicodedata.combining(char)
        or codepoint in {0x200D, 0xFE0E, 0xFE0F}
        or 0x1F3FB <= codepoint <= 0x1F3FF
    ):
        return 0

    if unicodedata.category(char) in {"Cc", "Cf"}:
        return 0

    if unicodedata.east_asian_width(char) in {"W", "F"}:
        return 2
    return 1


def display_width(text: str) -> int:
    """Return the visual width of *text* in monospaced editor cells.

    Emoji sequences that explicitly request emoji presentation (VS16) are
    treated as two cells even when the base Unicode symbol is normally narrow.
    ZWJ-linked emoji sequences are treated as one glyph rather than summing the
    widths of every component.
    """
    total = 0
    index = 0

    while index < len(text):
        char = text[index]
        codepoint = ord(char)

        if (
            unicodedata.combining(char)
            or codepoint in {0x200D, 0xFE0E, 0xFE0F}
            or 0x1F3FB <= codepoint <= 0x1F3FF
        ):
            index += 1
            continue

        cluster_width = _codepoint_width(char)

        if index + 1 < len(text) and ord(text[index + 1]) == 0xFE0F:
            cluster_width = max(cluster_width, 2)
            index += 1

        while index + 1 < len(text) and ord(text[index + 1]) == 0x200D:
            index += 2
            if index >= len(text):
                break

            component_width = _codepoint_width(text[index])
            if index + 1 < len(text) and ord(text[index + 1]) == 0xFE0F:
                component_width = max(component_width, 2)
                index += 1
            if index + 1 < len(text) and 0x1F3FB <= ord(text[index + 1]) <= 0x1F3FF:
                index += 1

            cluster_width = max(cluster_width, component_width)

        total += cluster_width
        index += 1

    return total


def align_text(text: str, width: int, alignment: str) -> str:
    """Pad text to *width* visual cells rather than Python character count."""
    padding = max(0, width - display_width(text))

    if alignment == "right":
        return " " * padding + text
    if alignment == "center":
        left_padding = padding // 2
        right_padding = padding - left_padding
        return " " * left_padding + text + " " * right_padding
    return text + " " * padding


def minimum_separator_width(alignment: str) -> int:
    """Return the minimum visible width for a valid Markdown separator cell."""
    if alignment == "center":
        # Center syntax is :---: (three dashes plus two colons).
        return 5
    if alignment in {"left", "right"}:
        # Left/right syntax is :--- or ---: (three dashes plus one colon).
        return 4
    return 3


def separator_text(width: int, alignment: str) -> str:
    """Build a separator cell whose visible width exactly matches the column."""
    width = max(width, minimum_separator_width(alignment))

    if alignment == "right":
        return "-" * (width - 1) + ":"
    if alignment == "center":
        return ":" + "-" * (width - 2) + ":"
    if alignment == "left":
        return ":" + "-" * (width - 1)
    return "-" * width


def format_row(cells: Sequence[str], widths: Sequence[int], alignments: Sequence[str]) -> str:
    formatted = [
        align_text(cell, widths[index], alignments[index]) for index, cell in enumerate(cells)
    ]
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
            display_width(row[column]) for index, row in enumerate(rows) if index != separator_index
        )
        widths.append(max(content_width, minimum_separator_width(alignments[column])))

    header_index = separator_index - 1
    header_alignments = ["center"] * column_count

    formatted_lines: list[str] = []
    for index, row in enumerate(rows):
        if index == separator_index:
            formatted_lines.append(format_separator(widths, alignments))
        elif index == header_index:
            formatted_lines.append(format_row(row, widths, header_alignments))
        else:
            formatted_lines.append(format_row(row, widths, alignments))

    return formatted_lines


def find_table_end(lines: Sequence[str], start: int) -> int:
    """Return the first index after a contiguous table block."""
    end = start
    while end < len(lines) and is_probable_pipe_row(lines[end]):
        end += 1
    return end


def normalize_heading_spacing(lines: Sequence[str]) -> list[str]:
    """Place one blank line around ATX headings outside fenced code blocks."""
    output: list[str] = []
    in_fence = False

    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            continue

        if not in_fence and HEADING_RE.match(line):
            if output and output[-1].strip():
                output.append("")
            output.append(line)

            next_line = lines[index + 1] if index + 1 < len(lines) else None
            if next_line is not None and next_line.strip():
                output.append("")
            continue

        output.append(line)

    return output


def format_markdown_text(text: str) -> str:
    """Normalize headings and format pipe tables outside fenced code blocks."""
    has_trailing_newline = text.endswith("\n")
    lines = normalize_heading_spacing(text.splitlines())
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
        description="Normalize headings and align Markdown pipe tables across files.",
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
