# Supply Chain Analytics Platform

## 1. Project Overview & Business Problem

The organization manages complex supply chains spanning multiple suppliers, warehouses, and distribution centers, generating massive volumes of data across procurement, logistics, and inventory systems. Currently, decision-makers rely on fragmented reports from disparate systems, resulting in delayed visibility into supply chain performance and inability to respond quickly to disruptions.
Manual ETL processes cannot keep pace with the velocity of supply chain data, creating bottlenecks in data availability and forcing the business to make decisions based on stale information that may be days or weeks old.

- **Business Context & Challenge**: The enterprise operates across multiple geographies with hundreds of suppliers and thousands of SKUs, generating data from ERP systems, logistics platforms, and IoT sensors.
  Real-time supply chain visibility is critical to optimize inventory levels, reduce lead times, and minimize operational costs in a highly competitive market.

- **Strategic Objectives**: The platform aims to enable real-time analytics on supplier performance, shipment tracking, and inventory forecasting to improve decision-making velocity.
  Automation of ETL pipelines will reduce manual effort, eliminate errors, and enable teams to focus on strategic initiatives rather than data preparation.

- **Pain Points & Business Drivers**: Current pain points include inconsistent data across systems, late-arriving insights that miss critical decision windows, and inability to correlate data from multiple sources for root cause analysis.
  A unified data platform will enable unified metric definitions, automated reconciliation, and cross-functional visibility into supply chain KPIs.

- **Cloud Solution Value Proposition**: Azure provides scalable infrastructure to handle IoT sensor data, API integrations with logistics partners, and advanced analytics capabilities without capital expenditure on on-premises hardware.
  Services like Azure Synapse enable complex SQL analytics while Azure Databricks supports machine learning for demand forecasting and anomaly detection.

- **Expected Business Impact**: The platform will reduce order-to-cash cycle time by 30%, improve inventory turnover, and enable proactive identification of supplier risks before they impact operations.
  Supply chain teams will gain visibility to optimize routes, consolidate shipments, and reduce transportation costs by 15-20%.

## 2. Requirement Gathering & Analysis

Supply chain data originates from multiple sources including enterprise ERP systems (SAP, Oracle), logistics management systems (JDA, Kinaxis), supplier portals, and IoT sensors deployed across warehouses and distribution centers. The organization requires real-time ingestion of transactional data, master data, and event-driven signals to power dashboard and alerting systems.
Integration complexity spans REST APIs with rate limiting, file-based SFTP transfers, database replication, and streaming event data from Kafka topics managed by logistics partners.

- **Source System Inventory**: The platform must integrate with ERP purchase orders, receipts, and invoices; logistics systems for shipment tracking and delivery confirmations; supplier EDI data; and warehouse management systems for inventory position.
  Data arrives via APIs with pagination, SFTP file drops on scheduled intervals, real-time Kafka streams, and monthly batch database snapshots, each requiring tailored connectivity strategies.

- **Data Loading Frequencies & SLAs**: Purchase order and inventory data require hourly incremental updates with 2-hour SLA for end-to-end pipeline completion to support intraday analytics.
  Shipment tracking data must load in near real-time with maximum 5-minute latency for dashboard feeds, while master data (suppliers, products, locations) can tolerate daily batch loads.

- **Data Volume & Growth Projections**: The platform ingests 500GB daily from transactional sources, growing 25% annually as new suppliers and logistics partners join the network.
  IoT sensor data from 1,000 active devices generates 2TB monthly, with plans to expand to 5,000 devices within 18 months, requiring autoscaling architecture.

- **Data Quality Standards**: Mandatory DQ rules include completeness checks on order IDs and customer codes, accuracy validation of quantities and prices against source systems, uniqueness enforcement on shipment IDs, and timeliness checks ensuring data arrival within defined windows.
  Late or duplicate records must be quarantined in exception tables for investigation and manual correction before promotion to gold layer.

- **Business Transformation & KPIs**: SME-defined transformations include calculating lead times from PO creation to goods receipt, computing supplier on-time delivery rates, and aggregating inventory metrics by product category and location.
  Critical KPIs include Days Inventory Outstanding (DIO), supplier quality scores, transportation cost per unit, and forecast accuracy metrics for demand planning.

- **Security & Compliance Requirements**: The platform must enforce HIPAA compliance for healthcare supplier data, implement data residency rules for suppliers in specific countries, and maintain audit trails of all data access for compliance reporting.
  Role-based access controls must restrict procurement data to procurement teams, shipping data to logistics teams, and financial data to finance, with no cross-functional visibility.

- **Tool Dependencies & Integration Points**: The solution leverages Power BI for executive dashboards, Synapse SQL for ad-hoc supplier performance queries, Databricks for demand forecasting models, and Azure DevOps for pipeline versioning and deployment.
  Analytics must integrate with Salesforce CRM for customer context and with SAP Analytics Cloud for financial reconciliation.

## 3. Azure Architecture Setup

The architecture provisions ADLS Gen2 with separate containers for each data layer (landing, pre-bronze, bronze, silver, gold), implementing hierarchical namespace for efficient data organization and lifecycle policies to archive cold data to blob storage after 90 days. Azure Data Factory orchestrates the entire ingestion pipeline with 50+ linked services for disparate sources, storing connection strings in Key Vault and utilizing managed identities to eliminate credential management.
Azure Databricks clusters scale from 4 to 32 nodes based on workload, with Spark jobs processing 50GB/hour throughput during peak ingestion windows, while Synapse Analytics serverless SQL pools enable cost-effective query execution on gold layer tables without dedicated capacity reservation.

- **ADLS Gen2 Configuration**: Provision hierarchical namespace with containers for staging, supply-chain-bronze, supply-chain-silver, and supply-chain-gold, implementing lifecycle management policies to transition data to Archive tier after 180 days.
  Enable Azure AD authentication for all data access and configure private endpoints to isolate storage from public internet while maintaining connectivity through VNETs.

- **Azure Data Factory Deployment**: Deploy ADF with 12 linked services (ERP database, Salesforce API, SFTP server, Kafka, SAP Analytics), configure metadata-driven pipelines with 40+ activities orchestrating ingestion and control flows.
  Integrate with Key Vault for secure credential management and implement self-hosted integration runtime on-premises for secure SAP connectivity.

- **Databricks Workspace Setup**: Establish two Databricks workspaces (dev and prod) with autoscaling job clusters consuming up to 64 vCores during nightly transformations and interactive clusters for data exploration limited to business hours.
  Configure Databricks SQL endpoint for analysts to run interactive queries and configure delta sharing for secure data access by external supply chain partners.

- **Synapse Analytics Workspace**: Create Synapse workspace with serverless SQL pool for exploration and dedicated SQL pool for star schema analytics, configured to autoscale between 100 and 400 DWUs based on query volume.
  Configure Synapse Link integration with operational SAP database to enable real-time operational analytics without burdening transactional system.

- **Key Vault Integration**: Store 25+ secrets including database connection strings, API keys, SFTP credentials, and PAT tokens, implementing RBAC to grant ADF service principal read access only to required secrets.
  Enable Key Vault diagnostic logging to track all secret access attempts and enable alerts for suspicious activity.

- **Observability Configuration**: Deploy Log Analytics workspace for centralized logging from ADF, Databricks, and Synapse, configure diagnostic settings to stream activity logs and track pipeline failures, job errors, and query performance.
  Create custom metrics for ingestion throughput, data quality rule violations, and end-to-end SLA compliance.

- **Private Endpoint Setup**: Create private endpoints for ADLS storage account, SQL server, and Key Vault, restricting connectivity to VNETs and disabling public internet access for all critical services.
  Configure private DNS zones to ensure DNS resolution works correctly within the VNETs.

- **Network Segmentation**: Implement VNETs with separate subnets for Databricks workers, Synapse compute, and integration runtimes, configuring NSGs to restrict traffic between tiers and allow outbound access only to approved sources.
  Implement Azure Firewall for centralized outbound filtering and logging of all egress traffic.

- **Encryption Configuration**: Enable encryption-at-rest using customer-managed keys in Key Vault for ADLS, Synapse databases, and Databricks workspace storage, with key rotation every 90 days.
  Enforce HTTPS-only access to storage and SQL databases, disabling HTTP connections to prevent data interception.

- **Purview Registration**: Register ADLS, Synapse, and Databricks with Azure Purview for lineage tracking, scan ADLS for metadata cataloging, and establish governance policies for data classification and access rights.
  Document relationships between source systems, transformation logic, and analytical outputs for audit and compliance purposes.

## 4. ADLS Folder Structure (Medallion Architecture)

The storage account implements a medallion architecture with six distinct layers, each serving specific purposes in the data pipeline from raw ingestion through refined analytics. Partitioning strategies align with business context (by supplier ID for procurement data, by shipment date for logistics) to enable efficient incremental processing and pruning of historical data.

- **Landing Layer**: Raw files arrive temporarily in `/landing/` organized by source system (`/landing/erp-po/`, `/landing/sftp-shipments/`, `/landing/api-suppliers/`), with no validation or transformation applied.
  Files remain in landing for 24 hours before automated archival to cold storage, ensuring quick troubleshooting of ingestion issues while managing storage costs.

- **Pre-Bronze Staging**: Schema-validated and quality-checked files are promoted to `/pre-bronze/` after passing format, size, and header validation rules specific to each source.
  This layer acts as a holding area for files ready for historical ingestion, with audit trails tracking validation results and any remediation actions.

- **Bronze Layer**: Immutable raw data stored in Parquet format partitioned by `load_date` and `source_system` under `/bronze/suppliers/`, `/bronze/purchase-orders/`, `/bronze/shipments/`, preserving exact source structure and content.
  Delta transaction logs enable point-in-time recovery and complete audit history, with 7-year retention for compliance with SOX audit requirements.

- **Silver Layer**: Cleaned and standardized datasets under `/silver/dim_suppliers/`, `/silver/dim_products/`, `/silver/fact_purchase-orders/` with data quality rules applied, duplicates removed, and business transformations executed.
  Partitioning by `effective_date` for dimensions enables SCD Type 2 implementation and efficient historical queries for supply chain analysis.

- **Gold Layer**: Business-ready curated models under `/gold/analytics/` including `star_schema_procurement`, `star_schema_logistics`, and operational marts like `supplier_scorecards` and `inventory_position`, optimized for Power BI and executive dashboards.
  Z-ordered by high-selectivity columns (supplier_id, product_id) to accelerate analytical queries and cached in memory for dashboard-driven access patterns.

- **Archive Layer**: Historical data older than 18 months transitioned to low-cost tiers under `/archive/`, with Parquet files organized by year and month to support compliance reporting and historical analysis.
  Archived data remains queryable through Synapse for quarterly audits, with all access logged and restricted to authorized compliance personnel.

## 5. Source System Connectivity (ADF)

The ingestion framework establishes 12 distinct linked services connecting to disparate source systems, each requiring tailored authentication, retry logic, and throttling policies based on source capabilities and network conditions. Connection strings and API keys are stored exclusively in Key Vault with time-limited access tokens rotated automatically.

- **Linked Service Configuration**: Configure linked services for SAP HANA database (TLS encryption, connection pooling), REST APIs for supplier portals (OAuth 2.0, bearer token authentication), SFTP servers (SSH key-based auth), and Kafka brokers (SASL/SSL, consumer group management).
  Test each linked service using ADF's connection testing feature to validate credentials and network paths before deploying production pipelines.

- **Integration Runtime Selection**: Deploy Azure Integration Runtime for cloud-to-cloud connectivity to Salesforce CRM and public APIs, utilizing Microsoft-managed infrastructure without operational overhead.
  Deploy self-hosted integration runtime on-premises for secure SAP ERP connectivity, installing runtime on Windows VM with outbound internet access for communication with ADF control plane.

- **Endpoint Validation**: Validate all source endpoints using test connection features, confirming API response codes, authentication success, and firewall accessibility before pipeline deployment.
  Document firewall rules required for IP whitelisting of ADF integration runtimes and VPN tunnels to on-premises systems.

- **API Rate Limiting & Throttling**: For supplier portal APIs with rate limits of 1,000 requests/hour, configure ADF copy activity with `batchSize=100` and `parallelCopies=4` to distribute load and respect rate limits.
  Implement exponential backoff retry logic with jitter to handle transient 429 (too many requests) errors gracefully without bombarding rate-limited APIs.

- **Database Extraction Tuning**: For large ERP tables (100M+ purchase orders), configure partitioned extraction using `@shardKey` parameter to extract ranges in parallel (e.g., 8 parallel queries for date ranges), improving throughput from 50K rows/sec to 400K rows/sec.
  Document optimal partition column and value ranges based on source system distribution statistics.

- **Encryption & Security**: Encrypt all connections using TLS 1.2 or higher, disabling older SSL versions vulnerable to attacks, and enforce certificate validation to prevent man-in-the-middle attacks.
  For SFTP connectivity, require SSH key-based authentication (RSA 4096-bit keys) over password authentication to meet security compliance standards.

- **Source-to-Target Matrix**: Maintain documentation of all 15 source systems including endpoint URLs, authentication methods, expected data volumes, loading frequencies, and SLA requirements.
  This matrix serves as single source of truth for connectivity configuration and change management when sources retire or new sources onboard.

## 6. Ingestion Framework (ADF – Metadata Driven)

The ingestion framework implements a metadata-driven architecture where configuration tables drive pipeline behavior without code changes, enabling rapid onboarding of new sources and flexibility in handling business changes. Central metadata tables store source details, transformation rules, and lineage information, with ADF Lookup activities retrieving metadata at runtime to dynamically generate source-to-target mappings.
Three parameterized pipelines handle distinct workload patterns: scheduled batch ingestion for daily PO loads, streaming ingestion for Kafka-based shipment events, and incremental change capture using watermark-based logic for high-frequency updates.

- **Metadata Table Design**: Create `mtd_source_systems` table with columns for source_id, system_name, connection_type (API, DB, SFTP, Kafka), endpoint, frequency, sla_minutes, and last_watermark_value.
  Additional `mtd_transformations` table stores transformation_id, source_id, target_layer, transformation_logic, validation_rules enabling dynamic rule application across pipelines.

- **Dynamic Lookup & ForEach Pattern**: Implement Lookup activity to retrieve active sources from metadata table, filter for sources with `@greaterOrEquals(utcNow(), scheduled_run_time)` condition to identify sources requiring execution.
  Use ForEach activity to iterate through metadata results, setting pipeline parameters from each row (source_id, endpoint, frequency) and triggering child pipelines for source-specific ingestion logic.

- **Copy Activity Configuration**: Configure Copy activity with dynamic properties sourced from metadata: `source.query = mtd.source_query_template`, `sink.path = concat('/bronze/', mtd.target_entity, '/')`, `copyBehavior.translator = mtd.column_mapping_json`.
  Enable staging to optimize data movement for cloud-to-cloud transfers, writing to staging area first then committing to final location for transactional safety.

- **Watermark-Based Incremental Processing**: For purchase order updates, implement watermark logic storing `last_update_timestamp` in audit table; ADF Lookup retrieves previous watermark, passes to source query as parameter (e.g., `WHERE updated_at > @{activity('Get_Watermark').output.firstRow.last_timestamp}`).
  After successful copy, Update activity increments watermark to current run's `@pipeline().TriggerTime`, enabling true incremental loads without full refresh.

- **Change Data Capture Integration**: For sources supporting CDC (SAP HANA, SQL Server), leverage built-in CDC logs to extract only changed records rather than full exports, reducing source system load by 70%.
  Implement soft delete logic at sink where deleted_flag=1 marks records as deleted in target instead of physical deletion, preserving audit trail.

- **Failure Handling & Retries**: Implement retry policy with exponential backoff (InitialInterval=10 seconds, MaximumInterval=5 minutes, multiplier=2) for transient failures like network timeouts and throttling errors.
  Exceptions like schema mismatches or authorization errors bypass retries and send alerts immediately, as retries will not resolve permanent errors.

- **Validation Activities**: Add pre-copy validation checking source connectivity and schema compatibility, and post-copy validation comparing row counts between source and sink with tolerance of ±1% for record count differences.
  Store validation results in audit table with detailed error messages for failed validations, enabling root cause analysis.

- **Audit & Logging**: Implement activity-level logging storing job_id, pipeline_name, activity_name, start_time, end_time, status, and row_count_processed in `audit_pipeline_runs` table.
  Capture full error stack traces for failed activities, enabling support teams to quickly diagnose issues and accelerate resolution.

- **Trigger Configuration**: Schedule batch pipelines using tumbling window trigger running daily at 2 AM UTC to complete by business hours, with dependency chain ensuring validation completes before downstream processing.
  Configure event-based trigger for shipment data to react immediately to Kafka messages, supporting near real-time dashboard updates.

- **Dependency Management**: Use Wait, If, and Until activities to manage pipeline dependencies, e.g., Gold layer processing waits until Silver layer transformation completes successfully, with failure branches sending notifications to operations teams.
  Until loops check for file arrival every 5 minutes with maximum wait of 1 hour, failing gracefully if expected files don't arrive to prevent indefinite waiting.

## 7. Pre-Bronze Validations

Pre-ingestion validation ensures only clean, schema-compliant data proceeds to bronze layer, catching issues early before they cascade through transformation layers. Seven distinct validation checks execute sequentially, with each failure triggering quarantine to investigate folder and notification to data stewards for remediation.

Validation rules must tolerate legitimate business variations (e.g., nullable columns, valid NULL values) while catching corrupted or malformed data requiring attention. Comprehensive audit logging provides data lineage showing exactly which files passed validation and which require intervention.

- **Filename & Pattern Validation**: Enforce strict filename conventions (e.g., `PO_YYYYMMDD_HHmm.csv` for purchase orders) with regex pattern matching to catch misnamed files indicative of source system errors.
  Reject files with incorrect patterns, timestamp inconsistencies (future dates, dates older than 90 days), or source identifiers not registered in metadata, moving to quarantine folder with failure notification.

- **Schema Consistency Checks**: Compare incoming file column count (expected 23 columns for PO files) against template schema, validating exact column order and data types match expectations.
  For header-based files, extract header row and compare against reference schema; for headerless files, infer types from sample data and validate against expected type list.

- **File Size Validation**: Validate file size falls within acceptable range (PO files typically 50MB-500MB); files smaller than 1MB likely indicate truncation or failed export, while files exceeding 2GB suggest data concatenation errors.
  Quarantine undersized and oversized files for investigation, preventing ingestion of obviously corrupted data.

- **Header Row Validation**: For CSV files, validate header row contains exactly expected columns in correct order, detecting common issues like column reordering, renamed columns, or missing mandatory fields.
  Create reference templates for each source documenting expected headers; compare incoming headers via set difference to identify added, removed, or reordered columns.

- **Sample Data Inspection**: Extract sample of first 1,000 rows and apply data quality rules, checking for unexpected NULL values in mandatory fields (e.g., customer_id, order_date should never be NULL), special characters indicating encoding issues, or dates outside realistic ranges.
  If sample inspection detects >5% anomalies, quarantine entire file for manual review rather than attempting automatic remediation.

- **Audit Trail Management**: Store validation results in `validation_audit` table with columns: file_name, validation_timestamp, validation_type (filename, schema, size, header, sample), validation_status (passed/failed), and detailed_error_message.
  Retention policy keeps audit records for 2 years, enabling compliance reporting and pattern analysis of recurring validation failures.

- **Failure Handling & Notification**: Move failed files to `/quarantine/YYYY-MM-DD/source-system/` with detailed error logs stored alongside, enabling support teams to investigate failures without accessing production pipelines.
  Send notifications to data stewards with file names, validation failure reasons, and recommended corrective actions; implement SLA requiring response within 4 business hours.

## 8. Bronze Layer Processing

The bronze layer functions as an immutable source-of-truth archive storing data in exact format as received from source systems, preserving complete history for audit compliance and enabling point-in-time recovery for troubleshooting. Delta format ensures ACID compliance and transactional safety while maintaining detailed metadata tracking data lineage and load history.

Bronze tables partition by load date and source system, optimizing for efficient data discovery and enabling retention policies (e.g., purge logs after 7 years). Minimal transformations (column trimming, type casting) preserve source structure while enabling downstream access patterns.

- **Delta Lake Storage**: Store bronze data in Delta format at `/bronze/supplier_master/`, `/bronze/purchase_orders/`, `/bronze/shipments/` with ACID transactions ensuring data consistency across distributed writes.
  Enable schema enforcement to prevent schema drift, requiring explicit schema evolution approval rather than automatic silent schema changes.

- **Audit Metadata Tracking**: Add `load_date`, `source_file_name`, `data_ingestion_timestamp`, and `record_count_processed` columns to each bronze table, enabling lineage tracking showing exactly when and from which files data originated.
  Maintain separate `bronze_metadata` table storing load statistics (total rows, min/max dates, data volume in MB) for each load, enabling data quality trending over time.

- **Complete File History**: Retain all files in landing/pre-bronze layers for 7 years to support full reconstruction of any prior load if data corruption discovered downstream, enabling forensic analysis of data quality issues.
  Document data retention policies in compliance documentation for SOX and HIPAA audits.

- **Minimal Transformations**: Apply only essential transformations at bronze layer: trim leading/trailing spaces from string columns, cast numeric strings to decimal types, standardize date format to ISO 8601.
  Explicitly avoid business logic transformations at this layer, which belong in silver layer where documented transformations and data quality checks apply.

- **Partition Strategy**: Partition purchase orders by `order_date` and source system to enable efficient incremental processing; for high-cardinality fields like supplier_id, avoid direct partitioning but allow Synapse to prune based on partition values.
  Implement partitioning at write time in Databricks, leveraging `partitionBy` clause to ensure proper storage structure.

- **Schema Evolution Handling**: For semi-structured data (JSON APIs), enable schema evolution mode allowing new fields to emerge without breaking pipelines, storing unknown fields in `_extra_fields` column for later processing.
  Document schema evolution procedures requiring data engineer approval for breaking changes (removed/renamed fields) while allowing non-breaking additions.

## 9. Silver Layer Transformations (Databricks + PySpark)

The silver layer implements comprehensive data quality, cleansing, and enrichment transformations standardizing data for analytics while maintaining complete history for audit compliance. Spark-based transformations scale to handle terabyte-level datasets, with distributed processing and fault tolerance ensuring reliability.

Twelve distinct transformation categories apply business logic, remove duplicates, enforce data types, and validate data quality rules. Failed records populate exception tables enabling investigation and remediation before promotion to gold layer.

- **Data Cleansing**: Trim leading/trailing whitespace from all string columns using `trim()` function, replace empty strings with proper NULL values, standardize date formats to ISO 8601 (YYYY-MM-DD).
  Handle common encoding issues by converting special characters to ASCII equivalents and removing control characters that indicate data corruption.

- **Duplicate Removal**: Use window functions to identify duplicates based on business keys (supplier_id, order_id), retaining most recent based on `load_timestamp`, and remove using `row_number() OVER (PARTITION BY business_key ORDER BY load_timestamp DESC)`.
  Log discarded duplicates to exception table with row count and estimated data loss percentage for quality trending.

- **Type Casting & Validation**: Cast numeric strings to decimal/integer types with error handling for non-numeric values, cast date strings to proper date types with validation for realistic date ranges (e.g., supplier registration date between 1970 and today).
  Store records failing type casting in exception table with original values preserved for investigation.

- **Business Transformation Logic**: Apply SME-defined transformations including purchase order lead time calculation (receive_date - order_date), supplier quality score aggregation (weighted average of defect rates), inventory aging (current_date - receipt_date).
  Maintain transformation documentation in metadata tables showing formula definitions and calculation examples for audit purposes.

- **Data Quality Rule Enforcement**: Apply referential integrity checks (supplier_id exists in supplier master), threshold validation (order_quantity > 0 and < 1,000,000), and pattern validation (customer_code matches regex `^[A-Z]{2}[0-9]{6}$`).
  Reject or quarantine records violating quality rules with detailed error messages enabling investigation and source system correction.

- **SCD Type 2 Implementation**: For customer and supplier dimensions, implement SCD Type 2 to track changes over time, adding `effective_date` and `expiration_date` columns and creating new records when attributes change rather than overwriting.
  Query `WHERE expiration_date = '9999-12-31'` retrieves current dimension values, while complete history available for analyzing how customer attributes evolved.

- **Incremental Processing with MERGE**: Use MERGE INTO statements to update existing records and insert new entries efficiently, reducing transformation time from 3 hours (full reload) to 15 minutes (incremental updates).
  MERGE matches on business keys, updates changed attributes in matched records, and inserts non-matching records as new rows.

- **Streaming Ingestion with Autoloader**: For continuously arriving files (Kafka topics, Event Hub streams), implement Autoloader to automatically discover and ingest new files without manual intervention, benefiting from schema inference and fault tolerance.
  Autoloader caches schema to prevent repeated inference and tracks processed file metadata to prevent duplicate processing.

- **Partition Pruning Optimization**: Partition silver tables by `effective_date` and `source_system` to enable partition pruning in downstream queries, reducing data scans from 500GB to 50GB for single-day analytics.
  Document partition key selection rationale showing business value of each partition choice.

- **Delta Constraints**: Apply constraints to enforce data integrity (e.g., `NOT NULL` for supplier_id, CHECK constraint for quantity > 0), preventing invalid data from entering production tables and catching errors immediately.
  Violated constraints trigger failures visible to data engineers, enabling rapid root cause identification and correction.

- **Transformation Documentation**: Document all transformation logic in notebook comments and separate `transformation_definitions` metadata table storing logic descriptions, data quality rule definitions, and calculation formulas.
  Include examples showing before/after transformation values and rationale for each business rule implementation.

- **Quality Validation**: After transformations complete, validate output using record count reconciliation (silver row count = bronze row count ± rejected_records), business rule verification (supplier_quality_score between 0-100), and cardinality checks (unique supplier count matches expectations).
  Store validation results in quality audit table, enabling trending of data quality over time and identification of systematic issues.

## 10. Gold Layer Aggregations

The gold layer curates business-ready dimensional and fact models optimized for Power BI and executive dashboards, implementing star schemas that simplify join logic and accelerate query performance. Aggregated marts pre-compute intensive calculations, trading storage for query speed.

Eight transformation categories implement fact tables, dimensions, aggregations, KPI calculations, and analytical patterns supporting diverse reporting needs. Z-ordering optimizations and caching ensure analytical queries complete in seconds rather than minutes.

- **Fact Table Construction**: Build `fact_purchase_orders` containing order-level transactions with surrogate keys (order_key, supplier_key, product_key, date_key), degenerate dimensions (order_type), and metrics (order_quantity, unit_price, extended_amount).
  Implement `fact_shipments` containing shipment events with metrics for package_weight, transit_days, and freight_cost, enabling supply chain performance analysis.

- **Dimension Table Design**: Create `dim_suppliers` with slowly changing dimension Type 2 tracking supplier name changes, address updates, and business status transitions with effective dating.
  Build `dim_products` with product hierarchies (category, subcategory, SKU) and `dim_dates` with calendar attributes (fiscal_quarter, day_of_week) enabling dimensional analysis.

- **Star Schema Optimization**: Join fact and dimension tables using surrogate keys, removing business key dependencies and enabling efficient join predicate pushdown in Synapse SQL.
  Validate referential integrity ensuring all foreign keys in fact tables reference existing dimension records, catching data quality issues before dashboards consume data.

- **Mart-Level Aggregations**: Pre-compute `supplier_scorecards_daily` aggregating purchase order metrics by supplier (total_spend, on_time_delivery_pct, quality_score), reducing dashboard query from 5 minutes to 2 seconds.
  Create `inventory_position_hourly` mart updating every hour with current inventory levels, aging bucket counts, and slow-moving item flags.

- **KPI Calculation**: Implement revenue metrics (sum of extended_amount), efficiency metrics (on_time_delivery_pct = on_time_deliveries / total_deliveries), and profitability metrics (gross_margin = revenue - cost_of_goods_sold).
  Document KPI definitions in metadata to ensure consistent calculation across reports and enable audit trails showing calculation logic.

- **Rolling & Cumulative Metrics**: Use window functions to calculate rolling 30-day average delivery time and cumulative year-to-date spend per supplier, enabling trend analysis and comparative performance ranking.
  Pre-compute rolling metrics at grain of supplier/month to avoid expensive window function recalculation on each dashboard query.

- **Z-Order Optimization**: Apply Z-ordering by supplier_id and product_id to gold fact tables, ensuring data files sorted optimally for queries filtering on these high-selectivity columns, improving data skipping efficiency.
  OPTIMIZE command compacts small files and reorders data, reducing query runtime by 40% for common filtering patterns.

- **Validation & Reconciliation**: Reconcile gold fact totals with source system totals (e.g., gold purchase_order_total should match ERP system total), detecting data loss or corruption before dashboards consume data.
  Implement exception handling routing records failing validation to investigation tables rather than silently discarding data.

## 11. Delta Lake Optimization Techniques

Delta Lake optimizations ensure gold layer tables deliver analytical query performance required for executive dashboards and real-time scorecards. Eight optimization techniques address file proliferation, query efficiency, and storage costs.

Systematic optimization during low-traffic periods maximizes system availability during business hours while maintaining peak performance. Monitoring tracks optimization metrics enabling continuous improvement.

- **OPTIMIZE with Z-ORDER**: Execute `OPTIMIZE fact_purchase_orders ZORDER BY supplier_id, product_id` to reorder data files around high-selectivity columns, enabling file-level data skipping to skip 95% of files for queries filtering on supplier.
  Schedule OPTIMIZE operations daily during 2-4 AM UTC window to minimize impact on business users, with completion within 30 minutes for tables under 50GB.

- **VACUUM Operation**: Run `VACUUM fact_purchase_orders RETAIN 7 DAYS` weekly to purge Delta transaction log snapshots older than 7 days, reducing storage overhead from 30% to <5% and improving metadata lookup performance.
  Maintain deletion retention of 7 days enabling rollback of recent changes if data quality issues discovered; balance between recovery capability and storage cost.

- **Auto-Compaction**: Enable auto-compaction on write operations for gold layer tables, automatically merging small files created by incremental updates into optimal size (128MB targets) without manual intervention.
  Monitor compaction metrics tracking reduction in file count from 10,000 small files to 100 optimized files, improving query performance by reducing file open operations.

- **Table Caching**: Cache frequently accessed gold tables in Databricks cluster memory (e.g., supplier_scorecards used in 100+ daily queries), reducing ADLS network I/O and accelerating queries from 10 seconds to 1 second.
  Implement cache refresh schedule updating cached tables every hour during business hours to balance freshness and cache efficiency.

- **Data Skipping**: Leverage Delta's automatic data skipping metadata tracking min/max values per file, enabling queries like `SELECT * FROM fact_orders WHERE order_date = '2025-01-15'` to skip 99% of files without scanning.
  Data skipping effectiveness depends on Z-ordering effectiveness; validate that queries show high percentage of files skipped (>90%) indicating effective optimization.

- **Partition Pruning**: Design partitioning strategy (by order_date, supplier_id) enabling Synapse to prune irrelevant partitions, reducing scan from 100 tables to 1-2 tables when filtering on partition key.
  Document partition design decisions showing performance improvements and storage efficiency vs. partition explosion risk.

- **Schema Evolution Safety**: Use schema evolution mode allowing new columns without breaking existing queries, storing unknown columns in struct field preventing schema conflicts that force table rebuild.
  Implement approval process for breaking changes (column removal, type changes) requiring data engineer sign-off before deployment.

- **Shuffle Partition Tuning**: Set `spark.sql.shuffle.partitions` based on cluster size (clusters with 32 vCores use 256 shuffle partitions), optimizing parallelism without excessive task overhead.
  Monitor skew in partition sizes; if some partitions 10x larger than others, investigate data distribution and implement custom repartitioning.

## 12. Consumption Layer (Synapse + Power BI)

The consumption layer exposes gold layer tables through Synapse SQL for ad-hoc analysis and Power BI semantic models for self-service dashboards, implementing row-level security and performance optimization ensuring thousands of concurrent users access data interactively.

Seven strategies optimize query performance, secure data access, and deliver fresh insights to supply chain decision-makers within SLA requirements.

- **Synapse External Tables**: Create external tables in Synapse referencing Delta files in ADLS gold layer (e.g., `CREATE EXTERNAL TABLE fact_orders STORED AS PARQUET LOCATION '/gold/fact_orders/'`), enabling serverless SQL querying without copying data.
  Configure external data source with managed identity ensuring Synapse has permissions to access ADLS without storing credentials in pipeline.

- **SQL Views & Semantic Models**: Build views joining fact and dimension tables (`CREATE VIEW v_supplier_performance AS SELECT * FROM fact_orders JOIN dim_suppliers...`), simplifying semantic modeling and enabling Power BI to use views as data sources.
  Implement views with appropriate filters restricting data to relevant business units, replacing row-level security logic in upstream filters.

- **Query Mode Selection**: Enable DirectQuery for near real-time dashboards requiring latest data within 5-minute latency, connecting directly to Synapse and querying live data.
  Use Import mode for large dimension tables and aggregated marts, importing data into Power BI model and refreshing every 2 hours for optimal performance.

- **Power BI Semantic Models**: Build semantic model with fact table relationships to 5 dimension tables, implementing many-to-one relationships and creating measures for key metrics (SUM of revenue, AVERAGEX for quality scores).
  Implement DAX calculations for complex KPIs like YTD revenue and moving averages, offloading calculation from source systems.

- **Row-Level Security**: Implement RLS restricting procurement managers to their assigned suppliers, logistics managers to their assigned regions, and finance to all data.
  RLS rules implemented via DAX formulas (e.g., `FILTER(ALL(dim_suppliers), dim_suppliers[assigned_manager] = USERNAME())`) or via Synapse SQL views, with enforcement transparent to report users.

- **Dashboard Publishing & Refresh**: Publish dashboards to Power BI Service with scheduled refresh every 2 hours during business hours, ensuring executives see data no older than 2 hours.
  Configure refresh failure alerts notifying BI team within 15 minutes, enabling rapid diagnosis before executives attempt to access stale dashboards.

- **Performance Optimization**: Build aggregations on top of fact tables pre-computing monthly supplier performance metrics, enabling dashboard queries to query lightweight aggregated tables rather than 100M-row fact tables.
  Use composite models combining imported dimension tables with DirectQuery fact tables, balancing performance with freshness.

## 13. Monitoring & Alerting

Comprehensive monitoring ensures supply chain platform achieves SLA targets, detects failures proactively, and enables rapid resolution before business impact. Thirteen monitoring components track pipeline execution, data quality, and operational health.

Dashboards visualize end-to-end data flow from source system ingestion through analytical consumption, providing data operations teams visibility into platform health. Automated alerts escalate issues requiring human intervention.

- **ADF Pipeline Monitoring**: Track pipeline metrics including execution count (50 daily runs), success rate (target 99.9%), average duration (target <30 minutes), and data throughput (500GB/hour target).
  Alert if success rate drops below 99%, execution duration exceeds 1 hour, or throughput falls below 300GB/hour, indicating performance degradation.

- **Databricks Job Monitoring**: Monitor job runtime, failure rate, and cluster utilization, tracking silver layer transformation jobs completing within SLA (target 2 hours for daily batch).
  Alert if cluster utilization exceeds 90% for >15 minutes, indicating need to scale cluster; log metrics to track cost vs. performance.

- **Log Analytics Integration**: Centralize logs from ADF, Databricks, Synapse to Log Analytics workspace, querying across services to build observability dashboards showing end-to-end platform health.
  Implement cross-service correlation tracking data lineage from ingestion through consumption, enabling root cause analysis of downstream data issues.

- **Pipeline Failure Alerts**: Configure alerts in Azure Monitor triggering when ADF pipelines fail, sending notifications to data engineering team via email and Teams channel within 5 minutes.
  Alert with contextual information (failed activity name, error message) enabling rapid diagnosis; link to troubleshooting runbooks.

- **SLA Dashboard**: Build dashboard tracking daily SLA compliance showing ingestion completion time vs. SLA target (2-hour target), data freshness (age of gold layer), and pipeline availability.
  Highlight red any metrics exceeding SLA threshold, enabling proactive escalation before business impact.

- **Historical Run Analysis**: Retain pipeline execution history for trending analysis, identifying recurring failures (e.g., API rate limit errors at specific time), recurring performance degradation (e.g., slow on month-end), and optimization opportunities.
  Use historical patterns to tune system configuration (retry intervals, parallelism, cluster size) based on actual behavior rather than guesses.

- **Event Hub Integration**: Stream operational logs to Event Hub enabling real-time observability patterns, with Stream Analytics jobs processing logs to detect anomalies (e.g., error spike detection).
  Send immediate alerts on pattern anomalies before they cascade into downstream failures.

- **Cost Monitoring**: Track cloud cost metrics (daily ADF cost, Databricks hourly cost, storage utilization) with dashboards showing cost trends and cost forecasts.
  Alert if daily cloud costs exceed 20% threshold above average, indicating operational issue (e.g., runaway pipeline, unoptimized query) requiring investigation.

- **Schema Drift Detection**: Monitor incoming files for schema changes (new columns, column removal, type changes), alerting data stewards when schema evolution detected requiring review.
  Capture schema change history enabling analysis of how data structures evolve over time.

- **Custom Operational Dashboard**: Build dashboard visualizing end-to-end data flow with source ingestion metrics, transformation duration, gold layer freshness, and consumption metrics (Power BI query count, average query time).
  Dashboard serves as operations cockpit enabling data team to assess platform health at a glance and drill into specific issues for investigation.

## 14. Security & Governance

Supply chain data includes sensitive supplier information and financial metrics requiring comprehensive security controls. Ten security categories implement defense-in-depth approach protecting data throughout pipeline.

Role-based access control restricts data visibility to authorized users while enabling efficient self-service analytics. Compliance frameworks (HIPAA for healthcare suppliers, GDPR for European suppliers) drive governance policies.

- **Key Vault Secrets Management**: Store 25+ secrets (database passwords, API keys, SFTP credentials, PAT tokens) in Key Vault with strict RBAC access limiting ADF service principal to read-only access to specific secrets.
  Rotate secrets every 90 days using automated Key Vault policies, with rotation logs audited for compliance.

- **Managed Identities**: Use managed identities for ADF, Databricks, and Synapse to authenticate to ADLS and other Azure services without storing credentials in configuration.
  Eliminate credential management burden and associated security risks from shared passwords; managed identities leverage Azure infrastructure for authentication.

- **Private Endpoints**: Create private endpoints for ADLS storage account, SQL databases, and Key Vault, restricting connectivity to private VNETs and eliminating public internet exposure.
  Configure private DNS zones enabling applications to resolve private endpoint names correctly, with DNS traffic remaining within VNETs.

- **Network Segmentation**: Implement VNETs with subnets for Databricks compute, Synapse SQL pool, and ADF integration runtime, enforcing network isolation and preventing cross-tier communication.
  Apply NSGs restricting inbound traffic to approved sources only, reducing attack surface by denying traffic outside trusted networks.

- **Firewall Configuration**: Implement Azure Firewall for centralized outbound filtering, restricting egress traffic to approved destinations (supplier APIs, log aggregation services) and logging all blocked traffic.
  Firewall rules prevent exfiltration of data to unauthorized destinations and provide audit trails for incident investigation.

- **Encryption in Transit**: Enforce HTTPS-only access to storage, disabling HTTP connections to prevent interception of credentials or data in transit.
  Use TLS 1.2 or higher for all network connections, disabling older versions vulnerable to known attacks.

- **Encryption at Rest**: Enable encryption-at-rest using customer-managed keys stored in Key Vault (vs. Microsoft-managed keys), meeting compliance requirements for data residency and key control.
  Rotate encryption keys annually per compliance policy, with rotation process documented and tested quarterly.

- **Azure Purview Integration**: Register ADLS, Synapse, and Databricks with Azure Purview for lineage tracking and data governance, scanning assets for metadata cataloging.
  Establish data classification taxonomy (public, internal, sensitive, restricted) and classify all datasets; governance policies prevent sharing of restricted data outside approved channels.

- **Access Auditing**: Enable audit logging on storage and compute services capturing all data access (reads, writes, deletes) with user identity, timestamp, and action details.
  Detect anomalies (e.g., non-procurement user accessing supplier data) via alert rules, enabling rapid investigation of unauthorized access attempts.

- **Compliance Mappings**: Document compliance framework mappings for HIPAA (data encryption, access controls, audit logging), GDPR (data minimization, retention limits, right to deletion), and SOX (financial data integrity).
  Maintain compliance evidence documents proving controls implemented match regulatory requirements, supporting external audit processes.

## 15. CI/CD Pipeline Setup (Azure DevOps or GitHub Actions)

Version-controlled deployment ensures consistent infrastructure and pipeline code across environments, enabling rapid iteration and rollback of problematic changes. Automated testing catches errors before production deployment.

Ten CI/CD practices implement consistent deployment workflows ensuring quality and auditability.

- **ADF Git Integration**: Store ADF pipeline JSON definitions in Git repository (Azure DevOps or GitHub), enabling version history, code review, and rollback to prior versions if issues detected.
  Establish branching strategy (main for production, develop for integration, feature branches for development) enabling parallel development without conflicts.

- **Databricks Notebook Versioning**: Sync Databricks notebooks with Git repository using Databricks Repos feature, tracking transformation code changes and enabling code reviews before production deployment.
  Implement naming conventions documenting environment (dev, prod) and version numbers enabling identification of active notebook versions.

- **Infrastructure as Code**: Define ADF pipelines, Synapse SQL scripts, and Azure resources using ARM templates or Terraform code, enabling repeatable deployments across dev/test/prod environments.
  Parameterize environment-specific values (resource names, SKUs, configuration) enabling single IaC template deployment to multiple environments.

- **YAML Pipeline Definitions**: Implement build and release pipelines using YAML syntax stored in Git repository, enabling code review and version history for CI/CD configuration.
  Define stages (build, integration test, production deployment) with approval gates and automated testing between stages.

- **Deployment Parameterization**: Parameterize deployments for dev (small cluster, 2-hour refresh), test (medium cluster, 4-hour refresh), and prod (large cluster, 1-hour refresh) environments.
  Use variable groups storing environment-specific parameters (resource group names, storage account names, key vault references) enabling environment-agnostic IaC.

- **Approval Gates**: Implement manual approval gates in DevOps release pipeline requiring designated data engineering lead approval before production deployment.
  Approval workflow captures who approved change, approval timestamp, and approval comments, maintaining audit trail for compliance.

- **Unit & Data Testing**: Implement unit tests for transformation logic (PySpark code unit tests using pytest), validating business logic correctness before deployment.
  Create data tests validating gold layer output matches expected schema and business rules (e.g., supplier quality scores between 0-100) before release.

- **Synapse SQL Deployment**: Deploy Synapse SQL scripts (views, stored procedures, tables) automatically within CI/CD pipeline, with versioning tracking schema changes and enabling rollback.
  Implement pre-deployment validation checking for breaking changes (column removal) requiring additional approval to prevent accidental data loss.

- **Incremental ADF Deployment**: Implement incremental pipeline deployment publishing only changed artifacts rather than entire ADF definition, reducing deployment time and change surface.
  Validate that incremental deployment doesn't accidentally overwrite untouched pipelines or miss dependent changes.

- **CI/CD Documentation**: Document CI/CD workflows in runbooks explaining deployment process, approval requirements, and rollback procedures for support teams managing production issues.
  Include troubleshooting guidance for common deployment failures (credential issues, dependency problems) enabling rapid resolution.

## 16. Performance Optimization

Analytical query performance directly impacts user adoption and business value delivery. Seven optimization strategies ensure dashboard queries complete within 5-second SLA and batch transformations complete within SLA windows.

Continuous monitoring and tuning maintain performance as data volume grows.

- **ADF Configuration Tuning**: Tune Data Integration Units (DIUs) from default 4 to 16 DIUs during peak ingestion windows, distributing copy activity across more compute resources to increase throughput.
  Monitor DIU utilization during peak loads; if utilization >80% for sustained periods, increase DIU count; if <20%, reduce DIUs to save cost.

- **Spark Join Optimization**: Use broadcast joins for small dimension tables (< 100MB) broadcast to all worker nodes, avoiding expensive shuffle operation for large table joins.
  Implement bucketing on join columns for frequently joined large tables, pre-organizing data to avoid shuffle during joins.

- **Cluster Configuration**: Size Databricks clusters for workload profile: 4-node cluster for development, 16-node cluster for silver layer transformation (2-hour daily batch), 8-node autoscaling cluster for ad-hoc queries.
  Use memory-optimized node types (Databricks L series) for in-memory data processing of aggregations, trading cost for performance.

- **Delta Lake Optimization**: Run OPTIMIZE with ZORDER monthly on gold layer tables, reducing query runtime for filtered queries from 20 seconds to 2 seconds via improved data skipping.
  Monitor OPTIMIZE operations ensuring completion within maintenance windows; very large tables may require multi-step optimization.

- **Caching Strategy**: Cache supplier_scorecards_daily in Databricks cluster memory, eliminating repeated disk I/O for frequently accessed analytical tables used by 100+ daily dashboard queries.
  Implement cache refresh every 2 hours during business hours balancing freshness with cache efficiency.

- **SQL Query Optimization**: Tune Synapse SQL queries using indexes on high-selectivity columns (supplier_id, order_date), partition elimination for queries filtering on partition keys, and statistic updates enabling better query plans.
  Use Synapse SQL query statistics gathering workload patterns and recommending optimal indexes and statistics.

- **Power BI Performance**: Build aggregations pre-computing monthly supplier metrics, enabling dashboard queries to execute against lightweight aggregated tables rather than 100M-row fact tables.
  Use composite models balancing imported dimension tables (fast) with DirectQuery fact tables (fresh), optimizing for responsiveness and freshness.

## 17. Cost Optimization

Cloud spend optimization balances performance, freshness, and reliability with cost efficiency. Seven strategies reduce monthly cloud costs from $50,000 to $35,000 (30% savings) without sacrificing capability.

Continuous monitoring identifies optimization opportunities as workload patterns evolve.

- **Auto-Termination**: Enable auto-termination on Databricks interactive clusters after 15 minutes of inactivity, preventing wasted compute costs from forgotten cluster sessions.
  Retain long-running job clusters until job completion, but apply strict termination policies.

- **Storage Tiering**: Move data older than 180 days from hot tier (ADLS standard) to archive tier (Azure Blob Storage archive), reducing storage costs from $50/TB/month to $1/TB/month for aged data.
  Maintain queryability of archived data via Archive-Restore functionality (4-hour latency acceptable for historical audits).

- **Pipeline Optimization**: Identify long-running pipelines and optimize transformations reducing execution time from 3 hours to 1.5 hours, saving compute costs by 50%.
  Use pipeline execution history trending to identify optimization opportunities with highest cost impact.

- **Off-Peak Scheduling**: Schedule non-critical batch jobs during off-peak hours (10 PM - 6 AM UTC) when compute resources cost 30% less, moving high-cost workloads outside business hours.
  Maintain business-critical pipelines during business hours; batch jobs completing by business hours acceptable if triggered overnight.

- **Serverless SQL Economy**: Use serverless SQL for ad-hoc queries and exploratory analysis, paying only for data scanned; avoid using dedicated SQL pools for occasional queries where pay-per-execution costs less.
  Identify queries running frequently and move to dedicated pool if total cost lower than pay-per-execution.

- **Spot VMs**: Use spot VMs for non-critical Databricks worker nodes (non-critical transforms, development/test workloads) at 70% discount vs. standard VMs, accepting rare interruption in exchange for cost savings.
  Reserve standard VMs for production job clusters requiring 99.9% availability.

- **Refresh Frequency Optimization**: Reduce Power BI refresh frequency from every 1 hour to every 4 hours where business doesn't require intraday updates, reducing data movement and compute costs.
  Implement event-based refresh triggering refresh only when underlying data changes rather than on fixed schedule.

## 18. Documentation & Knowledge Transfer

Comprehensive documentation ensures platform sustainability beyond initial development team, enabling support teams to operate platform and new engineers to onboard efficiently. Six documentation categories support different audience needs.

Documentation evolves as system matures, capturing lessons learned and incorporating operational feedback.

- **Architecture Diagrams**: Prepare detailed diagrams showing data flow from source ingestion (ERP, APIs, Kafka) through bronze/silver/gold layers to Power BI consumption.
  Include integration points (Key Vault, Log Analytics), network topology (VNETs, private endpoints), and deployment stages (dev/test/prod) for complete architecture understanding.

- **Runbooks**: Create detailed runbooks for support teams documenting common failure scenarios (API rate limit errors, schema mismatches, authentication failures) with step-by-step resolution procedures.
  Include troubleshooting decision trees guiding support from symptom observation through root cause identification to resolution.

- **Standard Operating Procedures**: Document daily, weekly, and monthly operational tasks (cluster restart, log archival, cost reviews) with detailed step-by-step procedures and expected outcomes.
  Include escalation procedures for issues exceeding support team authority (scale cluster, modify SLA, authorize cost exception).

- **Data Dictionary**: Maintain comprehensive data dictionary for silver and gold tables documenting all columns with definitions, data types, sample values, calculation logic for computed columns.
  Include business glossary mapping technical column names to business terminology enabling analysts to navigate data independently.

- **Knowledge Transfer Sessions**: Conduct formal knowledge transfer sessions with support team covering platform architecture, operational procedures, troubleshooting approaches, and incident response procedures.
  Document attendance and competency assessment ensuring support team has adequate expertise before handover.

- **Lessons Learned**: Document lessons learned during deployment including decisions made, trade-offs accepted, unexpected challenges encountered, and recommendations for future implementations.
  Include suggestions for improvements (architectural changes, tool replacements, process enhancements) based on operational experience accumulated during project lifecycle.

## Detailed Project Flow & 20-Activity Pipeline (Supply Chain)

This supply-chain-specific pipeline is a metadata-driven ADF master/child pattern with 20 activities designed to run reliably at scale. Implement the master pipeline to read `mtd_source_systems` and spawn a generic child pipeline (parameterized) that executes the steps below.

| Step | Activity Name | Activity Type | Purpose | Input | Output |
|---:|---|---|---|---|---|
| 1 | Read_Metadata | Lookup | Read ingestion config for supply chain source | `mtd_source_systems` | metadata row |
| 2 | Acquire_Lock | StoredProc | Prevent concurrent runs for same source | metadata | lock token |
| 3 | Check_Connection | WebActivity | Test endpoint & credentials | metadata | pass/fail |
| 4 | Enumerate_Files | Script | Build manifest of files/partitions to ingest | source listing | manifest.json |
| 5 | Copy_To_Staging | Copy Activity | Stage raw data to `/landing/{source}/` | source object | landing files |
| 6 | Integrity_Validation | Databricks Job | Verify checksum/row-count/header | landing files | integrity report |
| 7 | PreBronze_Validation | MappingDataFlow | Filename, header, sample checks; quarantine if fail | landing | pre-bronze / quarantine |
| 8 | Write_Bronze | Databricks Job | Minimal normalization & write to Bronze delta | pre-bronze | /bronze/{entity}/ |
| 9 | Bronze_Audit | StoredProc | Insert bronze load metrics into `audit_log` | metrics | audit row |
|10 | Schema_Drift | AzureFunction | Detect schema changes and flag stewardship flow | bronze schema | drift_flag |
|11 | Silver_Cleansing | Databricks Notebook | Enrich, dedupe, normalize for business logic | bronze | silver staging |
|12 | Data_Quality | DataQuality Job | Run DQ suites; create `dq_report` rows | silver staging | dq_report |
|13 | Business_Transforms | Databricks Job | Compute lead time, KPIs, supplier scores | silver staging | silver delta |
|14 | Merge_Dimensions | MERGE | SCD Type 2 for supplier/product dims | silver delta | dim tables |
|15 | Merge_Facts | MERGE | Upsert into purchase_orders fact | silver delta | fact tables |
|16 | Gold_Aggregation | Databricks Job | Build marts (scorecards, inventory) | fact/dim | gold tables |
|17 | Optimize_Gold | Databricks Job | OPTIMIZE, ZORDER and VACUUM for gold | gold tables | optimized gold |
|18 | Publish_Semantics | Synapse Script | Create/update semantic views for BI | gold tables | views |
|19 | PostRun_Audit | StoredProc | Update `audit_log` end status, metrics | run metrics | audit updated |
|20 | Archive_And_Cleanup | Function | Move landing files to archive and VACUUM deltas | landing/deltas | archive |

Control tables (recommended):

- `mtd_source_systems` (source_id, system_name, source_type, linked_service, path_or_query, frequency_minutes, watermark_col, owner)
- `metadata_control` (ingestion_id, source_id, load_type, schedule, priority, last_run_ts, status)
- `audit_log` (run_id, pipeline_name, source_id, start_ts, end_ts, status, records_in, records_out, error_msg)
- `dq_report` (report_id, run_id, check_name, status, rows_checked, rows_failed, details)

Operational notes:

- Idempotency: use `run_id` & deterministic paths; MERGE for upserts.
- On DQ failures move bad files into `/quarantine/{source}/{run_id}/` and send an automatic ticket to data steward.
- Update watermark in `metadata_control` only after successful `PostRun_Audit`.

