# Tasks — 18 Security, Privacy & Compliance

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-18-01 | Legal review: Terms, Privacy, Returns, Seller Agreement, Prohibited items, grievance officer | Q-17 | M | Todo |
| T-18-02 | Threat model (STRIDE) for checkout, payouts, vendor portal, admin | T-16-01 | S | Todo |
| T-18-03 | Field-level encryption & PII tagging; masking rules in vendor UI | T-17-02 | M | Todo |
| T-18-04 | Security headers, CSP, WAF rules, rate limits, bot protection | T-20-03 | M | Todo |
| T-18-05 | CI security scanning (SAST, deps, containers, IaC, secrets) | T-20-02 | S | Todo |
| T-18-06 | Data map, retention schedule, deletion/export jobs (with 03) | T-18-03 | M | Todo |
| T-18-07 | Fraud rules (velocity, self-purchase detection, high-claim flag) | T-12-04 | M | Todo |
| T-18-08 | Incident response & breach notification runbook | — | S | Todo |
| T-18-09 | External penetration test + fix findings | M5 | M | Todo |
| T-18-10 | Compliance checklist sign-off (§2) | T-18-01 | S | Todo |

---

### T-18-01 — Legal docs
- **Done when:** Lawyer-reviewed documents published; versioned; acceptance tracked.

### T-18-02 — Threat model
- **Done when:** Document lists threats, mitigations, owners; high risks have tasks.

### T-18-03 — Encryption & masking
- **Done when:** Encrypted columns via app-level crypto with keys in Key Vault; vendor UI masks per §4 after order closure + 30 days.

### T-18-04 — Edge security
- **Done when:** securityheaders.com grade A; WAF in prevention mode in prod.

### T-18-05 — Scanning
- **Done when:** PRs blocked on high/critical findings.

### T-18-06 — Data lifecycle
- **Done when:** Retention jobs scheduled; data map document approved.

### T-18-07 — Fraud rules
- **Done when:** Rules configurable; flagged cases appear in admin.

### T-18-08 — Runbook
- **Done when:** Runbook tested in a tabletop exercise.

### T-18-09 — Pen test
- **Done when:** No open critical/high findings.

### T-18-10 — Compliance sign-off
- **Done when:** Every §2 row marked compliant with evidence link.
