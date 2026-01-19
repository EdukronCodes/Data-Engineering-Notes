# Expanded Source Schemas, ER Diagrams, Facts & Dimensions

This standardized expansion provides five logical sources for the project and a canonical set of artifacts to be appended to project markdown files when a detailed schema is required.

NOTE: The artifacts below are design artifacts created for documentation and implementation planning. They are original work and may be used for internal design and implementation purposes.

Project-specific prefix: `{{PREFIX}}` (derived from filename: `{{FILENAME}}`).

---

### Source A: Ingest & Landing (Source: `{{PREFIX}}_ingest`)

Tables (20):
1. {{PREFIX}}_stg_raw
2. {{PREFIX}}_raw_records
3. {{PREFIX}}_dim_source_system
4. {{PREFIX}}_dim_data_owner
5. {{PREFIX}}_dim_file_type
6. {{PREFIX}}_ref_file_schema
7. {{PREFIX}}_fact_raw_events
8. {{PREFIX}}_stage_enrichments
9. {{PREFIX}}_dim_geo
10. {{PREFIX}}_dim_business_unit
11. {{PREFIX}}_audit_ingest
12. {{PREFIX}}_dim_environment
13. {{PREFIX}}_ref_parsing_errors
14. {{PREFIX}}_stage_cdc
15. {{PREFIX}}_dim_schema_version
16. {{PREFIX}}_fact_event_counts
17. {{PREFIX}}_audit_transforms
18. {{PREFIX}}_stage_retries
19. {{PREFIX}}_ref_mappings
20. {{PREFIX}}_dim_status

ER Diagram (ASCII):

{{PREFIX}}_fact_raw_events (event_id, source_system_id, record_key, payload_hash, event_ts)
  |-- source_system_id --> {{PREFIX}}_dim_source_system(source_system_id)
  |-- record_key --> {{PREFIX}}_raw_records(record_key)

Description: Ingest staging (immutable) → raw normalization → enrichment → audit. `{{PREFIX}}_fact_raw_events` is used for throughput and source health monitoring.

---

### Source B: Operational Logs & Metrics (Source: `{{PREFIX}}_ops`)

Tables (20):
1. {{PREFIX}}_stg_ops_logs
2. {{PREFIX}}_raw_ops
3. {{PREFIX}}_dim_service
4. {{PREFIX}}_dim_instance
5. {{PREFIX}}_dim_log_level
6. {{PREFIX}}_ref_error_codes
7. {{PREFIX}}_fact_logs
8. {{PREFIX}}_stage_alerts
9. {{PREFIX}}_dim_team
10. {{PREFIX}}_dim_region
11. {{PREFIX}}_audit_ops_ingest
12. {{PREFIX}}_ref_runbooks
13. {{PREFIX}}_stage_incidents
14. {{PREFIX}}_fact_incident_metrics
15. {{PREFIX}}_dim_priority
16. {{PREFIX}}_ref_maintenance_windows
17. {{PREFIX}}_audit_recon
18. {{PREFIX}}_stage_trimmed_logs
19. {{PREFIX}}_ref_retention_policy
20. {{PREFIX}}_dim_status

ER Diagram (ASCII):

{{PREFIX}}_fact_logs (log_id, service_id, instance_id, log_level, message_ts)
  |-- service_id --> {{PREFIX}}_dim_service(service_id)
  |-- instance_id --> {{PREFIX}}_dim_instance(instance_id)

---

### Source C: Governance & Catalog (Source: `{{PREFIX}}_gov`)

Tables (20):
1. {{PREFIX}}_stg_catalog
2. {{PREFIX}}_raw_catalog
3. {{PREFIX}}_dim_dataset
4. {{PREFIX}}_dim_owner
5. {{PREFIX}}_dim_tag
6. {{PREFIX}}_ref_policies
7. {{PREFIX}}_fact_data_quality
8. {{PREFIX}}_stage_lineage
9. {{PREFIX}}_dim_classification
10. {{PREFIX}}_dim_sensitivity
11. {{PREFIX}}_audit_policies
12. {{PREFIX}}_ref_sla
13. {{PREFIX}}_stage_certifications
14. {{PREFIX}}_fact_issues
15. {{PREFIX}}_dim_remediation_team
16. {{PREFIX}}_ref_controls
17. {{PREFIX}}_audit_certification
18. {{PREFIX}}_stage_policy_changes
19. {{PREFIX}}_ref_standards
20. {{PREFIX}}_dim_status

ER Diagram (ASCII):

{{PREFIX}}_fact_data_quality (dq_id, dataset_id, check_name, check_status, checked_ts)
  |-- dataset_id --> {{PREFIX}}_dim_dataset(dataset_id)

---

### Source D: Cost, Billing & Usage (Source: `{{PREFIX}}_cost`)

Tables (20):
1. {{PREFIX}}_stg_billing_records
2. {{PREFIX}}_raw_billing
3. {{PREFIX}}_dim_cost_center
4. {{PREFIX}}_dim_resource_type
5. {{PREFIX}}_dim_region
6. {{PREFIX}}_ref_price_catalog
7. {{PREFIX}}_fact_cost_usage
8. {{PREFIX}}_stage_allocations
9. {{PREFIX}}_dim_tagging
10. {{PREFIX}}_dim_currency
11. {{PREFIX}}_audit_billing_ingest
12. {{PREFIX}}_ref_discounts
13. {{PREFIX}}_stage_corrections
14. {{PREFIX}}_fact_monthly_costs
15. {{PREFIX}}_dim_billing_account
16. {{PREFIX}}_ref_chargeback_rules
17. {{PREFIX}}_audit_allocations
18. {{PREFIX}}_stage_forecasts
19. {{PREFIX}}_ref_rates
20. {{PREFIX}}_dim_status

ER Diagram (ASCII):

{{PREFIX}}_fact_cost_usage (usage_id, resource_id, cost_amount, currency, start_ts, end_ts)
  |-- resource_id --> {{PREFIX}}_dim_resource_type(resource_id)
  |-- cost_center_id --> {{PREFIX}}_dim_cost_center(cost_center_id)

---

### Source E: Canonical Transactions / Facts (Source: `{{PREFIX}}_txn`)

Tables (20):
1. {{PREFIX}}_stg_transactions
2. {{PREFIX}}_raw_transactions
3. {{PREFIX}}_dim_account
4. {{PREFIX}}_dim_customer
5. {{PREFIX}}_dim_product
6. {{PREFIX}}_ref_exchange_rates
7. {{PREFIX}}_fact_transactions
8. {{PREFIX}}_stage_reconciliations
9. {{PREFIX}}_dim_channel
10. {{PREFIX}}_dim_merchant
11. {{PREFIX}}_audit_txn_ingest
12. {{PREFIX}}_ref_fee_schedule
13. {{PREFIX}}_stage_settlements
14. {{PREFIX}}_fact_settlements
15. {{PREFIX}}_dim_status
16. {{PREFIX}}_ref_limits
17. {{PREFIX}}_audit_recon
18. {{PREFIX}}_stage_adjustments
19. {{PREFIX}}_fact_balance_snapshots
20. {{PREFIX}}_dim_time

ER Diagram (ASCII):

{{PREFIX}}_fact_transactions (transaction_id, account_id, amount, currency, txn_type, posted_ts)
  |-- account_id --> {{PREFIX}}_dim_account(account_id)
  |-- customer_id --> {{PREFIX}}_dim_customer(customer_id)
  |-- product_id --> {{PREFIX}}_dim_product(product_id)

Common guidance:
- Always keep an immutable staging/raw zone for auditable ingestion.
- Use `audit_*` tables and checksums for reconciliation between source and target facts.
- Implement SCD patterns for dimensions where history is required.
- Register datasets in a data catalog and apply RBAC and PII protections as required.
