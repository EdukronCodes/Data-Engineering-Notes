### Project 1 — Predictive sales forecasting and demand planning platform (Flow)

### Goal
Build an end-to-end platform that turns multi-source retail/CPG signals into **reliable forecasts** and **actionable demand plans**, with governed data, repeatable model training, and monitored production scoring.

### Objectives
- Deliver accurate, bias-controlled forecasts at agreed granularity (e.g., SKU-store-week) and horizon (e.g., 1–12 weeks).
- Reduce planner effort via exception-based workflows and scenario comparisons (baseline vs overrides).
- Provide traceability from forecast outputs back to input data versions, feature sets, and model versions.
- Enable scalable, automated retraining and scoring with monitoring and alerting.
- Support operational integration (exports/APIs) and controlled write-back to planning systems.

### Primary users and outputs
- **Demand planners**: baseline + adjusted forecasts, scenario comparisons, exceptions
- **Supply chain / replenishment**: recommended order quantities, safety stock signals
- **Business stakeholders**: KPI dashboards (MAPE/WAPE, bias, service level)
- **Downstream systems**: write-back to planning tools (e.g., SAP IBP/APS) via API/files

### Reference architecture (high-level)
```mermaid
flowchart LR
  subgraph Sources
    POS[POS / sales transactions]
    ERP[ERP / orders / shipments]
    INV[Inventory / stock]
    PROMO[Promotions / pricing]
    CAL[Calendar / holidays]
    EXT[Weather / events / macro]
    MDM[Product & store master data]
  end

  subgraph Ingest
    ADF[Azure Data Factory / Synapse Pipelines]
    EH[Event Hubs (optional streaming)]
  end

  subgraph Lakehouse
    ADLS[(ADLS Gen2)]
    BR[Bronze: raw]
    SL[Silver: cleaned/conformed]
    GL[Gold: marts/features]
  end

  subgraph Compute
    DBX[Databricks / Spark]
    DQ[Data Quality checks]
    FS[Feature store (Delta / AML Feature Store)]
  end

  subgraph ML
    AML[Azure ML: train/track/registry]
    REG[Model registry]
    SCORE[Batch scoring jobs]
    MON[Model monitoring: drift & performance]
  end

  subgraph Serve
    DW[(Synapse Dedicated SQL / Fabric DW / SQL DB)]
    API[Forecast API (Functions/App Service)]
    PBI[Power BI / Fabric reports]
    WB[Write-back to planning system]
  end

  Sources --> Ingest
  POS --> ADF
  ERP --> ADF
  INV --> ADF
  PROMO --> ADF
  CAL --> ADF
  EXT --> ADF
  MDM --> ADF
  EH --> ADLS
  ADF --> ADLS
  ADLS --> BR --> SL --> GL
  SL --> DBX --> DQ --> GL
  GL --> FS --> AML --> REG --> SCORE --> DW
  SCORE --> MON
  DW --> PBI
  DW --> API
  API --> WB
```

### End-to-end data + ML flow (detailed)
- **0) Foundation**
  - Resource group(s), naming/tags, networking (private endpoints where required)
  - Secrets in **Key Vault**, identities via **Entra ID (AAD)**, RBAC + ACLs on ADLS
  - Data governance catalog (e.g., **Purview**) and lineage collection

- **1) Source onboarding**
  - Define entities: SKU/store/day, hierarchy levels, granularity (daily/weekly)
  - Contract for each source: refresh cadence, schema, keys, SLAs, ownership

- **2) Ingestion (batch and/or streaming)**
  - **Batch**: ADF copies from SQL/ERP/SFTP/APIs into ADLS **Bronze**
  - **Streaming (optional)**: POS events → Event Hubs → landing in Bronze
  - Capture ingestion metadata: file date, source watermark, load id, row counts

- **3) Bronze → Silver (standardize & clean)**
  - De-duplication, type casting, timezone alignment
  - Conform keys with MDM (SKU/store mappings), handle slowly changing dimensions
  - Missing value strategy (e.g., stock-outs vs true zero-sales)
  - Write standardized Delta tables to **Silver**

- **4) Silver → Gold (business logic & feature engineering)**
  - Build gold marts:
    - `sales_fact` (aligned by calendar, channel, region)
    - `inventory_fact` (on-hand, on-order, stock-out flags)
    - `promo_fact` (promo type, depth, duration)
    - `dim_product`, `dim_store`, `dim_calendar`
  - Features:
    - Lag/rolling windows, seasonality indicators, price elasticity signals
    - Promo uplift features, holiday/event flags, weather aggregates
  - Persist curated features to **Gold** / Feature Store

- **5) Model training & registry**
  - Training pipeline (scheduled or triggered on data freshness):
    - Data extract from Gold/Feature Store
    - Train candidates (baseline + advanced) and hyperparameter search
    - Evaluate by segment (SKU class/store cluster) with business-friendly metrics
    - Register best model + metadata (feature set version, training window, code hash)
  - Governance: approval workflow for production promotion (Dev → Test → Prod)

- **6) Forecast generation (batch scoring)**
  - Generate forecasts by horizon (e.g., 1–12 weeks) and level (SKU-store, rollups)
  - Apply post-processing:
    - Reconciliation across hierarchies (top-down/bottom-up)
    - Bias correction, constraints (non-negative, capacity caps), new item logic
  - Store outputs in a serving store (DW / Delta Gold) with run id + timestamps

- **7) Demand planning & scenario workflow**
  - Baseline forecast + planner adjustments stored as separate versions
  - Scenario runs (promo calendar changes, price changes, new store openings)
  - Write-back:
    - API-based updates to planning tool
    - Or scheduled exports (CSV/Parquet) to SFTP/SharePoint/Blob

- **8) Serving & consumption**
  - **Power BI**: planner dashboards, exception lists, forecast accuracy, bias
  - **API**: programmatic access for downstream replenishment systems
  - Role-based access: planners see their business unit/region only

- **9) Monitoring, quality, and continuous improvement**
  - Data monitoring: freshness, volume anomalies, schema drift, null spikes
  - Model monitoring: drift, performance backtests when actuals arrive
  - Alerting: Teams/Email via Azure Monitor action groups
  - Retraining triggers: schedule (weekly) + drift/performance thresholds

### Orchestration pattern
- **ADF** orchestrates end-to-end DAG:
  - Ingest → Bronze validation → Silver transforms → Gold features → AML train/score → publish marts
- Use **watermarks** (per source) and **idempotent loads** (run id partitions).

### Environments and CI/CD
- Environments: **Dev / Test / Prod** with separate workspaces and storage accounts (or strict paths + RBAC).
- Git-based deployment:
  - Infra: Bicep/Terraform
  - ADF: publish branch + automated release
  - ML: pipelines as code + model registry promotion gates

### Non-functional requirements (quick checklist)
- **Security**: private networking, managed identities, Key Vault references, least privilege
- **Reliability**: retries, dead-letter for streaming, reprocessing by run id
- **Cost**: autoscaling clusters, partitioning strategy, lifecycle policies on ADLS
- **Performance**: Z-order / clustering in Delta, incremental processing

### Notes (design choices + interview talking points)
- **Forecast granularity trade-off**: SKU-store often improves actionability but increases sparsity; mitigate with clustering, hierarchy rollups, or models per segment.
- **“Zero sales” vs stock-outs**: treat stock-out periods as censored demand (not true zero). Add explicit stock-out flags and imputation strategies.
- **Promotions and price**: promotions can dominate demand; keep a clean promo calendar, and separate baseline vs uplift modeling if needed.
- **Cold start / new items**: use attribute-based models (category/brand/price tier) and analog matching; fall back to hierarchy-level forecasts.
- **Hierarchical reconciliation**: ensure totals at category/region roll up correctly; pick a reconciliation method (bottom-up, top-down, MinT).
- **Evaluation metrics**: WAPE/MAE often aligns better than MAPE for intermittent demand; track bias and service-level impacts, not only error.
- **Backtesting**: implement rolling-origin backtests (time-series CV) and track per-segment performance to avoid “average hides failures.”
- **Feature/label leakage**: strictly time-align features to the forecast creation date; enforce cutoff timestamps in feature generation.
- **Versioning**: store run id, training window, feature set version, and model registry version alongside every forecast output for auditability.
- **Planner overrides**: treat overrides as a first-class versioned artifact; measure override rate and whether overrides improve accuracy.

### Deliverables (what you can show in a portfolio)
- Architecture + flow diagram
- Data model (bronze/silver/gold) + feature definitions
- ADF pipeline screenshots (or exported JSON) + run history
- AML experiment tracking + model registry + batch scoring outputs
- Monitoring dashboards + alert rules
