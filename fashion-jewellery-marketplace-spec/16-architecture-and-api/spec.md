# 16 — Architecture & API

**Phase:** P0 · **Depends on:** 00 · **Status:** Draft (recommendations — confirm in T-16-01)

## 1. Principles
1. **API-first** — web and future mobile apps are clients of the same versioned API.
2. **Modular monolith** for MVP — one deployable backend split into modules that mirror these spec folders (identity, catalog, cart, orders, payments, delivery, notifications, vendor, admin). Extract services later only where scale demands.
3. **Multi-tenant by `vendor_id`**, enforced in the database (PostgreSQL Row-Level Security), not only in code.
4. **Events for side-effects** — transactional outbox + queue; idempotent consumers.
5. **Managed services** over self-hosted wherever possible (small team).

## 2. Recommended stack
| Layer | Choice | Why |
|---|---|---|
| Web (customer, vendor, admin) | **Next.js (React, TypeScript)**, SSR/ISR for SEO pages; PWA | SEO for product pages, shared React components |
| Mobile (P3) | **React Native (Expo)** | Reuses TypeScript, API client, design tokens |
| Backend API | **NestJS (TypeScript)** or .NET 8 — pick one in T-16-01 | Structured modules, OpenAPI generation |
| Database | **PostgreSQL 16** (Azure Database for PostgreSQL Flexible Server) | Relational money/order data, RLS, JSONB for attributes |
| Cache / rate limit / locks | **Redis** (Azure Cache for Redis) | Sessions, rate limits, hot catalog data |
| Queue & scheduler | Azure Service Bus (scheduled messages) or BullMQ on Redis | Events, timers (12) |
| Search | **Meilisearch** (simple, typo-tolerant) or Azure AI Search | Facets, synonyms (04) |
| Media | Azure Blob Storage + **Azure Front Door CDN**; image processing worker (sharp) producing WebP/AVIF sizes | Fast images worldwide |
| Secrets | Azure Key Vault | Gateway keys, API keys |
| Observability | OpenTelemetry → Azure Monitor / App Insights | Traces, metrics, logs |
| Hosting | **Azure Container Apps** (API, workers, web) | Scales to zero, simpler than AKS for MVP |
| IaC / CI/CD | **Terraform** + GitHub Actions | See 20 |

## 3. Logical architecture
```
[Customer PWA]  [Vendor portal]  [Admin portal]  [Mobile apps (P3)]
        \             |               |               /
         └──── Azure Front Door (CDN, WAF, TLS) ─────┘
                         |
              Next.js web (SSR)  ──►  API (modular monolith, /v1)
                                         |  ├─ identity   ├─ catalog   ├─ cart
                                         |  ├─ orders     ├─ payments  ├─ delivery
                                         |  ├─ vendor     ├─ admin     └─ notifications
                     ┌───────────────────┼──────────────────────┐
                PostgreSQL           Redis              Service Bus / queue
               (RLS, outbox)                                  |
                                                     Workers: notifications, search indexer,
                                                     media processor, timers, reconciliation
External: Payment gateway (split) · KYC API · Tracking aggregator · WhatsApp/SMS/Email · Search
```

## 4. API conventions
- REST, JSON, base `/v1`; OpenAPI 3.1 generated from code and published; typed client generated for web & mobile.
- Auth: Bearer JWT (15 min) + rotating refresh token (03). Claims: `sub`, `roles[]`, `vendor_id?`, `admin_role?`.
- Resource naming plural nouns; actions as sub-resources (`POST /vendor-orders/{id}/dispatch`).
- Pagination: cursor-based (`?cursor=&limit=`), max 100.
- Errors: RFC 9457 problem+json `{type,title,status,detail,code,errors[]}`.
- **Idempotency-Key** header required on POSTs that create orders, payments, refunds, transitions.
- Money: integer paise + `currency: "INR"`. Time: ISO-8601 UTC; display in IST.
- Rate limits per IP and per user (Redis); 429 with `Retry-After`.
- Webhooks inbound (gateway, tracking, WhatsApp) at `/webhooks/<provider>`, signature verified, stored raw, processed async.

## 5. Multi-tenancy
- Vendor-owned tables carry `vendor_id`. API sets `SET app.vendor_id = '<id>'` per request transaction; RLS policies restrict SELECT/UPDATE/DELETE to that vendor for vendor-role connections.
- Admin and system workers use a separate DB role with explicit, audited bypass.
- Tests prove cross-tenant access is impossible even with a buggy query.

## 6. Media pipeline
Client requests signed upload URL → uploads original to `media-originals` → event → worker validates (type, dimensions ≥ 1200 px, size ≤ 15 MB images / 50 MB video), strips EXIF, generates 200/400/800/1200 px WebP + AVIF → public container via CDN. Video transcoded to H.264/WebM ≤ 15 s.

## 7. Config & feature flags
Runtime config table + cache (SLA hours, return window, commission rules, ranking weights); feature flags (per environment, per vendor %) for gradual rollout.
