-- v1 rollback for local and CI. Drops objects created by migrations 001–006.
-- The app_user role is kept so a following migrate-up can GRANT again.
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO public;
