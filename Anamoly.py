import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class Anomaly:
    date: str
    kpi: str
    current: float
    baseline_mean: float
    baseline_std: float
    delta_pct: float
    z_score: float
    anomaly_type: str  # "spike" or "drop"

def detect_anomalies(
    kpi_daily: pd.DataFrame,
    kpi_cols: List[str],
    window: int = 28,
    z_threshold: float = 2.5,
    pct_threshold: float = 0.20,
) -> List[Anomaly]:
    df = kpi_daily.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    anomalies: List[Anomaly] = []

    for kpi in kpi_cols:
        series = df[kpi].astype(float)

        rolling_mean = series.rolling(window=window, min_periods=window).mean()
        rolling_std = series.rolling(window=window, min_periods=window).std(ddof=0)

        current = series
        mean = rolling_mean
        std = rolling_std.replace(0, np.nan)

        z = (current - mean) / std
        delta_pct = (current - mean) / mean.replace(0, np.nan)

        for i in range(len(df)):
            if np.isnan(mean.iloc[i]) or np.isnan(std.iloc[i]):
                continue

            is_z = abs(z.iloc[i]) >= z_threshold
            is_pct = abs(delta_pct.iloc[i]) >= pct_threshold

            if is_z or is_pct:
                anomaly_type = "spike" if delta_pct.iloc[i] > 0 else "drop"
                anomalies.append(
                    Anomaly(
                        date=df["date"].iloc[i].date().isoformat(),
                        kpi=kpi,
                        current=float(current.iloc[i]),
                        baseline_mean=float(mean.iloc[i]),
                        baseline_std=float(std.iloc[i]),
                        delta_pct=float(delta_pct.iloc[i]),
                        z_score=float(z.iloc[i]) if not np.isnan(z.iloc[i]) else 0.0,
                        anomaly_type=anomaly_type,
                    )
                )

    return anomalies
