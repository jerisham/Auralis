import { createHash } from "node:crypto";
import type { PGlite } from "@electric-sql/pglite";

const TREE: Array<[string, string[]]> = [
  ["Earrings", ["Studs", "Jhumkas", "Hoops", "Drops & Danglers", "Chandbalis", "Ear cuffs", "Ear chains"]],
  ["Necklaces", ["Chokers", "Pendants", "Layered", "Long / Rani haar", "Chains"]],
  ["Jewellery sets", ["Necklace sets", "Bridal sets", "Choker sets"]],
  ["Bangles & Bracelets", ["Bangles", "Kada", "Bracelets", "Cuffs"]],
  ["Rings", ["Statement", "Adjustable", "Stackable", "Toe rings"]],
  ["Anklets", []],
  ["Nose pins & rings", ["Nose pins", "Nath", "Septum (clip-on)"]],
  ["Head & Hair", ["Maang tikka", "Matha patti", "Hair clips", "Passa"]],
  ["Others", ["Brooches", "Waist chains (kamarbandh)", "Men's"]],
];

const STATES = [
  "AWAITING_ACCEPTANCE",
  "ACCEPTED",
  "DISPATCHED",
  "DELIVERED",
  "COMPLETED",
  "SETTLED",
  "REJECTED_BY_VENDOR",
  "CANCELLED_BY_CUSTOMER",
  "CANCELLED_SLA",
  "CLAIM_OPEN",
  "CLAIM_RESOLVED",
  "REFUNDED",
] as const;

export function deterministicUuid(name: string): string {
  const chars = createHash("sha256").update(name).digest("hex").slice(0, 32).split("");
  chars[12] = "7";
  chars[16] = "8";
  const hex = chars.join("");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

function slug(value: string): string {
  return value
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export async function seed(db: PGlite): Promise<void> {
  const customerId = deterministicUuid("user:customer");
  await db.query(
    `INSERT INTO users (id, phone, name) VALUES ($1, $2, $3) ON CONFLICT (id) DO NOTHING`,
    [customerId, "9000000000", "Priya"],
  );
  await db.query(
    `INSERT INTO user_roles (id, user_id, role) VALUES ($1, $2, 'customer') ON CONFLICT (id) DO NOTHING`,
    [deterministicUuid("role:customer"), customerId],
  );

  const vendorIds: string[] = [];
  for (let index = 0; index < 5; index += 1) {
    const userId = deterministicUuid(`user:vendor:${index}`);
    const vendorId = deterministicUuid(`vendor:${index}`);
    vendorIds.push(vendorId);
    await db.query(
      `INSERT INTO users (id, phone, name) VALUES ($1, $2, $3) ON CONFLICT (id) DO NOTHING`,
      [userId, `900000000${index + 1}`, `Vendor ${index + 1}`],
    );
    await db.query(
      `INSERT INTO vendors (id, owner_user_id, legal_name, display_name, slug, business_type, status, gateway_linked_account_status)
       VALUES ($1, $2, $3, $4, $5, 'individual', 'active', 'active')
       ON CONFLICT (id) DO NOTHING`,
      [vendorId, userId, `Vendor ${index + 1} Jewels`, `Studio ${index + 1}`, `studio-${index + 1}`],
    );
    await db.query(
      `INSERT INTO user_roles (id, user_id, role, vendor_id) VALUES ($1, $2, 'vendor_owner', $3) ON CONFLICT (id) DO NOTHING`,
      [deterministicUuid(`role:vendor:${index}`), userId, vendorId],
    );
    await db.query(
      `INSERT INTO vendor_settings (vendor_id, dispatch_days, shipping_fee_paise, free_threshold_paise)
       VALUES ($1, 2, 6000, 99900) ON CONFLICT (vendor_id) DO NOTHING`,
      [vendorId],
    );
    await db.query(
      `INSERT INTO store_profiles (vendor_id, about, tags) VALUES ($1, $2, $3) ON CONFLICT (vendor_id) DO NOTHING`,
      [vendorId, "Fashion jewellery, shipped by the maker.", ["festive"]],
    );
  }

  const leaves: string[] = [];
  let position = 0;
  for (const [parent, children] of TREE) {
    const parentId = deterministicUuid(`cat:${slug(parent)}`);
    await db.query(
      `INSERT INTO categories (id, name, slug, position) VALUES ($1, $2, $3, $4) ON CONFLICT (id) DO NOTHING`,
      [parentId, parent, slug(parent), position],
    );
    position += 1;
    if (children.length === 0) {
      leaves.push(parentId);
      continue;
    }
    for (let childIndex = 0; childIndex < children.length; childIndex += 1) {
      const child = children[childIndex]!;
      const childId = deterministicUuid(`cat:${slug(parent)}:${slug(child)}`);
      leaves.push(childId);
      await db.query(
        `INSERT INTO categories (id, parent_id, name, slug, position) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (id) DO NOTHING`,
        [childId, parentId, child, `${slug(parent)}-${slug(child)}`, childIndex],
      );
    }
  }

  for (let index = 0; index < 300; index += 1) {
    const vendorId = vendorIds[index % vendorIds.length]!;
    const categoryId = leaves[index % leaves.length]!;
    const productId = deterministicUuid(`product:${index}`);
    const variantId = deterministicUuid(`variant:${index}`);
    const price = 30000 + (index % 40) * 1000;
    const mrp = price + 5000;
    const localIndex = Math.floor(index / vendorIds.length);
    await db.query(
      `INSERT INTO products (id, vendor_id, category_id, title, slug, status, skin_safety, published_at)
       VALUES ($1, $2, $3, $4, $5, 'published', $6, '2026-11-21T00:00:00Z')
       ON CONFLICT (id) DO NOTHING`,
      [productId, vendorId, categoryId, `Piece ${index + 1}`, `piece-${localIndex}`, index % 5 === 0 ? ["nickel-free"] : []],
    );
    await db.query(
      `INSERT INTO product_variants (id, product_id, vendor_id, price_paise, mrp_paise, stock, weight_g)
       VALUES ($1, $2, $3, $4, $5, 8, 12)
       ON CONFLICT (id) DO NOTHING`,
      [variantId, productId, vendorId, price, mrp],
    );
  }

  for (let index = 0; index < STATES.length; index += 1) {
    const state = STATES[index]!;
    const vendorId = vendorIds[index % vendorIds.length]!;
    const orderId = deterministicUuid(`order:${state}`);
    const vendorOrderId = deterministicUuid(`vendor-order:${state}`);
    await db.query(
      `INSERT INTO orders (id, number, user_id, address_snapshot, items_total_paise, shipping_total_paise, grand_total_paise, status, payment_status)
       VALUES ($1, $2, $3, '{}'::jsonb, 50000, 0, 50000, 'PAID', 'paid')
       ON CONFLICT (id) DO NOTHING`,
      [orderId, `ORD-2611-${String(index + 1).padStart(6, "0")}`, customerId],
    );
    await db.query(
      `INSERT INTO vendor_orders (
         id, order_id, vendor_id, number, state, items_total_paise, shipping_paise, commission_paise, vendor_net_paise, t1_paise, t2_paise
       ) VALUES ($1, $2, $3, $4, $5, 50000, 0, 7500, 42500, 31875, 10625)
       ON CONFLICT (id) DO NOTHING`,
      [vendorOrderId, orderId, vendorId, `ORD-2611-${String(index + 1).padStart(6, "0")}-A`, state],
    );
  }
}

export async function catalogFingerprint(db: PGlite): Promise<string> {
  const result = await db.query<{ hash: string; count: number }>(
    `SELECT md5(coalesce(string_agg(id::text, ',' ORDER BY id), '')) AS hash, count(*)::int AS count FROM products`,
  );
  const row = result.rows[0];
  return `${row?.count ?? 0}:${row?.hash ?? ""}`;
}
