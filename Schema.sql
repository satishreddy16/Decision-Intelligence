-- Minimal schema for the MVP (adapt column names to your dataset)

CREATE TABLE IF NOT EXISTS orders (
  order_id TEXT,
  customer_id TEXT,
  order_date TEXT,           -- store as ISO date string for SQLite
  revenue REAL,
  region TEXT,
  channel TEXT,
  category TEXT,
  is_refund INTEGER          -- 0/1
);

-- Helpful indexes (optional)
CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);

-- Daily KPIs
-- Output columns:
-- date, revenue, orders, aov, new_customers, repeat_purchase_rate, refund_rate

WITH base AS (
  SELECT
    DATE(order_date) AS date,
    order_id,
    customer_id,
    revenue,
    COALESCE(is_refund, 0) AS is_refund
  FROM orders
),
first_purchase AS (
  SELECT
    customer_id,
    MIN(DATE(order_date)) AS first_date
  FROM orders
  GROUP BY customer_id
),
daily AS (
  SELECT
    b.date,
    SUM(CASE WHEN b.is_refund = 0 THEN b.revenue ELSE 0 END) AS revenue,
    COUNT(DISTINCT CASE WHEN b.is_refund = 0 THEN b.order_id END) AS orders,
    COUNT(DISTINCT CASE WHEN fp.first_date = b.date THEN b.customer_id END) AS new_customers,
    COUNT(DISTINCT CASE WHEN fp.first_date < b.date THEN b.customer_id END) AS returning_customers,
    COUNT(DISTINCT b.customer_id) AS active_customers,
    SUM(CASE WHEN b.is_refund = 1 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(DISTINCT b.order_id), 0) AS refund_rate
  FROM base b
  LEFT JOIN first_purchase fp ON fp.customer_id = b.customer_id
  GROUP BY b.date
)
SELECT
  date,
  revenue,
  orders,
  CASE WHEN orders = 0 THEN NULL ELSE revenue * 1.0 / orders END AS aov,
  new_customers,
  CASE WHEN active_customers = 0 THEN NULL ELSE returning_customers * 1.0 / active_customers END AS repeat_purchase_rate,
  refund_rate
FROM daily
ORDER BY date;
