import sqlite3
import pandas as pd
from typing import Tuple

def run_query(conn: sqlite3.Connection, sql_path: str) -> pd.DataFrame:
    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
    return pd.read_sql_query(sql, conn)

def get_kpis(conn: sqlite3.Connection) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      kpi_daily_df: one row per day with KPI columns
      kpi_segment_df: one row per day per segment (e.g., region)
    """
    kpi_daily_df = run_query(conn, "sql/kpi_daily.sql")
    kpi_segment_df = run_query(conn, "sql/kpi_segment.sql")
    return kpi_daily_df, kpi_segment_df
