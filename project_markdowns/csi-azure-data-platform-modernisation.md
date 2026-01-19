# CSI – Azure Data Platform Modernisation

Brief: Modernise CSI's Azure data platform to current best practices.

- Objectives:
  - Move to a lakehouse, add governance and cost optimization.
- Scope:
  - Architecture refactor, migration, governance rollout.
- Key Components:
  - Lakehouse migration, Purview, performance tuning.
- Technologies:
  - Azure Databricks, Synapse, Purview.
- Deliverables:
  - Modernised platform, migration guides, cost metrics.

## Expanded Source Schemas, ER Diagrams, Facts & Dimensions

This section provides a standardized expansion: five logical sources per project, each with 20 tables (staging, raw, dims, facts, refs, audit), an ER-style diagram, fact/dimension details, reconciliation patterns, and a rights statement that these diagrams are original design artifacts.

Source naming uses a project-specific prefix `csi_`.

### Source A: Ingest & Landing (Source: csi_ingest)

Tables (20):
1. csi_stg_raw_events
2. csi_raw_records
3. csi_dim_source_system
4. csi_dim_data_owner
5. csi_dim_file_type
6. csi_ref_file_schema
7. csi_fact_raw_events
8. csi_stage_enrichments
9. csi_dim_geo
10. csi_dim_business_unit
11. csi_audit_ingest
12. csi_dim_environment
13. csi_ref_parsing_errors
14. csi_stage_cdc
15. csi_dim_schema_version
16. csi_fact_event_counts
17. csi_audit_transforms
18. csi_stage_retries
19. csi_ref_mappings
20. csi_dim_status

ER Diagram (ASCII):

csi_fact_raw_events (event_id, source_system_id, record_key, payload_hash, event_ts)
  |-- source_system_id --> csi_dim_source_system(source_system_id)
  |-- record_key --> csi_raw_records(record_key)

Fact/Dimension Notes:
- `csi_fact_raw_events`: grain is one ingested record; used to monitor throughput, duplicates, and source health.
- `csi_dim_source_system`: identifies upstream systems and owners.

Rights Statement: I confirm these flow diagrams and schema designs are original artifacts created for this engagement and may be used for internal design and implementation documentation.

---

### Source B: Operational Logs (Source: csi_ops)

Tables (20):
1. csi_stg_ops_logs
2. csi_raw_ops
3. csi_dim_service
4. csi_dim_instance
5. csi_dim_log_level
6. csi_ref_error_codes
7. csi_fact_logs
8. csi_stage_alerts
9. csi_dim_team
10. csi_dim_region
11. csi_audit_ops_ingest
12. csi_ref_runbooks
13. csi_stage_incidents
14. csi_fact_incident_metrics
15. csi_dim_priority
16. csi_ref_maintenance_windows
17. csi_audit_recon
18. csi_stage_trimmed_logs
19. csi_ref_retention_policy
20. csi_dim_status

ER Diagram (ASCII):

csi_fact_logs (log_id, service_id, instance_id, log_level, message_ts)
  |-- service_id --> csi_dim_service(service_id)
  |-- instance_id --> csi_dim_instance(instance_id)

Description: Logs are captured at event granularity and rolled up into incident and availability metrics.

---

### Source C: Governance Metadata (Source: csi_gov)

Tables (20):
1. csi_stg_catalog
2. csi_raw_catalog
3. csi_dim_dataset
4. csi_dim_owner
5. csi_dim_tag
6. csi_ref_policies
7. csi_fact_data_quality
8. csi_stage_lineage
9. csi_dim_classification
10. csi_dim_sensitivity
11. csi_audit_policies
12. csi_ref_sla
13. csi_stage_certifications
14. csi_fact_issues
15. csi_dim_remediation_team
16. csi_ref_controls
17. csi_audit_certification
18. csi_stage_policy_changes
19. csi_ref_standards
20. csi_dim_status

ER Diagram (ASCII):

csi_fact_data_quality (dq_id, dataset_id, check_name, check_status, checked_ts)
  |-- dataset_id --> csi_dim_dataset(dataset_id)

Description: Governance metadata tracks dataset quality, certifications, and owners for cataloging and audit.

---

### Source D: Cost & Billing (Source: csi_billing)

Tables (20):
1. csi_stg_billing_records
2. csi_raw_billing
3. csi_dim_cost_center
4. csi_dim_resource_type
5. csi_dim_region
6. csi_ref_price_catalog
7. csi_fact_cost_usage
8. csi_stage_allocations
9. csi_dim_tagging
10. csi_dim_currency
11. csi_audit_billing_ingest
12. csi_ref_discounts
13. csi_stage_corrections
14. csi_fact_monthly_costs
15. csi_dim_billing_account
16. csi_ref_chargeback_rules
17. csi_audit_allocations
18. csi_stage_forecasts
19. csi_ref_rates
20. csi_dim_status

ER Diagram (ASCII):

csi_fact_cost_usage (usage_id, resource_id, cost_amount, currency, start_ts, end_ts)
  |-- resource_id --> csi_dim_resource_type(resource_id)
  |-- cost_center_id --> csi_dim_cost_center(cost_center_id)

Description: Cost facts enable chargeback, cost optimization, and forecasting.

---

### Source E: Transactional Workloads (Source: csi_txn)

Tables (20):
1. csi_stg_transactions
2. csi_raw_transactions
3. csi_dim_account
4. csi_dim_customer
5. csi_dim_product
6. csi_ref_exchange_rates
7. csi_fact_transactions
8. csi_stage_reconciliations
9. csi_dim_channel
10. csi_dim_merchant
11. csi_audit_txn_ingest
12. csi_ref_fee_schedule
13. csi_stage_settlements
14. csi_fact_settlements
15. csi_dim_status
16. csi_ref_limits
17. csi_audit_recon
18. csi_stage_adjustments
19. csi_fact_balance_snapshots
20. csi_dim_time

ER Diagram (ASCII):

csi_fact_transactions (transaction_id, account_id, amount, currency, txn_type, posted_ts)
  |-- account_id --> csi_dim_account(account_id)
  |-- customer_id --> csi_dim_customer(customer_id)
  |-- product_id --> csi_dim_product(product_id)

Common Patterns: Use staging (immutable), raw normalized, enrichment stages, canonical fact loading, and audit/reconciliation tables. Dimensions follow SCD patterns appropriate to business needs.

## Implementation Notes
- Use `ingest_batch_id`, checksums, and `audit_*` tables for reconciliation.
- Implement data quality checks (Great Expectations or similar) before promoting to curated zones.
- Register datasets in a catalog and enforce RBAC via Unity Catalog/Purview.

## Detailed ER Diagram

# Detailed ER Diagram: Entities, Attributes, Relationships, Cardinalities

This detailed ER diagram template expands the ASCII ER stub into full entity descriptions, attribute lists, primary/foreign key definitions, and explicit relationships with cardinalities for the project prefix `csi_azure_data_platform_modernisation` (source file `csi-azure-data-platform-modernisation.md`).

The template covers a canonical canonical set of logical entities used across projects: Source/Stage/Raw, Dimension entities, Fact entities, Reference / Lookup tables, and Audit & Reconciliation tables.

---

**Entity: `csi_azure_data_platform_modernisation_raw_records`**
- Purpose: Immutable raw ingest payload store (one row per source record).
- PK: `record_key`
- Key attributes: `record_key (PK)`, `source_system`, `raw_payload` (JSON), `ingest_ts`, `ingest_batch_id`, `payload_hash`.

**Entity: `csi_azure_data_platform_modernisation_stg_<topic>`** (generic staging)
- Purpose: Parsed staging of a raw record specific to a topic (e.g. transactions, events).
- PK: `stg_id`
- Key attributes: `stg_id (PK)`, `record_key (FK -> csi_azure_data_platform_modernisation_raw_records.record_key)`, `parsed_fields...`, `ingest_ts`, `batch_id`, `load_status`.

**Entity: `csi_azure_data_platform_modernisation_dim_account`**
- Purpose: Account dimension used by transaction facts.
- PK: `account_id`
- Attributes: `account_id (PK)`, `customer_id`, `account_type`, `currency_code`, `open_date`, `close_date`, `status`, `valid_from`, `valid_to`.

**Entity: `csi_azure_data_platform_modernisation_dim_customer`**
- Purpose: Customer master attributes and identity.
- PK: `customer_id`
- Attributes: `customer_id (PK)`, `first_name`, `last_name`, `email_hash`, `birth_date`, `kyc_level`, `country`, `risk_score`, `valid_from`, `valid_to`.

**Entity: `csi_azure_data_platform_modernisation_dim_time`**
- Purpose: Standard time dimension for reporting.
- PK: `date_key`
- Attributes: `date_key (PK)`, `date`, `year`, `quarter`, `month`, `day`, `weekday`, `is_business_day`.

**Entity: `csi_azure_data_platform_modernisation_dim_product`**
- Purpose: Product/SKU master for retail-like facts.
- PK: `product_id`
- Attributes: `product_id (PK)`, `sku`, `name`, `category`, `brand`, `size`, `color`, `status`, `valid_from`, `valid_to`.

**Entity: `csi_azure_data_platform_modernisation_fact_transactions`**
- Purpose: Canonical transaction-level fact (grain: one event/transaction).
- PK: `transaction_id`
- Attributes: `transaction_id (PK)`, `source_event_id`, `account_id (FK)`, `customer_id (FK)`, `product_id (FK)`, `amount`, `currency_code`, `amount_usd`, `txn_type`, `channel_code`, `merchant_id`, `status`, `posted_ts`, `processed_ts`, `ingest_batch_id`, `checksum`.

---

Relationships and cardinalities (explicit):
- `csi_azure_data_platform_modernisation_fact_transactions.account_id` (M:1) -> `csi_azure_data_platform_modernisation_dim_account.account_id`
  - Cardinality: Many transactions map to one account.
- `csi_azure_data_platform_modernisation_fact_transactions.customer_id` (M:1) -> `csi_azure_data_platform_modernisation_dim_customer.customer_id`
  - Many transactions per customer; some transactions inferred to customer through account linkage.
- `csi_azure_data_platform_modernisation_fact_transactions.product_id` (M:1) -> `csi_azure_data_platform_modernisation_dim_product.product_id`
  - Many fact rows reference a single product row.
- `csi_azure_data_platform_modernisation_fact_transactions.posted_ts` (M:1) -> `csi_azure_data_platform_modernisation_dim_time.date_key` (via date_key derived from posted_ts)
  - Many transactions map to one date in the time dimension.
- `csi_azure_data_platform_modernisation_stg_<topic>.record_key` (M:1) -> `csi_azure_data_platform_modernisation_raw_records.record_key`
  - One staging row per raw record, after parsing.

Association tables / many-to-many patterns:
- If customers belong to segments or tags, model as `csi_azure_data_platform_modernisation_rel_customer_segment(customer_id FK, segment_id FK, assigned_ts)` with PK composite (`customer_id`, `segment_id`).

Detailed ER rules & integrity constraints:
- Use FK constraints where possible in the curated warehouse (e.g., `FOREIGN KEY (account_id) REFERENCES csi_azure_data_platform_modernisation_dim_account(account_id)`).
- Enforce uniqueness on natural keys (e.g., `transaction_id`, `account_id + source_event_id` as alternate key) and use checksums for content verification.
- Implement SCD2 pattern for dimensions needing history using `valid_from` and `valid_to` and a surrogate `dim_pk`.

Sample SQL DDL snippets (representative):

CREATE TABLE csi_azure_data_platform_modernisation_dim_customer (
  customer_id STRING PRIMARY KEY,
  first_name STRING,
  last_name STRING,
  email_hash STRING,
  kyc_level STRING,
  risk_score DOUBLE,
  valid_from DATE,
  valid_to DATE
);

CREATE TABLE csi_azure_data_platform_modernisation_fact_transactions (
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
  FOREIGN KEY (account_id) REFERENCES csi_azure_data_platform_modernisation_dim_account(account_id),
  FOREIGN KEY (customer_id) REFERENCES csi_azure_data_platform_modernisation_dim_customer(customer_id)
);

ER Diagram (visual guidance):
- Center the `csi_azure_data_platform_modernisation_fact_transactions` as the hub with outward links to `dim_account`, `dim_customer`, `dim_product`, and `dim_time`.
- Secondary facts (e.g., `csi_azure_data_platform_modernisation_fact_settlements`) link back to `fact_transactions` via `transaction_id` where the settlement is child of a transaction (1:M relationship).

---

Per-project extension guidance:
- For banking projects, expand `dim_account` and `dim_customer` with regulatory attributes (aml_flags, kyc_date, tax_id_hash).
- For retail projects, extend `dim_product` with merchandising attributes and `dim_store` to represent brick-and-mortar locations.
- For IoT/telemetry projects, add time-series entity `csi_azure_data_platform_modernisation_ts_measurements(device_id, measure_ts, metric, value)` with retention and rollup rules described.

This template is intended to be expanded with project-specific entities. The automation script will replace `csi_azure_data_platform_modernisation` and `csi-azure-data-platform-modernisation.md` and append the section to each markdown file that does not already contain a `## Detailed ER Diagram` marker.

