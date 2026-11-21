# Validation — 20 DevOps & Infrastructure

| ID | Validates | Type | Result | Date | Tester |
|---|---|---|---|---|---|
| V-20-01 | T-20-01 | Manual | Fail | 2026-11-21 | Local implementation review |
| V-20-02 | T-20-02 | CI | Fail | 2026-11-21 | Local implementation review |
| V-20-03 | T-20-03 | Rebuild test | Fail | 2026-11-21 | Local implementation review |
| V-20-04 | T-20-04 | Pipeline run | Fail | 2026-11-21 | Local implementation review |
| V-20-05 | T-20-05 | Pipeline run | Fail | 2026-11-21 | Local implementation review |
| V-20-06 | T-20-06 | Drill | Fail | 2026-11-21 | Local implementation review |
| V-20-07 | T-20-07 | Drill | Fail | 2026-11-21 | Local implementation review |
| V-20-08 | T-20-08 | Drill | Fail | 2026-11-21 | Local implementation review |
| V-20-09 | T-20-09 | Review | Fail | 2026-11-21 | Local implementation review |

### V-20-01 — Governance
- **Pass criteria:** Direct push to `main` rejected; prod deploy waits for approval.

### V-20-02 — PR CI
- **Pass criteria:** Failing test blocks merge; pipeline ≤ 10 min p90.

### V-20-03 — Reproducible infra
- **Steps:** Destroy and recreate `dev` from Terraform.
- **Pass criteria:** Env fully working with no manual portal steps; Checkov shows 0 high findings.

### V-20-04 — Promotion
- **Pass criteria:** Prod runs exactly the image SHA validated in staging (verified via revision labels).

### V-20-05 — Previews
- **Pass criteria:** URL posted on PR within 15 min; resources gone ≤ 30 min after close.

### V-20-06 — Canary & rollback
- **Steps:** Deploy a build with failing health check.
- **Pass criteria:** Traffic stays/returns to previous revision automatically; no customer errors beyond canary %.

### V-20-07 — DR
- **Pass criteria:** RPO/RTO met (V-17-08).

### V-20-08 — On-call
- **Pass criteria:** Synthetic alert reaches on-call within 5 min; runbook followed successfully by second engineer.

### V-20-09 — Cost
- **Pass criteria:** Actual first-month cost within ±20% of estimate.

## Review notes (2026-11-21)

Module 20 was validated again on 21 Nov 2026. It is not completed, so it is not in `modulescompletedandvalidated.pdf`.

- **V-20-01 Fail.** CODEOWNERS and the pull-request template exist. This folder is not a git repository. `gh` is not installed, so there is no GitHub branch protection and a direct push to `main` cannot be shown as rejected. Prod approval cannot be shown either.
- **V-20-02 Fail.** `scripts/local-ci.ps1` was run on this machine and finished in 1.62 minutes: lint, typecheck, test, build, and the OpenAPI check all exited 0. That is under the 10-minute budget for this one run. It is not a p90, and nothing rejects a merge when a test fails, because there is no protected `main`.
- **V-20-03 Fail.** Q-14 is local hosting. `infra/docker-compose.yml` describes Postgres, Redis, Meilisearch, and MinIO. Docker is not installed, Terraform is not installed, and no `dev` environment was destroyed and recreated. Checkov was not run.
- **V-20-04 through V-20-09 Fail.** No image promotion, preview environment, canary rollback, restore drill, on-call page, or cloud invoice exists yet. Azure is still the documented production target and is not provisioned.

## Module sign-off
- [ ] All checks Pass
- [ ] DevOps lead approval
