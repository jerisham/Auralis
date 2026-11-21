-- App role used by the API. Superusers bypass RLS, so policies target app_user
-- and vendor-owned tables use FORCE ROW LEVEL SECURITY.

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_user') THEN
    CREATE ROLE app_user NOLOGIN NOSUPERUSER NOBYPASSRLS;
  END IF;
END
$$;

GRANT USAGE ON SCHEMA public TO app_user;

-- Append-only money and audit tables: the app may insert, never update or delete.
GRANT SELECT, INSERT ON ledger_entries, audit_log, order_events TO app_user;
REVOKE UPDATE, DELETE ON ledger_entries, audit_log, order_events FROM app_user;

GRANT SELECT, INSERT, UPDATE, DELETE ON
  users, user_roles, addresses, otp_requests, refresh_tokens,
  vendor_applications, vendors, vendor_kyc, vendor_bank, vendor_settings, store_profiles,
  seller_agreement_acceptances, categories, attributes, category_attributes,
  products, product_variants, price_history, media, collections, collection_products,
  looks, look_items, wishlists, follows, dashboard_layouts,
  carts, cart_items, orders, vendor_orders, order_items, stock_reservations, shipments, claims,
  reviews, vendor_ratings, pincodes,
  payments, transfers, refunds, commission_rules, invoices, payout_holds,
  reconciliation_runs, reconciliation_items,
  notifications, notification_templates, notification_preferences, support_tickets, moderation_items,
  config, feature_flags, cms_sections, banners, outbox, webhook_events, idempotency_keys
TO app_user;

CREATE OR REPLACE FUNCTION app_vendor_id() RETURNS uuid
LANGUAGE sql
STABLE
AS $$
  SELECT NULLIF(current_setting('app.vendor_id', true), '')::uuid
$$;

CREATE OR REPLACE FUNCTION app_bypass_rls() RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT current_setting('app.bypass_rls', true) = 'on'
$$;

-- Vendor isolation. Admin and workers set app.bypass_rls = on (audited in application code).
DO $$
DECLARE
  tbl text;
BEGIN
  FOREACH tbl IN ARRAY ARRAY[
    'products', 'product_variants', 'price_history', 'media', 'collections', 'collection_products',
    'vendor_settings', 'vendor_kyc', 'vendor_bank', 'store_profiles', 'dashboard_layouts',
    'vendor_orders', 'order_items', 'order_events', 'stock_reservations', 'shipments', 'claims',
    'transfers', 'payout_holds'
  ]
  LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', tbl);
    EXECUTE format('ALTER TABLE %I FORCE ROW LEVEL SECURITY', tbl);
    EXECUTE format('DROP POLICY IF EXISTS tenant_isolation ON %I', tbl);
    EXECUTE format(
      'CREATE POLICY tenant_isolation ON %I FOR ALL TO app_user USING (vendor_id = app_vendor_id() OR app_bypass_rls()) WITH CHECK (vendor_id = app_vendor_id() OR app_bypass_rls())',
      tbl
    );
  END LOOP;
END
$$;

ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendors FORCE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS tenant_isolation ON vendors;
CREATE POLICY tenant_isolation ON vendors
  FOR ALL TO app_user
  USING (id = app_vendor_id() OR app_bypass_rls())
  WITH CHECK (id = app_vendor_id() OR app_bypass_rls());
