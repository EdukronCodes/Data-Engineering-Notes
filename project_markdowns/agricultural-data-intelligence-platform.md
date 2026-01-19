# Agricultural Data Intelligence Platform

Brief: Platform for analytics in agriculture — yields, weather, supply chain.

- Objectives:
  - Provide insights to improve yield, forecasting, and logistics.
- Scope:
  - Sensor data, satellite imagery, market data.
- Key Components:
  - Time-series ingestion, remote-sensing processing, models.
- Technologies:
  - GIS tools, ML frameworks, data lakehouse.
- Deliverables:
  - Yield models, dashboards, advisory reports.

# Expanded Source Schemas, ER Diagrams, Facts & Dimensions

This standardized expansion provides five logical sources for the project and a canonical set of artifacts to be appended to project markdown files when a detailed schema is required.

NOTE: The artifacts below are design artifacts created for documentation and implementation planning. They are original work and may be used for internal design and implementation purposes.

Project-specific prefix: `agricultural_data_intelligence_platform` (derived from filename: `agricultural-data-intelligence-platform.md`).

---

### Source A: Ingest & Landing (Source: `agricultural_data_intelligence_platform_ingest`)

Tables (20):
1. agricultural_data_intelligence_platform_stg_raw
2. agricultural_data_intelligence_platform_raw_records
3. agricultural_data_intelligence_platform_dim_source_system
4. agricultural_data_intelligence_platform_dim_data_owner
5. agricultural_data_intelligence_platform_dim_file_type
6. agricultural_data_intelligence_platform_ref_file_schema
7. agricultural_data_intelligence_platform_fact_raw_events
8. agricultural_data_intelligence_platform_stage_enrichments
9. agricultural_data_intelligence_platform_dim_geo
10. agricultural_data_intelligence_platform_dim_business_unit
11. agricultural_data_intelligence_platform_audit_ingest
12. agricultural_data_intelligence_platform_dim_environment
13. agricultural_data_intelligence_platform_ref_parsing_errors
14. agricultural_data_intelligence_platform_stage_cdc
15. agricultural_data_intelligence_platform_dim_schema_version
16. agricultural_data_intelligence_platform_fact_event_counts
17. agricultural_data_intelligence_platform_audit_transforms
18. agricultural_data_intelligence_platform_stage_retries
19. agricultural_data_intelligence_platform_ref_mappings
20. agricultural_data_intelligence_platform_dim_status

ER Diagram (ASCII):

agricultural_data_intelligence_platform_fact_raw_events (event_id, source_system_id, record_key, payload_hash, event_ts)
  |-- source_system_id --> agricultural_data_intelligence_platform_dim_source_system(source_system_id)
  |-- record_key --> agricultural_data_intelligence_platform_raw_records(record_key)

Description: Ingest staging (immutable) → raw normalization → enrichment → audit. `agricultural_data_intelligence_platform_fact_raw_events` is used for throughput and source health monitoring.

---

### Source B: Operational Logs & Metrics (Source: `agricultural_data_intelligence_platform_ops`)

Tables (20):
1. agricultural_data_intelligence_platform_stg_ops_logs
2. agricultural_data_intelligence_platform_raw_ops
3. agricultural_data_intelligence_platform_dim_service
4. agricultural_data_intelligence_platform_dim_instance
5. agricultural_data_intelligence_platform_dim_log_level
6. agricultural_data_intelligence_platform_ref_error_codes
7. agricultural_data_intelligence_platform_fact_logs
8. agricultural_data_intelligence_platform_stage_alerts
9. agricultural_data_intelligence_platform_dim_team
10. agricultural_data_intelligence_platform_dim_region
11. agricultural_data_intelligence_platform_audit_ops_ingest
12. agricultural_data_intelligence_platform_ref_runbooks
13. agricultural_data_intelligence_platform_stage_incidents
14. agricultural_data_intelligence_platform_fact_incident_metrics
15. agricultural_data_intelligence_platform_dim_priority
16. agricultural_data_intelligence_platform_ref_maintenance_windows
17. agricultural_data_intelligence_platform_audit_recon
18. agricultural_data_intelligence_platform_stage_trimmed_logs
19. agricultural_data_intelligence_platform_ref_retention_policy
20. agricultural_data_intelligence_platform_dim_status

ER Diagram (ASCII):

agricultural_data_intelligence_platform_fact_logs (log_id, service_id, instance_id, log_level, message_ts)
  |-- service_id --> agricultural_data_intelligence_platform_dim_service(service_id)
  |-- instance_id --> agricultural_data_intelligence_platform_dim_instance(instance_id)

---

### Source C: Governance & Catalog (Source: `agricultural_data_intelligence_platform_gov`)

Tables (20):
1. agricultural_data_intelligence_platform_stg_catalog
2. agricultural_data_intelligence_platform_raw_catalog
3. agricultural_data_intelligence_platform_dim_dataset
4. agricultural_data_intelligence_platform_dim_owner
5. agricultural_data_intelligence_platform_dim_tag
6. agricultural_data_intelligence_platform_ref_policies
7. agricultural_data_intelligence_platform_fact_data_quality
8. agricultural_data_intelligence_platform_stage_lineage
9. agricultural_data_intelligence_platform_dim_classification
10. agricultural_data_intelligence_platform_dim_sensitivity
11. agricultural_data_intelligence_platform_audit_policies
12. agricultural_data_intelligence_platform_ref_sla
13. agricultural_data_intelligence_platform_stage_certifications
14. agricultural_data_intelligence_platform_fact_issues
15. agricultural_data_intelligence_platform_dim_remediation_team
16. agricultural_data_intelligence_platform_ref_controls
17. agricultural_data_intelligence_platform_audit_certification
18. agricultural_data_intelligence_platform_stage_policy_changes
19. agricultural_data_intelligence_platform_ref_standards
20. agricultural_data_intelligence_platform_dim_status

ER Diagram (ASCII):

agricultural_data_intelligence_platform_fact_data_quality (dq_id, dataset_id, check_name, check_status, checked_ts)
  |-- dataset_id --> agricultural_data_intelligence_platform_dim_dataset(dataset_id)

---

### Source D: Cost, Billing & Usage (Source: `agricultural_data_intelligence_platform_cost`)

Tables (20):
1. agricultural_data_intelligence_platform_stg_billing_records
2. agricultural_data_intelligence_platform_raw_billing
3. agricultural_data_intelligence_platform_dim_cost_center
4. agricultural_data_intelligence_platform_dim_resource_type
5. agricultural_data_intelligence_platform_dim_region
6. agricultural_data_intelligence_platform_ref_price_catalog
7. agricultural_data_intelligence_platform_fact_cost_usage
8. agricultural_data_intelligence_platform_stage_allocations
9. agricultural_data_intelligence_platform_dim_tagging
10. agricultural_data_intelligence_platform_dim_currency
11. agricultural_data_intelligence_platform_audit_billing_ingest
12. agricultural_data_intelligence_platform_ref_discounts
13. agricultural_data_intelligence_platform_stage_corrections
14. agricultural_data_intelligence_platform_fact_monthly_costs
15. agricultural_data_intelligence_platform_dim_billing_account
16. agricultural_data_intelligence_platform_ref_chargeback_rules
17. agricultural_data_intelligence_platform_audit_allocations
18. agricultural_data_intelligence_platform_stage_forecasts
19. agricultural_data_intelligence_platform_ref_rates
20. agricultural_data_intelligence_platform_dim_status

ER Diagram (ASCII):

agricultural_data_intelligence_platform_fact_cost_usage (usage_id, resource_id, cost_amount, currency, start_ts, end_ts)
  |-- resource_id --> agricultural_data_intelligence_platform_dim_resource_type(resource_id)
  |-- cost_center_id --> agricultural_data_intelligence_platform_dim_cost_center(cost_center_id)

---

### Source E: Canonical Transactions / Facts (Source: `agricultural_data_intelligence_platform_txn`)

Tables (20):
1. agricultural_data_intelligence_platform_stg_transactions
2. agricultural_data_intelligence_platform_raw_transactions
3. agricultural_data_intelligence_platform_dim_account
4. agricultural_data_intelligence_platform_dim_customer
5. agricultural_data_intelligence_platform_dim_product
6. agricultural_data_intelligence_platform_ref_exchange_rates
7. agricultural_data_intelligence_platform_fact_transactions
8. agricultural_data_intelligence_platform_stage_reconciliations
9. agricultural_data_intelligence_platform_dim_channel
10. agricultural_data_intelligence_platform_dim_merchant
11. agricultural_data_intelligence_platform_audit_txn_ingest
12. agricultural_data_intelligence_platform_ref_fee_schedule
13. agricultural_data_intelligence_platform_stage_settlements
14. agricultural_data_intelligence_platform_fact_settlements
15. agricultural_data_intelligence_platform_dim_status
16. agricultural_data_intelligence_platform_ref_limits
17. agricultural_data_intelligence_platform_audit_recon
18. agricultural_data_intelligence_platform_stage_adjustments
19. agricultural_data_intelligence_platform_fact_balance_snapshots
20. agricultural_data_intelligence_platform_dim_time

ER Diagram (ASCII):

agricultural_data_intelligence_platform_fact_transactions (transaction_id, account_id, amount, currency, txn_type, posted_ts)
  |-- account_id --> agricultural_data_intelligence_platform_dim_account(account_id)
  |-- customer_id --> agricultural_data_intelligence_platform_dim_customer(customer_id)
  |-- product_id --> agricultural_data_intelligence_platform_dim_product(product_id)

Common guidance:
- Always keep an immutable staging/raw zone for auditable ingestion.
- Use `audit_*` tables and checksums for reconciliation between source and target facts.
- Implement SCD patterns for dimensions where history is required.
- Register datasets in a data catalog and apply RBAC and PII protections as required.

## Detailed ER Diagram

# Detailed ER Diagram: Entities, Attributes, Relationships, Cardinalities

This detailed ER diagram template expands the ASCII ER stub into full entity descriptions, attribute lists, primary/foreign key definitions, and explicit relationships with cardinalities for the project prefix `agricultural_data_intelligence_platform` (source file `agricultural-data-intelligence-platform.md`).

The template covers a canonical canonical set of logical entities used across projects: Source/Stage/Raw, Dimension entities, Fact entities, Reference / Lookup tables, and Audit & Reconciliation tables.

---

**Entity: `agricultural_data_intelligence_platform_raw_records`**
- Purpose: Immutable raw ingest payload store (one row per source record).
- PK: `record_key`
- Key attributes: `record_key (PK)`, `source_system`, `raw_payload` (JSON), `ingest_ts`, `ingest_batch_id`, `payload_hash`.

**Entity: `agricultural_data_intelligence_platform_stg_<topic>`** (generic staging)
- Purpose: Parsed staging of a raw record specific to a topic (e.g. transactions, events).
- PK: `stg_id`
- Key attributes: `stg_id (PK)`, `record_key (FK -> agricultural_data_intelligence_platform_raw_records.record_key)`, `parsed_fields...`, `ingest_ts`, `batch_id`, `load_status`.

**Entity: `agricultural_data_intelligence_platform_dim_account`**
- Purpose: Account dimension used by transaction facts.
- PK: `account_id`
- Attributes: `account_id (PK)`, `customer_id`, `account_type`, `currency_code`, `open_date`, `close_date`, `status`, `valid_from`, `valid_to`.

**Entity: `agricultural_data_intelligence_platform_dim_customer`**
- Purpose: Customer master attributes and identity.
- PK: `customer_id`
- Attributes: `customer_id (PK)`, `first_name`, `last_name`, `email_hash`, `birth_date`, `kyc_level`, `country`, `risk_score`, `valid_from`, `valid_to`.

**Entity: `agricultural_data_intelligence_platform_dim_time`**
- Purpose: Standard time dimension for reporting.
- PK: `date_key`
- Attributes: `date_key (PK)`, `date`, `year`, `quarter`, `month`, `day`, `weekday`, `is_business_day`.

**Entity: `agricultural_data_intelligence_platform_dim_product`**
- Purpose: Product/SKU master for retail-like facts.
- PK: `product_id`
- Attributes: `product_id (PK)`, `sku`, `name`, `category`, `brand`, `size`, `color`, `status`, `valid_from`, `valid_to`.

**Entity: `agricultural_data_intelligence_platform_fact_transactions`**
- Purpose: Canonical transaction-level fact (grain: one event/transaction).
- PK: `transaction_id`
- Attributes: `transaction_id (PK)`, `source_event_id`, `account_id (FK)`, `customer_id (FK)`, `product_id (FK)`, `amount`, `currency_code`, `amount_usd`, `txn_type`, `channel_code`, `merchant_id`, `status`, `posted_ts`, `processed_ts`, `ingest_batch_id`, `checksum`.

---

Relationships and cardinalities (explicit):
- `agricultural_data_intelligence_platform_fact_transactions.account_id` (M:1) -> `agricultural_data_intelligence_platform_dim_account.account_id`
  - Cardinality: Many transactions map to one account.
- `agricultural_data_intelligence_platform_fact_transactions.customer_id` (M:1) -> `agricultural_data_intelligence_platform_dim_customer.customer_id`
  - Many transactions per customer; some transactions inferred to customer through account linkage.
- `agricultural_data_intelligence_platform_fact_transactions.product_id` (M:1) -> `agricultural_data_intelligence_platform_dim_product.product_id`
  - Many fact rows reference a single product row.
- `agricultural_data_intelligence_platform_fact_transactions.posted_ts` (M:1) -> `agricultural_data_intelligence_platform_dim_time.date_key` (via date_key derived from posted_ts)
  - Many transactions map to one date in the time dimension.
- `agricultural_data_intelligence_platform_stg_<topic>.record_key` (M:1) -> `agricultural_data_intelligence_platform_raw_records.record_key`
  - One staging row per raw record, after parsing.

Association tables / many-to-many patterns:
- If customers belong to segments or tags, model as `agricultural_data_intelligence_platform_rel_customer_segment(customer_id FK, segment_id FK, assigned_ts)` with PK composite (`customer_id`, `segment_id`).

Detailed ER rules & integrity constraints:
- Use FK constraints where possible in the curated warehouse (e.g., `FOREIGN KEY (account_id) REFERENCES agricultural_data_intelligence_platform_dim_account(account_id)`).
- Enforce uniqueness on natural keys (e.g., `transaction_id`, `account_id + source_event_id` as alternate key) and use checksums for content verification.
- Implement SCD2 pattern for dimensions needing history using `valid_from` and `valid_to` and a surrogate `dim_pk`.

Sample SQL DDL snippets (representative):

CREATE TABLE agricultural_data_intelligence_platform_dim_customer (
  customer_id STRING PRIMARY KEY,
  first_name STRING,
  last_name STRING,
  email_hash STRING,
  kyc_level STRING,
  risk_score DOUBLE,
  valid_from DATE,
  valid_to DATE
);

CREATE TABLE agricultural_data_intelligence_platform_fact_transactions (
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
  FOREIGN KEY (account_id) REFERENCES agricultural_data_intelligence_platform_dim_account(account_id),
  FOREIGN KEY (customer_id) REFERENCES agricultural_data_intelligence_platform_dim_customer(customer_id)
);

ER Diagram (visual guidance):
- Center the `agricultural_data_intelligence_platform_fact_transactions` as the hub with outward links to `dim_account`, `dim_customer`, `dim_product`, and `dim_time`.
- Secondary facts (e.g., `agricultural_data_intelligence_platform_fact_settlements`) link back to `fact_transactions` via `transaction_id` where the settlement is child of a transaction (1:M relationship).

---

Per-project extension guidance:
- For banking projects, expand `dim_account` and `dim_customer` with regulatory attributes (aml_flags, kyc_date, tax_id_hash).
- For retail projects, extend `dim_product` with merchandising attributes and `dim_store` to represent brick-and-mortar locations.
- For IoT/telemetry projects, add time-series entity `agricultural_data_intelligence_platform_ts_measurements(device_id, measure_ts, metric, value)` with retention and rollup rules described.

This template is intended to be expanded with project-specific entities. The automation script will replace `agricultural_data_intelligence_platform` and `agricultural-data-intelligence-platform.md` and append the section to each markdown file that does not already contain a `## Detailed ER Diagram` marker.



# Complete Flow Diagram & Medallion Architecture with ADF, ADB, and PySpark

This section provides a comprehensive, production-grade Medallion architecture (Bronze → Silver → Gold) for the project `agricultural_data_intelligence_platform`, including:
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
   │  - agricultural_data_intelligence_platform_bro_*  │    │   (Staging area)    │
   │  - Immutable raw     │    └─────────────────────┘
   │  - 20 Validations    │
   │  - Checksums & hash  │
   └──────────┬───────────┘
              │
              │ (ADB Spark Job)
              ▼
   ┌──────────────────────────────┐
   │  SILVER Layer (Curated)      │
   │  - agricultural_data_intelligence_platform_sil_*          │
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
   │  - agricultural_data_intelligence_platform_gld_*          │
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

### Pipeline: `agricultural_data_intelligence_platform_Master_Orchestration`

**Trigger:** On-schedule (daily 2 AM UTC) + manual trigger

**Parameters:**
- `pipeline_run_id` (UUID)
- `execution_date` (YYYY-MM-DD)
- `source_filter` (optional: comma-separated source names)

**Activities:**

1. **Activity: Lookup_ExecutionParams**
   - Query `agricultural_data_intelligence_platform_audit_ingest` for last successful run
   - Set variables: `last_run_ts`, `expected_record_count`, `batch_id`

2. **Activity: Copy_Source_A** (For each source in parallel)
   - Source: API endpoint / file share / database
   - Sink: `agricultural_data_intelligence_platform_bro_source_a_raw` (ADLS gen2)
   - Format: Parquet (snappy compression)
   - Error handling: Retry 3x, then store error metadata
   - Post-copy: Execute "Validate_Bronze_A"

3. **Activity: Validate_Bronze_A**
   - Stored procedure call to `sp_validate_bronze_agricultural_data_intelligence_platform_a(batch_id)`
   - Returns validation result set
   - If failures: Log to `agricultural_data_intelligence_platform_audit_validation_failures`, alert, optionally fail pipeline

4. **Activity: Trigger_Spark_Silver_Job**
   - Type: Databricks Notebook Activity
   - Notebook path: `/Workspace/agricultural_data_intelligence_platform/silver_transform`
   - Parameters: `batch_id`, `execution_date`
   - Cluster: `agricultural_data_intelligence_platform-shared-compute` (auto-scale 2-8 nodes)

5. **Activity: Trigger_Spark_Gold_Job**
   - Notebook path: `/Workspace/agricultural_data_intelligence_platform/gold_aggregate`
   - Depends on: Trigger_Spark_Silver_Job success
   - Parameters: `batch_id`

6. **Activity: Post_Load_Validations**
   - Execute SQL script validating row counts, nulls, business rules
   - Store results in `agricultural_data_intelligence_platform_gold_validation_log`

7. **Activity: Send_Notification**
   - If all succeed: Send success email with row count summary
   - If fail: Send alert with error details

---

## Bronze Layer: Raw Ingest (20 Validations)

**Purpose:** Immutable, auditable raw data storage with comprehensive validation.

**Table Schema Example:** `agricultural_data_intelligence_platform_bro_source_a_raw`

```sql
CREATE TABLE agricultural_data_intelligence_platform_bro_source_a_raw (
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

spark = SparkSession.builder.appName("agricultural_data_intelligence_platform_bronze_validate").getOrCreate()

# Load Bronze raw data
bro_df = spark.read.parquet(f"/mnt/adls/bronze/agricultural_data_intelligence_platform_bro_source_a_raw/load_date={exec_date}")

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
        INSERT INTO agricultural_data_intelligence_platform_audit_validation_results (validation_id, layer, fail_count, check_ts)
        VALUES ('{val_id}', 'BRONZE', {fail_count}, current_timestamp())
        """)

print("Bronze validations complete")
```

---

## Silver Layer: Curated & Transformed (20 Transformation Scenarios)

**Purpose:** Cleansed, enriched, deduplicated, and integrated data ready for analytics.

**Table Example:** `agricultural_data_intelligence_platform_sil_transactions_curated`

```sql
CREATE TABLE agricultural_data_intelligence_platform_sil_transactions_curated (
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

spark = SparkSession.builder.appName("agricultural_data_intelligence_platform_silver_transform").getOrCreate()

# Load Bronze data
bro_df = spark.read.parquet(f"/mnt/adls/bronze/agricultural_data_intelligence_platform_bro_source_a_raw/load_date={exec_date}")

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
acct_df = spark.read.table("agricultural_data_intelligence_platform_dim_account")
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
    .partitionBy("load_date").save(f"/mnt/adls/silver/agricultural_data_intelligence_platform_sil_transactions_curated")

print("Silver transformation complete")
```

---

## Gold Layer: Analytics & Aggregations (20 Business Validations)

**Purpose:** Business-ready facts and dimensions for reporting and analytics.

**Table Example:** `agricultural_data_intelligence_platform_gld_fact_transactions`

```sql
CREATE TABLE agricultural_data_intelligence_platform_gld_fact_transactions (
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

spark = SparkSession.builder.appName("agricultural_data_intelligence_platform_gold_aggregate").getOrCreate()

# Load Silver data
sil_df = spark.read.table("agricultural_data_intelligence_platform_sil_transactions_curated")

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
acct_df = spark.read.table("agricultural_data_intelligence_platform_dim_account").select("account_key")
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
    INSERT INTO agricultural_data_intelligence_platform_gold_validation_log (validation_id, layer, fail_count, check_ts)
    VALUES ('{val_id}', 'GOLD', {count}, current_timestamp())
    """)

# Write fact table
gld_df.write.format("delta").mode("append").option("mergeSchema", "true") \
    .partitionBy("date_key").save(f"/mnt/adls/gold/agricultural_data_intelligence_platform_gld_fact_transactions")

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

