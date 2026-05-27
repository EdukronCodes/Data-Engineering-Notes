# Student 1 - Project 2
## On-Premise Retail Data Warehouse Migration to Azure Databricks, Fabric, ADLS Gen2, and Synapse (Migration Project)
### Stack
ADF, Azure Databricks, ADLS Gen2, Microsoft Fabric, Synapse Analytics, PySpark, Power BI

### Step 1: Requirement Gathering
Assessed legacy warehouse pain points, migration scope, cutover constraints, and compliance requirements. Identified KPIs to preserve during migration: sales, profit, retention, and inventory turnover. Cataloged source extracts, dependency graphs, and historical retention windows.
### Step 2: Architecture Design
Designed hybrid transition architecture with dual-run (legacy + Azure) and Medallion storage on ADLS/Delta. Defined migration waves by subject area and dependency. Planned serving through Fabric/Synapse with backward-compatible semantic models.
### Step 3: Environment Setup
Provisioned migration landing zones, separate non-prod/prod workspaces, and network/security baselines. Configured ADF integration runtimes for on-prem connectivity. Established RBAC, private endpoints, and key management.
### Step 4: Source System Integration
Connected on-prem SQL/Oracle exports, flat-file drops, and API feeds into ADF linked services. Standardized extraction patterns and schema contracts. Enabled encrypted transport and managed secret rotation.
### Step 5: Data Ingestion using Azure Data Factory
Implemented full historical backfill pipelines plus incremental CDC-style ingestion. Parameterized ingestion by table, batch window, and watermark. Scheduled daily/hourly jobs and event-based arrivals for staged files.
### Step 6: Raw Data Storage in Bronze Layer
Landed immutable raw snapshots in Bronze with source/date partitioning. Preserved historical versions for rollback and audit. Logged ingestion lineage with run-level metadata and source hash totals.
### Step 7: Data Transformation using Azure Databricks
Rewrote legacy ETL rules in PySpark with parity tests against on-prem outputs. Implemented cleansing, de-duplication, and standardization at scale. Used Delta Lake transactions for safe reruns and merge semantics.
### Step 8: Silver Layer Processing
Built conformed dimensions/facts in Silver with SCD handling and key harmonization. Added quality gates for null, referential, and distribution checks. Tuned partitioning strategy to support reconciliation and query performance.
### Step 9: Gold Layer Aggregation
Created migration-ready marts for executive and operational reporting with star schema modeling. Aligned business KPI definitions with legacy dashboards to avoid interpretation drift. Published certified Gold tables for report cutover.
### Step 10: Microsoft Fabric Integration
Loaded Gold datasets to Fabric Lakehouse/Warehouse and mapped to semantic models. Enabled centralized governance and model reuse. Validated report parity through side-by-side comparisons.
### Step 11: Machine Learning Forecasting
Migrated or re-trained forecasting models on curated Azure historical datasets. Rebuilt feature pipelines for promotions/seasonality effects. Measured model parity and improvement using RMSE/MAE.
### Step 12: Power BI Dashboard Development
Switched reports to Fabric/Azure-backed semantic models with minimal visual redesign. Validated KPI parity and drill-through behavior against legacy baseline. Applied incremental refresh and workspace governance.
### Step 13: CI/CD and Deployment
Automated ADF, Databricks, and model artifact deployment using Azure DevOps. Implemented environment-specific parameterization and approvals. Added rollback plans for each migration wave.
### Step 14: Monitoring and Logging
Centralized logs across ADF, Databricks, and serving layers; added migration health dashboards. Alerted on failed dependencies, SLA misses, and data variance thresholds. Captured cutover checkpoint metrics.
### Step 15: Security and Governance
Applied least-privilege access controls, masked PII, and enforced data access boundaries. Governed data products via Fabric/Unity Catalog controls. Maintained migration audit evidence and lineage.
### Step 16: Performance Optimization
Optimized Spark joins, partition pruning, and file compaction for large backfills. Tuned ADF batch concurrency and IR throughput for migration windows. Reduced query latency in serving layers with model optimization.
### Step 17: Production Support and Maintenance
Executed phased cutover, hypercare, and incident triage during stabilization. Ran reconciliation and defect burn-down cycles post-migration. Transitioned operations to steady-state support with runbooks.

