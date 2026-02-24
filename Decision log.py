import os
import json
import uuid
import pandas as pd
from typing import Dict, List
from datetime import datetime

def to_log_row(anomaly, top_drivers: List[Dict], llm_output: Dict) -> Dict:
    return {
        "log_id": str(uuid.uuid4()),
        "run_ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "date": anomaly.date,
        "kpi": anomaly.kpi,
        "anomaly_type": anomaly.anomaly_type,
        "delta_pct": anomaly.delta_pct,
        "baseline_mean": anomaly.baseline_mean,
        "baseline_std": anomaly.baseline_std,
        "top_drivers": json.dumps(top_drivers, ensure_ascii=False),
        "summary": json.dumps(llm_output.get("summary_bullets", []), ensure_ascii=False),
        "recommendations": json.dumps(llm_output.get("recommended_actions", []), ensure_ascii=False),
        "risks_and_checks": json.dumps(llm_output.get("risks_and_checks", []), ensure_ascii=False),
        "confidence": llm_output.get("confidence", "Unknown"),
    }

def write_decision_log_csv(rows: List[Dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(rows)
    if os.path.exists(path):
        df_existing = pd.read_csv(path)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(path, index=False)
