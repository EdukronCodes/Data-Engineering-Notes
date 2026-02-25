### Project 1 — Predictive sales forecasting and demand planning platform (Flow)

### Spoken English overview (3 short paragraphs)
Think of this project as building a “forecast factory” for the business. Instead of teams arguing over spreadsheets and different versions of the truth, we bring all the sales, inventory, promotions, and external signals into one place and use them to generate a consistent forecast every week (or every day), at the level planners actually need.

The platform does two big things. First, it builds clean and trusted data (bronze → silver → gold) so everyone is working from the same numbers. Second, it trains and runs forecasting models in a repeatable way—so you can see which model version produced which forecast, why it changed, and how it performed once actual sales come in.

The end result is a forecast that planners can use, explain, and improve. They get a baseline forecast, they can run scenarios like “what if we run a promo” or “what if supply is limited,” and they can override where it makes sense. And behind the scenes, the system monitors data quality and model drift so it keeps getting better over time.

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

  subgraph Ingest[Ingestion (multiple paths)]
    ADF[ADF / Synapse Pipelines\nCopy/CDC/API]
    SHIR[Self-hosted IR\n(if on-prem)]
    EH[Event Hubs / Kafka\n(optional streaming)]
    SFTP[SFTP/Files\n(optional)]
  end

  subgraph Lakehouse[Databricks Medallion Lakehouse]
    ADLS[(ADLS Gen2 / OneLake)]
    UC[Unity Catalog\n(governance)]
    DLT[DLT / Jobs\n(Auto Loader)]
    BR[Bronze Delta\nraw + audit]
    SL[Silver Delta\ncleaned + conformed]
    GL[Gold Delta\nmarts + features]
  end

  subgraph Compute
    DBX[Databricks compute\n(Spark/SQL)]
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

  Sources --> Ingest --> ADLS
  SHIR --> ADF
  EH --> ADLS
  SFTP --> ADLS
  ADF --> ADLS

  ADLS --> DLT --> BR --> SL --> GL
  UC --- BR
  UC --- SL
  UC --- GL

  SL --> DBX --> DQ --> GL
  GL --> FS --> AML --> REG --> SCORE --> DW
  SCORE --> MON
  DW --> PBI
  DW --> API
  API --> WB
```

### Databricks Medallion architecture (Bronze → Silver → Gold)
- **Bronze (raw)**: land all source extracts as Delta with run ids/watermarks and minimal transformation.
- **Silver (conformed)**: standardize keys, calendars, units, and apply DQ gates so ML uses trusted inputs.
- **Gold (features + marts)**: publish versioned feature tables and forecast marts that downstream scoring/BI can consume reliably.

### Detailed flow diagrams
```mermaid
flowchart TD
  subgraph Data[Data pipeline]
    S[Sources\n(POS/ERP/Inventory/Promo/External)] --> I[Ingest\nADF/Event Hubs]
    I --> B[Bronze\nRaw + metadata]
    B --> SV[Silver\nConformed + DQ]
    SV --> G[Gold\nMarts + Features]
  end

  subgraph ML[ML lifecycle]
    G --> FE[Feature store]
    FE --> TR[Train + backtest\n(AML/Databricks)]
    TR --> REG[Model registry]
    REG --> SC[Batch scoring]
    SC --> OUT[Forecast outputs\n(run-id/versioned)]
  end

  subgraph Use[Consumption]
    OUT --> DW[Serving store\n(DW/Delta)]
    DW --> PBI[Planner dashboards]
    DW --> API[Forecast API]
    API --> WB[Write-back/exports]
  end

  subgraph Feedback[Feedback loop]
    ACT[Actuals arrive] --> EVAL[Accuracy + bias evaluation]
    EVAL --> MON[Drift/performance monitoring]
    MON -->|thresholds| TR
  end

  DW --> ACT
```

```mermaid
sequenceDiagram
  participant Or as Orchestrator (ADF)
  participant Lake as Lakehouse (ADLS/Delta)
  participant ML as ML pipelines (Train/Score)
  participant Reg as Model registry
  participant Serve as Serving (DW/API/BI)

  Or->>Lake: Ingest sources to Bronze (run-id)
  Or->>Lake: Transform to Silver + DQ gates
  Or->>Lake: Build Gold marts + features
  Or->>ML: Trigger training (schedule/drift)
  ML->>Reg: Register model version + metadata
  Or->>ML: Trigger batch scoring for horizon
  ML->>Serve: Publish forecasts + scenario versions
  Serve-->>Or: KPIs/alerts on failures or drift
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
