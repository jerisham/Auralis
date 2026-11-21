#!/usr/bin/env python3
"""
Generate one beginner-friendly PDF per feature module (00–24).

Content comes ONLY from each module's spec.md, task.md, validate.md,
plus shared root docs (README, ROADMAP, GLOSSARY, architecture stack).
No invented product functionality.
"""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "INDIVIDUAL_FEATURE_GUIDES"

NAVY = colors.HexColor("#1A1A2E")
GOLD = colors.HexColor("#8B7355")
SOFT = colors.HexColor("#F4F1EB")
DARK = colors.HexColor("#2C2C34")
MUTED = colors.HexColor("#5C5660")
WARN = colors.HexColor("#FFF4E5")
CODE_BG = colors.HexColor("#F0EEEA")
LINE = colors.HexColor("#D9D3C8")

MODULE_NAMES = {
    "00": "Product Vision",
    "01": "Design System",
    "02": "Intro Experience",
    "03": "Customer Accounts",
    "04": "Catalog and Discovery",
    "05": "Product Page",
    "06": "Cart and Checkout",
    "07": "Customer Orders Returns Reviews",
    "08": "Vendor Onboarding",
    "09": "Vendor Storefront",
    "10": "Vendor Dashboard",
    "11": "Platform Admin",
    "12": "Order Lifecycle",
    "13": "Payments and Settlement",
    "14": "Delivery Confirmation",
    "15": "Notifications",
    "16": "Architecture and API",
    "17": "Data Model",
    "18": "Security Privacy Compliance",
    "19": "Non Functional and Analytics",
    "20": "DevOps and Infrastructure",
    "21": "Testing Strategy",
    "22": "Launch and Vendor Acquisition",
    "23": "Growth Features",
    "24": "Mobile Apps",
}

# Friendly one-line "why" framed from Purpose when present; filled from parse.
TECH_STACK_BLURB = (
    "Recommended stack from module 16 (Architecture & API): "
    "Next.js (React/TypeScript) for web, NestJS or .NET 8 for API (pick in T-16-01), "
    "PostgreSQL 16 with Row-Level Security, Redis, Azure Service Bus or BullMQ, "
    "Meilisearch or Azure AI Search, Azure Blob + CDN, Azure Container Apps, "
    "Terraform + GitHub Actions. Mobile later: React Native (Expo)."
)


def esc(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    # Protect inline code first so * inside `product.*` cannot become <i>
    code_parts: list[str] = []

    def _park_code(m: re.Match) -> str:
        code_parts.append(m.group(1))
        return f"\x00CODE{len(code_parts) - 1}\x00"

    text = re.sub(r"`([^`]+)`", _park_code, text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for i, code in enumerate(code_parts):
        safe = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = text.replace(
            f"\x00CODE{i}\x00",
            f"<font face='Courier' size='8'>{safe}</font>",
        )
    # Drop any leftover unpaired * that would confuse the parser
    text = text.replace("*", "")
    return text


def styles():
    base = getSampleStyleSheet()
    s = {}
    s["cover"] = ParagraphStyle(
        "cover", parent=base["Title"], fontName="Helvetica-Bold", fontSize=18,
        leading=24, textColor=NAVY, alignment=TA_CENTER, spaceAfter=10,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"], fontName="Helvetica", fontSize=10,
        leading=14, textColor=MUTED, alignment=TA_CENTER, spaceAfter=6,
    )
    s["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=14,
        leading=18, textColor=NAVY, spaceBefore=14, spaceAfter=8,
    )
    s["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
        leading=15, textColor=DARK, spaceBefore=11, spaceAfter=5,
    )
    s["h3"] = ParagraphStyle(
        "h3", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=10,
        leading=13, textColor=GOLD, spaceBefore=8, spaceAfter=4,
    )
    s["body"] = ParagraphStyle(
        "body", parent=base["Normal"], fontName="Helvetica", fontSize=9,
        leading=12.5, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=5,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"], fontName="Helvetica", fontSize=9,
        leading=12, textColor=DARK, leftIndent=4, spaceAfter=2,
    )
    s["note"] = ParagraphStyle(
        "note", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=8.5,
        leading=11.5, textColor=MUTED, spaceAfter=8, backColor=WARN, borderPadding=5,
    )
    s["code"] = ParagraphStyle(
        "code", parent=base["Code"], fontName="Courier", fontSize=7.5,
        leading=10, textColor=DARK, backColor=CODE_BG, leftIndent=2, spaceBefore=3, spaceAfter=6,
    )
    s["small"] = ParagraphStyle(
        "small", parent=base["Normal"], fontName="Helvetica", fontSize=8,
        leading=11, textColor=MUTED, spaceAfter=4,
    )
    s["meta"] = ParagraphStyle(
        "meta", parent=base["Normal"], fontName="Helvetica", fontSize=9,
        leading=12, textColor=DARK, alignment=TA_CENTER, spaceAfter=4,
    )
    s["cell"] = ParagraphStyle(
        "cell", parent=base["Normal"], fontName="Helvetica", fontSize=7.5,
        leading=10, textColor=DARK,
    )
    s["cell_h"] = ParagraphStyle(
        "cell_h", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=7.5,
        leading=10, textColor=NAVY,
    )
    return s


def p(text: str, style) -> Paragraph:
    return Paragraph(esc(text), style)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(1.5 * cm, A4[1] - 1.1 * cm, A4[0] - 1.5 * cm, A4[1] - 1.1 * cm)
    canvas.line(1.5 * cm, 1.1 * cm, A4[0] - 1.5 * cm, 1.1 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.5 * cm, A4[1] - 0.9 * cm, "Fashion Jewellery Marketplace — Individual Feature Guide")
    canvas.drawRightString(A4[0] - 1.5 * cm, A4[1] - 0.9 * cm, doc.module_label)
    canvas.drawCentredString(A4[0] / 2, 0.7 * cm, f"Page {doc.page}")
    canvas.restoreState()


def parse_meta(spec_text: str) -> dict:
    meta = {"phase": "?", "depends": "—", "status": "Draft"}
    m = re.search(
        r"\*\*Phase:\*\*\s*([^\u00b7*]+).*?\*\*Depends on:\*\*\s*([^\u00b7*]+).*?\*\*Status:\*\*\s*(.+)",
        spec_text,
        re.I | re.S,
    )
    if m:
        meta["phase"] = m.group(1).strip()
        meta["depends"] = m.group(2).strip()
        meta["status"] = m.group(3).strip().split("\n")[0].strip()
    title = ""
    tm = re.search(r"^#\s+(.+)$", spec_text, re.M)
    if tm:
        title = tm.group(1).strip()
    meta["title"] = title
    return meta


def split_sections(md: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, body) by ## headings. Skip the H1."""
    lines = md.splitlines()
    sections: list[tuple[str, list[str]]] = []
    current = None
    buf: list[str] = []
    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            continue
        if line.startswith("## "):
            if current is not None:
                sections.append((current, buf))
            current = line[3:].strip()
            buf = []
        else:
            if current is None:
                # preamble after H1 / meta line
                continue
            buf.append(line)
    if current is not None:
        sections.append((current, buf))
    return [(h, "\n".join(b).strip()) for h, b in sections]


def extract_purpose(sections: list[tuple[str, str]]) -> str:
    for h, body in sections:
        if re.search(r"purpose|principles|vision", h, re.I):
            # first paragraph-ish
            paras = [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]
            if paras:
                # strip leading list markers for a short summary
                first = paras[0]
                if first.startswith("|"):
                    # table — use first non-table lines or whole
                    return re.sub(r"\s+", " ", first[:400])
                return first
    if sections:
        return sections[0][1][:500]
    return "See the source specification in this module folder."


def parse_md_table(block: str) -> list[list[str]] | None:
    lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return None
    rows = []
    for i, ln in enumerate(lines):
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if i == 1 and all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in cells):
            continue
        rows.append(cells)
    return rows if len(rows) >= 2 else None


def flow_body(body: str, S, max_table_rows: int = 40) -> list:
    """Convert a markdown body chunk into reportlab flowables (from source only)."""
    out = []
    if not body.strip():
        return out

    # code fences
    parts = re.split(r"(```[\s\S]*?```)", body)
    for part in parts:
        if part.startswith("```"):
            code = re.sub(r"^```\w*\n?", "", part)
            code = re.sub(r"\n?```$", "", code)
            # truncate huge diagrams slightly for page fit but keep content
            lines = code.splitlines()
            if len(lines) > 45:
                code = "\n".join(lines[:45]) + "\n… (see full diagram in spec.md)"
            out.append(Preformatted(code, S["code"]))
            continue

        # split by blank lines / ### / tables
        blocks = re.split(r"\n\s*\n", part)
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            if block.startswith("### "):
                first, _, rest = block.partition("\n")
                out.append(p(first[4:].strip(), S["h3"]))
                if rest.strip():
                    out.extend(flow_body(rest, S, max_table_rows))
                continue
            if block.startswith("|"):
                rows = parse_md_table(block)
                if rows:
                    out.append(make_table(rows, S, max_table_rows))
                    out.append(Spacer(1, 0.15 * cm))
                    continue
            # bullet / numbered list
            if re.match(r"^[-*] |\d+\. ", block, re.M) and "\n" in block or re.match(r"^[-*] ", block):
                items = []
                for ln in block.splitlines():
                    ln = ln.strip()
                    if not ln:
                        continue
                    m = re.match(r"^[-*]\s+(.*)$", ln) or re.match(r"^\d+\.\s+(.*)$", ln)
                    if m:
                        items.append(ListItem(Paragraph(esc(m.group(1)), S["bullet"]), leftIndent=12, value="bullet"))
                    else:
                        if items:
                            out.append(ListFlowable(items, bulletType="bullet", start="•"))
                            items = []
                        out.append(p(ln, S["body"]))
                if items:
                    out.append(ListFlowable(items, bulletType="bullet", start="•"))
                continue
            # single-line bullet
            m = re.match(r"^[-*]\s+(.*)$", block)
            if m:
                out.append(ListFlowable(
                    [ListItem(Paragraph(esc(m.group(1)), S["bullet"]), leftIndent=12, value="bullet")],
                    bulletType="bullet", start="•",
                ))
                continue
            out.append(p(block, S["body"]))
    return out


def make_table(rows: list[list[str]], S, max_rows: int = 40):
    rows = rows[: max_rows + 1]
    ncol = max(len(r) for r in rows)
    norm = []
    for r in rows:
        rr = r + [""] * (ncol - len(r))
        norm.append(rr)
    # column widths
    usable = A4[0] - 3.2 * cm
    widths = [usable / ncol] * ncol
    # prefer narrower first col for ID-like tables
    first_hdr = (norm[0][0] or "").strip()
    id_like = bool(re.match(r"^(T-|V-|FR-|ID)", first_hdr, re.I)) or first_hdr.lower() in (
        "id", "#", "entity", "layer", "role", "metric", "term",
    )
    if ncol >= 2 and id_like:
        if ncol == 4:
            widths = [2.2 * cm, 5.5 * cm, 3.5 * cm, usable - 11.2 * cm]
        elif ncol == 5:
            widths = [2.0 * cm, 4.2 * cm, 3.0 * cm, 2.2 * cm, usable - 11.4 * cm]
        elif ncol == 3:
            widths = [3.0 * cm, usable - 7.5 * cm, 4.5 * cm]
        elif ncol == 2:
            widths = [4.5 * cm, usable - 4.5 * cm]

    data = []
    for i, r in enumerate(norm):
        style = S["cell_h"] if i == 0 else S["cell"]
        data.append([Paragraph(esc(c), style) for c in r])

    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("TEXTCOLOR", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF8F5")]),
    ]))
    return t


def parse_task_details(task_md: str) -> list[tuple[str, str]]:
    """Return list of (task heading, detail body) from ### T-xx blocks."""
    parts = re.split(r"(?=^###\s+T-)", task_md, flags=re.M)
    details = []
    for part in parts:
        m = re.match(r"^###\s+(T-\d+-\d+[^\n]*)\n([\s\S]*)", part.strip())
        if m:
            details.append((m.group(1).strip(), m.group(2).strip()))
    return details


def parse_validate_details(val_md: str) -> list[tuple[str, str]]:
    parts = re.split(r"(?=^###\s+V-)", val_md, flags=re.M)
    details = []
    for part in parts:
        m = re.match(r"^###\s+(V-\d+-\d+[^\n]*)\n([\s\S]*)", part.strip())
        if m:
            details.append((m.group(1).strip(), m.group(2).strip()))
    return details


def find_endpoints(text: str) -> list[str]:
    pats = re.findall(
        r"`((?:GET|POST|PATCH|PUT|DELETE)\s+/[^`]+)`|`(/v1/[^`]+)`|`(/webhooks/[^`]+)`",
        text,
    )
    out = []
    for a, b, c in pats:
        out.append(a or b or c)
    more = re.findall(r"(?:GET|POST|PATCH|PUT|DELETE)\s+/[A-Za-z0-9_{}\-/?=&]+", text)
    out.extend(more)
    # dedupe preserve order
    seen = set()
    uniq = []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def find_urls(text: str) -> list[str]:
    urls = re.findall(r"`(/[a-zA-Z0-9_\-/{}.]+)`", text)
    # filter likely page paths
    keep = []
    for u in urls:
        if u.startswith("/v1") or "webhook" in u:
            continue
        if any(k in u for k in ("/", "admin", "vendor", "cart", "order", "search", "product", "store", "sell", "account")):
            keep.append(u)
    seen = set()
    out = []
    for u in keep:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out[:30]


def related_modules(depends: str, folder: str, all_folders: list[str]) -> list[str]:
    nums = re.findall(r"\d{2}", depends)
    # also scan for module numbers mentioned in folder name context — skip
    related = []
    for n in nums:
        for f in all_folders:
            if f.startswith(n + "-") and f != folder:
                related.append(f)
    return related


def beginner_terms_used(text: str) -> list[tuple[str, str]]:
    glossary = {
        "vendor": "A seller who lists jewellery and ships their own packages.",
        "customer": "A shopper who buys on the marketplace.",
        "admin": "A platform staff member who approves vendors and handles disputes.",
        "OTP": "One-Time Password — a short code sent by SMS/WhatsApp to prove you own the phone number.",
        "JWT": "JSON Web Token — a short-lived digital pass the API gives after login.",
        "KYC": "Know Your Customer — checking a vendor’s identity (PAN, GST, bank).",
        "RLS": "Row-Level Security — database rules so one vendor cannot see another vendor’s rows.",
        "SKU": "Stock Keeping Unit — one exact product version (size/colour/style).",
        "tranche": "A partial payout to a vendor (T1 on dispatch, T2 after delivery + return window).",
        "ledger": "The official money diary of the platform (double-entry).",
        "webhook": "A message a payment/courier company sends to our server when something happens.",
        "idempotency": "Doing the same request twice must not create two orders or two payments.",
        "PWA": "Progressive Web App — a website that can sit on your phone home screen.",
        "SSR": "Server-Side Rendering — the server builds the page HTML for SEO and speed.",
        "commission": "The fee the platform keeps from a vendor order.",
        "SLA": "Service Level Agreement — time limits (for example: accept or dispatch within X hours).",
        "sandbox": "A safe test mode of payments/SMS — fake money, not real charges.",
    }
    found = []
    lower = text.lower()
    for term, meaning in glossary.items():
        if term.lower() in lower or term in text:
            found.append((term, meaning))
    return found[:12]


def extract_errors_from_validate_and_spec(spec: str, task: str, val: str) -> list[tuple[str, str]]:
    """Derive common errors ONLY from edge cases / pass criteria language in docs."""
    errors = []
    # Edge cases section
    for h, body in split_sections(spec):
        if re.search(r"edge case", h, re.I):
            for ln in body.splitlines():
                ln = ln.strip()
                m = re.match(r"^[-*]\s+(.*)$", ln)
                if m:
                    item = m.group(1)
                    # split "→" style into problem / what docs say
                    if "→" in item:
                        left, right = item.split("→", 1)
                        errors.append((left.strip(), right.strip() + " (from this module’s edge cases)"))
                    else:
                        errors.append((item, "Follow the rule described in this module’s Edge cases section in spec.md."))
    # Also from validate pass criteria about failures
    for title, body in parse_validate_details(val):
        if re.search(r"fail|reject|error|timeout|duplicate|race|stock|signature", body, re.I):
            short = re.sub(r"\s+", " ", body)[:220]
            errors.append((f"Check that fails: {title}", f"Source validate.md: {short}"))
    # Deduplicate by first 60 chars of problem
    seen = set()
    uniq = []
    for a, b in errors:
        key = a[:60]
        if key not in seen:
            seen.add(key)
            uniq.append((a, b))
    return uniq[:15]


def load_module(folder: Path) -> dict:
    spec = (folder / "spec.md").read_text(encoding="utf-8")
    task = (folder / "task.md").read_text(encoding="utf-8")
    val = (folder / "validate.md").read_text(encoding="utf-8")
    meta = parse_meta(spec)
    return {
        "folder": folder.name,
        "num": folder.name[:2],
        "spec": spec,
        "task": task,
        "val": val,
        "meta": meta,
        "spec_sections": split_sections(spec),
        "task_sections": split_sections(task),
        "val_sections": split_sections(val),
        "task_details": parse_task_details(task),
        "val_details": parse_validate_details(val),
    }


def build_pdf(mod: dict, all_folders: list[str], S) -> Path:
    num = mod["num"]
    folder = mod["folder"]
    nice = MODULE_NAMES.get(num, folder)
    filename = f"{num}-{nice.replace(' ', '-')}.pdf"
    out_path = OUT_DIR / filename

    meta = mod["meta"]
    title = meta.get("title") or f"{num} — {nice}"
    depends = meta.get("depends", "—")
    phase = meta.get("phase", "?")
    status = meta.get("status", "Draft")

    purpose = extract_purpose(mod["spec_sections"])
    related = related_modules(depends, folder, all_folders)
    endpoints = find_endpoints(mod["spec"] + "\n" + mod["task"] + "\n" + mod["val"])
    urls = find_urls(mod["spec"] + "\n" + mod["task"])
    terms = beginner_terms_used(mod["spec"] + "\n" + mod["task"])
    errors = extract_errors_from_validate_and_spec(mod["spec"], mod["task"], mod["val"])

    story = []

    # Cover
    story.append(Spacer(1, 1.2 * cm))
    story.append(p(f"Feature Guide {num}", S["cover_sub"]))
    story.append(p(title, S["cover"]))
    story.append(p(f"Folder: {folder}", S["meta"]))
    story.append(p(f"Phase: {phase}  ·  Depends on: {depends}  ·  Status: {status}", S["meta"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(p(
        "This PDF teaches one feature module from the Fashion Jewellery Marketplace specification pack. "
        "Every capability below is taken from this module’s actual files: spec.md (what/why), task.md (how to build), "
        "and validate.md (how to prove it works). There is no separate application source code in this folder yet — "
        "these three files ARE the source of truth for the feature.",
        S["note"],
    ))
    story.append(PageBreak())

    # 1 What / why
    story.append(p("1. What is this feature?", S["h1"]))
    story.append(p(
        "In plain words: this module is one piece of the marketplace. "
        "Think of the whole product like a big house — this folder is one room with a clear job.",
        S["body"],
    ))
    story.append(p("Purpose (from spec.md)", S["h2"]))
    story.extend(flow_body(purpose, S))

    story.append(p("Why it is used", S["h2"]))
    story.append(p(
        f"Without this module, later features that depend on it cannot work safely. "
        f"The spec says this module depends on: <b>{esc(depends)}</b>. "
        "If that list is empty (—), it is a starting foundation.",
        S["body"],
    ))
    if related:
        story.append(p("It connects directly to these other feature folders (from Depends on):", S["body"]))
        story.extend(flow_body("\n".join(f"- `{r}`" for r in related), S))

    # Terms
    if terms:
        story.append(p("Simple meanings of words you will see", S["h2"]))
        for term, meaning in terms:
            story.append(p(f"<b>{term}</b> — {meaning}", S["bullet"]))

    story.append(PageBreak())

    # 2 What it does / functionalities from spec sections
    story.append(p("2. What it does (all functionalities in the spec)", S["h1"]))
    story.append(p(
        "The sections below are the real contents of this module’s spec.md, rewritten only for readability "
        "(headings kept; tables and lists preserved from the source).",
        S["small"],
    ))
    for h, body in mod["spec_sections"]:
        story.append(p(h, S["h2"]))
        story.extend(flow_body(body, S))
    story.append(PageBreak())

    # 3 How it works step by step from tasks
    story.append(p("3. How it works step by step (from task.md)", S["h1"]))
    story.append(p(
        "Each task ID (like T-06-01) is one build step. Do them in dependency order. "
        "A task is finished only when its matching V- check in validate.md passes.",
        S["body"],
    ))

    # Task overview table if present
    for h, body in mod["task_sections"]:
        if "task" in h.lower() or body.strip().startswith("|"):
            story.append(p("Task list", S["h2"]))
            story.extend(flow_body(body if body.strip().startswith("|") else body, S))
            break
    else:
        # first table in task file
        tables = re.findall(r"(\|.+\|[\s\S]*?\n\n)", mod["task"] + "\n\n")
        if tables:
            story.append(p("Task list", S["h2"]))
            story.extend(flow_body(tables[0], S))

    if mod["task_details"]:
        story.append(p("Step-by-step task details (from source)", S["h2"]))
        for title, body in mod["task_details"]:
            block = [p(title, S["h3"])]
            block.extend(flow_body(body, S))
            story.append(KeepTogether(block))
    else:
        story.append(p(
            "This module’s task.md mainly uses a table of tasks. Open task.md for the Done-when criteria of each row.",
            S["note"],
        ))
        story.extend(flow_body(mod["task"], S))

    story.append(PageBreak())

    # 4 Background / tech / files
    story.append(p("4. What happens in the background", S["h1"]))
    story.append(p(
        "Background behaviour is whatever the Functional requirements, Edge cases, and task Done-when notes describe "
        "(for example: webhooks, jobs, stock reservation, RLS). Those rules are already listed in sections 2 and 3 above — "
        "do not invent extra silent behaviour beyond the documents.",
        S["body"],
    ))
    story.append(p("Technologies involved (project recommendation)", S["h2"]))
    story.append(p(TECH_STACK_BLURB, S["body"]))
    story.append(p(
        "Module 16 also says the backend should be a modular monolith with modules that mirror these spec folders "
        "(identity, catalog, cart, orders, payments, delivery, notifications, vendor, admin).",
        S["body"],
    ))

    story.append(p("Source files for THIS feature (actual files in the project)", S["h2"]))
    story.extend(flow_body(
        f"- `{folder}/spec.md` — what to build and why\n"
        f"- `{folder}/task.md` — build tasks T-{num}-xx\n"
        f"- `{folder}/validate.md` — proof checks V-{num}-xx\n"
        "- `TRACKER.md` — update status when a V- check passes\n"
        "- `ROADMAP.md` — when this module fits in milestones\n"
        "- `GLOSSARY.md` — shared word meanings\n"
        "- `16-architecture-and-api/spec.md` — API and stack rules for engineering modules\n"
        "- `17-data-model/spec.md` — database entities when the feature stores data",
        S,
    ))

    if endpoints:
        story.append(p("API endpoints / paths mentioned in this module’s docs", S["h2"]))
        story.append(p(
            "These strings appear in the module files. Use them when implementing or testing — do not invent others.",
            S["small"],
        ))
        story.extend(flow_body("\n".join(f"- `{e}`" for e in endpoints), S))
    if urls:
        story.append(p("Page paths mentioned in this module’s docs", S["h2"]))
        story.extend(flow_body("\n".join(f"- `{u}`" for u in urls), S))

    story.append(p("How it connects with other features", S["h2"]))
    story.append(p(
        f"Declared dependency line from the spec header: <b>Depends on: {esc(depends)}</b>.",
        S["body"],
    ))
    story.append(p(
        "ROADMAP.md build order (shared across the project): vision (00) feeds design (01) and architecture (16); "
        "architecture feeds data model (17); order lifecycle (12) feeds payments (13) then delivery (14); "
        "vendor onboarding (08) feeds storefront (09) and dashboard (10); notifications (15) support onboarding and fulfilment; "
        "devops (20) and testing (21) run in parallel from day one.",
        S["body"],
    ))
    story.append(PageBreak())

    # 5 How to run
    story.append(p("5. How to run / exercise this feature", S["h1"]))
    story.append(p(
        "Important: this repository is a <b>specification pack</b>, not a finished website you can start with "
        "`npm start` today. “Running” a feature means: implement the tasks, deploy to the staging environment "
        "described in modules 20 and 16, then follow validate.md.",
        S["note"],
    ))
    story.append(p("Before you start", S["h2"]))
    story.extend(flow_body(
        "- Read OPEN-QUESTIONS.md blockers if the feature touches money, fees, or legal.\n"
        f"- Finish dependency modules listed as: {depends}\n"
        "- Have staging ready (20-devops-and-infrastructure): API, web, database migrations, secrets.\n"
        "- For payment/SMS tests, use sandbox/test mode only (stated in several validate.md files).\n"
        f"- Open `{folder}/task.md` and work tasks in dependency order.",
        S,
    ))
    story.append(p("What output to expect", S["h2"]))
    story.append(p(
        "Expected output is whatever each V- check’s Pass criteria describes (section 6). "
        "Examples from other modules include: API JSON grouped by vendor, a UI banner, a PAID order after webhook, "
        "or a document/sign-off. Use only the Pass criteria written for THIS module.",
        S["body"],
    ))
    story.append(PageBreak())

    # 6 Validate
    story.append(p("6. How to test and validate (from validate.md)", S["h1"]))
    story.append(p(
        "Validation is the official proof. Matching rule from README: task T-xx-yy is Done only when V-xx-yy passes "
        "(usually in staging).",
        S["body"],
    ))
    for h, body in mod["val_sections"]:
        story.append(p(h, S["h2"]))
        story.extend(flow_body(body, S))

    if mod["val_details"]:
        story.append(p("Detailed validation steps (from source)", S["h2"]))
        for title, body in mod["val_details"]:
            block = [p(title, S["h3"])]
            block.extend(flow_body(body, S))
            story.append(KeepTogether(block))

    # sign-off leftover
    if "## Module sign-off" in mod["val"] or "Module sign-off" in mod["val"]:
        story.append(p("Module sign-off", S["h2"]))
        after = mod["val"].split("Module sign-off", 1)[-1]
        story.extend(flow_body(after.strip(), S))

    story.append(PageBreak())

    # 7 Errors
    story.append(p("7. Common errors and how to fix them", S["h1"]))
    story.append(p(
        "The list below is built only from this module’s Edge cases and validation failure scenarios — "
        "not from guessed bugs.",
        S["small"],
    ))
    if errors:
        for err, fix in errors:
            story.append(p(f"<b>Situation:</b> {err}", S["bullet"]))
            story.append(p(f"<b>What the docs say / how to handle:</b> {fix}", S["bullet"]))
            story.append(Spacer(1, 0.08 * cm))
    else:
        story.append(p(
            "This module’s docs do not list a long Edge cases section. Use the Pass criteria in validate.md: "
            "if a check fails, re-read the matching task’s Done-when notes and fix until the criteria match.",
            S["body"],
        ))

    story.append(p("General beginner fixes (still grounded in project rules)", S["h2"]))
    story.extend(flow_body(
        "- Validation fails in local only — README requires staging for Done; redeploy and re-run V- checks.\n"
        "- Payment looks paid in browser but order not PAID — confirm via signed webhook (modules 06/13), not redirect alone.\n"
        "- Wrong money amounts — store money as integer paise (module 16).\n"
        "- Vendor sees another vendor’s data — fix RLS / vendor_id (modules 16/17) and keep V-16-04 green.\n"
        "- Forgot to update TRACKER.md — a task is not tracked Done until the matching V- check passes and the tracker is updated.",
        S,
    ))

    story.append(Spacer(1, 0.4 * cm))
    story.append(p(
        f"End of guide for {folder}. Always prefer the live markdown files if anything conflicts with this PDF.",
        S["note"],
    ))

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title=f"{num} {nice} — Feature Guide",
        author="Generated from Fashion Jewellery Marketplace specifications",
    )
    doc.module_label = f"{num} · {nice}"
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return out_path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    folders = sorted(
        [p for p in ROOT.iterdir() if p.is_dir() and re.match(r"^\d{2}-", p.name)],
        key=lambda p: p.name,
    )
    if len(folders) != 25:
        raise SystemExit(f"Expected 25 feature folders, found {len(folders)}: {[f.name for f in folders]}")

    S = styles()
    names = [f.name for f in folders]
    written = []
    for folder in folders:
        mod = load_module(folder)
        path = build_pdf(mod, names, S)
        size = path.stat().st_size
        print(f"OK {path.name} ({size} bytes)")
        if size < 1000:
            raise SystemExit(f"PDF too small: {path}")
        written.append(path.name)

    # Verification report
    pdfs = sorted(OUT_DIR.glob("*.pdf"))
    print("---")
    print(f"Generated: {len(pdfs)} PDFs in {OUT_DIR}")
    expected_nums = {f"{i:02d}" for i in range(25)}
    got_nums = {p.name[:2] for p in pdfs}
    missing = sorted(expected_nums - got_nums)
    extra = sorted(got_nums - expected_nums)
    if missing:
        raise SystemExit(f"MISSING feature numbers: {missing}")
    if extra:
        raise SystemExit(f"UNEXPECTED PDFs: {extra}")
    if len(pdfs) != 25:
        raise SystemExit(f"Count mismatch: {len(pdfs)}")
    print("VERIFICATION PASSED: all 25 feature PDFs present and non-empty.")
    for p in pdfs:
        print(f"  - {p.name} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
