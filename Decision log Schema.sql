CREATE TABLE IF NOT EXISTS decision_log (
  log_id TEXT,
  run_ts TEXT,
  date TEXT,
  kpi TEXT,
  anomaly_type TEXT,
  delta_pct REAL,
  baseline_mean REAL,
  baseline_std REAL,
  top_drivers TEXT,          -- JSON string
  summary TEXT,              -- JSON string
  recommendations TEXT,      -- JSON string
  risks_and_checks TEXT,     -- JSON string
  confidence TEXT
);
