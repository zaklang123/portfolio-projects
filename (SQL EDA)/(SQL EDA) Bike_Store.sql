-- Exploratory Data Analysis (Bike Stores)
-- Data was obtained from https://www.sqlservertutorial.net/sql-server-sample-database/


-- Where are the majority of customers from?

SELECT state, COUNT(customer_id) AS num_customers, ROUND(100*COUNT(customer_id)/SUM(COUNT(customer_id)) OVER(), 0) AS percent_of_total_customers
FROM customers
GROUP BY state
ORDER BY num_customers DESC

-- Most customers buy products in New York (71%) followed by California (20%) and Texas (10%). It seems as though there are only customers in these states.



-- What is the most commonly bought product?

SELECT order_items.product_id, SUM(order_items.quantity) AS total_quantity, products.product_name
FROM order_items
LEFT JOIN products USING(product_id)
GROUP BY product_id, product_name
ORDER BY total_quantity DESC

-- The most commonly bought product is a Surly Ice Cream Trucj Frameset - 2016 (with 167 of them bought)

SELECT order_items.product_id, COUNT(order_items.quantity) AS total_order_quantity, products.product_name, AVG(order_items.list_price)
FROM order_items
LEFT JOIN products USING(product_id)
GROUP BY product_id, product_name
ORDER BY total_order_quantity DESC

-- The most commonly bought product per order is also a Surly Ice Cream Trucj Frameset - 2016 (with 110 of them bought)

WITH product_by_quantity AS
	(SELECT order_items.product_id, SUM(order_items.quantity) AS total_quantity, products.product_name
	FROM order_items
	LEFT JOIN products USING(product_id)
	GROUP BY product_id, product_name
	ORDER BY total_quantity DESC)
SELECT COUNT(product_id)
FROM product_by_quantity
WHERE total_quantity = 1

-- There are 32 products that are only sold once.


-- What email providers are the most popular among customers?

WITH email AS
	(SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(email, '@', -1), '.', 1) AS email_provider
	FROM customers)
SELECT email_provider, COUNT(email_provider) AS num_of_users, ROUND(100*COUNT(email_provider)/SUM(COUNT(email_provider)) OVER(), 0) AS percent_customers_with_email_provider
FROM email
GROUP BY email_provider
ORDER BY num_of_users DESC

-- The bike store's customers use 5 email providers Yahoo, Gmail, MSN, AOL, and Hotmail. They use them in approximately the same proportion. 


-- What is the most expensive product sold, and what is the least expensive product sold?

SELECT products.product_id, products.product_name, MAX(products.list_price) AS list_price, SUM(order_items.quantity) AS items_sold
FROM products 
RIGHT JOIN order_items
ON order_items.product_id = products.product_id
GROUP BY product_id, product_name
ORDER BY MAX(list_price) DESC
LIMIT 1

-- The most expensive product is Trek Domane SLR 9 Disc - 2018 with a list price of $11999.99 and a total of 5 sold.

SELECT products.product_id, products.product_name, MAX(products.list_price) AS list_price, SUM(order_items.quantity) AS items_sold
FROM products 
RIGHT JOIN order_items
ON order_items.product_id = products.product_id
GROUP BY product_id, product_name
ORDER BY MAX(list_price) ASC
LIMIT 1

-- The least expensive product sold is Strider Classic 12 Balance Bike - 2018 with a list price of $89.99 and a total of 11 sold.


-- Which store has the most revenue and are the store employees allocated efficiently?

WITH revenue_cte AS
(SELECT order_id, SUM((list_price - discount)*quantity) AS revenue
FROM order_items
GROUP BY order_id),
store_revenue AS
(SELECT o.store_id, SUM(r.revenue) AS revenue
FROM revenue_cte AS r
LEFT JOIN orders AS o
ON r.order_id = o.order_id
GROUP BY o.store_id)
SELECT st.store_id, st.store_name, st.city, st.state, COUNT(s.staff_id) AS num_of_staff, ROUND(SUM(str.revenue), 0) AS total_revenue, ROUND(100*ROUND(SUM(str.revenue), 0)/SUM(ROUND(SUM(str.revenue), 0)) OVER(), 0) AS percent_of_total_revenue
FROM stores AS st
RIGHT JOIN staffs AS s 
ON s.store_id = st.store_id
JOIN store_revenue AS str
ON str.store_id = st.store_id
GROUP BY st.store_id, st.store_name, st.city, st.state
ORDER BY total_revenue DESC

-- The store in Baldwin, NY earns 63% of the revenue. Whereas, Santa Cruz, CA and Rowlett, TX earn 26% and 10% of the revenue respectively. The employees are allocated in an approximately even fashion with 3 in NY, 3 in TX, and 4 in CA.


-- What brands contribute the most to total revenue?

SELECT b.brand_name, ROUND(SUM(o.quantity * (o.list_price - o.discount)), 0) AS total_revenue, ROUND(100*ROUND(SUM(o.quantity * (o.list_price - o.discount)), 0)/SUM(ROUND(SUM(o.quantity * (o.list_price - o.discount)), 0)) OVER(), 1) AS percent_revenue
FROM brands AS b
RIGHT JOIN products AS p
ON b.brand_id = p.brand_id
RIGHT JOIN order_items AS o
ON o.product_id = p.product_id
GROUP BY b.brand_name
ORDER BY total_revenue DESC

-- Trek represents 59.8% of the total revenue with $5 million sold. Strider represents 0.1% of the total revenue with $5000 sold.






