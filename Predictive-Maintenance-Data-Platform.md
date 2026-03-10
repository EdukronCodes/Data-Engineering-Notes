## Azure-Based Predictive Maintenance Data Platform for Heavy Equipment Fleet

### Goal
Build a scalable Azure data platform that ingests fleet telemetry + maintenance/operations data and produces curated (Gold) datasets for predictive maintenance analytics to reduce downtime and improve maintenance planning.

### Primary Data Sources (5)
- **Real-time telemetry**: Azure IoT Hub / Event Hubs (engine hours, temperatures, pressures, fault codes)
- **OEM / Telematics API**: REST APIs (GPS, utilization, diagnostic snapshots)
- **Maintenance system (CMMS/EAM)**: SQL source (work orders, parts replaced, failure codes, service history)
- **ERP**: SAP/Oracle via database connector or API (asset master, cost centers, parts procurement)
- **File drops**: ADLS Gen2 landing (operator inspection checklists, CSV/Excel from sites/vendors)

### Orchestration (Azure Data Factory)
- **Triggering**
  - Event-based trigger for IoT/Event Hub micro-batches
  - Scheduled triggers for CMMS/ERP incremental loads
  - Storage event trigger for file drops
- **Pipeline pattern**
  - Metadata-driven ingestion (source configs stored in a control table)
  - Parameterized datasets, linked services, and reusable pipeline templates
  - Dependency chaining: Ingest → Validate → Transform → Publish Gold
- **Security**
  - Secrets stored in **Azure Key Vault** and referenced by ADF linked services
  - Managed Identity for ADF/Databricks access to ADLS Gen2

### Processing & Storage (Medallion Architecture on ADLS Gen2 + Delta Lake)
- **Bronze (Raw)**
  - Land data as-is (JSON/Avro/CSV/Parquet) in ADLS Gen2
  - Persist as **Delta Bronze** with ingestion timestamps and source lineage
- **Silver (Clean/Conformed)**
  - Databricks (PySpark) cleansing: schema normalization, dedup, null handling, unit standardization
  - Data quality checks (range rules, sensor sanity checks, referential integrity to asset master)
  - Conformed entities: `equipment`, `sensor_readings`, `fault_events`, `work_orders`, `parts_usage`
- **Gold (Business/Analytics)**
  - Feature-ready datasets for predictive maintenance:
    - rolling aggregations (1h/24h/7d), utilization rates, anomaly flags
    - time-to-failure labels from work orders + fault events
  - Publish curated Delta tables and Synapse-friendly views

### Consumption Layer
- **Azure Synapse Analytics**
  - Serverless / dedicated SQL views over Gold Delta tables (semantic access + performance)
- **Power BI**
  - Dashboards: fleet health KPIs, failure trends, utilization vs downtime, maintenance backlog
  - Drill-through by asset/site/model and leading indicators (fault frequency, thermal anomalies)

### Project Flow (End-to-End)
1. **Ingest (ADF)** from IoT Hub, APIs, CMMS DB, ERP, and ADLS file drops into **Bronze**.
2. **Persist raw** as **Bronze Delta** with schema evolution + source/audit columns.
3. **Transform (Databricks)** to **Silver**: cleanse, standardize, validate quality rules.
4. **Curate (Databricks)** to **Gold**: aggregates + predictive features + reporting marts.
5. **Serve** via **Synapse SQL** and **Power BI**; schedule refresh and incremental updates.
6. **Monitor** pipeline SLAs and data quality; alert on failures and anomaly spikes.

### Key Engineering Highlights
- **Incremental processing** using watermark columns (event_time, last_updated) + merge/upserts into Delta
- **ACID + versioning** with Delta Lake (time travel, rollback, auditability)
- **Performance**: partitioning by `event_date`/`equipment_id`, optimized file sizing, auto-compaction
- **Observability**: ADF run logs + Databricks job metrics + Log Analytics dashboards and alerts

### Skills / Technologies
Azure Data Factory (ADF), Azure Databricks (PySpark), ADLS Gen2, Delta Lake, Azure Synapse Analytics, SQL, Python, Azure Key Vault, Power BI, Azure DevOps CI/CD, Azure Monitor/Log Analytics

### Roles & Responsibilities
- Designed ADF orchestration for real-time + batch ingestion across 5 enterprise/IoT sources
- Implemented Medallion (Bronze/Silver/Gold) on ADLS Gen2 using Delta Lake
- Developed PySpark pipelines for high-volume telemetry cleansing, validation, and feature creation
- Built incremental, idempotent processing with Delta MERGE and watermarking
- Published Gold datasets to Synapse + Power BI with governance-ready lineage and audit columns
- Secured secrets in Key Vault and automated deployments with Azure DevOps CI/CD
