CREATE TABLE category (
	category_id SERIAL PRIMARY KEY,
	name VARCHAR(128) NOT NULL,
	description VARCHAR(512)
);

ALTER TABLE products DROP COLUMN category;
ALTER TABLE products ADD COLUMN category BIGINT;

INSERT INTO category( name, description )
VALUES 
		( 'hlib-bulki', '' ),
		( 'miaso', 'kovbasa, svige miaso, chota tam'),
		( 'molochka', 'sir, smetana,yogyrt,moloko,take vsiake'),
		( 'solodochi', 'chokolad,vafli, cykerki'),
		( 'riba', 'ny riba vsyaka'),
		( 'alkogol', 'vodkaaaaaaaaaaaaa'),
		( 'tytyn', 'sigary, pody '),
		( 'himia', 'chipsiki, syhariki, goriski'),
		( 'dodomy', 'servetki tipa, tyaletka, take vsiake');

UPDATE products
SET category = 4
WHERE products_id = 1;

UPDATE products
SET category = 3
WHERE products_id = 2;

UPDATE products
SET category = 9
WHERE products_id = 3;

UPDATE products
SET category = 2
WHERE products_id = 4;

UPDATE products
SET category = 7
WHERE products_id = 5;

UPDATE products
SET category = 7
WHERE products_id = 6;

UPDATE products
SET category = 9
WHERE products_id = 7;

UPDATE products
SET category = 3
WHERE products_id = 8;

UPDATE products
SET category = 2
WHERE products_id = 9;

UPDATE products
SET category = 5
WHERE products_id = 10;

UPDATE products
SET category = 1
WHERE products_id = 11;

ALTER TABLE products
ADD CONSTRAINT fk_category 
FOREIGN KEY (category) REFERENCES category(category_id)
ON DELETE CASCADE;

CREATE TABLE customers (
	customer_id BIGSERIAL PRIMARY KEY,
	first_name VARCHAR(64) NOT NULL,
	last_name VARCHAR(64) NOT NULL,
	phone BIGINT NOT NULL
);

CREATE TABLE order_items ( 
 	items_id BIGSERIAL PRIMARY KEY,
	products_id BIGINT NOT NULL,
	amount VARCHAR(128) NOT NULL,

	CONSTRAINT fk_products FOREIGN KEY (products_id) REFERENCES products(products_id)
);

CREATE TABLE payments (
	payments_id BIGSERIAL PRIMARY KEY ,
	total MONEY NOT NULL,
	date DATE NOT NULL,
	method_pay VARCHAR(64) NOT NULL
);

CREATE TABLE orders (
	order_id BIGSERIAL PRIMARY KEY,
	customer_id BIGINT NOT NULL,
	items BIGINT NOT NULL,
	order_date DATE NOT NULL,
	status VARCHAR(64) NOT NULL,
	payment BIGINT NOT NULL,

	CONSTRAINT fk_castomer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
	CONSTRAINT fk_items FOREIGN KEY (items) REFERENCES order_items(items_id),
	CONSTRAINT fk_payment FOREIGN KEY (payment) REFERENCES payments(payments_id)
);

ALTER TABLE customers 
ADD CONSTRAINT number_ph CHECK (LENGTH(phone :: text ) <= 10); 

INSERT INTO customers (first_name, last_name, phone)
VALUES 
	( 'Vasia', 'Chiloviy', 1441221230 ),
	( 'Vitia', 'Hard', 1457764539 ),
	( 'Sanya', 'Beli', 3564758746 ),
	( 'Olga', 'Kryta', 9877635467 ),
	( 'Cocos', 'Sigma', 1997465364 ),
	( 'Nina', 'Tymba', 1991730678 ),
	( 'Yarik', 'Klyovi', 1985477878 ),
	( 'Stas', 'Bandit', 1978961323 );

INSERT INTO payments ( total, date, method_pay)
VALUES 
	( 50, '2024-11-09', 'card_doma' ),
	( 120, '2023-12-12', 'online' ),
	( 53, '2022-04-07', 'gotivka_doma' ),
	( 12, '2020-01-13', 'online' ),
	( 4, '2024-11-23', 'gotivka_doma' ),
	( 90, '2023-02-03', 'online' ),
	( 342, '2023-08-24', 'gotivka_doma' ),
	( 14, '2021-04-20', 'card_doma' ),
	( 98, '2019-05-09', 'card_doma' );

ALTER TABLE order_items 
ADD CONSTRAINT ch_amount CHECK(amount ~ '^\d+$' OR amount ~ '^\d+(\.\d+)?kg$');

INSERT INTO order_items (products_id, amount)
VALUES 
	( 2, '3kg' ),
	( 10, '7' ),
	( 7, '39' ),
	( 10, '3.56kg' ),
	( 6, '8' ),
	( 7, '9' ),
	( 2, '3' ),
	( 11, '300kg' ),
	( 11, '37.2kg' ),
	( 11, '121' );

ALTER TABLE orders
ADD CONSTRAINT uni_pay UNIQUE (payment);

INSERT INTO orders (customer_id, items, order_date, status, payment)
VALUES 
	( 4, 9, '2024-09-11', 'v dorozi', 2),
	( 7, 6, '2021-01-13', 'obrobka', 7),
	( 7, 5, '2022-05-16', 'ochikye vidpravki', 3),
	( 5, 8, '2022-10-06', 'pribylo', 8),
	( 4, 5, '2024-04-02', 'vidmova', 9),
	( 8, 9, '2023-02-07', 'v dorozi', 1),
	( 4, 9, '2019-09-29', 'ochikye vidpravki', 4),
	( 6, 10, '2020-02-01', 'obrobka', 6);

ALTER TABLE products ADD COLUMN availability BOOLEAN;

UPDATE products
SET availability = TRUE
WHERE products_id = 1;

UPDATE products
SET availability = TRUE
WHERE products_id = 2;

UPDATE products
SET availability = TRUE
WHERE products_id = 3;

UPDATE products
SET availability = FALSE
WHERE products_id = 4;

UPDATE products
SET availability = TRUE
WHERE products_id = 5;

UPDATE products
SET availability = FALSE
WHERE products_id = 6;

UPDATE products
SET availability = TRUE
WHERE products_id = 7;

UPDATE products
SET availability = TRUE
WHERE products_id = 8;

UPDATE products
SET availability = TRUE
WHERE products_id = 9;

UPDATE products
SET availability = FALSE
WHERE products_id = 10;

UPDATE products
SET availability = TRUE
WHERE products_id = 11;

ALTER TABLE products
ALTER COLUMN availability SET NOT NULL;

SELECT s.name, s.address, ARRAY_AGG(p.products_id) AS product_id
FROM suppliers s
JOIN products p ON s.name = p.suppliers_name
WHERE p.availability = TRUE
GROUP BY s.name, s.address;

SELECT p.products_id, p.category, category.name,description
FROM products p
JOIN category  ON p.category = category_id
WHERE p.realization_date <= '2024-11-10';

CREATE TABLE delivery (
	delivery_id BIGSERIAL PRIMARY KEY,
	product_id BIGINT NOT NULL,
	weight numeric(18,3) NOT NULL,
	supplier text NOT NULL,
	date DATE,

	CONSTRAINT fk_products_d FOREIGN KEY (product_id) REFERENCES products(products_id),
	CONSTRAINT fk_suppliers FOREIGN KEY (supplier) REFERENCES suppliers(name)
);

INSERT INTO delivery (product_id, weight, supplier, date)
VALUES 
	( 1, 55, 'tipyli', '2024-12-09'),
	( 3, 51, 'lapki', '2024-12-09'),
	( 2, 56, 'did_baba', '2024-12-09'),
	( 5, 17, 'slych', '2024-12-09'),
	( 6, 40, 'mleko', '2024-12-09'),
	( 8, 34, 'did_baba', '2024-12-09'),
	( 6, 85, 'mleko', '2024-12-09'),
	( 4, 13, 'zabiy', '2024-12-09'),
	( 9, 965, 'popki', '2024-12-09'),
	( 11, 62, 'chyhpani', '2024-12-09'),
	( 3, 1, 'lapki', '2024-12-09'),
	( 7, 76, 'ROSHEN', '2024-12-09'),
	( 7, 33, 'ROSHEN', '2024-12-09');

SELECT product_id, SUM(weight)
FROM delivery
GROUP BY product_id;

CREATE TABLE sklad (
	product_id BIGINT NOT NULL,
	full_weight numeric(18,3) NOT NULL,
	"min" numeric(18,3) NOT NULL,

	CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES products(products_id)
);

INSERT INTO sklad (product_id, full_weight, "min")
VALUES 
	 (1, 4000, 2000),
	 (2, 14, 20),
	 (3, 403.2, 500),
	 (4, 756.1, 200),
	 (5, 3124, 1000),
	 (6, 56.32, 100),
	 (7, 2344, 2345),
	 (8, 988776, 123456783),
	 (9, 1232.12, 1232.15),
	 (10, 8765, 5000),
	 (11, 345, 467);

SELECT s.product_id, c.name
FROM sklad s
JOIN products p ON p.products_id = s.product_id
JOIN category c ON p.category = c.category_id  
WHERE full_weight < "min";