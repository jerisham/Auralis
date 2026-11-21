# ADR 0003 — Queue and scheduler

**Status:** Accepted · **Date:** 21 Nov 2026 · **Task:** T-16-01

## Context

Side-effects (notifications, payouts, search, media, SLA timers) must survive a crash. Module 16 allows Azure Service Bus or BullMQ on Redis. Q-14 keeps the first environment local.

## Options

| Option | Cost | Exit |
|---|---|---|
| BullMQ on Redis | Redis is already required for rate limits and locks. BullMQ adds no new hosted service locally. Delayed jobs cover SLA timers. | A `Queue` interface swaps the transport for Azure Service Bus when the cloud is chosen. Outbox rows in Postgres stay the source of "what happened". |
| Azure Service Bus | Scheduled messages are built in. Needs Azure now, which Q-14 defers. | Leaving Service Bus means replaying unpublished outbox rows into the new queue. |

## Decision

BullMQ on Redis for the deployed local/cloud worker. The domain code talks to a small queue interface. Tests use an in-memory implementation of that interface so CI does not need Redis.

## Consequences

- Producers write the outbox in the same database transaction as the business change.
- A relay publishes unpublished outbox rows.
- Consumers are idempotent by event id. Poison messages go to a dead-letter list and raise an alert callback.
