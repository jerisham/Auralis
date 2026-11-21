import type { JobQueue } from "@auralis/events";
import type { PGlite } from "@electric-sql/pglite";

export type OutboxRow = { id: string; event_type: string; payload: unknown };

export async function listUnpublished(db: PGlite): Promise<OutboxRow[]> {
  const result = await db.query<OutboxRow>(
    "SELECT id, event_type, payload FROM outbox WHERE published_at IS NULL ORDER BY created_at",
  );
  return result.rows;
}

export async function markPublished(db: PGlite, id: string): Promise<void> {
  await db.query("UPDATE outbox SET published_at = now() WHERE id = $1 AND published_at IS NULL", [id]);
}

/** Publish unpublished outbox rows. Marking is separate so a crash before the mark leaves the row to retry. */
export async function relayOutbox(db: PGlite, queue: JobQueue): Promise<number> {
  const rows = await listUnpublished(db);
  for (const row of rows) {
    await queue.publish({ id: row.id, type: row.event_type, payload: row.payload });
    await markPublished(db, row.id);
  }
  return rows.length;
}
