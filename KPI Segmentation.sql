-- Segment KPIs by region (duplicate this query for channel/category if needed)

WITH base AS (
  SELECT
    DATE(order_date) AS date,
    region,
    order_id,
    customer_id,
    revenue,
    COALESCE(is_refund, 0) AS is_refund
  FROM orders
)
SELECT
  date,
  region AS segment_value,
  SUM(CASE WHEN is_refund = 0 THEN revenue ELSE 0 END) AS revenue,
  COUNT(DISTINCT CASE WHEN is_refund = 0 THEN order_id END) AS orders,
  CASE
    WHEN COUNT(DISTINCT CASE WHEN is_refund = 0 THEN order_id END) = 0 THEN NULL
    ELSE SUM(CASE WHEN is_refund = 0 THEN revenue ELSE 0 END) * 1.0
         / COUNT(DISTINCT CASE WHEN is_refund = 0 THEN order_id END)
  END AS aov,
  COUNT(DISTINCT customer_id) AS active_customers
FROM base
GROUP BY date, region
ORDER BY date, region;
