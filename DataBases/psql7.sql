CREATE OR REPLACE PROCEDURE nema_post()
LANGUAGE plpgsql
AS $$
DECLARE
spisok TEXT;
BEGIN
    SELECT STRING_AGG(name, ', ') 
    INTO spisok 
    FROM suppliers
    WHERE name NOT IN (SELECT suppliers_name FROM products);
    RAISE NOTICE 'Postachalniki vid yakih nema postavok: %', spisok;
END;
$$;

CREATE OR REPLACE PROCEDURE ch_price(id BIGINT, a money)
LANGUAGE plpgsql
AS $$
DECLARE 
old_price numeric;
BEGIN
SELECT price :: numeric INTO old_price 
FROM products
WHERE products_id = id;
UPDATE products
SET price = a
WHERE products_id = id;
RAISE NOTICE 'OLD PRICE: %', old_price;
RAISE NOTICE 'NEW PRICE: %', a;
END;
$$;