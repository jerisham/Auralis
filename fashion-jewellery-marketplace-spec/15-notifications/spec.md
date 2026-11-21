# 15 — Notifications

**Phase:** P1 · **Depends on:** 12, 16 · **Status:** Draft

## 1. Purpose
Tell the right person, on the right channel, at the right moment — especially vendors, who must act on new orders quickly. One notification service, template-driven, triggered by domain events.

## 2. Channels
| Channel | Provider (examples) | Notes |
|---|---|---|
| WhatsApp | Meta WhatsApp Business Platform (Cloud API) or a BSP | Business-initiated messages need **pre-approved templates**; opt-in required |
| SMS | DLT-registered provider | India requires sender ID + template registration on DLT before sending |
| Email | Azure Communication Services / SES / SendGrid | SPF, DKIM, DMARC on sending domain |
| Web push / app push | Web Push (VAPID) now; FCM/APNs in 24 | Opt-in prompt after first order, not on first visit |
| In-app inbox | Own | Bell icon in vendor portal, admin, customer account |

## 3. Event matrix (MVP)
| Event | Customer | Vendor | Admin |
|---|---|---|---|
| Order paid | WhatsApp + email (confirmation, per-vendor packages) | **WhatsApp + email + push + inbox** ("New order #… — accept within 24 h") | — |
| Accept SLA 50% / 90% | — | WhatsApp + push | 90%: inbox |
| Vendor accepted | (silent, timeline only) | — | — |
| Vendor rejected / SLA cancel | WhatsApp + email (refund info) | WhatsApp + email (strike info) | inbox |
| Dispatched | WhatsApp + email (tracking link) | — | — |
| Out for delivery | WhatsApp (P2 incl. OTP) | — | — |
| Delivered | WhatsApp (+ review ask after 24 h) | inbox | — |
| Payout released (T1/T2) | — | WhatsApp + email | — |
| Claim opened | email | WhatsApp + email + inbox | — |
| Claim escalated / decided | WhatsApp + email | WhatsApp + email | inbox |
| Low stock | — | WhatsApp (daily digest) + inbox | — |
| Vendor application state change | — | WhatsApp + email | inbox (new submission) |
| Reconciliation mismatch / failed transfer | — | — | email + inbox (Finance) |
| OTP | SMS (WhatsApp fallback) | SMS | — |

## 4. Vendor new-order message content
WhatsApp: order no., items + qty, amount, **customer name, city/PIN**, deadline, button "View & accept" (deep link).
Full customer **phone and address** are shown in the vendor portal and on the packing slip (needed to deliver), not in chat messages — limits personal-data spread (18). Configurable if pilot vendors strongly prefer full address in WhatsApp.

## 5. Functional requirements
| ID | Requirement |
|---|---|
| FR-15-01 | Templates per event × channel × language, versioned, editable in admin (11); variables validated. |
| FR-15-02 | Preferences: users choose channels per category (transactional cannot be fully disabled — at least one channel stays on). |
| FR-15-03 | Delivery tracking: status per message (queued, sent, delivered, read, failed); retries with backoff; fallback channel on failure (WhatsApp → SMS). |
| FR-15-04 | Quiet hours 22:00–08:00 IST for non-urgent (marketing, digests); order alerts to vendors always sent. |
| FR-15-05 | Marketing messages only with explicit opt-in; unsubscribe link/keyword honoured. |
| FR-15-06 | Idempotency: same event ID never produces duplicate messages. |
