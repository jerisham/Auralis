# Tasks — 20 DevOps & Infrastructure

| ID | Task | Depends on | Size | Status |
|---|---|---|---|---|
| T-20-01 | GitHub org/repo, branch protection, CODEOWNERS, PR template, environments with approvals | — | S | Todo |
| T-20-02 | CI pipeline for PRs (lint, test, build, scans, OpenAPI diff) | T-20-01, T-16-02 | M | Todo |
| T-20-03 | Terraform modules + state backend; provision dev & staging | Q-14 | L | Todo |
| T-20-04 | CD pipeline: image build, migrate, deploy, smoke, promote by SHA | T-20-02, T-20-03 | M | Todo |
| T-20-05 | Preview environments per PR + auto-teardown | T-20-04 | M | Todo |
| T-20-06 | Prod environment: HA DB, WAF, custom domain, TLS, canary + auto-rollback | T-20-04 | M | Todo |
| T-20-07 | Backups, PITR, DR restore runbook | T-20-03 | S | Todo |
| T-20-08 | Runbooks + on-call + alert routing | T-19-02 | S | Todo |
| T-20-09 | Cost estimate + budgets + scale-to-zero settings | T-20-03 | S | Todo |

---

### T-20-01 — Repo governance
- **Done when:** `main` protected (reviews, status checks); prod environment requires approval.

### T-20-02 — PR CI
- **Done when:** Pipeline < 10 min; required checks enforced.

### T-20-03 — Terraform
- **Steps:** Remote state in Azure Storage with locking; modules per §3; env folders `envs/dev|staging|prod`.
- **Done when:** `terraform apply` from scratch builds a working env; drift detection weekly.

### T-20-04 — CD
- **Done when:** Same image SHA flows dev → staging → prod; migrations gated.

### T-20-05 — Previews
- **Done when:** PR comment shows preview URL; destroyed on close.

### T-20-06 — Prod
- **Done when:** Canary + automatic rollback on failing health probes demonstrated.

### T-20-07 — DR
- **Done when:** Restore runbook executed successfully (see V-17-08).

### T-20-08 — Ops readiness
- **Done when:** Runbooks in `runbooks/`; alerts route to on-call; test page received.

### T-20-09 — Cost
- **Done when:** Monthly estimate per env documented; budget alerts at 80/100%.
