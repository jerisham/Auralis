#!/usr/bin/env python3
"""Generate TECH_STACK.pdf from modules 16, 20, and 24 specifications."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
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
OUT = ROOT / "TECH_STACK.pdf"

NAVY = colors.HexColor("#1A1A2E")
GOLD = colors.HexColor("#8B7355")
SOFT = colors.HexColor("#F4F1EB")
DARK = colors.HexColor("#2C2C34")
MUTED = colors.HexColor("#5C5660")
WARN = colors.HexColor("#FFF4E5")
CODE_BG = colors.HexColor("#F0EEEA")
LINE = colors.HexColor("#D9D3C8")


def esc(t: str) -> str:
    return (
        t.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def styles():
    base = getSampleStyleSheet()
    return {
        "cover": ParagraphStyle(
            "cover", parent=base["Title"], fontName="Helvetica-Bold", fontSize=22,
            leading=28, textColor=NAVY, alignment=TA_CENTER, spaceAfter=10,
        ),
        "sub": ParagraphStyle(
            "sub", parent=base["Normal"], fontName="Helvetica", fontSize=10.5,
            leading=14, textColor=MUTED, alignment=TA_CENTER, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=14,
            leading=18, textColor=NAVY, spaceBefore=14, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5,
            leading=15, textColor=DARK, spaceBefore=10, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
            leading=13, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["Normal"], fontName="Helvetica", fontSize=9.5,
            leading=12.5, textColor=DARK, leftIndent=4, spaceAfter=2,
        ),
        "note": ParagraphStyle(
            "note", parent=base["Normal"], fontName="Helvetica-Oblique", fontSize=9,
            leading=12, textColor=MUTED, spaceAfter=8, backColor=WARN, borderPadding=6,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Code"], fontName="Courier", fontSize=7.5,
            leading=10, textColor=DARK, backColor=CODE_BG, leftIndent=2,
            spaceBefore=4, spaceAfter=8,
        ),
        "cell": ParagraphStyle(
            "cell", parent=base["Normal"], fontName="Helvetica", fontSize=8,
            leading=11, textColor=DARK,
        ),
        "cell_h": ParagraphStyle(
            "cell_h", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=8,
            leading=11, textColor=NAVY,
        ),
        "small": ParagraphStyle(
            "small", parent=base["Normal"], fontName="Helvetica", fontSize=8,
            leading=11, textColor=MUTED, spaceAfter=4, alignment=TA_CENTER,
        ),
    }


def p(text: str, style) -> Paragraph:
    return Paragraph(esc(text), style)


def bullets(items, style):
    return ListFlowable(
        [ListItem(Paragraph(esc(i), style), leftIndent=12, value="bullet") for i in items],
        bulletType="bullet",
        start="•",
    )


def table(rows, widths):
    S = styles()
    data = []
    for i, r in enumerate(rows):
        st = S["cell_h"] if i == 0 else S["cell"]
        data.append([Paragraph(esc(c), st) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), SOFT),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF8F5")]),
    ]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(1.5 * cm, A4[1] - 1.1 * cm, A4[0] - 1.5 * cm, A4[1] - 1.1 * cm)
    canvas.line(1.5 * cm, 1.1 * cm, A4[0] - 1.5 * cm, 1.1 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(1.5 * cm, A4[1] - 0.9 * cm, "Fashion Jewellery Marketplace")
    canvas.drawRightString(A4[0] - 1.5 * cm, A4[1] - 0.9 * cm, "TECH_STACK")
    canvas.drawCentredString(A4[0] / 2, 0.7 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    S = styles()
    story = []
    usable = A4[0] - 3 * cm

    story.append(Spacer(1, 1.5 * cm))
    story.append(p("Tech Stack Guide", S["cover"]))
    story.append(p("Fashion Jewellery Marketplace", S["sub"]))
    story.append(p(
        "Planned technologies for frontend, backend, database, hosting, and related tools — "
        "with simple reasons for each choice.",
        S["sub"],
    ))
    story.append(Spacer(1, 0.4 * cm))
    story.append(p(
        "Source of truth: 16-architecture-and-api/spec.md, 20-devops-and-infrastructure/spec.md, "
        "and 24-mobile-apps/spec.md. Status is Draft / recommendations — backend framework "
        "must still be confirmed in task T-16-01.",
        S["note"],
    ))
    story.append(PageBreak())

    # Overview
    story.append(p("1. Big picture (simple English)", S["h1"]))
    story.append(p(
        "We build one shared API. Three websites talk to it: the customer shop, the vendor portal, "
        "and the admin portal. Later, phone apps use the same API. For the first launch (MVP), "
        "the backend is one deployable application split into clear modules — not dozens of "
        "microservices. Prefer managed cloud services so a small team does not run servers by hand.",
        S["body"],
    ))
    story.append(p("Architecture principles (from module 16)", S["h2"]))
    story.append(bullets([
        "<b>API-first</b> — web and future mobile apps are clients of the same versioned API (/v1).",
        "<b>Modular monolith for MVP</b> — one backend with modules: identity, catalog, cart, orders, payments, delivery, notifications, vendor, admin.",
        "<b>Multi-tenant by vendor_id</b> — enforced in PostgreSQL with Row-Level Security (RLS), not only in app code.",
        "<b>Events for side-effects</b> — transactional outbox + queue; consumers must be idempotent (safe if run twice).",
        "<b>Managed services first</b> — use cloud-managed tools wherever possible.",
    ], S["bullet"]))
    story.append(PageBreak())

    # Recommended stack table
    story.append(p("2. Recommended stack at a glance", S["h1"]))
    story.append(p(
        "This table is copied from the recommended stack in 16-architecture-and-api/spec.md §2.",
        S["small"],
    ))
    story.append(table([
        ["Layer", "Choice", "Why it was chosen"],
        [
            "Web (customer, vendor, admin)",
            "Next.js (React, TypeScript), SSR/ISR; PWA",
            "SEO for product pages; shared React components; installable website before native apps",
        ],
        [
            "Mobile (Phase 3)",
            "React Native (Expo)",
            "Reuses TypeScript, API client, and design tokens — no backend rewrite",
        ],
        [
            "Backend API",
            "NestJS (TypeScript) OR .NET 8 — pick in T-16-01",
            "Structured modules and OpenAPI generation",
        ],
        [
            "Database",
            "PostgreSQL 16 (Azure Database for PostgreSQL Flexible Server)",
            "Strong for money/orders; RLS for vendor isolation; JSONB for product attributes",
        ],
        [
            "Cache / rate limits / locks",
            "Redis (Azure Cache for Redis)",
            "Sessions, rate limits, hot catalog data",
        ],
        [
            "Queue & scheduler",
            "Azure Service Bus OR BullMQ on Redis",
            "Background events and timers (order lifecycle)",
        ],
        [
            "Search",
            "Meilisearch OR Azure AI Search",
            "Facets, synonyms, typo-tolerant search (catalog)",
        ],
        [
            "Media",
            "Azure Blob Storage + Azure Front Door CDN; sharp worker (WebP/AVIF)",
            "Fast product images worldwide",
        ],
        [
            "Secrets",
            "Azure Key Vault",
            "Gateway keys and API keys stay out of code",
        ],
        [
            "Observability",
            "OpenTelemetry → Azure Monitor / App Insights",
            "Traces, metrics, and logs in one place",
        ],
        [
            "Hosting",
            "Azure Container Apps (API, workers, web)",
            "Scales to zero; simpler than Kubernetes (AKS) for MVP",
        ],
        [
            "IaC / CI/CD",
            "Terraform + GitHub Actions",
            "Repeatable environments and safe deployments (see module 20)",
        ],
    ], [3.8 * cm, 6.2 * cm, usable - 10 * cm]))
    story.append(PageBreak())

    # Frontend deep dive
    story.append(p("3. Frontend", S["h1"]))
    story.append(p("Web — Next.js + React + TypeScript", S["h2"]))
    story.append(p(
        "Next.js is the framework for the customer shop, vendor portal, and admin portal. "
        "It uses React for UI and TypeScript for safer code. SSR (Server-Side Rendering) and "
        "ISR (Incremental Static Regeneration) help product and catalog pages rank in Google. "
        "The site is also a PWA (Progressive Web App), so customers can add it to their phone "
        "home screen before native apps exist.",
        S["body"],
    ))
    story.append(p("Mobile — React Native with Expo (Phase 3)", S["h2"]))
    story.append(p(
        "When native apps ship (module 24), they use React Native with Expo. Customer app first; "
        "a lighter vendor app second (orders, dispatch, push alerts). Full catalog management "
        "stays on the web. Apps share packages/api-client, validation schemas, and design tokens "
        "from the monorepo. Crash reporting: Sentry. Push: FCM/APNs. OTA JS fixes via Expo EAS Update.",
        S["body"],
    ))
    story.append(PageBreak())

    # Backend
    story.append(p("4. Backend & API", S["h1"]))
    story.append(p(
        "The API is a modular monolith: one deployable service with internal modules that match "
        "the feature folders. Clients call REST JSON endpoints under /v1. OpenAPI 3.1 is generated "
        "from code; typed clients are generated for web and mobile.",
        S["body"],
    ))
    story.append(p("Still to decide", S["h2"]))
    story.append(p(
        "Backend framework is NestJS (TypeScript) or .NET 8. The team must pick one in task T-16-01. "
        "Both options were listed because they support clear modules and OpenAPI well.",
        S["note"],
    ))
    story.append(p("API conventions (from module 16)", S["h2"]))
    story.append(bullets([
        "Auth: Bearer JWT (15 min) + rotating refresh token.",
        "Claims include sub, roles[], optional vendor_id, optional admin_role.",
        "Cursor pagination (?cursor=&limit=), max 100.",
        "Errors: RFC 9457 problem+json.",
        "Idempotency-Key required on POSTs that create orders, payments, refunds, or state transitions.",
        "Money: integer paise + currency INR. Time: ISO-8601 UTC; display in IST.",
        "Rate limits per IP and per user via Redis; HTTP 429 with Retry-After.",
        "Inbound webhooks at /webhooks/<provider> — signature verified, stored raw, processed async.",
    ], S["bullet"]))
    story.append(PageBreak())

    # Data layer
    story.append(p("5. Database & supporting data stores", S["h1"]))
    story.append(p("PostgreSQL 16", S["h2"]))
    story.append(p(
        "Main database for users, products, orders, and money. Hosted as Azure Database for "
        "PostgreSQL Flexible Server. Chosen because marketplace data is relational, money must "
        "be exact, and Row-Level Security can enforce that one vendor cannot read another "
        "vendor’s rows even if application code has a bug. JSONB stores flexible product attributes.",
        S["body"],
    ))
    story.append(p("Redis", S["h2"]))
    story.append(p(
        "Used for sessions, rate limiting, locks, and hot catalog cache — not as the source of "
        "truth for money or orders.",
        S["body"],
    ))
    story.append(p("Search engine", S["h2"]))
    story.append(p(
        "Meilisearch (simple, typo-tolerant) or Azure AI Search. Supports facets and synonyms "
        "needed by catalog & discovery (module 04). Final choice is an ADR / open decision.",
        S["body"],
    ))
    story.append(PageBreak())

    # Infra
    story.append(p("6. Cloud, hosting, CI/CD, workers", S["h1"]))
    story.append(p(
        "Cloud platform is Azure. Module 20 lists environments: dev, preview (per PR), staging, prod.",
        S["body"],
    ))
    story.append(p("Key Azure resources (per environment)", S["h2"]))
    story.append(bullets([
        "Azure Container Apps: web, api, and workers (notifications, media, search, timers, reconciliation)",
        "Azure Container Registry for images",
        "PostgreSQL Flexible Server; Redis; Service Bus",
        "Storage: media-originals (private), media-public (CDN), exports (private)",
        "Azure Front Door Premium: CDN + WAF + TLS + custom domains",
        "Key Vault + managed identities (no long-lived secrets in apps)",
        "Log Analytics + Application Insights",
        "Terraform modules define infrastructure as code",
        "GitHub Actions for CI/CD; OIDC federation to Azure",
    ], S["bullet"]))
    story.append(p("Logical architecture diagram (from module 16)", S["h2"]))
    diagram = """[Customer PWA]  [Vendor portal]  [Admin portal]  [Mobile apps (P3)]
        \\             |               |               /
         └──── Azure Front Door (CDN, WAF, TLS) ─────┘
                         |
              Next.js web (SSR)  ──►  API (modular monolith, /v1)
                                         |  identity · catalog · cart
                                         |  orders · payments · delivery
                                         |  vendor · admin · notifications
                     ┌───────────────────┼──────────────────────┐
                PostgreSQL           Redis              Service Bus / queue
               (RLS, outbox)                                  |
                                                     Workers: notifications, search,
                                                     media, timers, reconciliation
External: Payment gateway · KYC · Tracking · WhatsApp/SMS/Email · Search"""
    story.append(Preformatted(diagram, S["code"]))
    story.append(PageBreak())

    # External
    story.append(p("7. External services", S["h1"]))
    story.append(p(
        "These are not frameworks we build, but they are part of the planned system:",
        S["body"],
    ))
    story.append(bullets([
        "Payment gateway with split payments / linked vendor accounts",
        "KYC API (vendor identity checks)",
        "Tracking aggregator (shipment tracking)",
        "WhatsApp / SMS / Email providers (OTP and order alerts)",
        "Search engine (Meilisearch or Azure AI Search)",
    ], S["bullet"]))

    story.append(p("8. What is still open", S["h1"]))
    story.append(table([
        ["Decision", "Options", "Where decided"],
        ["Backend framework", "NestJS (TypeScript) or .NET 8", "T-16-01"],
        ["Search product", "Meilisearch or Azure AI Search", "Architecture ADR / module 16 & 20"],
        ["Queue product", "Azure Service Bus or BullMQ on Redis", "Module 16 recommended stack"],
    ], [4.2 * cm, 6.5 * cm, usable - 10.7 * cm]))

    story.append(Spacer(1, 0.5 * cm))
    story.append(p("9. Beginner glossary", S["h1"]))
    story.append(table([
        ["Term", "Simple meaning"],
        ["API", "The backend door that apps and websites call to read/write data"],
        ["SSR / ISR", "Server builds (or refreshes) page HTML — good for SEO and speed"],
        ["PWA", "Website that can sit on a phone home screen like an app"],
        ["Modular monolith", "One backend app, organised into clear internal modules"],
        ["RLS", "Database rules so Vendor A cannot see Vendor B’s rows"],
        ["JWT", "Short-lived login token the API gives after authentication"],
        ["OpenAPI", "Machine-readable list of all API endpoints"],
        ["CDN", "Copies of files (images) served from locations closer to users"],
        ["WAF", "Web Application Firewall — blocks common web attacks at the edge"],
        ["IaC (Terraform)", "Cloud resources described in code and applied repeatably"],
        ["Sandbox", "Test mode for payments/SMS — not real customer money"],
    ], [4.0 * cm, usable - 4.0 * cm]))

    story.append(Spacer(1, 0.6 * cm))
    story.append(p(
        "End of TECH_STACK.pdf. If this PDF and the markdown specs disagree, trust "
        "16-architecture-and-api/spec.md, 20-devops-and-infrastructure/spec.md, and "
        "24-mobile-apps/spec.md.",
        S["note"],
    ))

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title="TECH_STACK — Fashion Jewellery Marketplace",
        author="Generated from project specifications",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
