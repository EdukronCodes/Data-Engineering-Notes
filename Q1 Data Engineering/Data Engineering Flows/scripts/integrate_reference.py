"""Integrate Analytics6 reference notes into project markdown files."""
from pathlib import Path

ROOT = Path(r"c:\Users\Admin\Desktop\Data Engineering Flows")
REF_URL = "https://github.com/Analytics6/Azure-Data-Engineering-Notes"

PLATFORM = """
## Platform Concepts (Analytics6 Reference)

**Medallion ADLS layout:** Landing by source → Pre-Bronze (schema validation) → Bronze (immutable Delta) → Silver (cleansed, DQ, SCD) → Gold (business models) → Archive.

**ADF:** Metadata-driven ingestion (Lookup + ForEach), watermark incrementals, CDC, exponential backoff, audit logging. Linked services use MSI + Key Vault; SHIR for on-prem.

**Databricks / Delta:** MERGE incrementals, `OPTIMIZE`/`VACUUM`, partition pruning, Unity Catalog governance.

**Monitoring:** Log Analytics diagnostics, pipeline failure action groups, SLA KQL dashboards.
"""

UPDATE_MAP = {
    "projects/vikitha/vikitha-01-customer-recommendation.md": "03-Customer-Behavior-Analytics-Engine.md, 10-Retail-Customer-Analytics-Platform.md",
    "projects/vikitha/vikitha-02-ecommerce-ssis-migration.md": "15-Retail-Migration-OnPrem-to-Azure.md, Data_Platform_Development_Global_Organisation.md",
    "projects/vikitha/vikitha-03-retail-customer-analytics-support.md": "14-Retail-Support-Project.md",
    "projects/shiva/shiva-01-finlake-banking-dw.md": "02-Financial-Data-Processing-System.md, Banking_Transaction_Processing_Pipeline.md",
    "projects/shiva/shiva-02-streampulse-ecommerce.md": "04-Retail-E-commerce-Data-Platform.md",
    "projects/shiva/shiva-03-orderflow-sla.md": "09-Enterprise-Data-Governance-Observability-Platform.md, 12-Supply-Chain-Optimization-Dashboard.md",
    "projects/pavani/pavani-01-realtime-inventory-supply-chain.md": "01-Supply-Chain-Analytics-Platform.md, 12-Supply-Chain-Optimization-Dashboard.md",
    "projects/pavani/pavani-02-legacy-pos-erp-migration.md": "15-Retail-Migration-OnPrem-to-Azure.md",
    "projects/pavani/pavani-03-inventory-pipeline-support.md": "14-Retail-Support-Project.md",
}

CREATE_MAP = {
    "projects/devi/devi-01-sales-analytics-forecasting.md": {
        "title": "# Retail Sales Analytics & Forecasting Platform (Devi)",
        "refs": "17-Sales-and-Content-Performance-Analytics.md, Retail_Sales_Analytics_Pipeline.md",
        "overview": "Analyze sales funnels, campaign performance, and attribution across channels; batch medallion with Databricks forecasting models.",
        "diff": "**Devi focus:** Synapse dedicated SQL serving + Prophet/ARIMA demand models; not streaming-first.",
        "pipelines": ["PL_DEVI_Bronze_Sales", "PL_DEVI_Silver_Gold", "PL_DEVI_Forecast_Scoring", "PL_DEVI_Attribution"],
        "notebooks": ["/Devi/Sales/NB_Bronze_Orders", "NB_Silver_Attribution", "NB_Gold_Forecast", "NB_Model_Scoring"],
        "gold": ["gold.fact_sales_daily", "gold.forecast_sku_week", "gold.campaign_attribution"],
    },
    "projects/devi/devi-02-etl-monitoring-support.md": {
        "title": "# Retail ETL Pipeline Monitoring & Production Support (Devi)",
        "refs": "14-Retail-Support-Project.md, 09-Enterprise-Data-Governance-Observability-Platform.md",
        "overview": "L2 support for retail ETL: incident runbooks, SLA dashboards, automated retries on ADF failures.",
        "diff": "**Devi focus:** Retail domain runbooks (POS, promo calendars) and ETL-specific KQL workbooks.",
        "pipelines": ["PL_DEVI_Health_Check", "PL_DEVI_Incident_Retry", "PL_DEVI_SLA_Report"],
        "notebooks": ["/Devi/Support/NB_Pipeline_Audit", "NB_SLA_Metrics"],
        "gold": ["support.pipeline_runs", "support.sla_daily"],
    },
    "projects/devi/devi-03-onprem-dw-migration-lakehouse.md": {
        "title": "# On-Premise Retail DW Migration to Azure Lakehouse (Devi)",
        "refs": "15-Retail-Migration-OnPrem-to-Azure.md",
        "overview": "Classic on-prem SQL Server DW cutover to Synapse dedicated SQL + ADLS medallion.",
        "diff": "**Devi focus:** Synapse dedicated pool external tables (not Databricks SQL warehouse).",
        "pipelines": ["PL_DEVI_MIG_Bronze", "PL_DEVI_MIG_Silver_Gold", "PL_DEVI_MIG_Validation", "PL_DEVI_Cutover"],
        "notebooks": ["/Devi/Migration/NB_Silver_Conform", "NB_Gold_Star_Schema", "NB_Reconcile"],
        "gold": ["gold.fact_retail_sales", "gold.dim_store"],
    },
    "projects/mugalin/mugalin-01-smartretail-streaming.md": {
        "title": "# SmartRetail Real-Time Inventory & Demand Streaming (Mugalin)",
        "refs": "04-Retail-E-commerce-Data-Platform.md, Multi_Channel_Retail_Data_Platform.md",
        "overview": "Micro-batch demand signals from e-commerce + POS for inventory allocation; Event Hubs + Structured Streaming.",
        "diff": "**Mugalin focus:** Demand forecasting micro-batch (5-min) vs Pavani supply-chain SLA alerts.",
        "pipelines": ["PL_MUG_Stream_Health", "PL_MUG_Bronze_Orders", "PL_MUG_Gold_Demand"],
        "notebooks": ["/Mugalin/NB_Stream_Orders", "NB_Gold_Demand_Forecast_Input"],
        "gold": ["gold.demand_signal_5min", "gold.inventory_allocation"],
    },
    "projects/mugalin/mugalin-02-enterprise-dw-migration.md": {
        "title": "# Enterprise Retail DW Migration to Databricks (Mugalin)",
        "refs": "15-Retail-Migration-OnPrem-to-Azure.md, Data_Platform_Development_Global_Organisation.md",
        "overview": "Full enterprise star schema lift from on-prem SSIS/SQL to Databricks SQL warehouse.",
        "diff": "**Mugalin focus:** Enterprise-wide star schema (all retail domains) vs Vikitha SSIS package conversion scope.",
        "pipelines": ["PL_MUG_MIG_Factory", "PL_MUG_MIG_Validation"],
        "notebooks": ["/Mugalin/Migration/NB_Enterprise_Gold"],
        "gold": ["gold.enterprise_fact_sales", "gold.enterprise_dim_product"],
    },
    "projects/mugalin/mugalin-03-etl-production-support.md": {
        "title": "# Retail ETL Production Support & Incident Resolution (Mugalin)",
        "refs": "14-Retail-Support-Project.md",
        "overview": "Production support with automated remediation for common ADF/Databricks failures.",
        "diff": "**Mugalin focus:** Incident resolution playbooks and Logic App auto-retry chains.",
        "pipelines": ["PL_MUG_Support_Health", "PL_MUG_Auto_Remediate"],
        "notebooks": ["/Mugalin/Support/NB_Incident_Log"],
        "gold": ["support.incidents"],
    },
    "projects/karthik/karthik-01-inventory-replenishment-batch.md": {
        "title": "# Retail Inventory Replenishment & Batch Analytics (Karthik)",
        "refs": "01-Supply-Chain-Analytics-Platform.md, 05-Retail-Store-Performance-Analytics-Platform.md",
        "overview": "Batch replenishment models using WMS/ERP feeds; nightly ADF + Databricks batch.",
        "diff": "**Karthik focus:** Replenishment optimization batch (not real-time streaming).",
        "pipelines": ["PL_KAR_Replenish_Bronze", "PL_KAR_Replenish_Gold"],
        "notebooks": ["/Karthik/NB_Replenishment_Model", "NB_Store_Performance"],
        "gold": ["gold.replenishment_recommendation", "gold.store_performance_daily"],
    },
    "projects/karthik/karthik-02-loans-collections-datamart.md": {
        "title": "# Loans & Collections Enterprise Reporting Data Mart (Karthik)",
        "refs": "02-Financial-Data-Processing-System.md, 11-Banking-Risk-Management-System.md",
        "overview": "Financial data mart for loans, collections, and risk KPIs with SOX audit trails.",
        "diff": "**Karthik focus:** Collections/regulatory reporting mart (lighter than Shiva core banking DW).",
        "pipelines": ["PL_KAR_LOAN_Bronze", "PL_KAR_LOAN_Gold", "PL_KAR_Risk_Weekly"],
        "notebooks": ["/Karthik/Loans/NB_Silver_Conform", "NB_Gold_Collections", "NB_Risk_Summary"],
        "gold": ["gold.fact_loan_balance", "gold.collections_aging", "gold.risk_exposure"],
    },
    "projects/karthik/karthik-03-irrops-airline-batch.md": {
        "title": "# IRROPS Airline Operations Batch Reporting & Alerting (Karthik)",
        "refs": "08-Serverless-Data-Processing-Kubernetes-Orchestration.md, Data_Pipeline_Optimization_Fertilizer_Company.md",
        "overview": "Batch IRROPS (irregular operations) reporting: flight delays, crew, baggage with SLA alerts.",
        "diff": "**Karthik focus:** Airline ops batch domain (unique in portfolio); optimized batch pipelines.",
        "pipelines": ["PL_KAR_IRROPS_Bronze", "PL_KAR_IRROPS_Gold", "PL_KAR_IRROPS_Alerts"],
        "notebooks": ["/Karthik/Airline/NB_IRROPS_Aggregates", "NB_Delay_Alerts"],
        "gold": ["gold.fact_flight_delay", "gold.irrops_daily_summary"],
    },
    "projects/roja/roja-01-retailpulse-streaming.md": {
        "title": "# RetailPulse Real-Time Sales & Customer Streaming Analytics (Roja)",
        "refs": "06-Retail-Customer-Loyalty-Rewards-Data-Pipeline.md, 10-Retail-Customer-Analytics-Platform.md",
        "overview": "Real-time sales and customer 360 streaming for loyalty and personalization.",
        "diff": "**Roja focus:** Sales/customer 360 streaming vs Mugalin demand forecasting.",
        "pipelines": ["PL_ROJA_Stream_Health", "PL_ROJA_Gold_Customer_360"],
        "notebooks": ["/Roja/NB_Stream_Sales", "NB_Gold_Customer_360"],
        "gold": ["gold.customer_360_snapshot", "gold.sales_realtime_kpi"],
    },
    "projects/roja/roja-02-legacy-erp-pos-migration.md": {
        "title": "# Legacy Retail ERP & POS Migration to Azure Lakehouse (Roja)",
        "refs": "15-Retail-Migration-OnPrem-to-Azure.md",
        "overview": "ERP/POS migration with DataOps validation gates before Gold promotion.",
        "diff": "**Roja focus:** DataOps validation gates (Great Expectations) at each medallion hop.",
        "pipelines": ["PL_ROJA_MIG_Bronze", "PL_ROJA_MIG_Validate_Gold", "PL_ROJA_MIG_Cutover"],
        "notebooks": ["/Roja/Migration/NB_DQ_Gates", "NB_Gold_Promote"],
        "gold": ["gold.pos_sales", "gold.erp_inventory"],
    },
    "projects/roja/roja-03-retail-dataops-support.md": {
        "title": "# Retail DataOps Production Support & SLA Monitoring (Roja)",
        "refs": "09-Enterprise-Data-Governance-Observability-Platform.md",
        "overview": "DataOps SLA monitoring, Purview lineage, and governance-aligned support.",
        "diff": "**Roja focus:** SLA dashboards + Purview lineage for retail DataOps.",
        "pipelines": ["PL_ROJA_SLA_Monitor", "PL_ROJA_Lineage_Scan"],
        "notebooks": ["/Roja/DataOps/NB_SLA_Metrics"],
        "gold": ["support.sla_retail", "governance.lineage_audit"],
    },
    "projects/manasa/manasa-01-realtime-inventory-supply-chain.md": {
        "title": "# Real-Time Retail Inventory & Supply Chain Monitoring (Manasa)",
        "refs": "01-Supply-Chain-Analytics-Platform.md, 13-Retail-Development-Cloud-Data-Platform.md",
        "overview": "Unity Catalog lakehouse-first inventory monitoring with WMS/3PL feeds and GDPR PII model.",
        "diff": "**Manasa vs Pavani:** Unity Catalog + Power BI DirectLake (Pavani uses Synapse Serverless + vendor ASN).",
        "pipelines": ["PL_MAN_Inventory_Stream", "PL_MAN_WMS_Batch", "PL_MAN_Gold_Refresh"],
        "notebooks": ["/Manasa/NB_Stream_Inventory", "NB_Gold_Stockout", "NB_PII_Mask"],
        "gold": ["gold.inventory_position_uc", "gold.stockout_risk"],
    },
    "projects/manasa/manasa-02-legacy-pos-erp-lakehouse.md": {
        "title": "# Legacy POS & ERP Migration to Azure Lakehouse (Manasa)",
        "refs": "15-Retail-Migration-OnPrem-to-Azure.md, Customer_Data_Management_System.md",
        "overview": "Lakehouse-first migration with Fivetran ingestion + dbt Silver transforms.",
        "diff": "**Manasa vs Pavani-02:** Fivetran + dbt lakehouse pattern (not ADF-only phased POS).",
        "pipelines": ["PL_MAN_MIG_Orchestrate", "PL_MAN_MIG_Validation"],
        "notebooks": ["/Manasa/Migration/NB_Lakehouse_Gold"],
        "gold": ["gold.pos_unified", "gold.customer_master"],
    },
    "projects/manasa/manasa-03-inventory-pipeline-support.md": {
        "title": "# Retail Inventory Pipeline Support & Incident Management (Manasa)",
        "refs": "14-Retail-Support-Project.md",
        "overview": "Inventory pipeline L2 support with GDPR-aware incident handling.",
        "diff": "**Manasa vs Pavani-03:** Stricter GDPR retail PII runbooks for inventory data.",
        "pipelines": ["PL_MAN_Support_Health", "PL_MAN_Incident_Response"],
        "notebooks": ["/Manasa/Support/NB_Incident_Audit"],
        "gold": ["support.inventory_incidents"],
    },
}


def inject_reference(text: str, refs: str) -> str:
    if "**Reference:**" in text:
        return text
    lines = text.splitlines()
    header = f"> **Reference:** Adapted from [{REF_URL}]({REF_URL}) — `{refs}`"
    if lines:
        lines = [lines[0], "", header, ""] + lines[1:]
    text = "\n".join(lines)
    if "## Platform Concepts" not in text:
        marker = "\n---\n"
        pos = text.find(marker)
        if pos > 0:
            text = text[:pos] + PLATFORM + marker + text[pos + len(marker) :]
        else:
            text += PLATFORM
    return text


def create_project(path: Path, cfg: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pipes = "\n".join(f"| `{p}` | See ADF orchestration below |" for p in cfg["pipelines"])
    nbs = "\n".join(f"- `{n}`" for n in cfg["notebooks"])
    gold = "\n".join(f"- `{g}`" for g in cfg["gold"])
    body = f"""{cfg['title']}

> **Reference:** Adapted from [{REF_URL}]({REF_URL}) — `{cfg['refs']}`

## Project Overview and Business Context

{cfg['overview']}

{cfg['diff']}

{PLATFORM}

---

## Architecture Diagram

```mermaid
flowchart TB
    Sources[Source Systems] --> ADF[Azure Data Factory]
    ADF --> Bronze[(Bronze Delta)]
    Bronze --> ADB[Databricks]
    ADB --> Silver --> Gold
    Gold --> PBI[Power BI / Synapse]
    ADF --> KV[Key Vault]
    ADB --> UC[Unity Catalog]
```

---

## Medallion Architecture

### Bronze
- Source-faithful ingest with `_adf_loaded_at`, `batch_id` metadata
- Paths: `abfss://bronze@st{{org}}{{env}}.dfs.core.windows.net/{{domain}}/`

### Silver
- Cleansing, dedup, SCD where applicable; DQ quarantine tables per reference pre-bronze validation patterns

### Gold
{gold}

---

## ADF Orchestration

| Pipeline | Purpose |
|----------|---------|
{pipes}

**Linked services:** `LS_ADLS`, `LS_Databricks`, `LS_KeyVault`, `LS_SHIR` (on-prem if needed).

**Triggers:** Schedule + tumbling window for validation; environment global parameters `g_env`, `g_storage_account`.

---

## ADB Notebooks

```
{chr(10).join(cfg['notebooks'])}
```

**Cluster:** Job clusters for batch; autoscaling streaming cluster where applicable. **Delta:** `delta.autoOptimize.optimizeWrite` on Silver/Gold.

---

## Security & Monitoring

- MSI + Key Vault; private endpoints in prod
- ADF failure → Action Group; Log Analytics KQL for SLA and row-count drift (per reference monitoring sections)

---

## Implementation Phases

| Phase | Focus |
|-------|-------|
| 1 | Foundation (RG, ADLS, Key Vault, ADF, Databricks) |
| 2 | Bronze ingest |
| 3 | Silver/Gold transforms |
| 4 | Consumption & monitoring |
| 5 | Hardening & runbooks |
"""
    path.write_text(body, encoding="utf-8")


def main():
    for rel, refs in UPDATE_MAP.items():
        p = ROOT / rel
        if p.exists():
            p.write_text(inject_reference(p.read_text(encoding="utf-8"), refs), encoding="utf-8")
            print("updated", rel)

    for rel, cfg in CREATE_MAP.items():
        p = ROOT / rel
        create_project(p, cfg)
        print("created", rel)


if __name__ == "__main__":
    main()
