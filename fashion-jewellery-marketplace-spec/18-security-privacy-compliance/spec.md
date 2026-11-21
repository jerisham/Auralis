# 18 — Security, Privacy & Compliance

**Phase:** P0 (rules) / P1 (audit) · **Depends on:** 16, 17 · **Status:** Draft
> Not legal advice. A lawyer and a CA must review the compliance items before pilot launch.

## 1. Purpose
Protect customers' and vendors' money and data, and meet Indian legal obligations for an e-commerce marketplace.

## 2. Compliance checklist (India, to confirm with lawyer/CA)
| Area | Obligation (summary) | Where handled |
|---|---|---|
| Consumer Protection (E-Commerce) Rules, 2020 | Display seller name, address, contact; return/refund/exchange policies; grievance officer with contact details; acknowledge complaints quickly and resolve within prescribed time; no manipulation of prices or fake reviews | 05, 07, 09, 11, footer |
| IT Act 2000 & intermediary rules | Terms of use, privacy policy, grievance mechanism, takedown process | Legal pages, 11 |
| Digital Personal Data Protection Act, 2023 + Rules | Notice & consent, purpose limitation, data-principal rights (access, correction, erasure, grievance), breach notification, reasonable security safeguards | 03, this module |
| GST | Commission invoices with GST; TCS collection & returns as e-commerce operator; vendor GST rules | 13 |
| Income-tax s.194-O | TDS on e-commerce participants' sales | 13 |
| Payments | Use RBI-authorised payment aggregator; no storage of card data | 13 |
| SMS / WhatsApp | TRAI DLT registration; WhatsApp opt-in & template rules | 15 |
| Legal Metrology (packaged goods) | MRP, country of origin, manufacturer/packer details shown for listings | 05, 10 product form |
| Product claims | No "gold/silver/hallmark" claims; skin-safety declarations by seller | 04, 08, 11 |

## 3. Security requirements
| ID | Requirement |
|---|---|
| SEC-01 | TLS 1.2+ everywhere; HSTS; Front Door WAF with OWASP rule set. |
| SEC-02 | OWASP ASVS Level 2 as baseline for API and web. |
| SEC-03 | Secrets only in Key Vault; managed identities; no secrets in repo (secret scanning in CI). |
| SEC-04 | Encryption at rest (managed); **field-level encryption** for KYC document refs, bank details, phone numbers in exports. |
| SEC-05 | Admin: mandatory 2FA, IP-logging, least-privilege roles (11), session timeout. |
| SEC-06 | RLS tenant isolation (16) + authorization tests on every endpoint. |
| SEC-07 | Input validation, output encoding, CSP headers, no vendor HTML. |
| SEC-08 | Uploads: type sniffing, size limits, AV scan, EXIF strip, private originals. |
| SEC-09 | Rate limiting, bot protection on OTP, login, checkout, reviews. |
| SEC-10 | Dependency scanning (Dependabot), SAST (CodeQL), container image scanning, IaC scanning (tfsec/Checkov). |
| SEC-11 | Audit logs for admin and money actions; retained ≥ 8 years for finance records (confirm). |
| SEC-12 | Incident response runbook; breach notification process per DPDP. |
| SEC-13 | Annual third-party penetration test; one before public launch. |

## 4. Privacy design
- Data minimisation: vendors see customer name, phone, address **only for their own orders** and only until order closes + 30 days; afterwards masked in vendor UI.
- Customer phone shown to vendor masked in lists; full on order detail/packing slip only.
- Consent records for marketing (WhatsApp/email), with timestamps.
- Data map: what personal data, where stored, purpose, retention, processor (gateway, KYC, messaging).
- Privacy policy and in-product notices written in plain language.

## 5. Fraud controls
- Velocity checks on accounts/devices/cards/UPI IDs; high-claim customers flagged (07).
- Vendor fraud: fake tracking (14), self-purchase to boost reviews (same phone/address/device as vendor → reviews excluded), off-platform payment requests (strike policy, 11).
