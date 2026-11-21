# Validation — 18 Security, Privacy & Compliance

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-18-01 | T-18-01 | Legal review | | | |
| V-18-02 | T-18-02 | Review | | | |
| V-18-03 | T-18-03 | Automated + manual | | | |
| V-18-04 | T-18-04 | Tooling | | | |
| V-18-05 | T-18-05 | CI | | | |
| V-18-06 | T-18-06 | Automated | | | |
| V-18-07 | T-18-07 | Automated | | | |
| V-18-08 | T-18-08 | Tabletop | | | |
| V-18-09 | T-18-09 | External | | | |
| V-18-10 | T-18-10 | Review | | | |

### V-18-01 — Legal
- **Pass criteria:** Signed lawyer note; footer links live; grievance officer details on site.

### V-18-02 — Threat model
- **Pass criteria:** Every "High" threat has a mitigation implemented or a dated task.

### V-18-03 — PII protection
- **Pass criteria:** DB dump shows bank/KYC fields as ciphertext; vendor views closed order after 31 days → phone/address masked.

### V-18-04 — Edge security
- **Pass criteria:** Security headers grade A; OTP endpoint brute-force blocked; WAF blocks sample SQLi/XSS payloads.

### V-18-05 — Scanning
- **Pass criteria:** Test PR with a known-vulnerable dependency and a fake secret is blocked.

### V-18-06 — Data lifecycle
- **Pass criteria:** Deletion job removes/anonymises per schedule while keeping invoices/ledger.

### V-18-07 — Fraud
- **Pass criteria:** Review from vendor's own phone excluded; customer with 4 claims in 60 days flagged.

### V-18-08 — Incident drill
- **Pass criteria:** Tabletop completed; notification steps and timelines confirmed.

### V-18-09 — Pen test
- **Pass criteria:** Report with 0 open critical/high.

### V-18-10 — Compliance
- **Pass criteria:** Checklist 100% with evidence.

## Module sign-off
- [ ] All checks Pass
- [ ] Lawyer + CA + tech lead approval
