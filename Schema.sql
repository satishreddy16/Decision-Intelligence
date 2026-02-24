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
