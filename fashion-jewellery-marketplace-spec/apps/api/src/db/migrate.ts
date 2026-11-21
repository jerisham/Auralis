import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { PGlite } from "@electric-sql/pglite";

export async function migrateUp(db: PGlite, migrationsDir: string): Promise<void> {
  await db.exec(`CREATE TABLE IF NOT EXISTS schema_migrations (
    id text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT now()
  )`);
  const files = readdirSync(migrationsDir)
    .filter((file) => file.endsWith(".sql"))
    .sort();
  for (const file of files) {
    const existing = await db.query<{ id: string }>("SELECT id FROM schema_migrations WHERE id = $1", [file]);
    if (existing.rows.length > 0) continue;
    await db.exec(readFileSync(join(migrationsDir, file), "utf8"));
    await db.query("INSERT INTO schema_migrations (id) VALUES ($1)", [file]);
  }
}

export async function migrateDown(db: PGlite, downFile: string): Promise<void> {
  await db.exec(readFileSync(downFile, "utf8"));
}
