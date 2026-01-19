# Banking Transaction Processing Pipeline

Brief: Reliable, auditable pipelines for banking transaction data processing.

- Objectives:
  - Ensure integrity, auditability, and timeliness of transaction data.
- Scope:
  - Ingestion, enrichment, settlement, reconciliation.
- Key Components:
  - Message queues, ETL, reconciliation jobs, audit logs.
- Technologies:
  - Kafka, Databricks, secure storage, monitoring.
- Deliverables:
  - Processed transaction tables, reconciliation reports.

## Expanded Source Schemas, ER Diagrams, Facts & Dimensions

This document expands the pipeline design into five distinct logical sources. Each source lists 20 tables (staging, raw, reference, dimension, fact, audit), an ER-style diagram showing relationships between the principal tables, a description of fact tables and dimensions, and an explicit rights statement about creating flow/ER diagrams.

NOTE: The diagrams and schemas below are illustrative design artifacts created to model the pipeline flow and canonical schemas for analytics. I confirm that I have the right to create and publish these flow diagrams and documentation as part of this engagement — they are original schematic designs and do not reproduce proprietary diagrams from third parties.

---

### Source A: Core Banking Transactions (Source: CoreBankingSystem)

Overview: Transactions originating from the bank's core ledger and account systems (debits, credits, transfers, fees).

Tables (20):
1. cb_stg_transactions — raw ingest from CoreBanking (raw payload, ingest_ts)
2. cb_raw_transactions — normalized raw records (one row per bank event)
3. cb_dim_account — account master (account_id, account_type, opened_date)
4. cb_dim_customer — customer master (customer_id, name, dob, kyc_flag)
5. cb_dim_branch — branch master (branch_id, name, region)
6. cb_dim_currency — currency lookup (currency_code, name)
7. cb_dim_txn_type — transaction type lookup (type_code, description)
8. cb_dim_channel — channel lookup (channel_code, description)
9. cb_fact_transactions — canonical transaction fact (transaction_id, account_id, amount...)
10. cb_fact_balances_snapshot — daily balance snapshots
11. cb_stage_enrichments — enrichment staging (fx rates, customer score)
12. cb_dim_merchant — merchant lookup (merchant_id, category)
13. cb_dim_fee_type — fee type lookup
14. cb_audit_ingest — ingest audit log (batch_id, rows_in, rows_out)
15. cb_audit_recon — reconciliation audit (source_rows, target_rows, mismatches)
16. cb_dim_settlement — settlement instructions lookup
17. cb_stage_reconciled — reconciled staging table
18. cb_dim_status — transaction status (posted, pending, failed)
19. cb_dim_card — card metadata (card_id, card_scheme)
20. cb_ref_exchange_rates — historical FX rates

ER Diagram (ASCII):

cb_fact_transactions (transaction_id, account_id, amount, currency_code, txn_type_code, channel_code, merchant_id, posted_ts)
  |-- account_id --> cb_dim_account (account_id)
  |-- customer_id --> cb_dim_customer (customer_id) (via account)
  |-- branch_id --> cb_dim_branch (branch_id)
  |-- currency_code --> cb_dim_currency (currency_code)
  |-- txn_type_code --> cb_dim_txn_type (type_code)
  |-- channel_code --> cb_dim_channel (channel_code)
  |-- merchant_id --> cb_dim_merchant (merchant_id)
  |-- card_id --> cb_dim_card (card_id)

Description: The central fact table `cb_fact_transactions` links to multiple dimensions to support analytics: customer/account analysis, channel analysis, merchant/product analytics, and FX normalization.

Fact Tables & Dimensions (detailed):
- Fact: `cb_fact_transactions` — grain is one financial event (transaction). Key columns: `transaction_id PK`, `account_id FK`, `amount`, `currency_code FK`, `amount_usd` (derived), `txn_type_code FK`, `channel_code FK`, `merchant_id FK`, `posted_ts`, `processed_ts`, `source_batch_id`.
- Dimension: `cb_dim_account` — account-level attributes used for segmentation: `account_id PK`, `customer_id FK`, `account_type`, `status`, `open_date`, `close_date`.
- Dimension: `cb_dim_customer` — personal attributes and risk flags: `customer_id PK`, `name`, `email_hash`, `kyc_level`, `risk_score`.
- Dimension: `cb_dim_currency` — normalization info and minor currency metadata.
- Dimension: `cb_dim_txn_type` — used to classify transactions for reporting.
- Dimension: `cb_dim_channel` — defines origin of transaction (ATM, branch, online, mobile, API).

ER Diagram Explanation (detailed):
- `cb_stg_transactions` → ETL cleans to `cb_raw_transactions`.
- Enrichment joins `cb_raw_transactions` with `cb_stage_enrichments` and `cb_ref_exchange_rates` to compute normalized amounts and flags.
- Consolidated rows inserted into `cb_fact_transactions` with FK references to dimensions.
- Audit tables (`cb_audit_ingest`, `cb_audit_recon`) record counts for reconciliation and SLA verification.

Operational Flow Diagram Rights & Notes:
- I assert rights to author these flow diagrams and schemas as original work for pipeline design and documentation. Use restrictions: these are design artifacts intended for internal architecture and implementation; if you require formal IP transfer or NDA-based ownership statements, provide the required legal agreement.

---

### Source B: Payments Gateway (Source: PaymentsGateway)

Overview: Payment authorizations and settlements from the external payments gateway (card authorizations, refunds).

Tables (20):
1. pg_stg_authorizations
2. pg_raw_authorizations
3. pg_dim_merchant
4. pg_dim_terminal
5. pg_dim_card
6. pg_dim_currency
7. pg_dim_response_code
8. pg_dim_acquirer
9. pg_fact_authorizations
10. pg_fact_settlements
11. pg_audit_ingest
12. pg_audit_settlement_recon
13. pg_ref_fee_schedule
14. pg_stage_chargebacks
15. pg_dim_scheme (Visa/Mastercard/etc)
16. pg_dim_processor (processor metadata)
17. pg_stage_retries
18. pg_dim_geo (country/region)
19. pg_ref_rate_limiting
20. pg_dim_risk_score

ER Diagram (ASCII):

pg_fact_authorizations (auth_id, card_id, merchant_id, terminal_id, amount, currency_code, auth_ts, response_code)
  |-- card_id --> pg_dim_card
  |-- merchant_id --> pg_dim_merchant
  |-- terminal_id --> pg_dim_terminal
  |-- response_code --> pg_dim_response_code
  |-- currency_code --> pg_dim_currency

pg_fact_settlements (settlement_id, auth_id FK, settled_amount, settlement_date, acquirer_id FK)
  |-- auth_id --> pg_fact_authorizations
  |-- acquirer_id --> pg_dim_acquirer

Description: Authorizations and settlement facts enable measurement of authorization rate, settlement latency, chargebacks, and reconciliation with issuer/acquirer statements.

Facts & Dimensions:
- `pg_fact_authorizations` — grain: one authorization attempt. Columns include `auth_id PK`, `card_id FK`, `merchant_id FK`, `amount`, `currency_code`, `response_code`, `auth_ts`, `auth_status`.
- `pg_fact_settlements` — grain: settlement event (can be many-to-one with auths). Columns: `settlement_id PK`, `auth_id FK`, `settled_amount`, `settlement_ts`, `acquirer_id FK`.
- Dimensions: `pg_dim_merchant`, `pg_dim_terminal`, `pg_dim_card`, `pg_dim_response_code`, `pg_dim_acquirer`, `pg_dim_geo`.

ER Diagram Explanation:
- Gateway events ingest into staging tables (`pg_stg_authorizations`) and normalize into `pg_raw_authorizations`.
- Authorizations are deduplicated and persisted to `pg_fact_authorizations`.
- Settlement feeds reconcile authorizations to settled amounts producing `pg_fact_settlements`.
- Audits capture mismatches between `pg_fact_settlements` and bank reimbursements.

Rights Statement: This ER diagram and flow are original design representations for payments pipeline implementation and I confirm the right to create and provide them for implementation documentation.

---

### Source C: ATM & POS Switch (Source: SwitchRouter)

Overview: Switch events for ATMs and POS devices (cash withdrawals, balance inquiries, reversals).

Tables (20):
1. sw_stg_events
2. sw_raw_events
3. sw_dim_device
4. sw_dim_terminal
5. sw_dim_network
6. sw_dim_branch
7. sw_dim_card
8. sw_dim_txn_type
9. sw_fact_switch_events
10. sw_fact_cash_movements
11. sw_audit_ingest
12. sw_ref_fees
13. sw_dim_status
14. sw_stage_reversals
15. sw_dim_provider
16. sw_ref_limits
17. sw_stage_settlement_batches
18. sw_fact_reversals
19. sw_dim_geo
20. sw_audit_recon

ER Diagram (ASCII):

sw_fact_switch_events (event_id, terminal_id, card_id, txn_type, amount, status, event_ts)
  |-- terminal_id --> sw_dim_terminal
  |-- card_id --> sw_dim_card
  |-- txn_type --> sw_dim_txn_type
  |-- terminal_id --> sw_dim_device

sw_fact_cash_movements (movement_id, event_id FK, amount, branch_id)
  |-- event_id --> sw_fact_switch_events
  |-- branch_id --> sw_dim_branch

Description: Switch events feed both authorization flows and cash movement accounting. Reconciliations occur between switch and core ledger.

Facts & Dimensions:
- `sw_fact_switch_events`: event-level grain. Key columns: `event_id`, `terminal_id FK`, `card_id FK`, `txn_type`, `amount`, `status`, `provider_id`, `event_ts`.
- `sw_fact_cash_movements`: aggregated cash movements used for ATM cash forecasting.
- Dimensions include `sw_dim_device`, `sw_dim_terminal`, `sw_dim_provider`, `sw_dim_branch`.

Explanation: Event stream -> staging -> raw -> dedup -> canonical fact; settlement batches later produce settlement facts used for recon.

---

### Source D: Card Processor / Acquirer (Source: CardProcessor)

Overview: Card network and acquirer feeds (issuer responses, clearing files, chargebacks).

Tables (20):
1. cp_stg_clearing_files
2. cp_raw_clearing
3. cp_dim_issuer
4. cp_dim_acquirer
5. cp_dim_scheme
6. cp_dim_merchant
7. cp_dim_fee_type
8. cp_fact_clearing_entries
9. cp_fact_chargebacks
10. cp_ref_fee_schedule
11. cp_stage_adjustments
12. cp_audit_clearing
13. cp_dim_currency
14. cp_dim_route
15. cp_fact_fees
16. cp_stage_reconciled
17. cp_dim_dispute_reason
18. cp_ref_fx_rates
19. cp_dim_settlement_status
20. cp_audit_recon

ER Diagram (ASCII):

cp_fact_clearing_entries (clearing_id, acquirer_id, issuer_id, merchant_id, amount, fee_amount, currency)
  |-- acquirer_id --> cp_dim_acquirer
  |-- issuer_id --> cp_dim_issuer
  |-- merchant_id --> cp_dim_merchant
  |-- currency --> cp_dim_currency

cp_fact_chargebacks (chargeback_id, clearing_id FK, dispute_reason, amount, status, cb_ts)
  |-- clearing_id --> cp_fact_clearing_entries
  |-- dispute_reason --> cp_dim_dispute_reason

Description: Clearing entries and chargebacks provide the settlement and dispute trail required for finance posting and reconciliation.

Facts & Dimensions:
- `cp_fact_clearing_entries`: grain is clearing line. Useful metrics: gross volume, net fees, cost per transaction, reconciliation status.
- `cp_fact_chargebacks`: captures disputes and chargeback flows for aging and liability.
- Dimensions: `cp_dim_issuer`, `cp_dim_acquirer`, `cp_dim_merchant`, `cp_dim_scheme`, `cp_dim_dispute_reason`.

Rights Statement: I confirm these diagrams and schemas are generated by me for design purposes and may be used for implementation documentation and flow diagrams.

---

### Source E: External Settlements & Clearing (Source: ExternalSettlements)

Overview: Files from external settlement systems and clearing houses (ACH, RTGS, correspondent banks).

Tables (20):
1. es_stg_settlement_files
2. es_raw_settlements
3. es_dim_counterparty
4. es_dim_settlement_method
5. es_dim_currency
6. es_fact_settlement_instructions
7. es_fact_settlement_postings
8. es_ref_cutoff_times
9. es_stage_fees
10. es_audit_ingest
11. es_audit_settlement_recon
12. es_dim_message_type
13. es_ref_exchange_rates
14. es_fact_netting_results
15. es_stage_returns
16. es_dim_bank_branch_lookup
17. es_dim_account_mapping
18. es_ref_statement_lines
19. es_fact_clearing_adjustments
20. es_audit_aging

ER Diagram (ASCII):

es_fact_settlement_instructions (instruction_id, counterparty_id, amount, currency, value_date, method)
  |-- counterparty_id --> es_dim_counterparty
  |-- method --> es_dim_settlement_method
  |-- currency --> es_dim_currency

es_fact_settlement_postings (posting_id, instruction_id FK, posting_amount, posting_ts, status)
  |-- instruction_id --> es_fact_settlement_instructions

Description: Settlement instructions and postings capture the lifecycle from instruction generation, netting, posting, to reconciliation with bank accounts.

Facts & Dimensions:
- `es_fact_settlement_instructions`: grain is one instruction to move funds. Columns: `instruction_id PK`, `counterparty_id FK`, `amount`, `currency`, `value_date`, `method`, `netting_group`.
- `es_fact_settlement_postings`: captures actual ledger postings created by settlement.
- Dimensions: `es_dim_counterparty`, `es_dim_settlement_method`, `es_dim_message_type`, `es_dim_bank_branch_lookup`.

ER Diagram Explanation: Ingestion of settlement files → normalization → enrichment (cutoff, FX) → create instructions → netting/aggregation → produce postings → reconciliation with ledger facts and cash positions.

---

## Common Fact Table Patterns (applies across sources)

- Transaction Fact (canonical): Grain is one event. Core columns: `event_id PK`, `source` (SourceSystem), `source_event_id`, `account_id FK`, `customer_id FK`, `amount`, `currency`, `amount_usd`, `txn_type`, `status`, `event_ts`, `processed_ts`, `ingest_batch_id`.
- Balance Snapshot Fact: Daily snapshots per account or per ledger partition: `account_id`, `snapshot_date`, `closing_balance`, `available_balance`.
- Settlement Fact: Settlement-level grain capturing cleared/settled amounts and counterparties.

## Common Dimension Patterns

- Account Dimension: `account_id PK`, `customer_id FK`, `acct_type`, `open_date`, `status`, `product_code`, `branch_id`.
- Customer Dimension: `customer_id PK`, `hashed_identifier`, `kyc_level`, `risk_score`, `first_active_date`, `last_active_date`.
- Time Dimension: standard `date_key`, `date`, `year`, `quarter`, `month`, `day_of_week`, `is_business_day`.
- Channel Dimension: `channel_code`, `channel_name`.
- Merchant Dimension: `merchant_id`, `name`, `category`, `mcc_code`.

## Example Fact Table Schema (detailed)
- Table: `cb_fact_transactions`
  - `transaction_id` (string) — PK
  - `source_system` (string)
  - `source_event_id` (string)
  - `account_id` (string) — FK to account dim
  - `customer_id` (string) — FK to customer dim
  - `amount` (decimal)
  - `currency_code` (string) — FK
  - `amount_usd` (decimal) — derived via `ref_exchange_rates`
  - `txn_type_code` (string) — FK
  - `channel_code` (string) — FK
  - `merchant_id` (string) — FK
  - `status` (string)
  - `posted_ts` (timestamp)
  - `processed_ts` (timestamp)
  - `ingest_batch_id` (string)

## Example Dimension Table Schema (detailed)
- Table: `cb_dim_account`
  - `account_id` (string) — PK
  - `customer_id` (string)
  - `account_type` (string)
  - `open_date` (date)
  - `close_date` (date)
  - `status` (string)
  - `currency_code` (string)

## Reconciliation & Audit Patterns
- Ingest audit tables record counts and checksums per batch.
- Reconciliation jobs compare source counts and sums to target fact aggregates; mismatches written to `*_audit_recon` tables and displayed on monitoring dashboards.
- Late-arriving and reversal handling: stage, tag with `is_reversal` and update facts with versioning fields (`valid_from`, `valid_to`) or CDC-style soft-deletes.

## Flow Diagram & Implementation Notes
- Recommended flow for each source:
  1. Source stream/file → staging (immutable raw) with `ingest_ts` and `batch_id`.
  2. Raw normalization → enrichment (FX, KYC flags, geo) → dedup.
  3. Load to canonical facts and dimensions (use upsert strategies for dimensions with SCD2/3 as needed).
  4. Run reconciliation & data quality checks (Great Expectations or custom tests).
  5. Publish datasets to analytics zone (curated), and register in data catalog.

## Next Steps & Options
- If you want the same expanded treatment for all other markdown files in `project_markdowns`, I can proceed in batches (e.g., 5 files per batch) and update the todo list accordingly. This iteration focused on the currently-open file. Please confirm if I should continue applying this level of detail to the remaining files.

## Detailed ER Diagram

# Detailed ER Diagram: Entities, Attributes, Relationships, Cardinalities

This detailed ER diagram template expands the ASCII ER stub into full entity descriptions, attribute lists, primary/foreign key definitions, and explicit relationships with cardinalities for the project prefix `banking_transaction_processing_pipeline` (source file `banking-transaction-processing-pipeline.md`).

The template covers a canonical canonical set of logical entities used across projects: Source/Stage/Raw, Dimension entities, Fact entities, Reference / Lookup tables, and Audit & Reconciliation tables.

---

**Entity: `banking_transaction_processing_pipeline_raw_records`**
- Purpose: Immutable raw ingest payload store (one row per source record).
- PK: `record_key`
- Key attributes: `record_key (PK)`, `source_system`, `raw_payload` (JSON), `ingest_ts`, `ingest_batch_id`, `payload_hash`.

**Entity: `banking_transaction_processing_pipeline_stg_<topic>`** (generic staging)
- Purpose: Parsed staging of a raw record specific to a topic (e.g. transactions, events).
- PK: `stg_id`
- Key attributes: `stg_id (PK)`, `record_key (FK -> banking_transaction_processing_pipeline_raw_records.record_key)`, `parsed_fields...`, `ingest_ts`, `batch_id`, `load_status`.

**Entity: `banking_transaction_processing_pipeline_dim_account`**
- Purpose: Account dimension used by transaction facts.
- PK: `account_id`
- Attributes: `account_id (PK)`, `customer_id`, `account_type`, `currency_code`, `open_date`, `close_date`, `status`, `valid_from`, `valid_to`.

**Entity: `banking_transaction_processing_pipeline_dim_customer`**
- Purpose: Customer master attributes and identity.
- PK: `customer_id`
- Attributes: `customer_id (PK)`, `first_name`, `last_name`, `email_hash`, `birth_date`, `kyc_level`, `country`, `risk_score`, `valid_from`, `valid_to`.

**Entity: `banking_transaction_processing_pipeline_dim_time`**
- Purpose: Standard time dimension for reporting.
- PK: `date_key`
- Attributes: `date_key (PK)`, `date`, `year`, `quarter`, `month`, `day`, `weekday`, `is_business_day`.

**Entity: `banking_transaction_processing_pipeline_dim_product`**
- Purpose: Product/SKU master for retail-like facts.
- PK: `product_id`
- Attributes: `product_id (PK)`, `sku`, `name`, `category`, `brand`, `size`, `color`, `status`, `valid_from`, `valid_to`.

**Entity: `banking_transaction_processing_pipeline_fact_transactions`**
- Purpose: Canonical transaction-level fact (grain: one event/transaction).
- PK: `transaction_id`
- Attributes: `transaction_id (PK)`, `source_event_id`, `account_id (FK)`, `customer_id (FK)`, `product_id (FK)`, `amount`, `currency_code`, `amount_usd`, `txn_type`, `channel_code`, `merchant_id`, `status`, `posted_ts`, `processed_ts`, `ingest_batch_id`, `checksum`.

---

Relationships and cardinalities (explicit):
- `banking_transaction_processing_pipeline_fact_transactions.account_id` (M:1) -> `banking_transaction_processing_pipeline_dim_account.account_id`
  - Cardinality: Many transactions map to one account.
- `banking_transaction_processing_pipeline_fact_transactions.customer_id` (M:1) -> `banking_transaction_processing_pipeline_dim_customer.customer_id`
  - Many transactions per customer; some transactions inferred to customer through account linkage.
- `banking_transaction_processing_pipeline_fact_transactions.product_id` (M:1) -> `banking_transaction_processing_pipeline_dim_product.product_id`
  - Many fact rows reference a single product row.
- `banking_transaction_processing_pipeline_fact_transactions.posted_ts` (M:1) -> `banking_transaction_processing_pipeline_dim_time.date_key` (via date_key derived from posted_ts)
  - Many transactions map to one date in the time dimension.
- `banking_transaction_processing_pipeline_stg_<topic>.record_key` (M:1) -> `banking_transaction_processing_pipeline_raw_records.record_key`
  - One staging row per raw record, after parsing.

Association tables / many-to-many patterns:
- If customers belong to segments or tags, model as `banking_transaction_processing_pipeline_rel_customer_segment(customer_id FK, segment_id FK, assigned_ts)` with PK composite (`customer_id`, `segment_id`).

Detailed ER rules & integrity constraints:
- Use FK constraints where possible in the curated warehouse (e.g., `FOREIGN KEY (account_id) REFERENCES banking_transaction_processing_pipeline_dim_account(account_id)`).
- Enforce uniqueness on natural keys (e.g., `transaction_id`, `account_id + source_event_id` as alternate key) and use checksums for content verification.
- Implement SCD2 pattern for dimensions needing history using `valid_from` and `valid_to` and a surrogate `dim_pk`.

Sample SQL DDL snippets (representative):

CREATE TABLE banking_transaction_processing_pipeline_dim_customer (
  customer_id STRING PRIMARY KEY,
  first_name STRING,
  last_name STRING,
  email_hash STRING,
  kyc_level STRING,
  risk_score DOUBLE,
  valid_from DATE,
  valid_to DATE
);

CREATE TABLE banking_transaction_processing_pipeline_fact_transactions (
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
  FOREIGN KEY (account_id) REFERENCES banking_transaction_processing_pipeline_dim_account(account_id),
  FOREIGN KEY (customer_id) REFERENCES banking_transaction_processing_pipeline_dim_customer(customer_id)
);

ER Diagram (visual guidance):
- Center the `banking_transaction_processing_pipeline_fact_transactions` as the hub with outward links to `dim_account`, `dim_customer`, `dim_product`, and `dim_time`.
- Secondary facts (e.g., `banking_transaction_processing_pipeline_fact_settlements`) link back to `fact_transactions` via `transaction_id` where the settlement is child of a transaction (1:M relationship).

---

Per-project extension guidance:
- For banking projects, expand `dim_account` and `dim_customer` with regulatory attributes (aml_flags, kyc_date, tax_id_hash).
- For retail projects, extend `dim_product` with merchandising attributes and `dim_store` to represent brick-and-mortar locations.
- For IoT/telemetry projects, add time-series entity `banking_transaction_processing_pipeline_ts_measurements(device_id, measure_ts, metric, value)` with retention and rollup rules described.

This template is intended to be expanded with project-specific entities. The automation script will replace `banking_transaction_processing_pipeline` and `banking-transaction-processing-pipeline.md` and append the section to each markdown file that does not already contain a `## Detailed ER Diagram` marker.



# Complete Flow Diagram & Medallion Architecture with ADF, ADB, and PySpark

This section provides a comprehensive, production-grade Medallion architecture (Bronze → Silver → Gold) for the project `banking_transaction_processing_pipeline`, including:
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
   │  - banking_transaction_processing_pipeline_bro_*  │    │   (Staging area)    │
   │  - Immutable raw     │    └─────────────────────┘
   │  - 20 Validations    │
   │  - Checksums & hash  │
   └──────────┬───────────┘
              │
              │ (ADB Spark Job)
              ▼
   ┌──────────────────────────────┐
   │  SILVER Layer (Curated)      │
   │  - banking_transaction_processing_pipeline_sil_*          │
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
   │  - banking_transaction_processing_pipeline_gld_*          │
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

### Pipeline: `banking_transaction_processing_pipeline_Master_Orchestration`

**Trigger:** On-schedule (daily 2 AM UTC) + manual trigger

**Parameters:**
- `pipeline_run_id` (UUID)
- `execution_date` (YYYY-MM-DD)
- `source_filter` (optional: comma-separated source names)

**Activities:**

1. **Activity: Lookup_ExecutionParams**
   - Query `banking_transaction_processing_pipeline_audit_ingest` for last successful run
   - Set variables: `last_run_ts`, `expected_record_count`, `batch_id`

2. **Activity: Copy_Source_A** (For each source in parallel)
   - Source: API endpoint / file share / database
   - Sink: `banking_transaction_processing_pipeline_bro_source_a_raw` (ADLS gen2)
   - Format: Parquet (snappy compression)
   - Error handling: Retry 3x, then store error metadata
   - Post-copy: Execute "Validate_Bronze_A"

3. **Activity: Validate_Bronze_A**
   - Stored procedure call to `sp_validate_bronze_banking_transaction_processing_pipeline_a(batch_id)`
   - Returns validation result set
   - If failures: Log to `banking_transaction_processing_pipeline_audit_validation_failures`, alert, optionally fail pipeline

4. **Activity: Trigger_Spark_Silver_Job**
   - Type: Databricks Notebook Activity
   - Notebook path: `/Workspace/banking_transaction_processing_pipeline/silver_transform`
   - Parameters: `batch_id`, `execution_date`
   - Cluster: `banking_transaction_processing_pipeline-shared-compute` (auto-scale 2-8 nodes)

5. **Activity: Trigger_Spark_Gold_Job**
   - Notebook path: `/Workspace/banking_transaction_processing_pipeline/gold_aggregate`
   - Depends on: Trigger_Spark_Silver_Job success
   - Parameters: `batch_id`

6. **Activity: Post_Load_Validations**
   - Execute SQL script validating row counts, nulls, business rules
   - Store results in `banking_transaction_processing_pipeline_gold_validation_log`

7. **Activity: Send_Notification**
   - If all succeed: Send success email with row count summary
   - If fail: Send alert with error details

---

## Bronze Layer: Raw Ingest (20 Validations)

**Purpose:** Immutable, auditable raw data storage with comprehensive validation.

**Table Schema Example:** `banking_transaction_processing_pipeline_bro_source_a_raw`

```sql
CREATE TABLE banking_transaction_processing_pipeline_bro_source_a_raw (
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

spark = SparkSession.builder.appName("banking_transaction_processing_pipeline_bronze_validate").getOrCreate()

# Load Bronze raw data
bro_df = spark.read.parquet(f"/mnt/adls/bronze/banking_transaction_processing_pipeline_bro_source_a_raw/load_date={exec_date}")

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
        INSERT INTO banking_transaction_processing_pipeline_audit_validation_results (validation_id, layer, fail_count, check_ts)
        VALUES ('{val_id}', 'BRONZE', {fail_count}, current_timestamp())
        """)

print("Bronze validations complete")
```

---

## Silver Layer: Curated & Transformed (20 Transformation Scenarios)

**Purpose:** Cleansed, enriched, deduplicated, and integrated data ready for analytics.

**Table Example:** `banking_transaction_processing_pipeline_sil_transactions_curated`

```sql
CREATE TABLE banking_transaction_processing_pipeline_sil_transactions_curated (
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

spark = SparkSession.builder.appName("banking_transaction_processing_pipeline_silver_transform").getOrCreate()

# Load Bronze data
bro_df = spark.read.parquet(f"/mnt/adls/bronze/banking_transaction_processing_pipeline_bro_source_a_raw/load_date={exec_date}")

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
acct_df = spark.read.table("banking_transaction_processing_pipeline_dim_account")
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
    .partitionBy("load_date").save(f"/mnt/adls/silver/banking_transaction_processing_pipeline_sil_transactions_curated")

print("Silver transformation complete")
```

---

## Gold Layer: Analytics & Aggregations (20 Business Validations)

**Purpose:** Business-ready facts and dimensions for reporting and analytics.

**Table Example:** `banking_transaction_processing_pipeline_gld_fact_transactions`

```sql
CREATE TABLE banking_transaction_processing_pipeline_gld_fact_transactions (
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

spark = SparkSession.builder.appName("banking_transaction_processing_pipeline_gold_aggregate").getOrCreate()

# Load Silver data
sil_df = spark.read.table("banking_transaction_processing_pipeline_sil_transactions_curated")

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
acct_df = spark.read.table("banking_transaction_processing_pipeline_dim_account").select("account_key")
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
    INSERT INTO banking_transaction_processing_pipeline_gold_validation_log (validation_id, layer, fail_count, check_ts)
    VALUES ('{val_id}', 'GOLD', {count}, current_timestamp())
    """)

# Write fact table
gld_df.write.format("delta").mode("append").option("mergeSchema", "true") \
    .partitionBy("date_key").save(f"/mnt/adls/gold/banking_transaction_processing_pipeline_gld_fact_transactions")

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

