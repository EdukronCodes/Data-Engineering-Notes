# Student 1 - Project 1
## Retail Sales Analytics and Forecasting Platform (Development Project)
### Stack
Azure Data Factory, Azure Databricks, Microsoft Fabric, PySpark, Python, ADLS Gen2, Power BI

### Step 1: Requirement Gathering
Collected reporting and forecasting requirements from retail business, merchandising, supply chain, and finance teams. Finalized KPIs: total sales, gross margin, basket size, retention rate, stock-out rate, and forecast accuracy. Defined source systems: POS, ERP, CRM, e-commerce APIs, flat files, and SQL databases, including SLA targets for daily batch and near real-time refreshes.

### Step 2: Architecture Design
Designed end-to-end Medallion architecture with Bronze (raw), Silver (validated/conformed), and Gold (business marts). Selected ADF for ingestion/orchestration, Databricks for transformations and ML feature prep, ADLS Gen2 + Delta for storage, Fabric Lakehouse/Warehouse for governed serving, and Power BI for executive/operational dashboards.

### Step 3: Environment Setup
Provisioned dev/qa/prod resource groups and configured ADF, Databricks, ADLS Gen2, Fabric workspace, and Power BI workspace. Set up networking, private endpoints (where required), RBAC, and managed identity-based access. Defined naming standards and environment tags for repeatable deployments.

### Step 4: Source System Integration
Created linked services and connection profiles for POS/ERP/CRM systems and e-commerce APIs. Integrated CSV/JSON/XML feeds from Blob/FTP with schema mapping and file pattern controls. Stored credentials in Key Vault and enforced secret-less runtime auth via managed identity.

### Step 5: Data Ingestion using Azure Data Factory
Built metadata-driven parameterized pipelines for full, incremental, and event-driven ingestion. Used Copy activity for structured loads and notebook execution for complex parsing or API normalization. Configured schedule triggers (daily/hourly) and event triggers for file arrivals.

### Step 6: Raw Data Storage in Bronze Layer
Stored source-native payloads in Bronze with source/date/region partitioning and run metadata (`run_id`, `ingestion_ts`, `source_system`). Enabled lineage and replay by preserving immutable raw snapshots. Added audit trail tables for file counts, row counts, and load status.

### Step 7: Data Transformation using Azure Databricks
Implemented PySpark transformations for null handling, deduplication, type casting, standardization, and outlier treatment. Applied retail business rules for net sales, returns, discount impact, and inventory valuation. Used Delta Lake for ACID writes, schema evolution control, and idempotent MERGE patterns.

### Step 8: Silver Layer Processing
Created conformed Silver datasets for customers, products, stores, orders, payments, and inventory. Applied SCD logic for dimensions and standardized surrogate/business keys for downstream joins. Optimized query performance with partitioning, z-ordering strategy, and compact file sizing.

### Step 9: Gold Layer Aggregation
Built Gold marts for daily sales, regional/store performance, product hierarchy analytics, retention cohorts, and inventory health. Implemented star schema with reusable dimensions and governed measures. Published certified KPI tables for Power BI and Fabric semantic models.

### Step 10: Microsoft Fabric Integration
Loaded curated Gold outputs into Fabric Lakehouse/Warehouse and configured Fabric pipelines for downstream serving. Created semantic model layers for business-friendly measure definitions. Enabled governed data sharing and centralized catalog visibility.

### Step 11: Machine Learning Forecasting
Developed forecasting pipelines (PySpark/Python) for demand prediction and replenishment planning. Engineered seasonality, promotions, and holiday features using historical sales and inventory events. Validated models using RMSE/MAE/MAPE and operationalized best model outputs to Gold forecast tables.

### Step 12: Power BI Dashboard Development
Connected Power BI to Fabric/Gold datasets and built dashboards for sales trend, margin, store ranking, customer behavior, inventory risk, and forecast vs actual. Implemented DAX KPIs and drill-through pages for region/store/product analysis. Configured incremental refresh and role-based report access.

### Step 13: CI/CD and Deployment
Integrated Git-based source control for ADF and Databricks artifacts. Built Azure DevOps release pipelines for automated deploy across dev/qa/prod with environment parameters. Added pre-deploy validation and post-deploy smoke checks.

### Step 14: Monitoring and Logging
Configured Azure Monitor, Log Analytics, Databricks job telemetry, and custom ops tables for pipeline observability. Enabled alerting on failures, SLA delay, and anomaly thresholds. Published operational dashboards for engineering support teams.

### Step 15: Security and Governance
Implemented Key Vault-backed secrets, RBAC, managed identities, and least-privilege policies. Applied masking/tokenization for sensitive customer attributes and enforced table-level permissions. Used Fabric governance and Unity Catalog controls for lineage and access governance.

### Step 16: Performance Optimization
Optimized Spark workloads with partition pruning, broadcast joins, caching, AQE, and skew handling. Reduced small-file overhead using OPTIMIZE/VACUUM and compaction jobs. Tuned ADF concurrency, integration runtime scaling, and trigger windows to reduce end-to-end latency.

### Step 17: Production Support and Maintenance
Established L2/L3 support playbooks for failed runs, replay requests, and data correction flows. Performed RCA for recurring issues and implemented preventive controls. Managed monthly enhancement releases and ensured freshness/SLA adherence for business reporting.

