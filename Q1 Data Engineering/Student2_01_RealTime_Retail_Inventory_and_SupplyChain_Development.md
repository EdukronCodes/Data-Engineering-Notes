# Student 2 - Project 1
## Real-Time Retail Inventory and Supply Chain Platform (Development Project)
### Stack
Azure Event Hubs, Azure Stream Analytics, Azure Data Factory, Azure Databricks, ADLS Gen2, Delta Lake, Microsoft Fabric, Power BI, Python, PySpark

### Step 1: Requirement Gathering
Gathered requirements from inventory planning, warehouse operations, procurement, and store operations teams. Finalized KPIs including stock availability, replenishment lead time, vendor fill rate, shrinkage, and stock-out frequency. Defined latency goals for near real-time inventory visibility and daily executive reporting.

### Step 2: Architecture Design
Designed a hybrid streaming and batch architecture with Bronze, Silver, and Gold layers. Chose Event Hubs and Stream Analytics for event capture, ADF for batch orchestration, Databricks for enrichment and conformance, and Fabric/Power BI for analytics serving. Included resilient design for delayed events, replay, and backfill.

### Step 3: Environment Setup
Provisioned dev, qa, and prod resources with standardized naming and tagging. Configured Databricks workspaces, Event Hubs namespaces, storage containers, and Fabric capacities. Applied RBAC, managed identities, and private connectivity where required by enterprise policy.

### Step 4: Source System Integration
Integrated POS inventory movement feeds, WMS dispatch updates, supplier ASN feeds, and ERP purchase order data. Configured API and file-based connectors for carrier updates and procurement status events. Standardized source metadata for consistent ingestion, lineage, and troubleshooting.

### Step 5: Streaming and Batch Ingestion
Built streaming ingestion for inventory movement events and batch ingestion for master/reference data. Parameterized ADF pipelines for incremental loads and schema drift handling. Added trigger coordination to align near real-time events with periodic dimension refreshes.

### Step 6: Bronze Layer Landing
Stored raw event payloads and source files in Bronze with partitioning by source and ingestion window. Preserved immutable raw history to support replay and audit requirements. Captured ingestion audit metrics such as message counts, lag, and malformed record rates.

### Step 7: Data Transformation
Implemented PySpark logic for deduplication, timestamp normalization, unit-of-measure conversion, and source harmonization. Applied business rules for available-to-sell, safety stock, and reorder thresholds. Used Delta MERGE and watermark logic to process late-arriving inventory events correctly.

### Step 8: Silver Layer Conformance
Created conformed Silver entities for products, locations, inventory snapshots, orders, shipments, and supplier events. Applied SCD patterns for product and supplier attributes to preserve history. Enforced quality checks on key integrity and event sequence consistency.

### Step 9: Gold Layer Analytics Marts
Built Gold marts for inventory health, replenishment performance, supplier reliability, and distribution center throughput. Modeled star schemas for regional and store-level operational analytics. Published certified KPI tables for planners and supply chain analysts.

### Step 10: Real-Time KPI Serving
Delivered real-time KPI feeds to operational dashboards for stock alerts and replenishment status. Created low-latency aggregate tables for hourly decision-making. Added freshness indicators and data delay flags for operational trust.

### Step 11: Forecast and Optimization Inputs
Prepared feature-ready datasets for demand forecasting and replenishment recommendation models. Generated lag and seasonality features combining inventory movement, promotions, and supplier performance. Delivered model input datasets into governed serving zones for data science consumption.

### Step 12: Dashboard and Reporting
Built Power BI dashboards for stock-out risk, slow-moving inventory, lead time variance, and transfer effectiveness. Added drill-through views by region, store, category, and supplier. Implemented row-level access and certified semantic measures for business users.

### Step 13: CI/CD and Release Management
Version-controlled ADF, Databricks notebooks, and SQL artifacts in Git. Set up automated deployments across environments with parameterized configurations and approval gates. Added smoke validation for ingestion, transformation, and dashboard refresh workflows.

### Step 14: Monitoring and Alerting
Configured Azure Monitor, Log Analytics, and Databricks job alerts for SLA, failure, and latency breaches. Implemented operational telemetry dashboards with pipeline and streaming lag visibility. Routed critical incidents to support channels with runbook links.

### Step 15: Security and Governance
Used Key Vault for secrets, managed identities for service authentication, and least-privilege RBAC for access control. Applied masking policies for sensitive supplier and logistics attributes where necessary. Maintained lineage and data catalog entries for enterprise governance and auditability.

### Step 16: Performance Optimization
Optimized streaming checkpointing, micro-batch interval settings, and partitioning strategies for lower latency. Tuned Spark joins, file compaction, and Delta optimization routines for stable runtime. Reduced cost by balancing cluster autoscaling with throughput patterns.

### Step 17: Production Support and Maintenance
Established support playbooks for event lag spikes, failed loads, and inconsistent inventory balances. Performed root cause analysis for recurring supplier feed issues and implemented preventive validations. Scheduled periodic enhancements for new KPIs, suppliers, and warehouse processes.

