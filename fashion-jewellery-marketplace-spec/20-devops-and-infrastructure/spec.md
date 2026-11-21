# 20 — DevOps & Infrastructure

**Phase:** P0 · **Depends on:** 16, Q-14 · **Status:** Draft
> **Decision (17 Nov 2026, Q-14):** Run **locally** until a cloud is chosen. Azure Container Apps (this document) remains the recommended production target, not the current environment. Local substitutes: Docker Compose or embedded Postgres for Postgres 16, Redis, Meilisearch, and MinIO.

## 1. Purpose
Reliable, repeatable, secure environments from day one, fully defined as code, with fast, safe delivery.

## 2. Environments
| Env | Purpose | Data | Deploy trigger |
|---|---|---|---|
| `dev` | Shared integration | Seed data | Merge to `main` |
| `preview` | Per-PR ephemeral web + API (shared DB schema per PR) | Seed | PR opened/updated |
| `staging` | Pre-prod, sandbox gateway, validations run here | Seed + anonymised | Tag `rc-*` / manual |
| `prod` | Live | Real | Manual approval after staging green |

## 3. Azure resources (per environment, Terraform modules)
- Resource group, VNet with private endpoints
- Azure Container Apps environment: `web`, `api`, `worker-notifications`, `worker-media`, `worker-search`, `worker-timers`, `worker-reconciliation`
- Azure Container Registry (shared)
- Azure Database for PostgreSQL Flexible Server (zone-redundant HA in prod, PITR 14–35 days)
- Azure Cache for Redis
- Azure Service Bus (queues/topics, scheduled messages)
- Storage accounts: `media-originals` (private), `media-public` (CDN origin), `exports` (private, SAS)
- Azure Front Door Premium (CDN + WAF + custom domains + TLS)
- Key Vault (per env), managed identities for every app
- Log Analytics + Application Insights
- Search: Meilisearch on Container Apps with persistent volume, or Azure AI Search (per ADR)
- Budget alerts per resource group

## 4. CI/CD (GitHub Actions)
```
PR:    lint → typecheck → unit tests → build → OpenAPI diff → security scans → preview deploy → E2E smoke on preview
main:  build images (tag = git SHA) → push ACR → terraform plan/apply dev → migrate → deploy dev → smoke
release: promote same image SHA → staging (migrate, deploy, full E2E + validations) → manual approval → prod (migrate, blue/green revision swap, smoke, auto-rollback on failed health)
infra: terraform fmt/validate/tflint/checkov → plan comment on PR → apply on merge (per env, with approvals for prod)
```
- OIDC federation from GitHub to Azure (no long-lived secrets).
- Database migrations run as a gated job before app rollout; backward-compatible (expand/contract) only.
- Container Apps revisions: traffic split for canary (10% → 100%).

## 5. Operations
- Runbooks: deploy, rollback, DB restore, gateway outage, webhook backlog, notification provider outage.
- On-call rotation (even if just 2 people) with alert routing.
- Cost guardrails: scale-to-zero for workers in dev/preview; preview envs auto-destroyed on PR close.
- Target monthly infra cost at pilot scale tracked in budget alerts (estimate in T-20-09).
