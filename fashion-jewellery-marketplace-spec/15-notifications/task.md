# Tasks — 15 Notifications

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-15-01 | Notification service: event consumer, template rendering, channel router, idempotency, status tracking | T-16-05 | L | Todo |
| T-15-02 | SMS (DLT registration + provider) and WhatsApp (business verification, number, template approvals) setup | Q-01 | M | Todo |
| T-15-03 | Email provider + domain authentication (SPF/DKIM/DMARC) + branded HTML templates | T-01-01 | M | Todo |
| T-15-04 | Web push + in-app inbox (customer, vendor, admin) | T-15-01 | M | Todo |
| T-15-05 | Wire all events in §3 matrix | T-12-04, T-15-01 | M | Todo |
| T-15-06 | Preferences UI + quiet hours + opt-in/unsubscribe | T-15-01 | S | Todo |
| T-15-07 | Retries, fallback channel, failure alerts | T-15-01 | S | Todo |

---

### T-15-01 — Service
- **Done when:** Given an event, correct template(s) rendered and queued per recipient prefs; duplicate event ignored.

### T-15-02 — SMS & WhatsApp onboarding
- **Steps:** Register entity, sender ID, templates on DLT; verify Meta Business; submit WhatsApp templates (one per event) for approval.
- **Done when:** All MVP templates approved on both platforms.

### T-15-03 — Email
- **Done when:** Mail-tester score ≥ 9/10; templates render well in Gmail, Outlook, iOS Mail (light/dark).

### T-15-04 — Push & inbox
- **Done when:** Opt-in after first order; inbox unread counter; mark read.

### T-15-05 — Event wiring
- **Done when:** Every matrix cell implemented and covered by a test.

### T-15-06 — Preferences
- **Done when:** FR-15-02, 04, 05 enforced.

### T-15-07 — Reliability
- **Done when:** Failed WhatsApp falls back to SMS within 2 min; persistent failures alert ops.
