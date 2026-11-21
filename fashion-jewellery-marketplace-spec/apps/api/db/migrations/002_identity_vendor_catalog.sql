-- Identity, vendor, catalog, media. Column lists follow 17-data-model/spec.md.
-- PII columns are tagged in comments for module 18.

CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  phone text UNIQUE,
  email text,
  name text,
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'disabled', 'deleted')),
  created_at timestamptz NOT NULL DEFAULT now(),
  deleted_at timestamptz
);
COMMENT ON COLUMN users.phone IS 'PII';
COMMENT ON COLUMN users.email IS 'PII';
COMMENT ON COLUMN users.name IS 'PII';

CREATE TABLE user_roles (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  user_id uuid NOT NULL REFERENCES users (id),
  role text NOT NULL CHECK (role IN ('customer', 'vendor_owner', 'vendor_staff', 'admin', 'super_admin')),
  vendor_id uuid,
  admin_role text CHECK (admin_role IS NULL OR admin_role IN ('ops', 'catalog', 'finance', 'support', 'super'))
);
CREATE UNIQUE INDEX user_roles_identity_idx
  ON user_roles (user_id, role, COALESCE(vendor_id, '00000000-0000-0000-0000-000000000000'::uuid));

CREATE TABLE addresses (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  user_id uuid NOT NULL REFERENCES users (id),
  name text NOT NULL,
  phone text NOT NULL,
  line1 text NOT NULL,
  line2 text,
  landmark text,
  city text NOT NULL,
  state text NOT NULL,
  pin text NOT NULL,
  type text NOT NULL DEFAULT 'shipping' CHECK (type IN ('shipping', 'billing')),
  is_default boolean NOT NULL DEFAULT false,
  deleted_at timestamptz
);
COMMENT ON COLUMN addresses.phone IS 'PII';
COMMENT ON COLUMN addresses.line1 IS 'PII';

CREATE TABLE otp_requests (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  phone text NOT NULL,
  code_hash text NOT NULL,
  expires_at timestamptz NOT NULL,
  attempts int NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now()
);
COMMENT ON COLUMN otp_requests.phone IS 'PII';

CREATE TABLE refresh_tokens (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  user_id uuid NOT NULL REFERENCES users (id),
  token_hash text NOT NULL,
  family_id uuid NOT NULL,
  expires_at timestamptz NOT NULL,
  revoked_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE vendor_applications (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  owner_user_id uuid NOT NULL REFERENCES users (id),
  state text NOT NULL DEFAULT 'DRAFT' CHECK (state IN (
    'DRAFT', 'SUBMITTED', 'IN_REVIEW', 'CHANGES_REQUESTED', 'APPROVED', 'REJECTED'
  )),
  step_data jsonb NOT NULL DEFAULT '{}'::jsonb,
  submitted_at timestamptz,
  reviewed_by uuid REFERENCES users (id),
  decision_reason text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE vendors (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  owner_user_id uuid NOT NULL REFERENCES users (id),
  legal_name text NOT NULL,
  display_name text NOT NULL,
  slug text NOT NULL UNIQUE,
  business_type text NOT NULL CHECK (business_type IN ('individual', 'partnership', 'pvt_ltd', 'llp')),
  pan_masked text,
  gstin text,
  pickup_address jsonb,
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'holiday', 'suspended')),
  holiday_until timestamptz,
  score numeric(5, 2) NOT NULL DEFAULT 0,
  strikes int NOT NULL DEFAULT 0,
  payout_status text NOT NULL DEFAULT 'active' CHECK (payout_status IN ('active', 'paused')),
  gateway_linked_account_id text,
  gateway_linked_account_status text NOT NULL DEFAULT 'pending' CHECK (
    gateway_linked_account_status IN ('pending', 'active', 'suspended')
  ),
  created_at timestamptz NOT NULL DEFAULT now()
);
COMMENT ON COLUMN vendors.pan_masked IS 'PII';
COMMENT ON COLUMN vendors.gstin IS 'PII';

ALTER TABLE user_roles
  ADD CONSTRAINT user_roles_vendor_fk FOREIGN KEY (vendor_id) REFERENCES vendors (id);

CREATE TABLE vendor_kyc (
  vendor_id uuid PRIMARY KEY REFERENCES vendors (id),
  provider_refs jsonb NOT NULL DEFAULT '{}'::jsonb,
  verified_at timestamptz,
  documents jsonb NOT NULL DEFAULT '{}'::jsonb
);
COMMENT ON COLUMN vendor_kyc.documents IS 'PII encrypted refs';

CREATE TABLE vendor_bank (
  vendor_id uuid PRIMARY KEY REFERENCES vendors (id),
  holder_name text NOT NULL,
  account_last4 text NOT NULL,
  ifsc text NOT NULL,
  verified_at timestamptz,
  gateway_ref text
);
COMMENT ON COLUMN vendor_bank.holder_name IS 'PII';
COMMENT ON COLUMN vendor_bank.account_last4 IS 'PII';

CREATE TABLE vendor_settings (
  vendor_id uuid PRIMARY KEY REFERENCES vendors (id),
  dispatch_days int NOT NULL DEFAULT 2 CHECK (dispatch_days BETWEEN 1 AND 7),
  shipping_fee_paise bigint NOT NULL DEFAULT 0 CHECK (shipping_fee_paise >= 0),
  free_threshold_paise bigint CHECK (free_threshold_paise IS NULL OR free_threshold_paise >= 0),
  excluded_pin_prefixes text[] NOT NULL DEFAULT '{}',
  return_addons jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE store_profiles (
  vendor_id uuid PRIMARY KEY REFERENCES vendors (id),
  logo_media_id uuid,
  banner_media_id uuid,
  about text,
  tags text[] NOT NULL DEFAULT '{}'
);

CREATE TABLE seller_agreement_acceptances (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  version text NOT NULL,
  accepted_at timestamptz NOT NULL DEFAULT now(),
  ip text,
  user_agent text
);
COMMENT ON COLUMN seller_agreement_acceptances.ip IS 'PII';

CREATE TABLE categories (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  parent_id uuid REFERENCES categories (id),
  name text NOT NULL,
  slug text NOT NULL UNIQUE,
  hsn_default text,
  position int NOT NULL DEFAULT 0
);

CREATE TABLE attributes (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  type text NOT NULL CHECK (type IN ('enum', 'multi', 'number', 'bool')),
  values text[] NOT NULL DEFAULT '{}'
);

CREATE TABLE category_attributes (
  category_id uuid NOT NULL REFERENCES categories (id),
  attribute_id uuid NOT NULL REFERENCES attributes (id),
  required boolean NOT NULL DEFAULT false,
  PRIMARY KEY (category_id, attribute_id)
);

CREATE TABLE products (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  category_id uuid NOT NULL REFERENCES categories (id),
  title text NOT NULL,
  slug text NOT NULL,
  description text,
  care text,
  status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'unpublished', 'archived')),
  attributes jsonb NOT NULL DEFAULT '{}'::jsonb,
  skin_safety text[] NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz,
  deleted_at timestamptz,
  UNIQUE (vendor_id, slug)
);

CREATE TABLE product_variants (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  product_id uuid NOT NULL REFERENCES products (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  options jsonb NOT NULL DEFAULT '{}'::jsonb,
  price_paise bigint NOT NULL CHECK (price_paise >= 0),
  mrp_paise bigint NOT NULL CHECK (mrp_paise >= 0),
  stock int NOT NULL DEFAULT 0 CHECK (stock >= 0),
  reserved int NOT NULL DEFAULT 0 CHECK (reserved >= 0),
  weight_g int CHECK (weight_g IS NULL OR weight_g >= 0),
  status text NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
  CONSTRAINT price_not_above_mrp CHECK (price_paise <= mrp_paise)
);

CREATE TABLE price_history (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  variant_id uuid NOT NULL REFERENCES product_variants (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  price_paise bigint NOT NULL,
  mrp_paise bigint NOT NULL,
  changed_by uuid REFERENCES users (id),
  changed_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE media (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  owner_type text NOT NULL,
  owner_id uuid NOT NULL,
  vendor_id uuid REFERENCES vendors (id),
  kind text NOT NULL CHECK (kind IN ('image', 'video')),
  original_url text,
  renditions jsonb NOT NULL DEFAULT '{}'::jsonb,
  position int NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE store_profiles
  ADD CONSTRAINT store_profiles_logo_fk FOREIGN KEY (logo_media_id) REFERENCES media (id);
ALTER TABLE store_profiles
  ADD CONSTRAINT store_profiles_banner_fk FOREIGN KEY (banner_media_id) REFERENCES media (id);

CREATE TABLE collections (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  name text NOT NULL,
  position int NOT NULL DEFAULT 0
);

CREATE TABLE collection_products (
  collection_id uuid NOT NULL REFERENCES collections (id),
  product_id uuid NOT NULL REFERENCES products (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  position int NOT NULL DEFAULT 0,
  PRIMARY KEY (collection_id, product_id)
);

CREATE TABLE looks (
  id uuid PRIMARY KEY DEFAULT uuidv7(),
  title text NOT NULL,
  occasion text,
  hero_media_id uuid REFERENCES media (id),
  status text NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published'))
);

CREATE TABLE look_items (
  look_id uuid NOT NULL REFERENCES looks (id),
  variant_id uuid NOT NULL REFERENCES product_variants (id),
  position int NOT NULL DEFAULT 0,
  PRIMARY KEY (look_id, variant_id)
);

CREATE TABLE wishlists (
  user_id uuid NOT NULL REFERENCES users (id),
  product_id uuid NOT NULL REFERENCES products (id),
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, product_id)
);

CREATE TABLE follows (
  user_id uuid NOT NULL REFERENCES users (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (user_id, vendor_id)
);

CREATE TABLE dashboard_layouts (
  user_id uuid NOT NULL REFERENCES users (id),
  vendor_id uuid NOT NULL REFERENCES vendors (id),
  layout jsonb NOT NULL DEFAULT '{}'::jsonb,
  version int NOT NULL DEFAULT 1,
  PRIMARY KEY (user_id, vendor_id)
);
