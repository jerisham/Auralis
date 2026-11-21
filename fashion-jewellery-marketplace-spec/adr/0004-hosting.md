# ADR 0004 — Hosting

**Status:** Accepted · **Date:** 21 Nov 2026 · **Task:** T-16-01

## Context

Module 20 specifies Azure Container Apps, PostgreSQL Flexible Server, Redis, Blob, Front Door, Key Vault, and Terraform. Q-14 (17 Nov 2026) says local for now, and a cloud is chosen later.

## Options

| Option | Cost | Exit |
|---|---|---|
| Local Compose + embedded Postgres in tests | No cloud bill. A developer machine runs Postgres 16, Redis, Meilisearch, and MinIO. CI uses PGlite so tests run without Docker. | When a cloud is chosen, Terraform modules from module 20 create the same processes (api, web, workers). Images do not change. |
| Azure now | Matches the module 20 resource list and adds a subscription, OIDC, and state backend before the product exists. | Switching clouds later is a Terraform port. Application code stays. |

## Decision

Local first. `infra/docker-compose.yml` is the dev environment. Tests use PGlite (Postgres in-process) because this machine has no Docker daemon. Azure remains the documented production target and is not provisioned in this slice. Terraform (T-20-03) starts after the cloud choice.

## Consequences

- Secrets for local dev are `.env` (gitignored) copied from `.env.example`. No Key Vault until Azure exists.
- Media originals and renditions go to the local disk (`.data/media`) until MinIO or Blob is wired.
- GitHub Actions CI runs lint, typecheck, test, and build. Preview environments and canary deploys wait on the cloud.
