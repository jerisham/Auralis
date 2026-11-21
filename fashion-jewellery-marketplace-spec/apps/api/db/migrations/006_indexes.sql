-- Hot paths: PLP, order lists, ledger by vendor (T-17-07).
CREATE INDEX products_published_category_idx ON products (category_id, published_at DESC)
  WHERE status = 'published' AND deleted_at IS NULL;
CREATE INDEX products_vendor_status_idx ON products (vendor_id, status);
CREATE INDEX variants_product_idx ON product_variants (product_id);
CREATE INDEX variants_vendor_idx ON product_variants (vendor_id);
CREATE INDEX orders_user_created_idx ON orders (user_id, created_at DESC);
CREATE INDEX vendor_orders_vendor_state_idx ON vendor_orders (vendor_id, state, created_at DESC);
CREATE INDEX vendor_orders_order_idx ON vendor_orders (order_id);
CREATE INDEX ledger_vendor_at_idx ON ledger_entries (vendor_id, at DESC);
CREATE INDEX order_events_vendor_order_idx ON order_events (vendor_order_id, at);
CREATE INDEX outbox_unpublished_idx ON outbox (created_at) WHERE published_at IS NULL;
CREATE INDEX webhook_events_provider_event_idx ON webhook_events (provider, event_id);
