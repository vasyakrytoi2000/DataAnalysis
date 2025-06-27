SELECT p.products_id, p.price, c.name
FROM products p
JOIN category c ON p.category = c.category_id
WHERE p.price::numeric > (SELECT AVG(price::numeric) FROM products);

SELECT oi.products_id, ARRAY_AGG(c.name) AS category, COUNT(oi.items_id) AS count_of_orders 
FROM order_items oi
JOIN products p ON p.products_id = oi.products_id
JOIN category c ON c.category_id = p.category
GROUP BY oi.products_id
HAVING COUNT(oi.items_id) = 
( SELECT MAX(item_count)
	FROM 
		(SELECT oi.products_id, COUNT(oi.items_id) AS item_count
			FROM order_items oi
			GROUP BY oi.products_id)
);

SELECT o.castomer_id, COUNT(o.items) AS count_items, ARRAY_AGG(oi.products_id) AS products_id, ARRAY_AGG(c.name) AS category
FROM orders o
JOIN order_items oi ON oi.items_id = o.items
JOIN products p ON p.products_id = oi.products_id
JOIN category c ON c.category_id = p.category
GROUP BY o.castomer_id
HAVING COUNT(o.items) > (
	SELECT AVG(count_items)
	FROM ( SELECT COUNT(items) AS count_items
		   FROM orders
		   GROUP BY castomer_id)
);
