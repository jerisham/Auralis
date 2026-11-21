import { join } from "node:path";
import { PGlite } from "@electric-sql/pglite";
import { InMemoryQueue } from "@auralis/events";
import { afterEach, describe, expect, it } from "vitest";
import { migrateDown, migrateUp } from "../src/db/migrate";
import { listUnpublished, markPublished, relayOutbox } from "../src/db/relay";
import { catalogFingerprint, deterministicUuid, seed } from "../src/db/seed";

const migrationsDir = join(__dirname, "..", "db", "migrations");
const downFile = join(__dirname, "..", "db", "down.sql");

async function freshDb(): Promise<PGlite> {
  const db = new PGlite();
  await migrateUp(db, migrationsDir);
  return db;
}

describe("schema v1", () => {
  const opened: PGlite[] = [];

  afterEach(async () => {
    await Promise.all(opened.splice(0).map((db) => db.close()));
  });

  it("migrates up, down, and up again, and rejects a price above MRP", async () => {
    const db = await freshDb();
    opened.push(db);
    await migrateDown(db, downFile);
    await migrateUp(db, migrationsDir);

    const userId = deterministicUuid("constraint-user");
    const vendorId = deterministicUuid("constraint-vendor");
    const categoryId = deterministicUuid("constraint-category");
    const productId = deterministicUuid("constraint-product");
    await db.query(`INSERT INTO users (id, phone, name) VALUES ($1, '9111111111', 'Ravi')`, [userId]);
    await db.query(
      `INSERT INTO vendors (id, owner_user_id, legal_name, display_name, slug, business_type)
       VALUES ($1, $2, 'Ravi Jewels', 'Ravi', 'ravi', 'individual')`,
      [vendorId, userId],
    );
    await db.query(`INSERT INTO categories (id, name, slug) VALUES ($1, 'Earrings', 'earrings-constraint')`, [categoryId]);
    await db.query(
      `INSERT INTO products (id, vendor_id, category_id, title, slug) VALUES ($1, $2, $3, 'Jhumka', 'jhumka')`,
      [productId, vendorId, categoryId],
    );
    await expect(
      db.query(
        `INSERT INTO product_variants (id, product_id, vendor_id, price_paise, mrp_paise)
         VALUES ($1, $2, $3, 20000, 10000)`,
        [deterministicUuid("constraint-variant"), productId, vendorId],
      ),
    ).rejects.toThrow(/price_not_above_mrp/);
  });

  it("seeds 5 vendors, 300 products, and every vendor-order state, twice with the same fingerprint", async () => {
    const db = await freshDb();
    opened.push(db);
    await seed(db);
    const first = await catalogFingerprint(db);
    await seed(db);
    const second = await catalogFingerprint(db);
    expect(first).toBe(second);
    expect(first.startsWith("300:")).toBe(true);
    const vendors = await db.query<{ count: number }>("SELECT count(*)::int AS count FROM vendors");
    expect(vendors.rows[0]?.count).toBe(5);
    const states = await db.query<{ count: number }>("SELECT count(DISTINCT state)::int AS count FROM vendor_orders");
    expect(states.rows[0]?.count).toBe(12);
  });

  it("hides vendor A rows from vendor B, including an unscoped query", async () => {
    const db = await freshDb();
    opened.push(db);
    await seed(db);
    const productA = deterministicUuid("product:0");
    const vendorB = deterministicUuid("vendor:1");
    const seen = await db.transaction(async (tx) => {
      await tx.query(`SELECT set_config('app.vendor_id', $1, true)`, [vendorB]);
      await tx.query("SET LOCAL ROLE app_user");
      const guessed = await tx.query<{ id: string }>("SELECT id FROM products WHERE id = $1", [productA]);
      const unscoped = await tx.query<{ id: string }>("SELECT id FROM products");
      return { guessed: guessed.rows.length, unscoped: unscoped.rows.map((row) => row.id) };
    });
    expect(seen.guessed).toBe(0);
    expect(seen.unscoped).not.toContain(productA);
    expect(seen.unscoped.length).toBe(60);
  });

  it("refuses updates to the ledger for the app role", async () => {
    const db = await freshDb();
    opened.push(db);
    const txn = deterministicUuid("ledger-txn");
    const entry = deterministicUuid("ledger-entry");
    await db.query(
      `INSERT INTO ledger_entries (id, txn_id, account, debit_paise, credit_paise) VALUES ($1, $2, 'customer_clearing', 100, 0)`,
      [entry, txn],
    );
    await expect(
      db.transaction(async (tx) => {
        await tx.query("SET LOCAL ROLE app_user");
        await tx.query("UPDATE ledger_entries SET debit_paise = 5 WHERE id = $1", [entry]);
      }),
    ).rejects.toThrow(/permission denied/i);
  });

  it("keeps an outbox event when the worker stops before marking it published", async () => {
    const db = await freshDb();
    opened.push(db);
    const id = deterministicUuid("outbox-1");
    await db.query(
      `INSERT INTO outbox (id, aggregate_type, aggregate_id, event_type, payload)
       VALUES ($1, 'order', $2, 'payment.captured', '{"ok":true}'::jsonb)`,
      [id, deterministicUuid("aggregate-1")],
    );
    const pending = await listUnpublished(db);
    expect(pending).toHaveLength(1);
    const queue = new InMemoryQueue();
    await queue.publish({ id: pending[0]!.id, type: pending[0]!.event_type, payload: pending[0]!.payload });
    const stillPending = await listUnpublished(db);
    expect(stillPending).toHaveLength(1);
    let applied = 0;
    await queue.drain(async () => {
      applied += 1;
    });
    await markPublished(db, id);
    await relayOutbox(db, queue);
    await queue.drain(async () => {
      applied += 1;
    });
    expect(applied).toBe(1);
    expect(await listUnpublished(db)).toHaveLength(0);
  });

  it("purges webhook bodies older than 90 days", async () => {
    const db = await freshDb();
    opened.push(db);
    await db.query(
      `INSERT INTO webhook_events (provider, signature_valid, payload, raw_body, status, received_at)
       VALUES ('razorpay', true, '{}'::jsonb, '{}', 'processed', now() - interval '91 days')`,
    );
    await db.query(
      `INSERT INTO webhook_events (provider, signature_valid, payload, raw_body, status, received_at)
       VALUES ('razorpay', true, '{}'::jsonb, '{}', 'processed', now() - interval '1 day')`,
    );
    await db.query("SELECT purge_webhook_events()");
    const remaining = await db.query<{ count: number }>("SELECT count(*)::int AS count FROM webhook_events");
    expect(remaining.rows[0]?.count).toBe(1);
  });
});
