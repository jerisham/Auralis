# 19 — Non-functional Requirements & Analytics

**Phase:** P0–P1 · **Depends on:** 16, 20 · **Status:** Draft

## 1. Performance
| Metric | Target (mobile, mid-range Android, 4G) |
|---|---|
| LCP | ≤ 2.5 s (home, PLP, PDP, store) |
| INP | ≤ 200 ms |
| CLS | ≤ 0.1 |
| JS per route (gzip) | ≤ 200 KB customer routes |
| API p95 | ≤ 300 ms reads, ≤ 600 ms writes; checkout create ≤ 1 s |
| Search suggest | ≤ 150 ms p95 |
| Image | WebP/AVIF, responsive `srcset`, lazy below fold |

## 2. Scalability & availability
- Launch capacity: 50k MAU, 2k orders/day, 50 RPS sustained, 300 RPS peak (sale days) — autoscaling verified by load test at 2× peak.
- Availability target 99.9% monthly for customer and vendor apps; payment webhooks must never be dropped (queue + retries).
- RPO ≤ 5 min, RTO ≤ 1 h (17, 20).

## 3. Accessibility
WCAG 2.2 AA across all portals: keyboard navigation, focus visible, alt text required for product images (vendor form prompts; auto-suggested), captions not needed for silent video, contrast per 01.

## 4. Internationalisation
English at launch; all UI strings in i18n files from day 1; Hindi & Tamil ready (Q-13); INR formatting `en-IN`; dates in IST.

## 5. Browser/device support
Last 2 versions of Chrome, Safari (iOS 16+), Edge, Firefox, Samsung Internet; min width 320 px.

## 6. Observability
- Structured logs with request ID, user/vendor ID (hashed), no PII.
- Traces across web → API → DB → queue → worker (OpenTelemetry).
- Dashboards: golden signals per service; business health (orders/min, payment success %, webhook lag, notification delivery %).
- Alerts (to on-call via email/phone/Teams): payment success < 90% over 15 min; webhook processing lag > 5 min; error rate > 2%; queue DLQ > 0; reconciliation mismatch.

## 7. Product analytics
Privacy-friendly analytics (e.g., PostHog self-hosted or GA4 with consent mode). Core events:

| Event | Key properties |
|---|---|
| `page_view` | route, referrer, utm_*, session_id |
| `intro_start/skip/complete/cta` | variant |
| `search` | query, results_count |
| `filter_apply` | filter, value |
| `product_view` | product_id, vendor_id, price |
| `add_to_cart` / `remove_from_cart` | variant_id, vendor_id, qty |
| `look_add_all` | look_id, items |
| `checkout_start` / `payment_success` / `payment_fail` | order_id, amount, vendors_count |
| `vendor_order_accepted/dispatched/delivered` | vendor_id, minutes_since_paid |
| `claim_opened` | type |
| `review_submitted` | rating |
| `vendor_onboarding_step` | step, duration |
| `product_published` / `product_unpublished` | product_id, vendor_id |
| `vendor_nps_submitted` | vendor_id, score |

Funnels: visit → PDP → add to cart → checkout → paid; vendor signup → approved → first order.
KPI definitions from 00 §8 computed from these events + DB.
