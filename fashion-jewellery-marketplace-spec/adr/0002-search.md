# ADR 0002 — Search

**Status:** Accepted · **Date:** 21 Nov 2026 · **Task:** T-16-01

## Context

Module 04 needs facets, synonyms (including Hinglish), and typo tolerance. The index must follow product events within 60 seconds. Module 16 allows Meilisearch or Azure AI Search.

## Options

| Option | Cost | Exit |
|---|---|---|
| Meilisearch | One container locally and later on Azure Container Apps with a disk. No per-query cloud fee at pilot size. | Replace the indexer adapter with Azure AI Search if relevance or SLA needs it. Documents are rebuilt from Postgres, which stays the source of truth. |
| Azure AI Search | Managed, and it requires the cloud account Q-14 postponed. | Moving off it is a reindex into Meilisearch or OpenSearch. |

## Decision

Meilisearch. Postgres remains the source of truth. The search index is a projection of product events.

## Consequences

- Local Compose runs Meilisearch on port 7700.
- The indexer is a worker (`apps/worker`), idempotent, fed by the outbox.
- Synonym lists live in config, not in application code.
