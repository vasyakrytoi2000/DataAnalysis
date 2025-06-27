CREATE VIEW availability 
AS
SELECT s.name, s.address, ARRAY_AGG(p.products_id) AS product_id
FROM suppliers s
JOIN products p ON s.name = p.suppliers_name
WHERE p.availability = TRUE
GROUP BY s.name, s.address;

CREATE VIEW date
AS
SELECT p.products_id, p.category, category.name,description
FROM products p
JOIN category  ON p.category = category_id
WHERE p.realization_date <= '2024-11-10';

CREATE VIEW all_weight
AS 
SELECT product_id, SUM(weight)
FROM delivery
GROUP BY product_id;

CREATE VIEW min_min
AS
SELECT s.product_id, c.name
FROM sklad s
JOIN products p ON p.products_id = s.product_id
JOIN category c ON p.category = c.category_id  
WHERE full_weight < "min";

CREATE TABLE positions(
	position_id SERIAL PRIMARY KEY,
	name VARCHAR(64) NOT NULL,
	head INT 
);

CREATE TABLE workers(
	worker_id SERIAL PRIMARY KEY,
	name VARCHAR(64) NOT NULL,
	surname VARCHAR(64) NOT NULL,
	position_id BIGINT NOT NULL,

	CONSTRAINT fk_position FOREIGN KEY (position_id) REFERENCES positions(position_id)
);

INSERT INTO positions(name, head)
VALUES
	('director', NULL),
	('meneger', 1),
	('men_vid', 2),
	('konsyltant', 3),
	('casir', 4),
	('vantagnik', 5),
	('ohorona', 5),
	('skladalnik', 3);

INSERT INTO workers(name, surname, position_id)
VALUES 
	('Vasil', 'Chorni', 1),
	('Vitia', 'Shyryp', 2),
	('Julia', 'Skovoroda', 2),
	('Yarik', 'Stil', 8),
	('Vika', 'Gnom', 3),
	('Stas', 'Noj', 3),
	('Artem', 'Gyba', 3),
	('Yura', 'Energetik', 7),
	('Nastia', 'Batareyka', 3),
	('Sanya', 'Paravoz', 4),
	('Lilia', 'Zavoz', 4),
	('Dasha', 'Krop', 8),
	('Vlados', 'Pampyska', 5),
	('Ilia', 'Kovbasa', 5),
	('Olya', 'Podik', 5),
	('Katia', 'Pivas', 6),
	('Zlata', 'Dovga', 7);

CREATE RECURSIVE VIEW rabotniki (worker_id, name, surname, position_id, position_name, head) AS
    SELECT w.worker_id, w.name, w.surname, w.position_id, p.name AS position_name, p.head
    FROM workers w
    JOIN positions p ON p.position_id = w.position_id
    WHERE p.head IS NULL
    UNION
    SELECT w.worker_id, w.name, w.surname, w.position_id, p.name AS position_name, p.head
    FROM workers w
    JOIN positions p ON p.position_id = w.position_id
    JOIN rabotniki r ON r.position_id = p.head




