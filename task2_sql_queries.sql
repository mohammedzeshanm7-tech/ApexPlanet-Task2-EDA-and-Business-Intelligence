-- TASK 2: SQL for Business Questions (classicmodels)
-- Database: classicmodels (MySQL sample database)
-- Revenue = quantityOrdered x priceEach, cancelled orders are excluded.

USE classicmodels;

-- Q1. What are the top 5 products by revenue?
-- (3-table join: orderdetails + orders + products)

SELECT p.productName,
       SUM(od.quantityOrdered) AS units_sold,
       ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS revenue
FROM orderdetails od
JOIN orders o ON od.orderNumber = o.orderNumber
JOIN products p ON od.productCode = p.productCode
WHERE o.status <> 'Cancelled'
GROUP BY p.productCode, p.productName
ORDER BY revenue DESC
LIMIT 5;

-- Q2. What is the monthly trend of orders and revenue?
-- (join: orders + orderdetails)

SELECT DATE_FORMAT(o.orderDate, '%Y-%m') AS order_month,
       COUNT(DISTINCT o.orderNumber) AS total_orders,
       ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS revenue
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE o.status <> 'Cancelled'
GROUP BY order_month
ORDER BY order_month;

-- Q3. Which product lines bring the most revenue?
-- (3-table join: orders + orderdetails + products)

SELECT p.productLine,
       SUM(od.quantityOrdered) AS units_sold,
       ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS revenue
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
WHERE o.status <> 'Cancelled'
GROUP BY p.productLine
ORDER BY revenue DESC;

-- Q4. Who are the top 10 customers by total payments?
-- (join: customers + payments)

SELECT c.customerName,
       c.country,
       ROUND(SUM(pay.amount), 2) AS total_paid
FROM customers c
JOIN payments pay ON c.customerNumber = pay.customerNumber
GROUP BY c.customerNumber, c.customerName, c.country
ORDER BY total_paid DESC
LIMIT 10;

-- Q5. Which 5 countries bring the most revenue?
-- (3-table join: customers + orders + orderdetails)

SELECT c.country,
       COUNT(DISTINCT o.orderNumber) AS total_orders,
       ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS revenue
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE o.status <> 'Cancelled'
GROUP BY c.country
ORDER BY revenue DESC
LIMIT 5;

-- Q6. Which 5 sales reps bring the most revenue?
-- (4-table join: employees + customers + orders + orderdetails)

SELECT CONCAT(e.firstName, ' ', e.lastName) AS sales_rep,
       COUNT(DISTINCT c.customerNumber) AS customers_handled,
       ROUND(SUM(od.quantityOrdered * od.priceEach), 2) AS revenue
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE o.status <> 'Cancelled'
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY revenue DESC
LIMIT 5;

-- Q7. How many orders were shipped late (after the required date) each year?
-- (orders table, filtering + aggregation)

SELECT YEAR(orderDate) AS order_year,
       COUNT(*) AS shipped_orders,
       SUM(shippedDate > requiredDate) AS late_orders,
       ROUND(SUM(shippedDate > requiredDate) * 100.0 / COUNT(*), 1) AS pct_late
FROM orders
WHERE shippedDate IS NOT NULL
GROUP BY YEAR(orderDate)
ORDER BY order_year;
