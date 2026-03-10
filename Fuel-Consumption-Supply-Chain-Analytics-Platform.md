## Azure Data Platform for Fuel Consumption and Supply Chain Optimization

### Goal
Deliver a unified Azure analytics platform that consolidates fuel transactions, logistics movements, and supply chain operations into curated (Gold) datasets to drive fuel efficiency insights, route optimization, and operational reporting.

### Primary Data Sources (5)
- **ERP**: SAP/Oracle (purchase orders, invoices, vendor master, cost allocations)
- **Transportation Management System (TMS)**: REST APIs (loads, routes, planned vs actual, carrier performance)
- **Fuel card / transaction provider**: API or database extract (fuel quantity, cost, location, timestamp)
- **Telematics / GPS / ELD**: streaming or API (mileage, idle time, speed bands, geofences)
- **Warehouse / operations files**: SFTP/ADLS drops (WMS extracts, inventory snapshots, exceptions logs)

### Orchestration (Azure Data Factory)
- **Triggers**
  - Scheduled incremental loads for ERP, TMS, and fuel transactions
  - Event triggers for file drops (warehouse extracts)
  - Optional near-real-time micro-batching for telematics
- **Pipeline pattern**
  - Standard ingestion framework with source metadata + reusable copy activities
  - Built-in retry policies, failure handling, and reprocessing support (by date/partition)
- **Security**
  - Key Vault-backed linked services, Managed Identity auth to ADLS Gen2 and Databricks

### Processing & Storage (Medallion Architecture on ADLS Gen2 + Delta Lake)
- **Bronze (Raw)**
  - Store extracted API payloads/files as immutable raw + ingest audit fields
  - Convert to **Bronze Delta** for scalable downstream processing
- **Silver (Clean/Standardized)**
  - Databricks (PySpark) standardization:
    - unify timestamps/timezones, currency normalization, unit conversions
    - deduplicate transactions, reconcile reference data (vehicles, depots, vendors)
  - Conformed datasets: `fuel_transactions`, `vehicle_telematics`, `shipments`, `routes`, `warehouse_events`
- **Gold (Analytics-Ready)**
  - Curated marts:
    - fuel efficiency KPIs (MPG/L-per-100km), idle impact, cost per mile/km
    - route performance (planned vs actual distance/time), delay root causes
    - supply chain KPIs (OTIF, cycle time, lane performance, vendor lead times)
  - Aggregations and dimensional models for reporting and ad-hoc analytics

### Consumption Layer
- **Azure Synapse Analytics**
  - SQL views / serving layer over Gold Delta for enterprise reporting
- **Power BI**
  - Executive and operational dashboards:
    - fuel cost trends, efficiency by fleet/region, idle heatmaps
    - logistics performance, lane benchmarking, exception monitoring

### Project Flow (End-to-End)
1. **Ingest (ADF)** ERP + TMS + fuel provider + telematics + warehouse files into **Bronze** on ADLS Gen2.
2. **Persist raw** and register **Bronze Delta** tables with audit/lineage columns.
3. **Transform (Databricks)** to **Silver**: cleanse, standardize, conform entities across systems.
4. **Curate (Databricks)** to **Gold**: KPIs, dimensional marts, and performance aggregates.
5. **Serve** via **Synapse SQL** and **Power BI**; incremental refresh for large models.
6. **Monitor & alert** using Azure Monitor + Log Analytics for pipeline and data-quality SLAs.

### Key Engineering Highlights
- **Incremental ingestion** using watermarks and CDC-style patterns where available
- **Delta Lake** merges for late-arriving transactions and corrections (idempotent replays)
- **Performance tuning** with partitioning (date/region), Z-Ordering (vehicle_id, route_id), caching hot tables
- **Operational monitoring** with alerts on pipeline failures, latency thresholds, and volume anomalies

### Skills / Technologies
Azure Data Factory, Azure Databricks (PySpark), ADLS Gen2, Delta Lake, Azure Synapse Analytics, SQL, Python, REST API integration, Power BI, Azure Monitor/Log Analytics, Azure Key Vault, Azure DevOps CI/CD

### Roles & Responsibilities
- Built ADF orchestration to ingest 5 heterogeneous sources (ERP, TMS, fuel, telematics, warehouse files)
- Implemented Medallion architecture with Delta Lake for reliable, scalable transformations
- Developed PySpark pipelines for data cleansing, conformance, and KPI dataset creation
- Created Synapse SQL serving views and Power BI models for fuel and logistics analytics
- Implemented monitoring/alerting and automated deployments using Azure DevOps CI/CD
