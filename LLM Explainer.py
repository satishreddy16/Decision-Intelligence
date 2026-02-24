import json
from typing import Dict, List

def build_prompt(payload: Dict) -> str:
    system = (
        "You are a senior business analyst writing for executives. "
        "Use only the provided evidence. Quantify drivers. Avoid speculation. "
        "Return valid JSON with keys: summary_bullets, likely_drivers, "
        "recommended_actions, risks_and_checks, confidence."
    )
    user = f"Evidence (JSON):\n{json.dumps(payload, indent=2)}"
    return system + "\n\n" + user

def explain_with_llm(payload: Dict) -> Dict:
    """
    MVP stub:
    - If you have an LLM API, plug it in here.
    - Otherwise return a deterministic, evidence-based template response.
    """
    # Deterministic fallback (still professional)
    kpi = payload.get("kpi")
    delta_pct = payload.get("delta_pct")
    date = payload.get("date")
    drivers: List[Dict] = payload.get("top_drivers", [])

    driver_text = []
    for d in drivers[:3]:
        driver_text.append(f"{d['segment']} (Δ {d['delta']:.2f})")

    response = {
        "summary_bullets": [
            f"{kpi} showed an anomalous movement on {date} (Δ {delta_pct*100:.1f}%).",
            f"Top contributing segments: {', '.join(driver_text) if driver_text else 'Insufficient segment evidence available.'}",
            "Recommendation focuses on isolating the primary driver and validating data integrity before actioning changes."
        ],
        "likely_drivers": drivers[:3],
        "recommended_actions": [
            "Validate tracking/data quality for the affected segment(s) and confirm the change is not an instrumentation issue.",
            "Review recent changes (campaigns, pricing, inventory, UX) tied to the top driver segments and identify the most plausible operational cause.",
            "Run a short-term controlled adjustment (e.g., budget reallocation, targeting change, inventory fix) and monitor KPI recovery over 48–72 hours."
        ],
        "risks_and_checks": [
            "Risk: Overreacting to noise. Check whether the anomaly persists beyond one period.",
            "Risk: Misattribution due to missing segment coverage. Confirm segmentation completeness."
        ],
        "confidence": "Medium"
    }
    return response
