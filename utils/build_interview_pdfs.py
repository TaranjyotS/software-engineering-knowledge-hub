"""Build company-neutral interview PDFs from reusable Markdown sources."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
OUTPUT_DIR = REPO_ROOT / "interview_questions"

NAVY = colors.HexColor("#0B1F33")
BLUE = colors.HexColor("#1479B8")
TEAL = colors.HexColor("#0A8F7A")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#5E6A7D")
PALE = colors.HexColor("#EDF4F8")
CODE_BG = colors.HexColor("#F3F5F7")
LINE = colors.HexColor("#CED8E2")

SANS = "HubSans"
SANS_BOLD = "HubSansBold"
MONO = "HubMono"

pdfmetrics.registerFont(TTFont(SANS, "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont(SANS_BOLD, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont(MONO, "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily(
    SANS,
    normal=SANS,
    bold=SANS_BOLD,
    italic=SANS,
    boldItalic=SANS_BOLD,
)

FORBIDDEN_PUBLIC_TERMS = (
    "citibank",
    "citigroup",
    "mississauga",
    "anuvu",
    "innodata",
    "outlier ai",
    "solut pvt",
)


@dataclass(frozen=True)
class PdfSpec:
    filename: str
    title: str
    subtitle: str
    sources: tuple[str, ...]


PDF_SPECS = (
    PdfSpec(
        filename="Behavioral_Interview_Playbook.pdf",
        title="Behavioral Interview Playbook",
        subtitle="Company-neutral answers, STAR stories, and practice guidance",
        sources=("interview_questions.md",),
    ),
    PdfSpec(
        filename="Backend_Data_AI_Project_Deep_Dive.pdf",
        title="Backend, Data, and AI Project Deep-Dive",
        subtitle="Technical answers, implementation examples, and production scenarios",
        sources=("project_deep_dive.md",),
    ),
    PdfSpec(
        filename="Software_Design_Patterns_Interview_Guide.pdf",
        title="Software Design Patterns Interview Guide",
        subtitle="Selection rules, Python examples, trade-offs, and low-level design",
        sources=("software_design_patterns.md",),
    ),
    PdfSpec(
        filename="Python_Backend_AI_Interview_Master_Guide.pdf",
        title="Python Backend, Distributed Systems, and AI Interview Master Guide",
        subtitle="Behavioral, coding, design-pattern, delivery, data, and AI preparation",
        sources=(
            "my_profile.md",
            "interview_questions.md",
            "project_deep_dive.md",
            "coding_interview_patterns.md",
            "python.md",
            "rest_api.md",
            "sql.md",
            "system_design.md",
            "software_design_patterns.md",
            "genai_llm_rag.md",
            "cloud_devops.md",
            "testing_security_observability.md",
        ),
    ),
)


def ascii_text(value: str) -> str:
    """Normalize punctuation and remove unsupported glyphs from PDF text."""
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2265": ">=",
        "\u2264": "<=",
        "\u2260": "!=",
        "\u00d7": "x",
        "\u00a0": " ",
    }
    for source, replacement in replacements.items():
        value = value.replace(source, replacement)
    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", "ignore").decode("ascii")


def assert_public_text(text: str, source_name: str) -> None:
    """Reject personal or employer-specific source content before publishing."""
    lowered = text.lower()
    found = [term for term in FORBIDDEN_PUBLIC_TERMS if term in lowered]
    if re.search(r"\bciti\b", lowered):
        found.append("citi")
    if found:
        raise ValueError(f"Forbidden public terms in {source_name}: {sorted(set(found))}")


def escape_xml(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_markup(value: str) -> str:
    """Convert a small, safe Markdown subset into ReportLab paragraph markup."""
    code_fragments: list[str] = []

    def preserve_code(match: re.Match[str]) -> str:
        code_fragments.append(escape_xml(match.group(1)))
        return f"CODETOKEN{len(code_fragments) - 1}ENDTOKEN"

    raw = re.sub(r"`([^`]+)`", preserve_code, ascii_text(value.strip()))
    text = escape_xml(raw)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"[image: \1]", text)
    text = re.sub(
        r"\[([^]]+)\]\(([^)]+)\)",
        lambda match: f'<link href="{match.group(2)}" color="#1479B8">{match.group(1)}</link>',
        text,
    )
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for index, fragment in enumerate(code_fragments):
        text = text.replace(f"CODETOKEN{index}ENDTOKEN", f'<font name="{MONO}">{fragment}</font>')
    return text


def create_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName=SANS_BOLD,
            fontSize=27,
            leading=32,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=18,
        ),
        "subtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=base["BodyText"],
            fontName=SANS,
            fontSize=12,
            leading=18,
            textColor=colors.HexColor("#D8E8F2"),
            alignment=TA_LEFT,
        ),
        "chapter": ParagraphStyle(
            "Chapter",
            parent=base["Heading1"],
            fontName=SANS_BOLD,
            fontSize=22,
            leading=27,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=14,
            keepWithNext=True,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName=SANS_BOLD,
            fontSize=18,
            leading=23,
            textColor=NAVY,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName=SANS_BOLD,
            fontSize=14,
            leading=18,
            textColor=BLUE,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName=SANS_BOLD,
            fontSize=11.5,
            leading=15,
            textColor=TEAL,
            spaceBefore=9,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "H4",
            parent=base["Heading4"],
            fontName=SANS_BOLD,
            fontSize=10.5,
            leading=14,
            textColor=INK,
            spaceBefore=7,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName=SANS,
            fontSize=9.2,
            leading=13.2,
            textColor=INK,
            spaceAfter=6,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName=SANS,
            fontSize=9,
            leading=13,
            textColor=INK,
            leftIndent=12,
            rightIndent=8,
            borderColor=TEAL,
            borderWidth=1.5,
            borderPadding=(6, 8, 6, 8),
            backColor=PALE,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName=MONO,
            fontSize=7,
            leading=9.2,
            textColor=colors.HexColor("#15202B"),
            backColor=CODE_BG,
            borderColor=LINE,
            borderWidth=0.5,
            borderPadding=7,
            leftIndent=3,
            rightIndent=3,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "BulletBody",
            parent=base["BodyText"],
            fontName=SANS,
            fontSize=9,
            leading=12.8,
            textColor=INK,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName=SANS_BOLD,
            fontSize=7.5,
            leading=9.5,
            textColor=colors.white,
            alignment=TA_LEFT,
        ),
        "table_body": ParagraphStyle(
            "TableBody",
            parent=base["BodyText"],
            fontName=SANS,
            fontSize=7.2,
            leading=9.3,
            textColor=INK,
        ),
        "toc_heading": ParagraphStyle(
            "TocHeading",
            parent=base["Heading1"],
            fontName=SANS_BOLD,
            fontSize=20,
            leading=24,
            textColor=NAVY,
            spaceAfter=12,
        ),
    }


class InterviewDocTemplate(BaseDocTemplate):
    """Document template with stable headers, footers, and TOC entries."""

    def __init__(self, filename: str, title: str) -> None:
        super().__init__(
            filename,
            pagesize=LETTER,
            leftMargin=0.68 * inch,
            rightMargin=0.68 * inch,
            topMargin=0.72 * inch,
            bottomMargin=0.62 * inch,
            title=title,
            author="Software Engineering Knowledge Hub",
            subject="Generic software engineering interview preparation",
        )
        self.document_title = title
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )
        self.addPageTemplates(PageTemplate(id="content", frames=frame, onPage=self.draw_page))

    def draw_page(self, canvas, doc) -> None:
        if doc.page > 1:
            canvas.saveState()
            canvas.setStrokeColor(LINE)
            canvas.setLineWidth(0.5)
            canvas.line(
                self.leftMargin,
                LETTER[1] - 0.48 * inch,
                LETTER[0] - self.rightMargin,
                LETTER[1] - 0.48 * inch,
            )
            canvas.setFont(SANS_BOLD, 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawString(self.leftMargin, LETTER[1] - 0.38 * inch, self.document_title[:78])
            canvas.setFont(SANS, 7.5)
            canvas.drawRightString(LETTER[0] - self.rightMargin, 0.34 * inch, f"{doc.page}")
            canvas.restoreState()

    def afterFlowable(self, flowable) -> None:
        if isinstance(flowable, Paragraph) and flowable.style.name in {"Chapter", "H1", "H2"}:
            level = {"Chapter": 0, "H1": 0, "H2": 1}[flowable.style.name]
            text = flowable.getPlainText()
            key = f"section-{self.seq.nextf('section')}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify("TOCEntry", (level, text, self.page, key))


def cover_story(spec: PdfSpec, styles: dict[str, ParagraphStyle]) -> list:
    accent = Table(
        [[""]],
        colWidths=[6.45 * inch],
        rowHeights=[0.12 * inch],
        style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL)]),
    )
    panel = Table(
        [
            [Paragraph(inline_markup(spec.title), styles["title"])],
            [Paragraph(inline_markup(spec.subtitle), styles["subtitle"])],
        ],
        colWidths=[6.45 * inch],
        rowHeights=[2.05 * inch, 1.25 * inch],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 24),
                ("RIGHTPADDING", (0, 0), (-1, -1), 24),
                ("TOPPADDING", (0, 0), (-1, 0), 28),
                ("TOPPADDING", (0, 1), (-1, 1), 8),
            ]
        ),
    )
    return [
        Spacer(1, 0.7 * inch),
        accent,
        panel,
        Spacer(1, 0.35 * inch),
        Paragraph(
            "Reusable engineering knowledge - no candidate or company identifiers",
            ParagraphStyle(
                "CoverNote",
                parent=styles["body"],
                fontSize=10,
                leading=14,
                textColor=MUTED,
                alignment=TA_CENTER,
            ),
        ),
        Spacer(1, 2.2 * inch),
        Paragraph(
            "Software Engineering Knowledge Hub",
            ParagraphStyle(
                "CoverBrand",
                parent=styles["body"],
                fontName=SANS_BOLD,
                fontSize=10,
                textColor=BLUE,
                alignment=TA_CENTER,
            ),
        ),
        PageBreak(),
    ]


def parse_table(
    lines: list[str], styles: dict[str, ParagraphStyle], available_width: float
) -> Table:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)

    column_count = max(len(row) for row in rows)
    normalized = [row + [""] * (column_count - len(row)) for row in rows]
    rendered = []
    for row_index, row in enumerate(normalized):
        style = styles["table_header"] if row_index == 0 else styles["table_body"]
        rendered.append([Paragraph(inline_markup(cell), style) for cell in row])

    if column_count == 1:
        widths = [available_width]
    elif column_count == 2:
        widths = [available_width * 0.32, available_width * 0.68]
    else:
        first = available_width * 0.22
        widths = [first] + [(available_width - first) / (column_count - 1)] * (column_count - 1)

    return Table(
        rendered,
        colWidths=widths,
        repeatRows=1,
        hAlign="LEFT",
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
            ]
        ),
    )


def markdown_flowables(
    text: str, styles: dict[str, ParagraphStyle], available_width: float
) -> list:
    flowables = []
    lines = ascii_text(text).splitlines()
    index = 0
    in_code = False
    code_lines: list[str] = []
    paragraph_lines: list[str] = []
    quote_lines: list[str] = []
    bullet_items: list[str] = []
    ordered_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_lines:
            value = " ".join(part.strip() for part in paragraph_lines).strip()
            if value:
                flowables.append(Paragraph(inline_markup(value), styles["body"]))
            paragraph_lines.clear()

    def flush_quote() -> None:
        if quote_lines:
            flowables.append(Paragraph(inline_markup(" ".join(quote_lines)), styles["quote"]))
            quote_lines.clear()

    def flush_bullets() -> None:
        if bullet_items:
            rendered_items = [
                Paragraph(inline_markup(item), styles["bullet"], bulletText="-")
                for item in bullet_items
            ]
            rendered_items.append(Spacer(1, 7))
            flowables.append(KeepTogether(rendered_items))
            bullet_items.clear()
        if ordered_items:
            rendered_items = [
                Paragraph(f"<b>{item_number}.</b> {inline_markup(item)}", styles["bullet"])
                for item_number, item in enumerate(ordered_items, start=1)
            ]
            rendered_items.append(Spacer(1, 7))
            flowables.append(KeepTogether(rendered_items))
            ordered_items.clear()

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_quote()
            flush_bullets()
            if in_code:
                code = "\n".join(code_lines).rstrip() or " "
                flowables.append(Preformatted(code, styles["code"], maxLineLength=92))
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            index += 1
            continue

        if in_code:
            code_lines.append(line.expandtabs(4))
            index += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            flush_quote()
            flush_bullets()
            table_lines = []
            while index < len(lines):
                candidate = lines[index].strip()
                if not (candidate.startswith("|") and candidate.endswith("|")):
                    break
                table_lines.append(candidate)
                index += 1
            if len(table_lines) >= 2:
                flowables.append(parse_table(table_lines, styles, available_width))
                flowables.append(Spacer(1, 8))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_quote()
            flush_bullets()
            level = len(heading.group(1))
            style_name = {1: "h1", 2: "h2", 3: "h3"}.get(level, "h4")
            flowables.append(Paragraph(inline_markup(heading.group(2)), styles[style_name]))
            index += 1
            continue

        if stripped in {"---", "***", "___"}:
            flush_paragraph()
            flush_quote()
            flush_bullets()
            flowables.append(
                HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=5, spaceAfter=8)
            )
            index += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            flush_bullets()
            quote_lines.append(stripped.lstrip("> "))
            index += 1
            continue
        flush_quote()

        bullet = re.match(r"^[-+*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if bullet:
            flush_paragraph()
            if ordered_items:
                flush_bullets()
            bullet_items.append(bullet.group(1))
            index += 1
            continue
        if ordered:
            flush_paragraph()
            if bullet_items:
                flush_bullets()
            ordered_items.append(ordered.group(1))
            index += 1
            continue
        flush_bullets()

        if not stripped:
            flush_paragraph()
        elif stripped.startswith("<") and stripped.endswith(">"):
            pass
        else:
            paragraph_lines.append(stripped)
        index += 1

    flush_paragraph()
    flush_quote()
    flush_bullets()
    if in_code:
        flowables.append(Preformatted("\n".join(code_lines), styles["code"], maxLineLength=92))
    return flowables


def source_story(spec: PdfSpec, styles: dict[str, ParagraphStyle], available_width: float) -> list:
    story = []
    for source_index, source_name in enumerate(spec.sources):
        source_path = DOCS_DIR / source_name
        text = source_path.read_text(encoding="utf-8")
        assert_public_text(text, source_name)
        if len(spec.sources) > 1:
            if source_index:
                story.append(PageBreak())
            chapter_title = next(
                (line[2:].strip() for line in text.splitlines() if line.startswith("# ")),
                source_path.stem.replace("_", " ").title(),
            )
            story.append(Paragraph(inline_markup(chapter_title), styles["chapter"]))
            story.append(
                Paragraph(
                    f'Source: <font name="{MONO}">docs/{escape_xml(source_name)}</font>',
                    styles["body"],
                )
            )
            story.append(HRFlowable(width="100%", thickness=1.2, color=TEAL, spaceAfter=12))

        lines = text.splitlines()
        if len(spec.sources) > 1 and lines and lines[0].startswith("# "):
            text = "\n".join(lines[1:])
        story.extend(markdown_flowables(text, styles, available_width))
    return story


def build_pdf(spec: PdfSpec) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / spec.filename
    styles = create_styles()
    doc = InterviewDocTemplate(str(output_path), spec.title)
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            "TOCLevel0",
            fontName=SANS_BOLD,
            fontSize=9.5,
            leading=13,
            leftIndent=0,
            firstLineIndent=0,
            textColor=NAVY,
            spaceBefore=4,
        ),
        ParagraphStyle(
            "TOCLevel1",
            fontName=SANS,
            fontSize=8.5,
            leading=11,
            leftIndent=14,
            firstLineIndent=0,
            textColor=MUTED,
        ),
    ]
    story = cover_story(spec, styles)
    story.extend([Paragraph("Contents", styles["toc_heading"]), toc, PageBreak()])
    story.extend(source_story(spec, styles, doc.width))
    doc.multiBuild(story)
    return output_path


def build_all(specs: Iterable[PdfSpec] = PDF_SPECS) -> list[Path]:
    return [build_pdf(spec) for spec in specs]


if __name__ == "__main__":
    for generated in build_all():
        print(generated.relative_to(REPO_ROOT))
