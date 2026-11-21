-- Commerce: cart, orders, vendor orders, shipments, claims.

CREATE TABLE carts (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  user_id uuid REFERENCES users (id),
  guest_token text UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CHECK (user_id IS NOT NULL OR guest_token IS NOT NULL)
);

CREATE TABLE cart_items (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  cart_id uuid NOT NULL REFERENCES carts (id),
  variant_id uuid NOT NULL REFERENCES product_variants (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  qty int NOT NULL CHECK (qty > 0 AND qty <= 5),
  UNIQUE (cart_id, variant_id)
);

CREATE TABLE orders (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  number text NOT NULL UNIQUE,
  user_id uuid NOT NULL REFERENCES users (id),
  address_snapshot jsonb NOT NULL,
  items_total_paise bigint NOT NULL CHECK (items_total_paise >= 0),
  shipping_total_paise bigint NOT NULL CHECK (shipping_total_paise >= 0),
  grand_total_paise bigint NOT NULL CHECK (grand_total_paise >= 0),
  currency text NOT NULL DEFAULT 'INR' CHECK (currency = 'INR'),
  status text NOT NULL DEFAULT 'PENDING_PAYMENT' CHECK (status IN (
    'PENDING_PAYMENT', 'PAID', 'PARTIALLY_FULFILLED', 'FULFILLED', 'CANCELLED', 'CLOSED'
  )),
  payment_status text NOT NULL DEFAULT 'pending' CHECK (payment_status IN (
    'pending', 'paid', 'failed', 'refunded', 'partially_refunded'
  )),
  created_at timestamptz NOT NULL DEFAULT now()
);
COMMENT ON COLUMN orders.address_snapshot IS 'PII snapshot';

CREATE TABLE vendor_orders (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  order_id uuid NOT NULL REFERENCES orders (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  number text NOT NULL UNIQUE,
  state text NOT NULL CHECK (state IN (
    'AWAITING_ACCEPTANCE', 'ACCEPTED', 'DISPATCHED', 'DELIVERED', 'COMPLETED', 'SETTLED',
    'REJECTED_BY_VENDOR', 'CANCELLED_BY_CUSTOMER', 'CANCELLED_SLA',
    'CLAIM_OPEN', 'CLAIM_RESOLVED', 'REFUNDED'
  )),
  items_total_paise bigint NOT NULL CHECK (items_total_paise >= 0),
  shipping_paise bigint NOT NULL CHECK (shipping_paise >= 0),
  commission_paise bigint NOT NULL CHECK (commission_paise >= 0),
  taxes jsonb NOT NULL DEFAULT '{}'::jsonb,
  vendor_net_paise bigint NOT NULL,
  t1_paise bigint NOT NULL CHECK (t1_paise >= 0),
  t2_paise bigint NOT NULL CHECK (t2_paise >= 0),
  sla_accept_at timestamptz,
  sla_dispatch_at timestamptz,
  return_window_ends_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE order_items (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_order_id uuid NOT NULL REFERENCES vendor_orders (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  variant_id uuid NOT NULL REFERENCES product_variants (id),
  title_snapshot text NOT NULL,
  qty int NOT NULL CHECK (qty > 0),
  unit_price_paise bigint NOT NULL CHECK (unit_price_paise >= 0),
  mrp_paise bigint NOT NULL CHECK (mrp_paise >= 0),
  commission_rate_bps int NOT NULL CHECK (commission_rate_bps >= 0),
  hsn text
);

CREATE TABLE order_events (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_order_id uuid NOT NULL REFERENCES vendor_orders (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  from_state text,
  to_state text NOT NULL,
  actor_type text NOT NULL CHECK (actor_type IN ('system', 'vendor', 'customer', 'admin')),
  actor_id uuid,
  reason text,
  meta jsonb NOT NULL DEFAULT '{}'::jsonb,
  at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE stock_reservations (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  variant_id uuid NOT NULL REFERENCES product_variants (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  order_id uuid NOT NULL REFERENCES orders (id),
  qty int NOT NULL CHECK (qty > 0),
  expires_at timestamptz NOT NULL
);

CREATE TABLE shipments (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_order_id uuid NOT NULL UNIQUE REFERENCES vendor_orders (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  courier text,
  tracking_id text,
  method text NOT NULL CHECK (method IN ('courier', 'hand')),
  dispatched_at timestamptz,
  delivered_at timestamptz,
  proof jsonb,
  events jsonb NOT NULL DEFAULT '[]'::jsonb
);

CREATE TABLE claims (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_order_id uuid NOT NULL REFERENCES vendor_orders (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  type text NOT NULL CHECK (type IN ('damaged', 'wrong', 'missing', 'not_received')),
  state text NOT NULL CHECK (state IN ('open', 'vendor_accepted', 'vendor_rejected', 'escalated', 'resolved')),
  items jsonb NOT NULL DEFAULT '[]'::jsonb,
  media jsonb NOT NULL DEFAULT '[]'::jsonb,
  vendor_response text,
  admin_decision text,
  amounts jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE reviews (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  product_id uuid NOT NULL REFERENCES products (id),
  vendor_order_item_id uuid NOT NULL REFERENCES order_items (id),
  user_id uuid NOT NULL REFERENCES users (id),
  rating int NOT NULL CHECK (rating BETWEEN 1 AND 5),
  text text,
  media jsonb NOT NULL DEFAULT '[]'::jsonb,
  status text NOT NULL DEFAULT 'published' CHECK (status IN ('pending', 'published', 'rejected')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (vendor_order_item_id, user_id)
);

CREATE TABLE vendor_ratings (
  vendor_order_id uuid NOT NULL REFERENCES vendor_orders (id),
  user_id uuid NOT NULL REFERENCES users (id),
  rating int NOT NULL CHECK (rating BETWEEN 1 AND 5),
  PRIMARY KEY (vendor_order_id, user_id)
);

CREATE TABLE pincodes (
  pin text PRIMARY KEY,
  city text NOT NULL,
  state text NOT NULL
);
