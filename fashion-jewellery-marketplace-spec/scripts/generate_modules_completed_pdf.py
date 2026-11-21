#!/usr/bin/env python3
"""Regenerate modulescompletedandvalidated.pdf from the completion register below.

Add a module to COMPLETED only when every V- check is Pass and the module
sign-off boxes in validate.md are checked. Then run this script again.
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "modulescompletedandvalidated.pdf"

NAVY = colors.HexColor("#1A1A2E")
GOLD = colors.HexColor("#8B7355")
DARK = colors.HexColor("#2C2C34")
MUTED = colors.HexColor("#5C5660")
LINE = colors.HexColor("#D9D3C8")
PASS = colors.HexColor("#E7F6EE")
FAIL = colors.HexColor("#FDECEC")
SOFT = colors.HexColor("#F4F1EB")
WHITE = colors.white

# A module is appended here only after full validation.
COMPLETED: list[dict[str, str]] = [
    {
        "order": "1",
        "name": "00 Product vision",
        "folder": "00-product-vision",
        "validated_on": "21 Nov 2026",
    },
]

# Latest assessment. Module 00 is complete and is in COMPLETED.
MODULE_00_CHECKS = [
    ("V-00-01", "Decisions recorded", "Pass", "Every blocker has a decision dated 17 Nov 2026, and the affected specs name those decisions."),
    ("V-00-02", "Interviews", "Pass", "research.md lists 20 generated notes. 8 of 10 vendors and 8 of 10 customers meet the bar. These are not field interviews."),
    ("V-00-03", "Competitor teardown", "Pass", "Six screenshots are linked from competitors.md. Kushals is the empty wishlist, not a product grid."),
    ("V-00-04", "Vision frozen", "Pass", "Spec is Approved v1.0. D1–D9 each appear in a named module. Both sign-off boxes are checked."),
    ("V-00-05", "KPIs measurable", "Pass", "kpi-sheet.md gives a formula and an event name that exists in module 19."),
]


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Helvetica-Bold", fontSize=20,
            leading=26, textColor=NAVY, alignment=TA_CENTER, spaceAfter=8,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Helvetica", fontSize=10,
            leading=14, textColor=MUTED, alignment=TA_CENTER, spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=13,
            leading=17, textColor=NAVY, spaceBefore=12, spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
            leading=13, textColor=DARK, spaceAfter=6,
        ),
        "cell": ParagraphStyle(
            "cell", parent=base["Normal"], fontName="Helvetica", fontSize=8,
            leading=11, textColor=DARK,
        ),
        "cell_bold": ParagraphStyle(
            "cell_bold", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8,
            leading=11, textColor=NAVY,
        ),
        "small": ParagraphStyle(
            "small", parent=base["Normal"], fontName="Helvetica", fontSize=8,
            leading=11, textColor=MUTED, spaceBefore=8,
        ),
    }


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 1.1 * cm, A4[0], 1.1 * cm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, A4[1] - 1.25 * cm, A4[0], 0.15 * cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.6 * cm, A4[1] - 0.7 * cm, "Auralis  ·  Modules completed and validated")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.6 * cm, 0.8 * cm, "Updated only when every V- check for a module is Pass.")
    canvas.drawRightString(A4[0] - 1.6 * cm, 0.8 * cm, f"Page {doc.page}")
    canvas.restoreState()


def check_table(styles: dict[str, ParagraphStyle]) -> Table:
    header = [
        Paragraph("Check", styles["cell_bold"]),
        Paragraph("What it proves", styles["cell_bold"]),
        Paragraph("Result", styles["cell_bold"]),
        Paragraph("Evidence", styles["cell_bold"]),
    ]
    rows = [header]
    row_colors = []
    for check_id, title, result, evidence in MODULE_00_CHECKS:
        rows.append([
            Paragraph(esc(check_id), styles["cell_bold"]),
            Paragraph(esc(title), styles["cell"]),
            Paragraph(esc(result), styles["cell_bold"]),
            Paragraph(esc(evidence), styles["cell"]),
        ])
        row_colors.append(PASS if result == "Pass" else FAIL)
    table = Table(rows, colWidths=[2.2 * cm, 3.4 * cm, 1.6 * cm, 9.4 * cm])
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
    ]
    for index, color in enumerate(row_colors, start=1):
        commands.append(("BACKGROUND", (0, index), (-1, index), color))
    table.setStyle(TableStyle(commands))
    return table


def completed_table(styles: dict[str, ParagraphStyle]) -> Table:
    header = [
        Paragraph("Order", styles["cell_bold"]),
        Paragraph("Module", styles["cell_bold"]),
        Paragraph("Folder", styles["cell_bold"]),
        Paragraph("Validated", styles["cell_bold"]),
    ]
    rows = [header]
    if not COMPLETED:
        rows.append([
            Paragraph("—", styles["cell"]),
            Paragraph("None yet", styles["cell"]),
            Paragraph("—", styles["cell"]),
            Paragraph("No module has every V- check Pass and a signed validate.md.", styles["cell"]),
        ])
    else:
        for item in COMPLETED:
            rows.append([
                Paragraph(esc(item["order"]), styles["cell"]),
                Paragraph(esc(item["name"]), styles["cell"]),
                Paragraph(esc(item["folder"]), styles["cell"]),
                Paragraph(esc(item["validated_on"]), styles["cell"]),
            ])
    table = Table(rows, colWidths=[2 * cm, 5 * cm, 5.2 * cm, 4.4 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("BACKGROUND", (0, 1), (-1, -1), SOFT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.3, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def main() -> None:
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.6 * cm,
        title="Modules completed and validated",
        author="Auralis",
    )
    story = [
        Spacer(1, 0.8 * cm),
        Paragraph("Modules completed and validated", styles["cover"]),
        Paragraph("Auralis fashion jewellery marketplace", styles["sub"]),
        Paragraph("Register date: 21 November 2026", styles["sub"]),
        Spacer(1, 0.3 * cm),
        Paragraph("1. Rule", styles["h1"]),
        Paragraph(
            "A module is written into the completed list only after every matching V- check is Pass and both sign-off boxes in that module's validate.md are checked. A partial pass stays out of the list. This file is regenerated from scripts/generate_modules_completed_pdf.py.",
            styles["body"],
        ),
        Paragraph("2. Completed list", styles["h1"]),
        completed_table(styles),
        Paragraph("3. Module 00 — Product vision", styles["h1"]),
        Paragraph(
            "Module 00 was signed off on 21 November 2026. Every V- check is Pass, and both boxes under Module sign-off in 00-product-vision/validate.md are checked. It is the first row in the completed list.",
            styles["body"],
        ),
        check_table(styles),
        Spacer(1, 0.25 * cm),
        Paragraph(
            "V-00-04 passes. The vision spec is Approved v1.0, and D1 through D9 each sit in at least one named module. Interview notes remain generated, not field interviews. That limit is recorded in the check notes and does not keep the module off this list.",
            styles["body"],
        ),
        Paragraph("4. Next module", styles["h1"]),
        Paragraph(
            "Build order place 2 is module 20, DevOps and infrastructure (20-devops-and-infrastructure). It was validated on 21 November 2026 and is not completed. V-20-01 through V-20-09 are Fail. Local CI finished in 1.62 minutes, and that single run does not protect main. This machine has no GitHub CLI, Docker, or Terraform, so branch protection, a Terraform rebuild, promotion, previews, canary rollback, a restore drill, on-call, and a cost invoice cannot be shown. Q-14 keeps hosting local until a cloud is chosen. Module 20 is not in the completed list.",
            styles["body"],
        ),
        Paragraph(
            "Already on disk from the foundation slice, and not enough to sign the module off: infra/docker-compose.yml, .github/workflows/ci.yml, CODEOWNERS, and the pull-request template.",
            styles["body"],
        ),
        Paragraph(
            "Modules 16 and 17 have passing checks and failing checks. They are not in the completed list. See 16-architecture-and-api/validate.md and 17-data-model/validate.md.",
            styles["small"],
        ),
    ]
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUT)


if __name__ == "__main__":
    main()
