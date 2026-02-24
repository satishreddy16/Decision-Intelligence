import pandas as pd
from typing import Dict, List

def driver_contributions(
    kpi_segment: pd.DataFrame,
    date: str,
    kpi: str,
    segment_col: str = "segment_value",
    value_col: str = "revenue",
    baseline_days: int = 28,
) -> List[Dict]:
    """
    Quantifies which segments contributed most to the KPI change on a given date.
    For MVP we use a baseline = mean of previous N days for each segment.
    """
    df = kpi_segment.copy()
    df["date"] = pd.to_datetime(df["date"])
    target_date = pd.to_datetime(date)

    seg = df[[ "date", segment_col, value_col ]].copy()
    seg = seg.sort_values(["date", segment_col])

    # Baseline window: previous N days (excluding target date)
    window_mask = (seg["date"] < target_date) & (seg["date"] >= target_date - pd.Timedelta(days=baseline_days))
    base = seg[window_mask].groupby(segment_col)[value_col].mean().rename("baseline").reset_index()

    curr = seg[seg["date"] == target_date][[segment_col, value_col]].rename(columns={value_col: "current"})

    merged = curr.merge(base, on=segment_col, how="left")
    merged["baseline"] = merged["baseline"].fillna(0.0)
    merged["delta"] = merged["current"] - merged["baseline"]

    # Sort by absolute contribution
    merged = merged.sort_values("delta", ascending=False)

    drivers = []
    for _, row in merged.head(5).iterrows():
        drivers.append({
            "segment": str(row[segment_col]),
            "current": float(row["current"]),
            "baseline": float(row["baseline"]),
            "delta": float(row["delta"]),
        })

    return drivers
