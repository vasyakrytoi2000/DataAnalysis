CREATE ROLE pr_ins;
CREATE USER John WITH PASSWORD '759153';
GRANT INSERT ON products TO pr_ins;
GRANT pr_ins TO John;

CREATE USER Bill WITH PASSWORD '759153';
GRANT EXECUTE ON PROCEDURE nema_post2 TO Bill;

REVOKE pr_ins FROM John;
CONNECT ON DATABASE postgres TO John;
REVOKE ALL PRIVILEGES ON DATABASE postgres FROM John;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

ALTER TABLE customers
ALTER COLUMN first_name SET DATA TYPE text

UPDATE customers
SET first_name = pgp_sym_encrypt(first_name, 'kokagera');

UPDATE customers
SET first_name = pgp_sym_decrypt(first_name :: bytea, 'kokagera');

select * from customers
