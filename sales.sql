-- Sales by product category
SELECT 
    p.category,
    SUM(s.quantity * s.price) AS category_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- Sales by region (assumes region is in customer table)
SELECT 
    c.region,
    SUM(s.quantity * s.price) AS regional_revenue
FROM sales s
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY c.region
ORDER BY regional_revenue DESC;

-- Stockout risk reduction example: identify underperforming stock
SELECT 
    p.product_name,
    p.stock_quantity,
    COUNT(s.sale_id) AS sales_count
FROM products p
LEFT JOIN sales s ON s.product_id = p.product_id
GROUP BY p.product_name, p.stock_quantity
HAVING COUNT(s.sale_id) < 10 AND p.stock_quantity > 0
ORDER BY p.stock_quantity DESC;
