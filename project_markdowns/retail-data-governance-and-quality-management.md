# Retail Data Governance & Quality Management

Brief: Ongoing management and operationalization of retail data governance.

- Objectives:
  - Operationalize governance, monitoring, and remediation.
- Scope:
  - Workflows for data issues, ownership, and remediation.
- Key Components:
  - Issue tracking, dashboards, automated checks.
- Technologies:
  - Data catalogs, quality tooling, ticketing systems.
- Deliverables:
  - Governance playbook, escalation flows, KPI dashboards.

## Expanded Source Schemas, ER Diagrams, Facts & Dimensions

This standard expansion provides five logical sources for retail data governance, each with 20 tables, ER diagrams, fact/dimension descriptions, reconciliation patterns, and a rights statement that these diagrams are original design artifacts.

Project prefix: `rdgq_` (Retail Data Governance & Quality)

### Source A: Channel Ingest (rdgq_channel)

Tables (20):
1. rdgq_stg_channel_events
2. rdgq_raw_channel_events
3. rdgq_dim_channel
4. rdgq_dim_source
5. rdgq_dim_format
6. rdgq_ref_schema
7. rdgq_fact_channel_events
8. rdgq_stage_enrichments
9. rdgq_dim_geo
10. rdgq_dim_store
11. rdgq_audit_ingest
12. rdgq_ref_event_map
13. rdgq_stage_dedup
14. rdgq_dim_event_type
15. rdgq_ref_error_codes
16. rdgq_fact_event_counts
17. rdgq_audit_recon
18. rdgq_stage_corrections
19. rdgq_ref_retention
20. rdgq_dim_status

ER Diagram (ASCII):

rdgq_fact_channel_events (event_id, channel_id, store_id, customer_id, event_ts)
  |-- channel_id --> rdgq_dim_channel(channel_id)
  |-- store_id --> rdgq_dim_store(store_id)

Rights Statement: I assert the right to author and publish these diagrams and schemas as original design artifacts for platform design and implementation.

---

### Source B: Catalog & Metadata (rdgq_catalog)

Tables (20):
1. rdgq_stg_catalog
2. rdgq_raw_catalog
3. rdgq_dim_dataset
4. rdgq_dim_owner
5. rdgq_dim_tag
6. rdgq_ref_policies
7. rdgq_fact_data_quality
8. rdgq_stage_lineage
9. rdgq_dim_classification
10. rdgq_dim_sensitivity
11. rdgq_audit_policies
12. rdgq_ref_sla
13. rdgq_stage_certifications
14. rdgq_fact_issues
15. rdgq_dim_remediation_team
16. rdgq_ref_controls
17. rdgq_audit_certification
18. rdgq_stage_policy_changes
19. rdgq_ref_standards
20. rdgq_dim_status

ER Diagram (ASCII):

rdgq_fact_data_quality (dq_id, dataset_id, check_name, status, checked_ts)
  |-- dataset_id --> rdgq_dim_dataset(dataset_id)

---

### Source C: Quality Checks & Alerts (rdgq_quality)

Tables (20):
1. rdgq_stg_checks
2. rdgq_raw_checks
3. rdgq_dim_check_type
4. rdgq_dim_dataset
5. rdgq_dim_rule_owner
6. rdgq_ref_thresholds
7. rdgq_fact_check_runs
8. rdgq_stage_alerts
9. rdgq_dim_priority
10. rdgq_dim_channel
11. rdgq_audit_check_ingest
12. rdgq_ref_remediation_steps
13. rdgq_stage_issues
14. rdgq_fact_issue_metrics
15. rdgq_dim_team
16. rdgq_ref_automations
17. rdgq_audit_issues
18. rdgq_stage_corrections
19. rdgq_ref_owner_contacts
20. rdgq_dim_status

---

### Source D: Remediation & Workflows (rdgq_workflow)

Tables (20):
1. rdgq_stg_workflows
2. rdgq_raw_tasks
3. rdgq_dim_workflow_type
4. rdgq_dim_assignee
5. rdgq_dim_priority
6. rdgq_ref_playbooks
7. rdgq_fact_task_metrics
8. rdgq_stage_attachments
9. rdgq_dim_sla
10. rdgq_dim_status
11. rdgq_audit_task_events
12. rdgq_ref_escalation_paths
13. rdgq_stage_comments
14. rdgq_fact_resolution_times
15. rdgq_dim_team
16. rdgq_ref_templates
17. rdgq_audit_workflow_changes
18. rdgq_stage_retries
19. rdgq_ref_automation_rules
20. rdgq_dim_channel

---

### Source E: Reporting & Compliance (rdgq_reporting)

Tables (20):
1. rdgq_stg_reports
2. rdgq_raw_reports
3. rdgq_dim_report_type
4. rdgq_dim_consumer
5. rdgq_dim_dataset
6. rdgq_ref_report_templates
7. rdgq_fact_report_consumption
8. rdgq_stage_exports
9. rdgq_dim_frequency
10. rdgq_dim_region
11. rdgq_audit_report_runs
12. rdgq_ref_compliance_rules
13. rdgq_stage_retention
14. rdgq_fact_compliance_checks
15. rdgq_dim_owner
16. rdgq_ref_signoffs
17. rdgq_audit_signoffs
18. rdgq_stage_distribution
19. rdgq_ref_formats
20. rdgq_dim_status

## Common Patterns
- Use staging (immutable) → raw normalization → enrichment → canonical facts/dimensions → audit & reconciliation.
- Implement SCD2 for slowly-changing dimensions where history is required.
- Use `audit_*` and checksums for reconciliations.

## Detailed ER Diagram

# Detailed ER Diagram: Entities, Attributes, Relationships, Cardinalities

This detailed ER diagram template expands the ASCII ER stub into full entity descriptions, attribute lists, primary/foreign key definitions, and explicit relationships with cardinalities for the project prefix `retail_data_governance_and_quality_management` (source file `retail-data-governance-and-quality-management.md`).

The template covers a canonical canonical set of logical entities used across projects: Source/Stage/Raw, Dimension entities, Fact entities, Reference / Lookup tables, and Audit & Reconciliation tables.

---

**Entity: `retail_data_governance_and_quality_management_raw_records`**
- Purpose: Immutable raw ingest payload store (one row per source record).
- PK: `record_key`
- Key attributes: `record_key (PK)`, `source_system`, `raw_payload` (JSON), `ingest_ts`, `ingest_batch_id`, `payload_hash`.

**Entity: `retail_data_governance_and_quality_management_stg_<topic>`** (generic staging)
- Purpose: Parsed staging of a raw record specific to a topic (e.g. transactions, events).
- PK: `stg_id`
- Key attributes: `stg_id (PK)`, `record_key (FK -> retail_data_governance_and_quality_management_raw_records.record_key)`, `parsed_fields...`, `ingest_ts`, `batch_id`, `load_status`.

**Entity: `retail_data_governance_and_quality_management_dim_account`**
- Purpose: Account dimension used by transaction facts.
- PK: `account_id`
- Attributes: `account_id (PK)`, `customer_id`, `account_type`, `currency_code`, `open_date`, `close_date`, `status`, `valid_from`, `valid_to`.

**Entity: `retail_data_governance_and_quality_management_dim_customer`**
- Purpose: Customer master attributes and identity.
- PK: `customer_id`
- Attributes: `customer_id (PK)`, `first_name`, `last_name`, `email_hash`, `birth_date`, `kyc_level`, `country`, `risk_score`, `valid_from`, `valid_to`.

**Entity: `retail_data_governance_and_quality_management_dim_time`**
- Purpose: Standard time dimension for reporting.
- PK: `date_key`
- Attributes: `date_key (PK)`, `date`, `year`, `quarter`, `month`, `day`, `weekday`, `is_business_day`.

**Entity: `retail_data_governance_and_quality_management_dim_product`**
- Purpose: Product/SKU master for retail-like facts.
- PK: `product_id`
- Attributes: `product_id (PK)`, `sku`, `name`, `category`, `brand`, `size`, `color`, `status`, `valid_from`, `valid_to`.

**Entity: `retail_data_governance_and_quality_management_fact_transactions`**
- Purpose: Canonical transaction-level fact (grain: one event/transaction).
- PK: `transaction_id`
- Attributes: `transaction_id (PK)`, `source_event_id`, `account_id (FK)`, `customer_id (FK)`, `product_id (FK)`, `amount`, `currency_code`, `amount_usd`, `txn_type`, `channel_code`, `merchant_id`, `status`, `posted_ts`, `processed_ts`, `ingest_batch_id`, `checksum`.

---

Relationships and cardinalities (explicit):
- `retail_data_governance_and_quality_management_fact_transactions.account_id` (M:1) -> `retail_data_governance_and_quality_management_dim_account.account_id`
  - Cardinality: Many transactions map to one account.
- `retail_data_governance_and_quality_management_fact_transactions.customer_id` (M:1) -> `retail_data_governance_and_quality_management_dim_customer.customer_id`
  - Many transactions per customer; some transactions inferred to customer through account linkage.
- `retail_data_governance_and_quality_management_fact_transactions.product_id` (M:1) -> `retail_data_governance_and_quality_management_dim_product.product_id`
  - Many fact rows reference a single product row.
- `retail_data_governance_and_quality_management_fact_transactions.posted_ts` (M:1) -> `retail_data_governance_and_quality_management_dim_time.date_key` (via date_key derived from posted_ts)
  - Many transactions map to one date in the time dimension.
- `retail_data_governance_and_quality_management_stg_<topic>.record_key` (M:1) -> `retail_data_governance_and_quality_management_raw_records.record_key`
  - One staging row per raw record, after parsing.

Association tables / many-to-many patterns:
- If customers belong to segments or tags, model as `retail_data_governance_and_quality_management_rel_customer_segment(customer_id FK, segment_id FK, assigned_ts)` with PK composite (`customer_id`, `segment_id`).

Detailed ER rules & integrity constraints:
- Use FK constraints where possible in the curated warehouse (e.g., `FOREIGN KEY (account_id) REFERENCES retail_data_governance_and_quality_management_dim_account(account_id)`).
- Enforce uniqueness on natural keys (e.g., `transaction_id`, `account_id + source_event_id` as alternate key) and use checksums for content verification.
- Implement SCD2 pattern for dimensions needing history using `valid_from` and `valid_to` and a surrogate `dim_pk`.

Sample SQL DDL snippets (representative):

CREATE TABLE retail_data_governance_and_quality_management_dim_customer (
  customer_id STRING PRIMARY KEY,
  first_name STRING,
  last_name STRING,
  email_hash STRING,
  kyc_level STRING,
  risk_score DOUBLE,
  valid_from DATE,
  valid_to DATE
);

CREATE TABLE retail_data_governance_and_quality_management_fact_transactions (
  transaction_id STRING PRIMARY KEY,
  source_event_id STRING,
  account_id STRING,
  customer_id STRING,
  product_id STRING,
  amount DECIMAL(18,2),
  currency_code STRING,
  posted_ts TIMESTAMP,
  ingest_batch_id STRING,
  checksum STRING,
  FOREIGN KEY (account_id) REFERENCES retail_data_governance_and_quality_management_dim_account(account_id),
  FOREIGN KEY (customer_id) REFERENCES retail_data_governance_and_quality_management_dim_customer(customer_id)
);

ER Diagram (visual guidance):
- Center the `retail_data_governance_and_quality_management_fact_transactions` as the hub with outward links to `dim_account`, `dim_customer`, `dim_product`, and `dim_time`.
- Secondary facts (e.g., `retail_data_governance_and_quality_management_fact_settlements`) link back to `fact_transactions` via `transaction_id` where the settlement is child of a transaction (1:M relationship).

---

Per-project extension guidance:
- For banking projects, expand `dim_account` and `dim_customer` with regulatory attributes (aml_flags, kyc_date, tax_id_hash).
- For retail projects, extend `dim_product` with merchandising attributes and `dim_store` to represent brick-and-mortar locations.
- For IoT/telemetry projects, add time-series entity `retail_data_governance_and_quality_management_ts_measurements(device_id, measure_ts, metric, value)` with retention and rollup rules described.

This template is intended to be expanded with project-specific entities. The automation script will replace `retail_data_governance_and_quality_management` and `retail-data-governance-and-quality-management.md` and append the section to each markdown file that does not already contain a `## Detailed ER Diagram` marker.



# Complete Flow Diagram & Medallion Architecture with ADF, ADB, and PySpark

This section provides a comprehensive, production-grade Medallion architecture (Bronze → Silver → Gold) for the project `retail_data_governance_and_quality_management`, including:
- Complete end-to-end flow diagrams
- Azure Data Factory (ADF) orchestration blueprint
- Azure Databricks (ADB) + PySpark transformations
- Bronze layer with 20 validation rules
- Silver layer with 20 transformation scenarios
- Gold layer with 20 business validations
- Sample code for each layer

---

## Complete Flow Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SOURCE SYSTEMS (5 sources)                       │
│  Source_A │ Source_B │ Source_C │ Source_D │ Source_E                  │
└────────┬──────┬──────────┬──────────┬──────────┬───────────────────────┘
         │      │          │          │          │
         └──────┴────┬─────┴──────────┴───────┬──┘
                     │ (Files, APIs, Streams)│
                     ▼                        │
        ┌────────────────────────────────────┴──────────┐
        │   Azure Data Factory (ADF)                   │
        │   - Copy Activity for each source            │
        │   - Error handling & retry logic             │
        │   - Checksum validation per batch            │
        │   - Logging to audit tables                  │
        └────────────────────┬───────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
   ┌──────────────────────┐    ┌─────────────────────┐
   │  BRONZE Layer (Raw)  │    │ Audit & Quality Log │
   │  - retail_data_governance_and_quality_management_bro_*  │    │   (Staging area)    │
   │  - Immutable raw     │    └─────────────────────┘
   │  - 20 Validations    │
   │  - Checksums & hash  │
   └──────────┬───────────┘
              │
              │ (ADB Spark Job)
              ▼
   ┌──────────────────────────────┐
   │  SILVER Layer (Curated)      │
   │  - retail_data_governance_and_quality_management_sil_*          │
   │  - 20 Transformation Scenarios
   │  - Dedup, enrich, join       │
   │  - SCD handling, late arriv.  │
   │  - Aggregations              │
   └──────────┬────────────────────┘
              │
              │ (ADF Lookup + Spark)
              ▼
   ┌──────────────────────────────┐
   │  GOLD Layer (Analytics)      │
   │  - retail_data_governance_and_quality_management_gld_*          │
   │  - 20 Business Validations   │
   │  - Dimensions & Facts        │
   │  - KPI computations          │
   │  - Business logic enforcement│
   └──────────┬────────────────────┘
              │
              ├─────────────────────────────┐
              │                             │
              ▼                             ▼
      ┌──────────────┐           ┌──────────────────┐
      │  BI Reports  │           │  Real-time APIs  │
      │  Dashboards  │           │  Serving Layer   │
      │  Queries     │           │  Feature Store   │
      └──────────────┘           └──────────────────┘
```

---

## Azure Data Factory (ADF) Orchestration Blueprint

### Pipeline: `retail_data_governance_and_quality_management_Master_Orchestration`

**Trigger:** On-schedule (daily 2 AM UTC) + manual trigger

**Parameters:**
- `pipeline_run_id` (UUID)
- `execution_date` (YYYY-MM-DD)
- `source_filter` (optional: comma-separated source names)

**Activities:**

1. **Activity: Lookup_ExecutionParams**
   - Query `retail_data_governance_and_quality_management_audit_ingest` for last successful run
   - Set variables: `last_run_ts`, `expected_record_count`, `batch_id`

2. **Activity: Copy_Source_A** (For each source in parallel)
   - Source: API endpoint / file share / database
   - Sink: `retail_data_governance_and_quality_management_bro_source_a_raw` (ADLS gen2)
   - Format: Parquet (snappy compression)
   - Error handling: Retry 3x, then store error metadata
   - Post-copy: Execute "Validate_Bronze_A"

3. **Activity: Validate_Bronze_A**
   - Stored procedure call to `sp_validate_bronze_retail_data_governance_and_quality_management_a(batch_id)`
   - Returns validation result set
   - If failures: Log to `retail_data_governance_and_quality_management_audit_validation_failures`, alert, optionally fail pipeline

4. **Activity: Trigger_Spark_Silver_Job**
   - Type: Databricks Notebook Activity
   - Notebook path: `/Workspace/retail_data_governance_and_quality_management/silver_transform`
   - Parameters: `batch_id`, `execution_date`
   - Cluster: `retail_data_governance_and_quality_management-shared-compute` (auto-scale 2-8 nodes)

5. **Activity: Trigger_Spark_Gold_Job**
   - Notebook path: `/Workspace/retail_data_governance_and_quality_management/gold_aggregate`
   - Depends on: Trigger_Spark_Silver_Job success
   - Parameters: `batch_id`

6. **Activity: Post_Load_Validations**
   - Execute SQL script validating row counts, nulls, business rules
   - Store results in `retail_data_governance_and_quality_management_gold_validation_log`

7. **Activity: Send_Notification**
   - If all succeed: Send success email with row count summary
   - If fail: Send alert with error details

---

## Bronze Layer: Raw Ingest (20 Validations)

**Purpose:** Immutable, auditable raw data storage with comprehensive validation.

**Table Schema Example:** `retail_data_governance_and_quality_management_bro_source_a_raw`

```sql
CREATE TABLE retail_data_governance_and_quality_management_bro_source_a_raw (
  record_id STRING COMMENT 'Unique record ID',
  source_batch_id STRING COMMENT 'Batch ID from ADF',
  source_system_code STRING COMMENT 'Source system identifier',
  raw_payload STRING COMMENT 'Original JSON/CSV payload',
  payload_hash STRING COMMENT 'SHA-256 hash for dedup',
  record_size_bytes BIGINT COMMENT 'Payload size',
  ingested_ts TIMESTAMP COMMENT 'UTC ingest timestamp',
  file_name STRING COMMENT 'Source file/API name',
  line_number INT COMMENT 'Line within file (for CSV)',
  load_date DATE COMMENT 'Partition key YYYY-MM-DD',
  load_hour INT COMMENT 'Partition key HH (0-23)',
  _etl_load_ts TIMESTAMP COMMENT 'ETL load time',
  _checksum_md5 STRING COMMENT 'Row-level checksum'
)
USING PARQUET
PARTITIONED BY (load_date, load_hour);
```

**20 Bronze-Layer Validations:**

1. **V_BRO_001**: Payload not null
2. **V_BRO_002**: record_id format matches pattern `^[A-Z0-9]{12}$`
3. **V_BRO_003**: source_system_code in whitelist ('SRC_A', 'SRC_B', ...)
4. **V_BRO_004**: payload_hash is valid SHA-256 (64 hex chars)
5. **V_BRO_005**: ingested_ts within last 48 hours
6. **V_BRO_006**: file_name not empty and contains expected date pattern
7. **V_BRO_007**: line_number > 0 (if applicable)
8. **V_BRO_008**: record_size_bytes between 10 and 1MB
9. **V_BRO_009**: No duplicate record_id + source_batch_id combination within batch
10. **V_BRO_010**: load_date matches ingested_ts date (within same day)
11. **V_BRO_011**: load_hour matches ingested_ts hour
12. **V_BRO_012**: Payload is valid JSON (if format is JSON)
13. **V_BRO_013**: Encoding is UTF-8 (check for invalid chars)
14. **V_BRO_014**: No leading/trailing whitespace on record_id
15. **V_BRO_015**: source_batch_id follows format `BATCH_{{YYYYMMDD}}_{{HHMMSS}}_{{COUNTER}}`
16. **V_BRO_016**: Record count per source_batch_id within expected bounds (min 100, max 10M)
17. **V_BRO_017**: No records with future dates (ingested_ts <= now())
18. **V_BRO_018**: _checksum_md5 is exactly 32 hex chars
19. **V_BRO_019**: Batch ingestion time (max_ts - min_ts) < 1 hour
20. **V_BRO_020**: All columns present and in expected order (schema validation)

**PySpark Code Snippet (Bronze Validation):**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("retail_data_governance_and_quality_management_bronze_validate").getOrCreate()

# Load Bronze raw data
bro_df = spark.read.parquet(f"/mnt/adls/bronze/retail_data_governance_and_quality_management_bro_source_a_raw/load_date={exec_date}")

# V_BRO_001: Payload not null
v001 = bro_df.filter(col("raw_payload").isNull()).count()

# V_BRO_002: record_id format
from pyspark.sql.types import *
import re
v002 = bro_df.filter(~col("record_id").rlike("^[A-Z0-9]{12}$")).count()

# V_BRO_006: file_name contains date pattern
v006 = bro_df.filter(~col("file_name").rlike(r"\d{8}")).count()

# V_BRO_009: No duplicates (record_id + source_batch_id)
v009_dup = bro_df.groupBy("record_id", "source_batch_id").count().filter(col("count") > 1).count()

# Collect all validation results
validations = {
    "V_BRO_001": v001,
    "V_BRO_002": v002,
    "V_BRO_006": v006,
    "V_BRO_009": v009_dup,
    # ... (add remaining 16 validations)
}

# Log results
for val_id, fail_count in validations.items():
    print(f"{val_id}: {fail_count} failures")
    if fail_count > 0:
        # Log to validation table
        spark.sql(f"""
        INSERT INTO retail_data_governance_and_quality_management_audit_validation_results (validation_id, layer, fail_count, check_ts)
        VALUES ('{val_id}', 'BRONZE', {fail_count}, current_timestamp())
        """)

print("Bronze validations complete")
```

---

## Silver Layer: Curated & Transformed (20 Transformation Scenarios)

**Purpose:** Cleansed, enriched, deduplicated, and integrated data ready for analytics.

**Table Example:** `retail_data_governance_and_quality_management_sil_transactions_curated`

```sql
CREATE TABLE retail_data_governance_and_quality_management_sil_transactions_curated (
  transaction_key STRING COMMENT 'Surrogate key (hash of source keys)',
  source_event_id STRING COMMENT 'Original source event ID',
  transaction_id STRING COMMENT 'Deduplicated transaction ID',
  account_id STRING COMMENT 'Linked account dimension key',
  customer_id STRING COMMENT 'Linked customer dimension key',
  transaction_amount DECIMAL(18,4) COMMENT 'Normalized amount',
  transaction_currency STRING COMMENT 'Currency code',
  transaction_ts TIMESTAMP COMMENT 'Event timestamp (normalized)',
  transaction_type STRING COMMENT 'Enumerated txn type',
  data_quality_score DOUBLE COMMENT 'DQ score 0-1',
  source_system_code STRING COMMENT 'Originating system',
  is_duplicate BOOLEAN COMMENT 'True if record is duplicate (SCD Type 2)',
  is_late_arriving BOOLEAN COMMENT 'True if arrived > 24h late',
  scd2_valid_from TIMESTAMP COMMENT 'SCD2 effective date',
  scd2_valid_to TIMESTAMP COMMENT 'SCD2 expiration (null = current)',
  scd2_is_current BOOLEAN COMMENT 'SCD2 current flag',
  _processed_ts TIMESTAMP COMMENT 'When record was transformed',
  _layer_version STRING COMMENT 'Transformation version'
)
USING DELTA;
```

**20 Silver-Layer Transformation Scenarios:**

1. **S_SIL_001**: Basic data type conversions (string → int, float, date)
2. **S_SIL_002**: Null handling strategy (default values, imputation, or filter)
3. **S_SIL_003**: Deduplication by source_event_id (keep latest by ingested_ts)
4. **S_SIL_004**: Datetime normalization (convert all to UTC, handle timezones)
5. **S_SIL_005**: Currency normalization (convert to base currency using daily FX rates)
6. **S_SIL_006**: Account lookup and enrichment (join with account dimension)
7. **S_SIL_007**: Customer lookup and enrichment (join with customer dimension)
8. **S_SIL_008**: Categorization mapping (txn_type enum mapping, merchant category)
9. **S_SIL_009**: Late-arriving record detection (arrival lag > 24 hours → flag)
10. **S_SIL_010**: Data quality scoring (composite score based on null%, outliers)
11. **S_SIL_011**: Slowly Changing Dimension (SCD) Type 2 handling (versioning)
12. **S_SIL_012**: Cross-source record matching (deduplicate across sources)
13. **S_SIL_013**: Amount validation and outlier detection (flag amounts > 3 sigma)
14. **S_SIL_014**: Address standardization (normalize, validate zip codes)
15. **S_SIL_015**: Phone/email normalization (format, validate)
16. **S_SIL_016**: PII anonymization/hashing (mask sensitive fields per policy)
17. **S_SIL_017**: Hierarchical attribute flattening (nested JSON → flat columns)
18. **S_SIL_018**: Period-over-period comparison precomp (YoY, MoM flags)
19. **S_SIL_019**: Seasonal and trend signal addition (day-of-week, holidays)
20. **S_SIL_020**: Incremental load flag (first occurrence, update, new customer)

**PySpark Code Snippet (Silver Transform):**

```python
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import *
from datetime import datetime, timedelta

spark = SparkSession.builder.appName("retail_data_governance_and_quality_management_silver_transform").getOrCreate()

# Load Bronze data
bro_df = spark.read.parquet(f"/mnt/adls/bronze/retail_data_governance_and_quality_management_bro_source_a_raw/load_date={exec_date}")

# S_SIL_001: Type conversions
sil_df = bro_df.select(
    col("record_id").cast("string").alias("transaction_key"),
    col("source_event_id").cast("string"),
    col("transaction_id").cast("string"),
    col("amount").cast("decimal(18,4)").alias("transaction_amount"),
    from_unixtime(col("event_ts"), "yyyy-MM-dd HH:mm:ss").cast("timestamp").alias("transaction_ts")
)

# S_SIL_002: Null handling
sil_df = sil_df.fillna({
    "transaction_amount": 0.0,
    "transaction_type": "UNKNOWN"
})

# S_SIL_003: Deduplication
w = Window.partitionBy("source_event_id").orderBy(desc("ingested_ts"))
sil_df = sil_df.withColumn("rn", row_number().over(w)).filter(col("rn") == 1).drop("rn")

# S_SIL_004: UTC normalization
sil_df = sil_df.withColumn("transaction_ts", to_utc_timestamp(col("transaction_ts"), "US/Eastern"))

# S_SIL_006: Account enrichment
acct_df = spark.read.table("retail_data_governance_and_quality_management_dim_account")
sil_df = sil_df.join(acct_df, on="account_id", how="left")

# S_SIL_009: Late-arriving detection
threshold_ts = (datetime.now() - timedelta(days=1))
sil_df = sil_df.withColumn("is_late_arriving", 
    col("ingested_ts") < to_timestamp(lit(threshold_ts.isoformat())))

# S_SIL_010: Data quality scoring
null_cols = ["customer_id", "transaction_amount", "transaction_ts"]
sil_df = sil_df.withColumn("null_count", 
    sum([when(col(c).isNull(), 1).otherwise(0) for c in null_cols]))
sil_df = sil_df.withColumn("data_quality_score", 
    (len(null_cols) - col("null_count")) / len(null_cols))

# S_SIL_011: SCD2 versioning
sil_df = sil_df.withColumn("scd2_valid_from", current_timestamp())
sil_df = sil_df.withColumn("scd2_valid_to", lit(None).cast("timestamp"))
sil_df = sil_df.withColumn("scd2_is_current", lit(True))

# Write to Silver
sil_df.write.format("delta").mode("append").option("mergeSchema", "true") \
    .partitionBy("load_date").save(f"/mnt/adls/silver/retail_data_governance_and_quality_management_sil_transactions_curated")

print("Silver transformation complete")
```

---

## Gold Layer: Analytics & Aggregations (20 Business Validations)

**Purpose:** Business-ready facts and dimensions for reporting and analytics.

**Table Example:** `retail_data_governance_and_quality_management_gld_fact_transactions`

```sql
CREATE TABLE retail_data_governance_and_quality_management_gld_fact_transactions (
  transaction_id STRING PRIMARY KEY,
  account_key STRING,
  customer_key STRING,
  date_key INT COMMENT 'FK to dim_date',
  time_key INT COMMENT 'FK to dim_time',
  product_key STRING COMMENT 'FK to dim_product',
  merchant_key STRING COMMENT 'FK to dim_merchant',
  transaction_amount DECIMAL(18,4),
  transaction_currency STRING,
  transaction_type_code STRING,
  channel_code STRING,
  is_return BOOLEAN,
  is_reversal BOOLEAN,
  is_fraud_suspected BOOLEAN,
  data_quality_flag INT COMMENT '0=pass, 1=warn, 2=fail',
  business_unit_code STRING,
  country_code STRING,
  created_ts TIMESTAMP,
  updated_ts TIMESTAMP
)
USING DELTA;
```

**20 Gold-Layer Business Validations:**

1. **V_GLD_001**: transaction_id is unique and non-null
2. **V_GLD_002**: All FK references (account_key, customer_key, product_key) exist in dimensions
3. **V_GLD_003**: transaction_amount > 0 or is valid negative (return/reversal)
4. **V_GLD_004**: transaction_currency in whitelist of valid codes
5. **V_GLD_005**: date_key matches transaction date (no date mismatches)
6. **V_GLD_006**: time_key within valid range (0-2359 for HHMM)
7. **V_GLD_007**: transaction_type_code in business-defined enum list
8. **V_GLD_008**: channel_code valid and non-null
9. **V_GLD_009**: is_return and is_reversal are mutually exclusive (XOR logic)
10. **V_GLD_010**: Fraud flag consistency (if is_fraud_suspected, data_quality_flag >= 1)
11. **V_GLD_011**: Sum of transactions by date equals Gold layer aggregate
12. **V_GLD_012**: No gaps in date_key sequence (no missing dates in fact table)
13. **V_GLD_013**: data_quality_flag in [0, 1, 2] only
14. **V_GLD_014**: business_unit_code matches account dimension
15. **V_GLD_015**: country_code matches customer dimension or business rules
16. **V_GLD_016**: created_ts and updated_ts in logical order (created <= updated)
17. **V_GLD_017**: Row counts per business_unit within expected range (no mass deletes/inserts)
18. **V_GLD_018**: created_ts and updated_ts within last 90 days (no ancient records)
19. **V_GLD_019**: No NULL values in mandatory columns: [transaction_id, account_key, transaction_amount]
20. **V_GLD_020**: Daily row count variance < 30% from 30-day rolling average

**PySpark Code Snippet (Gold Aggregation & Validation):**

```python
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("retail_data_governance_and_quality_management_gold_aggregate").getOrCreate()

# Load Silver data
sil_df = spark.read.table("retail_data_governance_and_quality_management_sil_transactions_curated")

# Build Gold fact table
gld_df = sil_df.select(
    col("transaction_id"),
    col("account_id").alias("account_key"),
    col("customer_id").alias("customer_key"),
    date_format(col("transaction_ts"), "yyyyMMdd").cast("int").alias("date_key"),
    date_format(col("transaction_ts"), "HHmm").cast("int").alias("time_key"),
    col("product_id").alias("product_key"),
    col("merchant_id").alias("merchant_key"),
    col("transaction_amount"),
    col("transaction_currency"),
    col("transaction_type").alias("transaction_type_code"),
    col("channel_code"),
    col("is_return").cast("boolean"),
    col("is_reversal").cast("boolean"),
    col("is_fraud_suspected").cast("boolean"),
    col("data_quality_score").cast("int").alias("data_quality_flag"),
    col("business_unit_code"),
    col("country_code"),
    current_timestamp().alias("created_ts"),
    current_timestamp().alias("updated_ts")
)

# V_GLD_001: Uniqueness
v001_dupes = gld_df.groupBy("transaction_id").count().filter(col("count") > 1).count()

# V_GLD_002: FK validation
acct_df = spark.read.table("retail_data_governance_and_quality_management_dim_account").select("account_key")
v002_missing = gld_df.join(acct_df, on="account_key", how="left_anti").count()

# V_GLD_003: Amount validation
v003_invalid = gld_df.filter((col("transaction_amount") <= 0) & ~col("is_reversal")).count()

# V_GLD_009: XOR logic (return and reversal mutually exclusive)
v009_invalid = gld_df.filter((col("is_return") == True) & (col("is_reversal") == True)).count()

# V_GLD_019: No NULLs in mandatory columns
v019_nulls = gld_df.filter(col("transaction_id").isNull() | 
                            col("account_key").isNull() | 
                            col("transaction_amount").isNull()).count()

# V_GLD_020: Daily row count variance
daily_counts = gld_df.groupBy("date_key").count().collect()
counts_list = [row["count"] for row in daily_counts]
avg_count = sum(counts_list) / len(counts_list) if counts_list else 0
variance_pct = (max(counts_list) - min(counts_list)) / avg_count * 100 if avg_count > 0 else 0
v020_flag = 1 if variance_pct > 30 else 0

# Collect validation results
validation_results = {
    "V_GLD_001_dupes": v001_dupes,
    "V_GLD_002_missing_fks": v002_missing,
    "V_GLD_003_invalid_amounts": v003_invalid,
    "V_GLD_009_xor_violations": v009_invalid,
    "V_GLD_019_nulls": v019_nulls,
    "V_GLD_020_variance_flag": v020_flag,
}

for val_id, count in validation_results.items():
    spark.sql(f"""
    INSERT INTO retail_data_governance_and_quality_management_gold_validation_log (validation_id, layer, fail_count, check_ts)
    VALUES ('{val_id}', 'GOLD', {count}, current_timestamp())
    """)

# Write fact table
gld_df.write.format("delta").mode("append").option("mergeSchema", "true") \
    .partitionBy("date_key").save(f"/mnt/adls/gold/retail_data_governance_and_quality_management_gld_fact_transactions")

print("Gold aggregation and validation complete")
```

---

## Architecture Decision Records (ADR)

**ADR-001: Why Medallion Architecture?**
- Separation of concerns: raw (Bronze) → curated (Silver) → analytics (Gold).
- Incremental transformation enables re-processing and auditing.
- Each layer has clear quality gates and SLAs.

**ADR-002: Why Parquet + Delta Lake?**
- Parquet: columnar format, compression, partitioning for fast queries.
- Delta Lake: ACID transactions, schema evolution, time travel, CDC support.

**ADR-003: Why Azure Data Factory + Databricks?**
- ADF: Enterprise orchestration, monitoring, error handling.
- Databricks: Collaborative notebooks, Unity Catalog (governance), MLOps integration.

**ADR-004: Why 20 Validations per Layer?**
- Comprehensive coverage: Format, domain, referential, statistical checks.
- Enables automated data quality monitoring and SLA reporting.

---

## Operational Monitoring & Alerting

**Metrics to track:**
- Bronze ingest latency (target: < 5 min from source)
- Silver transformation time (target: < 15 min)
- Gold aggregation time (target: < 10 min)
- Validation failure rate (target: < 0.1%)
- End-to-end pipeline SLA (target: complete by 6 AM UTC)

**Alert thresholds:**
- If any validation fails: Page on-call engineer
- If pipeline > 2× historical median runtime: Page
- If > 1000 late-arriving records per day: Investigate source

---

## Rights & Implementation Notes

I confirm these architecture diagrams, flow specifications, PySpark code samples, and validation frameworks are original designs created for this engagement and may be used for internal implementation documentation and deployment.

To implement:
1. Deploy ADF pipelines using ARM templates or Terraform.
2. Create Databricks clusters and import notebooks from repo.
3. Run validation suites hourly post-load.
4. Register datasets in Unity Catalog / Purview for governance.
5. Set up Power BI / Looker dashboards for monitoring.

