-- Finance, platform, outbox, webhooks. Money is bigint paise.

CREATE TABLE payments (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  order_id uuid NOT NULL REFERENCES orders (id),
  gateway text NOT NULL,
  gateway_order_id text NOT NULL,
  gateway_payment_id text,
  amount_paise bigint NOT NULL CHECK (amount_paise >= 0),
  currency text NOT NULL DEFAULT 'INR' CHECK (currency = 'INR'),
  status text NOT NULL CHECK (status IN ('created', 'captured', 'failed', 'refunded')),
  method text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE transfers (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_order_id uuid NOT NULL REFERENCES vendor_orders (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  tranche text NOT NULL CHECK (tranche IN ('T1', 'T2')),
  gateway_transfer_id text,
  amount_paise bigint NOT NULL CHECK (amount_paise >= 0),
  status text NOT NULL CHECK (status IN ('held', 'released', 'reversed', 'settled')),
  released_at timestamptz,
  UNIQUE (vendor_order_id, tranche)
);

CREATE TABLE refunds (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  order_id uuid NOT NULL REFERENCES orders (id),
  vendor_order_id uuid REFERENCES vendor_orders (id),
  amount_paise bigint NOT NULL CHECK (amount_paise >= 0),
  reason text NOT NULL,
  gateway_refund_id text,
  status text NOT NULL CHECK (status IN ('pending', 'processed', 'failed')),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE ledger_entries (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  txn_id uuid NOT NULL,
  account text NOT NULL,
  debit_paise bigint NOT NULL DEFAULT 0 CHECK (debit_paise >= 0),
  credit_paise bigint NOT NULL DEFAULT 0 CHECK (credit_paise >= 0),
  currency text NOT NULL DEFAULT 'INR' CHECK (currency = 'INR'),
  vendor_id uuid REFERENCES vendors (id),
  vendor_order_id uuid REFERENCES vendor_orders (id),
  at timestamptz NOT NULL DEFAULT now(),
  CHECK ((debit_paise = 0) <> (credit_paise = 0))
);

CREATE TABLE commission_rules (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  scope text NOT NULL CHECK (scope IN ('global', 'category', 'vendor')),
  scope_id uuid,
  rate_bps int NOT NULL CHECK (rate_bps >= 0),
  fixed_fee_paise bigint NOT NULL DEFAULT 0 CHECK (fixed_fee_paise >= 0),
  effective_from timestamptz NOT NULL,
  effective_to timestamptz
);

CREATE TABLE invoices (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  type text NOT NULL CHECK (type IN ('customer', 'commission')),
  series text NOT NULL,
  number text NOT NULL UNIQUE,
  vendor_id uuid REFERENCES vendors (id),
  vendor_order_id uuid REFERENCES vendor_orders (id),
  pdf_url text,
  issued_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE payout_holds (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  reason text NOT NULL,
  created_by uuid REFERENCES users (id),
  created_at timestamptz NOT NULL DEFAULT now(),
  released_at timestamptz
);

CREATE TABLE reconciliation_runs (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  started_at timestamptz NOT NULL DEFAULT now(),
  finished_at timestamptz,
  mismatch_count int NOT NULL DEFAULT 0
);

CREATE TABLE reconciliation_items (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  run_id uuid NOT NULL REFERENCES reconciliation_runs (id),
  gateway_id text NOT NULL,
  detail text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE notifications (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  event_id text NOT NULL,
  channel text NOT NULL CHECK (channel IN ('whatsapp', 'sms', 'email', 'web_push', 'in_app')),
  recipient_user_id uuid REFERENCES users (id),
  template_key text NOT NULL,
  status text NOT NULL CHECK (status IN ('queued', 'sent', 'failed', 'skipped')),
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (event_id, channel, recipient_user_id, template_key)
);

CREATE TABLE notification_templates (
  key text PRIMARY KEY,
  channel text NOT NULL,
  body text NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE notification_preferences (
  user_id uuid PRIMARY KEY REFERENCES users (id),
  marketing_email boolean NOT NULL DEFAULT false,
  quiet_hours boolean NOT NULL DEFAULT true
);

CREATE TABLE support_tickets (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  user_id uuid REFERENCES users (id),
  order_id uuid REFERENCES orders (id),
  subject text NOT NULL,
  body text NOT NULL,
  status text NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'pending', 'closed')),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE moderation_items (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  subject_type text NOT NULL,
  subject_id uuid NOT NULL,
  reason text NOT NULL,
  status text NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'approved', 'rejected')),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE config (
  key text PRIMARY KEY,
  value jsonb NOT NULL,
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE feature_flags (
  key text PRIMARY KEY,
  enabled boolean NOT NULL DEFAULT false,
  rollout_percent int NOT NULL DEFAULT 100 CHECK (rollout_percent BETWEEN 0 AND 100),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE cms_sections (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  slot text NOT NULL,
  payload jsonb NOT NULL,
  starts_at timestamptz,
  ends_at timestamptz
);

CREATE TABLE banners (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  title text NOT NULL,
  media_id uuid REFERENCES media (id),
  href text,
  position int NOT NULL DEFAULT 0,
  starts_at timestamptz,
  ends_at timestamptz
);

CREATE TABLE audit_log (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  actor_id uuid,
  action text NOT NULL,
  entity_type text NOT NULL,
  entity_id uuid,
  before jsonb,
  after jsonb,
  at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE outbox (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  aggregate_type text NOT NULL,
  aggregate_id uuid NOT NULL,
  event_type text NOT NULL,
  payload jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz
);

CREATE TABLE webhook_events (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  provider text NOT NULL,
  event_id text,
  signature_valid boolean NOT NULL,
  payload jsonb NOT NULL,
  raw_body text NOT NULL,
  status text NOT NULL CHECK (status IN ('rejected', 'pending', 'processed', 'failed')),
  error text,
  received_at timestamptz NOT NULL DEFAULT now(),
  processed_at timestamptz
);

CREATE TABLE idempotency_keys (
  scope text PRIMARY KEY,
  request_hash text NOT NULL,
  status_code int NOT NULL,
  response jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE FUNCTION purge_webhook_events(retain interval DEFAULT interval '90 days')
RETURNS bigint
LANGUAGE plpgsql
AS $$
DECLARE
  removed bigint;
BEGIN
  DELETE FROM webhook_events WHERE received_at < now() - retain;
  GET DIAGNOSTICS removed = ROW_COUNT;
  RETURN removed;
END
$$;

INSERT INTO config (key, value) VALUES
  ('return_window_hours', '48'::jsonb),
  ('accept_sla_hours', '24'::jsonb),
  ('dispatch_sla_hours', '72'::jsonb),
  ('t1_percent', '75'::jsonb),
  ('commission_rate_bps', '1500'::jsonb);

INSERT INTO commission_rules (scope, scope_id, rate_bps, fixed_fee_paise, effective_from)
VALUES ('global', NULL, 1500, 0, '2026-11-17T00:00:00Z');
