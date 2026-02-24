import sqlite3
from src.config import SETTINGS
from src.metrics import get_kpis
from src.anomaly import detect_anomalies
from src.drivers import driver_contributions
from src.llm_explainer import explain_with_llm
from src.decision_log import to_log_row, write_decision_log_csv

def main():
    conn = sqlite3.connect(SETTINGS.db_path)

    kpi_daily, kpi_segment = get_kpis(conn)

    # Choose KPI columns that exist in your kpi_daily query output
    kpi_cols = ["revenue", "orders", "aov", "new_customers", "repeat_purchase_rate", "refund_rate"]
    kpi_cols = [c for c in kpi_cols if c in kpi_daily.columns]

    anomalies = detect_anomalies(kpi_daily, kpi_cols=kpi_cols)

    rows = []
    for a in anomalies:
        # For MVP, run driver analysis on revenue-like metrics
        value_col = "revenue" if "revenue" in kpi_segment.columns else "revenue"
        top_drivers = driver_contributions(
            kpi_segment=kpi_segment,
            date=a.date,
            kpi=a.kpi,
            segment_col="segment_value",
            value_col=value_col
        )

        payload = {
            "date": a.date,
            "kpi": a.kpi,
            "anomaly_type": a.anomaly_type,
            "current": a.current,
            "baseline_mean": a.baseline_mean,
            "baseline_std": a.baseline_std,
            "delta_pct": a.delta_pct,
            "top_drivers": top_drivers,
        }

        llm_output = explain_with_llm(payload)
        rows.append(to_log_row(a, top_drivers, llm_output))

    write_decision_log_csv(rows, SETTINGS.decision_log_csv)
    print(f"Wrote {len(rows)} decision log rows to: {SETTINGS.decision_log_csv}")

if __name__ == "__main__":
    main()
