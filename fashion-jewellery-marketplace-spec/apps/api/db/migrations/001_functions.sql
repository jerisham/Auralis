-- UUIDv7 (time-ordered) without pgcrypto. PostgreSQL 16 has no built-in uuidv7().
CREATE OR REPLACE FUNCTION uuidv7() RETURNS uuid
LANGUAGE plpgsql
VOLATILE
AS $$
DECLARE
  unix_ts_ms bytea;
  rand_bytes bytea;
  uuid_bytes bytea;
  hex text;
BEGIN
  unix_ts_ms := substring(int8send((floor(extract(epoch FROM clock_timestamp()) * 1000))::bigint) FROM 3 FOR 6);
  rand_bytes := decode(md5(random()::text || clock_timestamp()::text || random()::text), 'hex');
  uuid_bytes := unix_ts_ms || substring(rand_bytes FROM 1 FOR 10);
  uuid_bytes := set_byte(uuid_bytes, 6, (get_byte(uuid_bytes, 6) & 15) | 112);
  uuid_bytes := set_byte(uuid_bytes, 8, (get_byte(uuid_bytes, 8) & 63) | 128);
  hex := encode(uuid_bytes, 'hex');
  RETURN (
    substring(hex FROM 1 FOR 8) || '-' ||
    substring(hex FROM 9 FOR 4) || '-' ||
    substring(hex FROM 13 FOR 4) || '-' ||
    substring(hex FROM 17 FOR 4) || '-' ||
    substring(hex FROM 21 FOR 12)
  )::uuid;
END
$$;
