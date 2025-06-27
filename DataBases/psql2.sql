--розкоментуйте дроп тейбл, якщо у вас якимось дивом є мої таблиці з першої лаби
--DROP TABLE products;
--DROP TABLE suppliers;
CREATE TABLE suppliers( 
	name TEXT, 
	address TEXT, 
	bank_details VARCHAR(64)
);

CREATE TABLE products( 
	products_id BIGINT, 																
	category VARCHAR(128),                                           
	realization_date DATE,                                            
	weight NUMERIC(18,3),                                             
	price MONEY,                                                     
	suppliers_name TEXT 
);

ALTER TABLE products
ALTER COLUMN products_id SET NOT NULL; 

ALTER TABLE products
ALTER COLUMN category SET NOT NULL;

ALTER TABLE products
ALTER COLUMN realization_date SET NOT NULL;

ALTER TABLE products
ALTER COLUMN weight SET NOT NULL;

ALTER TABLE products
ALTER COLUMN price SET NOT NULL;

ALTER TABLE products
ALTER COLUMN suppliers_name SET NOT NULL;

ALTER TABLE suppliers
ALTER COLUMN name SET NOT NULL;

ALTER TABLE suppliers
ALTER COLUMN address SET NOT NULL;

ALTER TABLE suppliers
ALTER COLUMN bank_details SET NOT NULL;

ALTER TABLE suppliers
ADD CONSTRAINT bank_det CHECK (LENGTH(bank_details) <= 34);

ALTER TABLE products
ADD CONSTRAINT price0 CHECK (price > 0::money);

ALTER TABLE products
ADD CONSTRAINT id_uni UNIQUE (products_id);

ALTER TABLE suppliers
ADD CONSTRAINT name_uni UNIQUE (name);

ALTER TABLE products
ADD CONSTRAINT pk_products PRIMARY KEY (products_id);

ALTER TABLE suppliers
ADD CONSTRAINT pk_suppliers PRIMARY KEY (name);

ALTER TABLE products
ADD CONSTRAINT fk_suppliers 
FOREIGN KEY (suppliers_name) REFERENCES suppliers(name)
ON DELETE CASCADE;

ALTER TABLE products
DROP CONSTRAINT fk_suppliers;

INSERT INTO products (products_id, category, realization_date, weight, price, suppliers_name) 
VALUES (1, 'bulochki', '2024-10-20', 10.5, 20.00, 'ATB');

INSERT INTO suppliers (name, address, bank_details)
VALUES ('ATB','Dnipro, dniprovska,251', '12225345NIKE-63PRO' );

ALTER TABLE products
ADD CONSTRAINT fk_suppliers 
FOREIGN KEY (suppliers_name) REFERENCES suppliers(name)
ON DELETE CASCADE;

ALTER TABLE products
DROP CONSTRAINT fk_suppliers;

ALTER TABLE products
ADD CONSTRAINT fk_suppliers
FOREIGN KEY (suppliers_name) REFERENCES suppliers(name)
ON DELETE CASCADE
ON UPDATE CASCADE ;

ALTER TABLE products
ADD COLUMN single VARCHAR(3) DEFAULT 'tak';

ALTER TABLE products
DROP COLUMN single;

ALTER TABLE suppliers RENAME TO postachalki;

ALTER TABLE postachalki RENAME TO suppliers;