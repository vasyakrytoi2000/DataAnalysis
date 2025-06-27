CREATE OR REPLACE FUNCTION del_supp()
RETURNS TRIGGER 
AS
$$
BEGIN
	IF EXISTS
	(SELECT 1 FROM suppliers s
	JOIN products p ON s.name = p.suppliers_name 
	WHERE suppliers_name = OLD.name)
	THEN
	RAISE EXCEPTION 'Removal is prohibited, there are products from the supplier. ';
	END IF;
	
	RETURN OLD;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER dell_supplir
BEFORE DELETE ON suppliers
FOR EACH ROW
EXECUTE FUNCTION del_supp();

CREATE MATERIALIZED VIEW sum_zal 
AS
SELECT products_id, price * weight AS total_price 
FROM products;


CREATE OR REPLACE FUNCTION pr_ch()
RETURNS TRIGGER
AS
$$
BEGIN
	REFRESH MATERIALIZED VIEW sum_zal;
	RETURN NEW;
END;
$$
LANGUAGE plpgsql;
	
CREATE TRIGGER vw_ref
AFTER UPDATE OR INSERT ON products
FOR EACH ROW
EXECUTE FUNCTION pr_ch();