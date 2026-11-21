# ADR 0001 — Backend framework

**Status:** Accepted · **Date:** 21 Nov 2026 · **Task:** T-16-01

## Context

The API is a modular monolith (identity, catalog, cart, orders, payments, delivery, notifications, vendor, admin) with OpenAPI 3.1 and a TypeScript web stack (Next.js). Module 16 allows NestJS or .NET 8.

## Options

| Option | Cost | Exit |
|---|---|---|
| NestJS (TypeScript) | One language across web, API, and workers. No runtime licence. Team context-switches less. | A later .NET rewrite keeps the OpenAPI contract and `PaymentProvider`. Expect a multi-month port, not a config change. |
| .NET 8 | Strong modules and OpenAPI. Adds a second language next to Next.js and Expo. | Leaving .NET later has the same contract-based exit, plus a hiring split until then. |

## Decision

NestJS on Node.js.

## Consequences

- Monorepo stays TypeScript: `apps/api`, `apps/worker`, `packages/*`.
- Decorators and a DI container are part of the API.
- Windows local dev uses the same `pnpm` commands as CI.
