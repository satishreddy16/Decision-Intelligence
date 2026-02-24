# Decision Intelligence Agent for Executive KPI Monitoring

## Business Context
Executives often rely on static dashboards and ad-hoc analysis to understand
business performance. While dashboards report historical metrics, they rarely
answer the critical follow-up questions required for decision-making:

- Why did performance change?
- Which factors contributed most?
- What actions should be taken next?
- What is the expected business impact?

This gap results in delayed responses, inconsistent interpretations,
and inefficient use of analytics resources.



## Solution Overview
This project implements a **Decision Intelligence Agent** that automates
KPI monitoring and supports business decisions by:

1. Calculating key performance indicators on a recurring basis  
2. Detecting statistically significant deviations from historical baselines  
3. Identifying the primary business drivers behind KPI changes  
4. Generating clear, executive-ready explanations and recommendations  
5. Logging insights into a structured decision journal for traceability  

The system is designed to complement dashboards by adding
**context, explanation, and actionability**.

---

## Why a Decision Agent (Not Just Reporting)
Traditional dashboards describe *what* happened.
This system focuses on *why* it happened and *what should be done next*.

The agent:
- Applies consistent evaluation logic across time
- Reduces manual diagnostic effort
- Produces repeatable and explainable recommendations
- Enables proactive rather than reactive decision-making

---

## System Architecture
The solution follows a modular analytics pipeline:

1. **Metrics Layer (SQL)**  
   - Daily and segmented KPI computation

2. **Anomaly Detection Module**  
   - Comparison against rolling historical baselines

3. **Driver Analysis Module**  
   - Quantification of segment-level contributions

4. **Explanation & Recommendation Layer**  
   - LLM-based narrative generation using structured evidence

5. **Decision Log Output**  
   - Persisted insights for reporting and review

Architecture details are documented in the `/docs` directory.

---

## KPIs Monitored
- Revenue
- Order Volume
- Average Order Value (AOV)
- New Customers
- Repeat Purchase Rate
- Refund / Cancellation Rate

KPIs are evaluated both in aggregate and across key segments
(e.g., region, channel, product category).

---

## Decision Log Example

| Date | KPI | Change (%) | Primary Driver | Summary | Recommended Action | Confidence |
|------|-----|------------|----------------|---------|--------------------|------------|
| 2024-09-15 | Revenue | -22% | Paid Channel – West | Revenue decline driven by reduced conversion in paid traffic | Review campaign targeting and reallocate spend | High |

---

## Business Value
- Reduced time required to identify performance issues
- Improved clarity around root causes of KPI movements
- More consistent and evidence-based recommendations
- Better alignment between analytics output and executive decisions

---

## Limitations
- Anomaly detection is statistical rather than predictive
- Recommendations are advisory and require human approval
- Data is historical rather than real-time

---

## Planned Enhancements
- Near real-time data ingestion
- Causal impact analysis
- Automated alert delivery
- Ongoing evaluation of recommendation quality
