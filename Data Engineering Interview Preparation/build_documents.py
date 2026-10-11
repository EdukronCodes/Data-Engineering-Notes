from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'Azure_Data_Engineering_Portfolio'
PROJECTS = ROOT / 'projects'
RESUMES = ROOT / 'resumes'
PROJECTS.mkdir(parents=True, exist_ok=True)
RESUMES.mkdir(parents=True, exist_ok=True)

sources = '''- [Fabric medallion lakehouse architecture](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture)
- [Fabric end-to-end lakehouse tutorial](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-introduction)
- [ADF incremental ingestion with watermarks](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-portal)
- [Azure Databricks MERGE reference](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)
- [Azure Databricks change data feed](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed)
- [Microsoft Purview governance setup](https://learn.microsoft.com/en-us/purview/data-governance-get-started)
'''

projects = [
dict(id='01', slug='citi_fabric_banking_analytics', client='Citi Bank (EMEA)', title='Enterprise Banking Data Analytics Platform on Microsoft Fabric', focus='Azure Data Engineer / Microsoft Fabric Data Engineer',
problem='Unify regional banking feeds into a consistent analytical model for balances, transaction activity, product performance, and customer reporting.',
stack='Microsoft Fabric Data Factory pipelines, Fabric Spark notebooks, OneLake Delta Lakehouses, Fabric SQL analytics endpoint, Power BI semantic models; Azure ADLS Gen2 for external landing where needed, Azure Key Vault for supported external connections, Microsoft Entra ID, Microsoft Purview, Azure DevOps.',
inputs='Illustrative sources: core banking transaction extracts, account master, customer master, branch hierarchy, product reference, daily FX rates, and general-ledger control totals. No access to actual Citi systems is assumed.',
flow='Core banking / approved regional extracts --> Azure landing or gateway --> Fabric pipeline --> OneLake bronze --> Fabric Spark silver --> gold Delta tables --> Power BI semantic model --> approved EMEA analytics users',
model=[('dim_customer','One customer version per effective interval','customer_sk, customer_id, segment, country_code, valid_from, valid_to'),('dim_account','One account version per effective interval','account_sk, account_id, customer_id, product_code, status'),('fact_transaction','One posted transaction line','transaction_id, line_id, account_sk, event_ts, amount, currency_code'),('fact_daily_balance','One account per business date','account_sk, business_date, closing_balance, currency_code'),('fact_fx_rate','One currency pair per rate date and rate type','rate_date, from_currency, to_currency, rate_type, fx_rate')],
steps=[('Define reporting contracts','Agree business date by source timezone, reporting currency, transaction grain, reversal handling, balance type, and approved country visibility. Preserve original amounts and rate provenance.'),('Ingest regional feeds','Use Fabric pipeline Copy activities through supported connections/gateways. Land files under source/entity/business_date/run_id. Record source count, extract boundary, checksum, and manifest before processing.'),('Build bronze tables','Fabric notebooks read immutable landed records with an explicit schema and append source_system, ingestion_ts, run_id, and file_name. Keep malformed rows in a separate restricted dataset.'),('Conform silver entities','Normalize timestamp/currency formats; deduplicate transaction line keys by source sequence; resolve account and customer identities. Apply changes and reversals from source semantics. Use Spark Delta writes for Lakehouse mutations.'),('Produce gold banking facts','Join transactions to account/customer versions as of event time. Use decimal types for money; join the approved dated FX rate and preserve its identifier. Generate balances from an authoritative balance feed or an agreed opening-balance calculation.'),('Reconcile and publish','Compare counts and sums by region, currency, source ledger, and business date before publishing a gold batch. Build Power BI measures for net activity and balances with explicit measure definitions; prevent summing balances across dates.'),('Secure and operate','Separate engineering and consumer access. Test Power BI country/region row filters with real role test identities. Validate Lakehouse/OneLake permissions separately because semantic-model filters do not secure underlying files.')],
sql='''-- Spark SQL executed in a Fabric notebook against pre-created Delta tables.
-- Source must contain at most one latest row for each transaction line.
MERGE INTO silver.transaction AS t
USING staging.transaction_latest AS s
ON t.source_system = s.source_system
 AND t.transaction_id = s.transaction_id AND t.line_id = s.line_id
WHEN MATCHED AND s.source_sequence > t.source_sequence THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;''',
checks=['Reconcile source transaction counts and signed decimal amounts by currency and business date; never combine currencies before conversion.','Quarantine missing FX rates and unknown accounts instead of silently substituting zero or today\'s rate.','Test duplicate transaction lines, reversals, late postings, daylight-saving boundaries, and closed accounts.','For daily balances, prove that a selected date reports the correct snapshot rather than a sum of historical snapshots.'],
scenario='A late regional transaction arrives for yesterday. Reprocess the affected business date, resolve the historical account version and dated FX rate, rerun currency-level control totals, then release a replacement gold partition. Consumers see only the accepted publication.',
tradeoff='Fabric brings orchestration, Spark, OneLake and BI together, but capacity contention and access boundaries need deliberate design. ADLS is an external landing option, not a replacement name for OneLake. The Lakehouse SQL endpoint serves queries; Spark performs Delta table mutations.',
bullets=['Built [verified scope] Fabric ingestion pipelines and Spark transformations for banking transactions, account data, and daily balances.','Implemented bronze/silver/gold Delta tables in OneLake with replayable batches and source-to-target financial reconciliation.','Delivered reporting-ready banking facts and Power BI semantic models with tested regional access controls.','Reduced [measured runtime/manual effort] from [baseline] to [result] through [verified optimization].']),
dict(id='02', slug='barclays_rft_ukc_gen3_modernization', client='Barclays (RFT-UKC Gen3)', title='Azure Data Lake Modernization', focus='Azure Data Engineer / Lakehouse Migration Engineer',
problem='Modernize an illustrative legacy analytical platform into an Azure lakehouse while preserving financial outputs, business rules, and controlled cutover.',
stack='Azure Data Factory, self-hosted integration runtime where required, ADLS Gen2, Azure Databricks with Delta Lake and Unity Catalog, Azure SQL Database for orchestration metadata, Azure Key Vault, Microsoft Entra ID, Microsoft Purview, Azure Monitor/Log Analytics, Azure DevOps.',
inputs='Illustrative sources: legacy warehouse tables, relational source extracts, scheduled file deliveries, account/reference data, position snapshots, and historical partitions. Expand RFT/UKC/Gen3 only using confirmed internal definitions.',
flow='Legacy warehouse / files --> ADF + integration runtime --> ADLS immutable landing --> Databricks bronze --> conformed silver --> gold risk/finance datasets --> Databricks SQL / Power BI',
model=[('migration_inventory','One source entity and migration version','entity_id, source_object, owner, extract_method, rule_version'),('position_snapshot','One instrument/account/book per business date','position_id, book_id, account_id, instrument_id, business_date, quantity'),('reference_instrument','One instrument version per effective interval','instrument_id, asset_class, currency_code, valid_from, valid_to'),('migration_reconciliation','One comparison per entity/date/control','entity_id, business_date, control_name, legacy_value, azure_value, status')],
steps=[('Inventory and baseline','Document upstream/downstream dependencies, schedules, historical volume, source keys, deletion semantics, existing transformation rules, and reconciliation controls. Capture representative legacy output before rewriting logic.'),('Build the Azure foundation','Create environment-specific storage, Databricks workspaces, identity/access configuration, catalog schemas, secrets, and metadata tables. Configure private connectivity and DNS where required; validate source connectivity before scheduling loads.'),('Backfill history','Extract immutable historical date/key ranges with ADF. Use chunk manifests and bounded concurrency to protect source systems. Convert landed data to bronze Delta with schema contracts; make each chunk independently replayable.'),('Catch up changes','Capture a consistent snapshot boundary and ingest later changes from that boundary. Use source-supported CDC for inserts/updates/deletes or timestamp ingestion only where its limitations are acceptable.'),('Port transformation rules','Implement conformed silver types, stable business keys, SCD dimensions, and gold aggregates in PySpark/SQL. Version every translated rule and record intentional differences from the legacy logic.'),('Run parallel reconciliation','Compare legacy and Azure row counts, keyed records, missing keys, and decimal totals over agreed representative periods. Resolve discrepancies by rule and source; preserve signed-off evidence.'),('Cut over and retire','Freeze the publication boundary, drain the change backlog, reconcile, then switch approved consumers. Keep the legacy route available for an agreed rollback period. Retire legacy jobs only after business and operational acceptance.')],
sql='''-- Azure Databricks SQL; staging has one ordered latest change per key.
MERGE INTO silver.position AS t
USING staging.position_latest AS s
ON t.position_id = s.position_id AND t.business_date = s.business_date
WHEN MATCHED AND s.source_sequence > t.source_sequence
 AND s.operation = 'DELETE' THEN DELETE
WHEN MATCHED AND s.source_sequence > t.source_sequence THEN UPDATE SET *
WHEN NOT MATCHED AND s.operation <> 'DELETE' THEN INSERT *;''',
checks=['Compare record-level hashes after canonical formatting; confirm business meaning through independent totals and key-level samples.','Prove historical backfill plus catch-up has neither a gap nor duplicate publication at the snapshot boundary.','Exercise source deletion, corrected historical positions, schema change, and partially failed extraction chunks.','Measure query and pipeline performance under representative concurrency before choosing cluster sizes.'],
scenario='A backfill chunk fails while catch-up continues. Resume only the failed chunk using its saved boundary and manifest. Do not advance the entity\'s accepted migration boundary until its reconciliation passes; pause consumer cutover if any critical control differs.',
tradeoff='A lift-and-shift speeds initial parity; redesign can improve maintainability but changes more rules at once. Establish parity first and optimize in separately measured increments. Source CDC and Delta change data feed are distinct: downstream Delta CDF cannot capture changes never ingested from the source.',
bullets=['Migrated [verified entities/history] from a legacy platform to ADLS Gen2 and Azure Databricks using ADF orchestration.','Implemented restartable backfill, incremental processing, and schema validation with Delta Lake.','Translated legacy business rules into PySpark/SQL and validated outputs through parallel reconciliation.','Improved [measured processing/query metric] by [verified amount] and supported a controlled consumer cutover.']),
dict(id='03', slug='bnp_enterprise_datahub', client='BNP Paribas', title='Enterprise Datahub and Data Integration Platform', focus='Azure Data Engineer / Data Integration Engineer',
problem='Provide reusable ingestion and standardized data products for multiple enterprise domains with clear contracts, ownership, and controlled consumption.',
stack='Azure Data Factory, ADLS Gen2, Azure Databricks/Delta Lake, Azure SQL Database metadata store, Azure Event Hubs for event sources where required, Azure Key Vault, Microsoft Entra ID, Microsoft Purview, Azure Monitor, Azure DevOps; Azure API Management and Azure Functions for narrowly scoped data APIs.',
inputs='Illustrative sources: customer and account databases, payment files, reference APIs, domain extracts, and optional business-event streams. Specific source products and business rules require confirmation.',
flow='Databases / files / APIs / optional events --> ADF or Event Hubs --> ADLS bronze --> Databricks domain silver --> governed gold data products --> SQL/Power BI/file exports or approved API',
model=[('entity_contract','One entity contract version','entity_id, version, owner, grain, key_columns, schema_uri, freshness_target'),('customer_crosswalk','One source customer mapped to enterprise identity','source_system, source_customer_id, enterprise_customer_id, match_method'),('payment','One payment lifecycle event','payment_id, event_id, event_ts, status, amount, currency_code'),('data_product_manifest','One released data product version','product_id, version, schema_version, accepted_run_id, owner, published_at')],
steps=[('Define contracts and domain ownership','Assign an owner for each domain and specify keys, types, nullable fields, retention, freshness, supported changes, and permitted consumers. Avoid treating similarly named source fields as identical without agreement.'),('Create metadata-driven onboarding','Register source connector, validated source object, extraction strategy, target paths, schema version, dependency list, and controls in Azure SQL. ADF orchestrates approved entity configurations; never execute unrestricted configuration text as SQL.'),('Handle each ingestion mode','Use Copy activities for supported database/file sources; implement API pagination, rate-limit retry, and cursor handling. For events, use Event Hubs and a dedicated checkpointed Spark stream; do not force streaming sources into a daily file schedule.'),('Standardize domain silver','Normalize codes and data types while retaining source identifiers. Build governed crosswalks for customer/account identity. Preserve ambiguous matches for stewardship instead of assigning identities through an unexplained heuristic.'),('Publish versioned products','Generate gold datasets with documented grain, compatibility rules, owner, lineage and quality results. Publish a manifest only after validation. Provide SQL and file delivery for bulk use; APIs read a serving store with appropriate request limits.'),('Protect consumer contracts','Expose stable views for compatible schema evolution. For breaking changes, release a separate version and deprecation window. Test downstream consumers before retiring the old contract.'),('Operate onboarding and lineage','Track source-to-product run IDs, automatically captured lineage where supported, and documented/custom lineage where needed. Alert owners on freshness or contract violations and capture consumer-facing incident status.')],
sql='''-- Example contract metadata in Azure SQL Database.
CREATE TABLE dbo.entity_contract (
 entity_id varchar(100) NOT NULL,
 contract_version int NOT NULL,
 domain_name varchar(100) NOT NULL,
 owner_group varchar(200) NOT NULL,
 schema_uri nvarchar(1000) NOT NULL,
 load_strategy varchar(20) NOT NULL,
 is_active bit NOT NULL,
 CONSTRAINT PK_entity_contract PRIMARY KEY(entity_id, contract_version),
 CONSTRAINT CK_load_strategy CHECK(load_strategy IN ('SNAPSHOT','WATERMARK','CDC','EVENT'))
);''',
checks=['Validate a new source against the registered contract before it enters the shared domain table.','Test paginated API failure after page N, replayed events, and a schema that removes a required field.','Prove every released product has an owner, source lineage, access policy, run ID and quality outcome.','Check that customer crosswalk changes do not silently rewrite historical identities.'],
scenario='An upstream API adds an optional field and later changes the type of a key. Accept the optional field only under the contract\'s evolution policy; block the incompatible key change, retain raw payloads, and resume from the saved cursor after a versioned migration.',
tradeoff='A generic ingestion framework reduces repeated plumbing but does not replace source-specific semantics. Keep contract validation and orchestration reusable, while domain transformations remain explicit. Purview lineage coverage depends on connector/workload support and must be verified.',
bullets=['Developed a metadata-driven Azure ingestion framework for [verified source types/entities] using ADF and ADLS Gen2.','Built domain-level Delta datasets and reusable data products with schema contracts and publication controls.','Integrated [verified API/file/event sources] with pagination, replay, and incremental processing.','Established ownership, lineage, and access patterns for [verified number] enterprise data products.']),
dict(id='04', slug='synchrony_data_quality_governance', client='Synchrony Financial', title='Enterprise Data Quality and Governance', focus='Azure Data Engineer / Data Quality Engineer',
problem='Make customer, account, and credit-related analytical data measurable, traceable, and suitable for governed reporting through automated controls and accountable remediation.',
stack='ADLS Gen2, Azure Data Factory, Azure Databricks/Delta Lake, Azure SQL Database for rule metadata, Microsoft Purview for supported catalog/governance capabilities, Microsoft Entra ID, Azure Key Vault, Azure Monitor/Log Analytics, Power BI, Azure DevOps.',
inputs='Illustrative sources: customer profiles, account snapshots, statement balances, payment data, approved product/reference lists, and existing curated datasets. Sensitive financial and personal attributes require approved classification and access policies.',
flow='Source/curated data --> ADF orchestration --> Databricks validation --> accepted silver + restricted quarantine + DQ results --> governed gold --> Power BI quality scorecards; Purview catalogs supported assets and ownership',
model=[('dq_rule','One version of one quality rule','rule_id, version, entity_id, dimension, severity, rule_expression, owner'),('dq_result','One rule result per run and partition','run_id, rule_id, rule_version, tested_count, failed_count, threshold, status'),('dq_exception','One failed record/rule combination','run_id, record_reference, rule_id, reason_code, remediation_status'),('product_quality_gate','One product publication assessment','product_id, run_id, critical_passed, accepted_at, approved_by')],
steps=[('Identify critical data elements','Meet product owners and stewards to classify fields, establish their business meaning, and distinguish contractual validity from analytical plausibility. Capture owners and evidence requirements for rule approval.'),('Design versioned rule metadata','Define completeness, validity, uniqueness, consistency, freshness, and source reconciliation rules. Store severity, eligibility denominator, threshold, effective version, owner, and approved parameter values.'),('Implement deterministic evaluation','Run approved PySpark/SQL validators against a pinned input batch. Execute built-in typed rules rather than arbitrary untrusted Python. Persist rule-level counts and record references with the rule version and source run.'),('Quarantine and gate publication','Restrict rejected payloads because they can contain personal information. Block gold publication for failed critical controls. Advisory failures can be published with an explicit status only under an approved product policy.'),('Catalog and govern','Register supported assets in Microsoft Purview, assign classifications/owners/glossary terms, and verify available lineage. Enforce actual access in storage, Databricks, identity, and serving layers; catalog classifications alone do not enforce all permissions.'),('Remediate and rerun','Route exceptions to the assigned owner through the agreed workflow. Correct at the source when possible, document approved overrides with expiry, replay the affected partition and resolve the exception only after revalidation.'),('Report trends and coverage','Build Power BI views of failure rate, critical-rule pass rate, freshness, coverage, exception age and reopened incidents. Show denominators and rule versions so score changes remain interpretable.')],
sql='''-- Spark SQL example: preserve a result for every tested record.
CREATE OR REPLACE TEMP VIEW account_validation AS
SELECT account_id, business_date, run_id,
       CASE WHEN account_id IS NULL THEN 'MISSING_ACCOUNT_ID'
            WHEN currency_code IS NULL OR length(currency_code) <> 3
              THEN 'INVALID_CURRENCY_FORMAT'
            ELSE NULL END AS reason_code
FROM bronze.account_snapshot;
-- Format is one rule; validate actual currency membership separately
-- against an approved reference table. Do not treat every negative
-- balance as invalid: eligibility depends on the business contract.''',
checks=['Test every rule with valid, invalid, null, boundary and ineligible records; denominators exclude only explicitly ineligible rows.','Prove a critical failure blocks publication and an approved advisory failure follows its documented policy.','Verify exception tables, logs, exports and dashboards do not expose restricted values to general consumers.','Reproduce a previous result using the same input snapshot and rule version.'],
scenario='A source introduces an unexpected account-status code. Retain raw records, quarantine the affected rows, fail the critical membership rule and hold the product. The steward validates the new code, approves a new reference/rule version, and authorizes replay with traceable results.',
tradeoff='This design uses a custom Databricks quality framework so rules can be versioned and evaluated across ingested datasets. Native Purview quality features may be used only after validating connector, region, licensing and feature availability; do not assume identical coverage for every asset.',
bullets=['Implemented a versioned PySpark/SQL data quality framework covering [verified entities and rules].','Built restricted quarantine, exception tracking, and publication gates for critical financial data controls.','Cataloged [verified scope] data assets in Microsoft Purview and documented ownership and lineage.','Improved [measured quality/exception metric] from [baseline] to [result] through automated validation and remediation.']),
dict(id='05', slug='barclays_rftbsl_srp_warehouse', client='Barclays (RFTBSL & SRP)', title='Financial Data Warehouse Integration', focus='Azure Data Engineer / Financial ETL Developer',
problem='Integrate financial subledger, journal, reference, and reporting feeds into a reconciled dimensional warehouse with historical traceability.',
stack='Azure Data Factory, ADLS Gen2, Azure Databricks for complex transformations, Azure Synapse Analytics dedicated SQL pool for dimensional serving, Azure SQL Database for pipeline metadata, Azure Key Vault, Microsoft Entra ID, Microsoft Purview, Azure Monitor, Azure DevOps, Power BI.',
inputs='Illustrative sources: journal lines, trial-balance extracts, subledger balances, legal-entity hierarchy, chart of accounts, reporting mappings and FX rates. Preserve RFTBSL/SRP as supplied labels until their internal definitions are confirmed.',
flow='Subledgers / GL / reporting feeds --> ADF --> ADLS raw --> Databricks standardized Delta --> immutable curated Parquet batch --> Synapse staging --> dimensions/facts --> reporting views / Power BI',
model=[('dim_legal_entity','One legal entity version per effective interval','legal_entity_sk, entity_code, parent_code, valid_from, valid_to'),('dim_gl_account','One account/mapping version per effective interval','gl_account_sk, account_code, reporting_line, valid_from, valid_to'),('fact_journal_line','One source journal line','source_system, journal_id, line_id, posting_date, debit_amount, credit_amount, currency_code'),('fact_trial_balance','One entity/account/currency/period snapshot','entity_sk, gl_account_sk, period_key, currency_code, debit_total, credit_total'),('reconciliation_control','One financial control per load','run_id, source_system, entity_code, period_key, control_name, difference, status')],
steps=[('Agree accounting and reporting rules','Define signed debit/credit convention, chart-of-account mappings, legal-entity hierarchy, fiscal periods, adjustment handling, FX policies and journal line keys. Reporting labels do not establish these rules automatically.'),('Land and validate extracts','Use ADF for immutable bounded batches; record file manifests and source control totals. Reject incomplete deliveries and unsupported schemas before transformation.'),('Standardize and reconcile','Use Databricks to parse decimal amounts, normalize codes and preserve source line identifiers. Validate debit/credit balancing at the agreed scope and compare subledger versus GL totals without hiding unexplained differences.'),('Load effective-dated dimensions','Maintain stable surrogate keys and nonoverlapping validity intervals. Resolve journal facts against dimension versions effective on the posting date. Put unknown mappings into a controlled suspense process.'),('Load warehouse staging','Export the accepted Delta batch as curated Parquet to ADLS and use a supported Synapse load path such as COPY INTO. Load batch-isolated staging, validate keys, then use a dedicated-pool-supported set-based publish transaction.'),('Publish finance facts','Load dimensions before facts, validate reconciliation, then commit the accepted batch. Use tested insert/update/delete patterns compatible with the chosen Synapse release; do not assume Databricks Delta MERGE syntax works in the SQL pool.'),('Serve and close periods','Create reporting views with explicit amount and period definitions, publish semantic models, and record a close-state/version for approved periods. Reopen and republish historical periods only through the agreed approval workflow.')],
sql='''-- Azure Databricks Spark SQL: transaction-currency journal control.
SELECT source_system, legal_entity_code, journal_id, currency_code,
       SUM(CAST(debit_amount AS DECIMAL(28, 6))) AS total_debit,
       SUM(CAST(credit_amount AS DECIMAL(28, 6))) AS total_credit,
       SUM(CAST(debit_amount AS DECIMAL(28, 6)))
         - SUM(CAST(credit_amount AS DECIMAL(28, 6))) AS difference
FROM silver.journal_line
WHERE run_id = :run_id
GROUP BY source_system, legal_entity_code, journal_id, currency_code;
-- Apply the agreed balancing scope and rounding tolerance;
-- some journal contracts require a different balancing scope.''',
checks=['Validate uniqueness at source system + journal ID + line ID and prove reversals remain linked to original entries.','Reconcile source-to-stage-to-fact counts and amounts by legal entity, currency, period and source.','Test changes to historical account mappings and demonstrate correct as-of dimension resolution.','Check dimensional load atomicity and distribution skew under representative fact volume.'],
scenario='A corrected journal arrives after a reporting period is closed. Retain it in landing and flag the impacted period. Follow the authorized reopen/correction policy, resolve historical mappings, rerun balancing and source controls, then publish a traceable reporting revision.',
tradeoff='Synapse dedicated SQL pool is useful for warehouse-style serving but needs distribution, load and workload tuning. Use measured high-cardinality join keys for large fact distribution and replicate only suitably small dimensions. Lakehouse and warehouse add separate copies and reconciliation points.',
bullets=['Integrated [verified finance feeds] using ADF, ADLS Gen2, Azure Databricks, and Synapse Analytics.','Developed dimensional models, historical account mappings, and journal/trial-balance facts.','Implemented financial reconciliation and controlled period-based publication for [verified reporting scope].','Optimized [verified warehouse load/query] from [baseline] to [result] using [measured tuning change].']),
dict(id='06', slug='mobistar_telecom_warehouse', client='Mobistar', title='Telecom Data Warehouse Transformation', focus='Azure Data Engineer / Telecom Data Engineer',
problem='Transform high-volume telecom usage and subscriber/billing feeds into reliable analytical facts for usage, billing comparison, and network/service performance.',
stack='Azure Event Hubs for event ingestion where justified, Azure Data Factory for batch feeds, ADLS Gen2, Azure Databricks Structured Streaming and Delta Lake, Databricks SQL, Azure Key Vault, Microsoft Entra ID, Microsoft Purview, Azure Monitor/Log Analytics, Azure DevOps, Power BI.',
inputs='Illustrative sources: call-detail records (CDRs), data-session events, subscriber/account master, tariff versions, cell/site reference, and billing extracts. A modern Azure redesign does not imply Azure was used during any historical Mobistar engagement.',
flow='CDR/session producers --> Event Hubs --> Databricks checkpointed stream --> bronze Delta; billing/subscriber files --> ADF --> ADLS --> bronze; bronze --> silver usage + dimensions --> gold daily facts --> Databricks SQL / Power BI',
model=[('fact_usage_event','One immutable source usage event','source_system, event_id, subscriber_id, event_ts, service_type, duration_sec, bytes_used, cell_id'),('dim_subscriber','One subscriber version per effective interval','subscriber_sk, subscriber_id, plan_id, status, valid_from, valid_to'),('dim_tariff','One tariff version per effective interval','tariff_sk, plan_id, unit_type, unit_rate, valid_from, valid_to'),('fact_daily_usage','One subscriber/service/date aggregation','subscriber_sk, usage_date, service_type, event_count, duration_sec, bytes_used'),('billing_comparison','One account/service/billing-period comparison','account_id, billing_period, expected_charge, billed_charge, difference')],
steps=[('Define event semantics','Specify a globally stable source event key, event timestamp timezone, duration/volume units, producer sequence, correction semantics and privacy policy for subscriber/location identifiers.'),('Build dual ingestion paths','Write Event Hubs events to bronze with source envelope metadata and durable checkpoints. Use ADF for billing and reference files, with delivery manifests and bounded extraction. Partitioning strategy follows measured throughput and query needs.'),('Parse and validate usage','Use explicit schemas; quarantine invalid payloads and impossible units according to contract. Retain raw timestamps and normalize to UTC. Ensure masked identifiers remain joinable only through approved controlled mappings.'),('Handle duplication and late events','Apply a stated event-time watermark for bounded streaming deduplication. Keep durable event keys and a reconciliation/backfill process for arrivals outside the streaming horizon; watermarking alone does not eliminate every future replay.'),('Enrich historical context','Resolve subscriber and tariff versions using event time. Determine expected usage charges only from approved tariff rules, including rounding, bundles and promotions. Avoid treating duration multiplied by unit rate as a complete billing engine.'),('Build usage and billing products','Aggregate accepted events by usage date, subscriber and service. Rebuild affected dates for late corrections; compare approved expected charges with billing extracts at the agreed account/period scope.'),('Operate streaming and serving','Monitor input rate, processing latency, checkpoint health and event lag. Scale based on measured bottlenecks. Publish governed SQL datasets and dashboards; explicitly handle expired Event Hubs retention through retained bronze/archive data.')],
sql='''-- Spark SQL on accepted silver usage, using UTC dates in this example.
SELECT subscriber_id, CAST(event_ts AS DATE) AS usage_date, service_type,
       COUNT(*) AS event_count,
       SUM(CAST(duration_sec AS BIGINT)) AS duration_sec,
       SUM(CAST(bytes_used AS BIGINT)) AS bytes_used
FROM silver.usage_event
WHERE CAST(event_ts AS DATE) = :affected_date
GROUP BY subscriber_id, CAST(event_ts AS DATE), service_type;
-- Rebuild and replace the affected gold date only after checks pass;
-- do not append a second aggregate for the same business key.''',
checks=['Replay duplicate events both inside and outside the watermark horizon; prove durable publication does not double count.','Test out-of-order events, malformed timestamps, plan changes at midnight and tariff version overlaps.','Compare aggregate duration/bytes/counts with source controls using compatible units and dates.','Simulate checkpoint recovery and a source outage longer than broker retention using a retained archive.'],
scenario='A stream restarts and replays an older CDR batch. Reuse its durable checkpoint where valid, deduplicate against stable event keys, reconcile the impacted days, and rebuild those gold dates. If offsets expired, recover from retained raw data rather than assuming Event Hubs still contains the events.',
tradeoff='Streaming improves freshness but introduces state, checkpoints, late-event policy and ongoing compute cost. Use batch for feeds whose freshness contract permits it. Separate operational event latency from the completeness of billing-period data.',
bullets=['Developed Azure batch and [if verified] streaming pipelines for telecom usage, subscriber, and billing datasets.','Implemented CDR parsing, durable event deduplication, late-event handling, and historical subscriber enrichment.','Created daily usage facts and billing-comparison datasets using Azure Databricks and Delta Lake.','Improved [measured freshness/processing metric] from [baseline] to [result] across [verified volume].'])
]

common_ops = '''## Deployment and production ownership

- Keep development, test, and production resources and identities separate. Provision Azure resources through reviewed Bicep/Terraform and deploy notebooks, SQL, configuration, and pipeline definitions through Azure DevOps.
- Run schema/contract checks and transformation tests on synthetic or approved masked data, followed by integration validation in test. Promote the same reviewed artifact with environment-specific parameters.
- Store supported secrets in Azure Key Vault; prefer managed identity or approved workload identity wherever the connector supports it. Do not embed secrets in notebooks or Markdown.
- Version contracts, business rules and published schemas. Take a recovery point before a destructive schema migration; validate both application rollback and data rollback.
- Record run ID, entity, source boundary, input/output counts, reconciliation result, quality status, execution time and publication ID. Monitor freshness separately from job success.
- Agree actual freshness target, RPO, RTO, support owner and escalation route before go-live. Targets in an interview must be verified, not invented.

## Security implementation

Use Microsoft Entra ID groups and least-privilege workload identities. Apply ADLS RBAC and ACLs, Databricks Unity Catalog grants or Fabric workload/OneLake permissions as appropriate. Limit storage network access through supported private networking, firewalls and validated DNS configuration. Review Fabric connectivity separately; Azure Private Link assumptions do not automatically apply to every Fabric workload. Restrict raw and quarantine zones, mask sensitive attributes in test and consumer datasets, and keep personal data out of logs. Configure Power BI access and row-level security independently of direct data access. Agree residency, retention and deletion requirements with the data owner rather than claiming a platform configuration guarantees compliance.

## Implementation deliverables and release evidence

1. Source inventory, data contract, sample input and expected output.
2. Architecture and identity/connectivity design approved for the environment.
3. Pipeline definitions, notebooks, SQL transformations and configuration metadata.
4. Model dictionary with grain, keys, decimal precision and historical behavior.
5. Test fixtures/results, source reconciliation and signed acceptance record.
6. CI/CD definition, infrastructure code, rollback procedure and cost baseline.
7. Lineage documentation, ownership/access matrix, operating dashboard and runbook.

These documents describe the implementation; they are not a deployed platform or evidence of work performed for the named client. Use the shared implementation handbook for code patterns, an executable build sequence, recovery handling and acceptance templates.
'''

for p in projects:
    tables='| Dataset | Grain | Example columns |\n|---|---|---|\n'+'\n'.join('| '+' | '.join(row)+' |' for row in p['model'])
    steps='\n\n'.join(f"### {i}. {title}\n\n{body}" for i,(title,body) in enumerate(p['steps'],1))
    checks='\n'.join('- '+c for c in p['checks'])
    bullets='\n'.join('- '+b for b in p['bullets'])
    doc=f'''# {p['client']}: {p['title']}

> Evidence status: the client and project labels were supplied by the user. Architecture, datasets, responsibilities and implementation below are proposed reference designs for preparation. They are not verified descriptions of a client's internal platform. Replace illustrative details with actual experience before using them as employment claims.

## Project profile

- Target role: {p['focus']}.
- Employer: [actual employer]; client engagement dates: [MM YYYY–MM YYYY].
- Contribution: [what you personally designed/built/operated]; team: [verified size and roles].
- Scale: [verified daily volume, entity count and historical size].
- Outcomes: [baseline, measured result, period and measurement method].

## Business objective

{p['problem']}

## Azure and Microsoft technology stack

{p['stack']}

{p['inputs']}

## End-to-end architecture

```text
{p['flow']}
Cross-cutting: identity + access | quality + reconciliation | metadata + lineage | CI/CD + monitoring
```

The source owner provides bounded, identifiable deliveries. Engineering preserves raw input, applies explicit business rules, validates the result and releases only an accepted dataset. Consumers receive a defined product with an owner and freshness contract.

## Data model

{tables}

All names and columns are illustrative. Confirm uniqueness, source precedence, null handling, timezones, history policy and retention before implementing physical tables. A snapshot fact and an event fact require different aggregation rules.

## Technical implementation

{steps}

## Project-specific SQL example

The snippet illustrates one transformation/control, not an executable project by itself. Create the referenced tables, bind parameters using the selected runtime's supported API, and validate input contracts first.

```sql
{p['sql']}
```

## Validation and acceptance

{checks}
- Replay the same accepted input twice and verify the business output is unchanged.
- Obtain approval from the business owner using source/control evidence before consumer cutover.

## Failure and recovery example

{p['scenario']}

Do not advance accepted source state when extraction, validation or publication fails. Resume from durable input and the last accepted boundary; do not resolve data differences by blindly rerunning downstream reports.

## Architecture tradeoff to explain in interviews

{p['tradeoff']}

{common_ops}

## Interview walkthrough

Use this sequence with your actual details: explain the business requirement; identify sources and their grain; draw the end-to-end flow; explain your personal contribution; describe one transformation and one control; walk through a failure/recovery; explain a measured optimization and its tradeoff; state the accepted result.

Practice these questions:

1. Why were these Azure services selected, and what alternative did you evaluate?
2. How were inserts, updates, deletes, duplicates and late data handled?
3. What proved the published data was complete and financially/operationally correct?
4. How did you prevent exposure through raw files, SQL, BI and exception logs?
5. How did you deploy, roll back, replay and recover the platform?
6. Which parts did you personally implement, and what evidence supports the claimed impact?

## Resume-ready project bullets — use only if verified

{bullets}

## Technical references

The following official references support the platform patterns, not the named client's implementation.

{sources}
'''
    (PROJECTS/f"{p['id']}_{p['slug']}.md").write_text(doc,encoding='utf-8')

handbook = '''# Shared Azure implementation handbook

This is a reference implementation guide for the six proposed project designs. Code uses illustrative tables and schemas. It requires Azure resources, approved source access, runtime configuration and synthetic/approved test data; the Markdown files do not provision or run Azure services.

## 1. Build sequence

1. Select one project and define a minimal vertical slice: one source entity, one transformation, one validated gold dataset and one consumer query.
2. Create a development Azure resource group, ADLS Gen2 account with hierarchical namespace, ADF instance, Azure SQL metadata database, Key Vault and Databricks workspace. For the Fabric project create licensed/capacity-backed Fabric workspaces and Lakehouses instead of assuming an Azure storage account is OneLake.
3. Assign workload identity permissions, catalog/table grants, storage ACLs and source access. Validate networking and DNS. Create separate development/test/production configurations before deployment.
4. Create raw paths and bronze/silver/gold Delta tables with explicit schemas. In Databricks use Unity Catalog storage credentials/external locations as appropriate; in Fabric attach the correct Lakehouse to the notebook.
5. Create control tables, register an approved entity and seed its initial boundary. Load a small synthetic snapshot, including intentionally invalid and duplicate records.
6. Build the source extraction pipeline, notebook transformations, reconciliation and publication gate. Record durable input and output locations for every run.
7. Implement one insert, update, delete and late-arrival scenario. Replay input twice. Validate the accepted result and recovery after a simulated failure.
8. Create a serving view/semantic model and validate both its numbers and access with consumer identities.
9. Add monitoring, CI/CD, infrastructure code, deployment parameters, operating procedures and a measured performance/cost baseline.
10. Scale only after correctness passes; use the project-specific acceptance controls before declaring completion.

## 2. Storage and metadata contracts

```text
landing/<source>/<entity>/business_date=YYYY-MM-DD/run_id=<uuid>/
bronze/<domain>/<entity>/                  # raw records plus ingestion metadata
silver/<domain>/<entity>/                  # conformed business records
gold/<product>/<dataset>/                  # accepted analytical datasets
quarantine/<domain>/<entity>/run_id=<uuid>/ # restricted failed records
checkpoints/<stream_name>/                 # one durable path per stream
```

These are ADLS examples. Fabric Files/Tables organization and managed catalog tables have their own locations. Do not manually move files inside a managed Delta table. Avoid subscriber/customer ID partitions; choose partitioning only after measuring date filtering, volume and file sizes.

```sql
-- Azure SQL orchestration metadata; add access, indexing and retention policies.
CREATE TABLE dbo.entity_state (
 entity_id varchar(100) PRIMARY KEY,
 accepted_watermark datetime2(7) NULL,
 accepted_run_id uniqueidentifier NULL,
 state_version rowversion
);
CREATE TABLE dbo.pipeline_run (
 run_id uniqueidentifier PRIMARY KEY,
 entity_id varchar(100) NOT NULL,
 old_watermark datetime2(7) NULL,
 new_watermark datetime2(7) NULL,
 status varchar(20) NOT NULL,
 source_count bigint NULL,
 target_count bigint NULL,
 started_at datetime2(7) NOT NULL,
 ended_at datetime2(7) NULL,
 CONSTRAINT CK_run_status CHECK
  (status IN ('STARTED','LANDED','VALIDATED','PUBLISHED','FAILED'))
);
```

Acquire a per-entity lease or use a serialized scheduler so two runs cannot publish the same boundary concurrently. Restrict configuration changes to reviewed values; table identifiers need allow-list validation because SQL parameters do not parameterize object names.

## 3. ADF incremental orchestration

```text
Lookup approved entity configuration
  -> acquire entity lock
  -> read last accepted boundary
  -> capture bounded source upper boundary
  -> create STARTED run record
  -> Copy bounded source rows into immutable run directory
  -> validate landing manifest / mark LANDED
  -> invoke Databricks notebook
  -> quality checks + reconciliation / mark VALIDATED
  -> publish accepted product
  -> compare-and-set accepted boundary / mark PUBLISHED
  -> release lock
Failure path: mark FAILED + preserve input + alert owner + release lock
```

For Fabric use supported Fabric pipeline/notebook/control-state mechanisms rather than assuming every ADF activity or connector is identical.

```sql
-- Bounded example query; timestamp semantics must be agreed with the source.
SELECT transaction_id, source_sequence, modified_at, amount, currency_code
FROM dbo.source_transaction
WHERE modified_at > @old_watermark
  AND modified_at <= @new_watermark;
```

A timestamp alone is safe only if the source's commit/update behavior guarantees it. Concurrent or late commits can otherwise fall behind the accepted boundary. Prefer source-supported CDC or consistent snapshots with a commit-ordered change boundary. If using a lookback overlap, deduplicate it and document residual risks. Use a timestamp plus key cursor for deterministic page ordering; this does not fix backdated updates or deletes. Timestamp extraction cannot detect hard deletes without a deletion feed or complete-snapshot comparison.

Advance state only after successful acceptance. Publication and Azure SQL state are usually in different transaction systems: use a durable publication manifest and idempotent reconciliation so a crash between them can resume safely. Never claim they are one atomic distributed transaction.

## 4. PySpark validation and deterministic deduplication

```python
from pyspark.sql import functions as F, Window

# `input_path`, `quarantine_path`, `silver_table` and `run_id` are validated job parameters.
schema = ('transaction_id STRING, line_id STRING, source_system STRING, '
          'source_sequence LONG, modified_at TIMESTAMP, '
          'amount DECIMAL(28,6), currency_code STRING')
raw = (spark.read.schema(schema).option('mode', 'FAILFAST')
       .json(input_path).withColumn('run_id', F.lit(run_id)))
# FAILFAST fails the batch for malformed JSON. An alternative permissive
# parser must explicitly capture corrupt records and quarantine them.
invalid = (F.col('transaction_id').isNull() | F.col('line_id').isNull()
           | F.col('source_system').isNull() | F.col('source_sequence').isNull()
           | F.col('modified_at').isNull() | F.col('amount').isNull()
           | F.col('currency_code').isNull())
bad = raw.where(invalid)
good = raw.where(~invalid)
bad.write.format('delta').mode('overwrite').save(quarantine_path)

keys = ['source_system', 'transaction_id', 'line_id']
# Assert one payload per key + source_sequence; contradictory ties fail
# rather than being silently chosen by nondeterministic ordering.
conflicts = (good.groupBy(*(keys + ['source_sequence']))
             .agg(F.countDistinct(F.struct('amount', 'currency_code',
                                          'modified_at')).alias('payloads'))
             .where('payloads > 1'))
if conflicts.limit(1).count():
    raise ValueError('Conflicting payloads for a source sequence')
window = Window.partitionBy(*keys).orderBy(F.col('source_sequence').desc())
latest = (good.dropDuplicates(keys + ['source_sequence'])
          .withColumn('rn', F.row_number().over(window))
          .where('rn = 1').drop('rn'))
latest.createOrReplaceTempView('transaction_latest')
```

Implement format, membership, uniqueness and reconciliation rules separately; null checks alone are not a complete quality framework. The subsequent MERGE target must already exist with a compatible schema. Run the critical quality gate before publication; a valid-row table may be staged even when the batch is held.

## 5. Delta upsert and deletion semantics

```sql
-- Spark SQL / Azure Databricks Delta; source is deduplicated and ordered.
MERGE INTO silver.transaction AS t
USING transaction_latest AS s
ON t.source_system = s.source_system
 AND t.transaction_id = s.transaction_id AND t.line_id = s.line_id
WHEN MATCHED AND s.source_sequence > t.source_sequence THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Keep the source sequence on each current record. A later-arriving older update must not overwrite a newer one. For physical deletes, retain ordering in a tombstone ledger or soft-deleted current row if stale events can be replayed; otherwise an old insert can resurrect a deleted entity. Use delete operations only from an explicit CDC contract or an authoritative complete snapshot, never from absence in a partial batch.

Delta change data feed exposes changes already written to Delta. Enable/configure the supported CDF mode for the chosen Databricks runtime, checkpoint consumers, and plan retention/backfills. Do not promise indefinite history or assume Azure Databricks-specific CDF modes are readable in Fabric.

## 6. SCD Type 2 and historical joins

Choose an entity business key, tracked attributes and effective-time source. Use half-open intervals `[valid_from, valid_to)` and a sentinel or null end date. Assert no overlapping intervals and at most one current row per key.

```sql
-- Spark SQL historical dimension lookup.
SELECT f.transaction_id, f.line_id, d.account_sk, f.amount
FROM silver.transaction f
LEFT JOIN silver.dim_account d
 ON f.account_id = d.account_id
 AND f.event_ts >= d.valid_from
 AND (d.valid_to IS NULL OR f.event_ts < d.valid_to);
```

Count matches: zero requires an approved unknown/suspense policy; more than one is a critical integrity failure. For an out-of-order dimension change, recompute that key's timeline from ordered source history and identify affected facts. A naive close-current-and-insert routine can misrepresent late history. Hashes can compare attributes but are not business keys or proof of equivalence without canonical types/null handling.

## 7. Streaming state and replay

Event Hubs ingestion uses its supported Spark integration for the selected runtime. Persist the original source identifier, event ID, event timestamp and producer sequence. Keep one durable checkpoint per query and environment. Validate connector/authentication options against the installed runtime.

```python
# `events` is an already parsed streaming DataFrame from the approved source.
deduped = (events.withWatermark('event_ts', '2 hours')
           .dropDuplicatesWithinWatermark(['source_system', 'event_id']))
query = (deduped.writeStream.format('delta')
         .option('checkpointLocation', checkpoint_path)
         .outputMode('append').start(bronze_delta_path))
```

The two-hour window is an illustrative configuration, not an SLA. Verify runtime support for `dropDuplicatesWithinWatermark`; if unavailable use an explicitly designed alternative with measured state behavior. Windowed deduplication expires state and can accept replays beyond the horizon. Enforce durable business-key idempotency in silver, retain raw data, and reconcile late partitions. `foreachBatch` handlers must be idempotent because microbatches can execute again; a checkpoint alone does not make arbitrary external writes exactly once.

## 8. Financial and operational reconciliation

Record expected and observed counts and decimal totals at matching grain. Counts alone can miss a duplicated row replacing a missing row. Combine key uniqueness, missing-key comparisons, signed totals, reference coverage and independent samples.

| Control | Expected evidence | Failure action |
|---|---|---|
| Manifest completeness | Declared files/rows vs landed files/rows | Hold batch and request missing delivery |
| Key uniqueness | Distinct business keys equal accepted record count | Resolve source duplicates/conflicts |
| Financial amounts | Decimal totals by date/entity/currency | Hold publication and investigate |
| Dimension resolution | Exactly one historical match per eligible fact | Fix timeline or agreed suspense policy |
| Freshness | Last accepted business timestamp vs target | Alert owner even if jobs succeeded |
| Replay | Same input creates same business output | Fix idempotency before go-live |

Define tolerance from an approved rounding/accounting policy; do not use an arbitrary percentage to suppress differences. Keep rejected-row counts in the balance equation. Test `source = accepted + rejected` where the extract contract and deduplication rules make that equation applicable.

## 9. CI/CD and infrastructure

Suggested repository structure:

```text
infra/                 # Bicep/Terraform, parameters, network/identity declarations
pipelines/             # ADF/Fabric definitions and deployment configuration
notebooks/             # parameterized PySpark transformations
sql/                   # metadata DDL and engine-specific serving objects
contracts/             # reviewed schemas and data-product definitions
tests/fixtures/        # synthetic examples and expected outputs
tests/integration/     # connectivity/replay/reconciliation scenarios
monitoring/            # queries, dashboards and alert definitions
runbooks/              # recovery, access and cutover procedures
```

PR validation checks code/contracts and meaningful fixtures. Test deployment creates resources/configuration and executes the vertical slice. Production promotion uses a reviewed artifact, environment identity, approved parameters and release evidence. Fabric Git/deployment support differs by item type; verify the actual items before promising fully automated promotion. Migration rollback can require recovering data, not just reverting a notebook.

## 10. Performance, costs and observability

Measure extraction bottleneck, shuffle volume, skew, file counts, read amplification, concurrency and serving query latency. Tune one measured bottleneck at a time. Do not apply repartition, caching, broadcast joins, clustering or partitioning mechanically. Avoid tiny files and full-table scans in daily incremental jobs. Run maintenance only under the retention policy; aggressive VACUUM can remove replay/time-travel data still needed by consumers.

Monitor pipeline failure, accepted-data age, reconciliation difference, quarantine rate, streaming lag, execution duration and cost per accepted batch. Use ADF diagnostics and Azure logs where available; use Fabric monitoring and capacity metrics for Fabric workloads rather than assuming all internal events automatically appear in Log Analytics. Benchmark representative data and concurrency and retain before/after results.

## 11. Production recovery runbook

1. Identify the failed run, entity, boundary, input manifest and affected consumers.
2. Prevent concurrent publication for the affected entity; preserve raw input and error evidence.
3. Determine whether landing, transformation, quality, serving publication or state update failed.
4. Resume from the durable phase using the same business input. If publication succeeded but state did not, reconcile the manifest and advance state without appending duplicate facts.
5. Revalidate keys, amounts, quality and access; release only the accepted output.
6. Confirm freshness restored, communicate through the approved incident route, and document root cause and prevention.

Recovery objectives must be backed by tested infrastructure/data restoration. Delta time travel alone is not a complete disaster recovery strategy. Agree source retention, checkpoints, configuration backups, identity/network recovery and regional constraints.

## 12. Completion checklist and evidence form

- [ ] Source owner and data-product owner confirmed.
- [ ] Source snapshot/change semantics documented, including deletes.
- [ ] Reconciliation, critical quality gates and access tests passed.
- [ ] Replay, partial failure, late data and schema-change scenarios passed.
- [ ] Deployment/rollback/recovery demonstrated in the target environment.
- [ ] Freshness, RPO/RTO and cost targets agreed and measured.
- [ ] Consumer acceptance recorded with run/publication IDs.

```text
Project / entity:
Input manifest / source boundary:
Contract / rule version:
Run ID / publication ID:
Source / accepted / rejected counts:
Reconciliation totals / differences:
Failure and replay evidence:
Performance baseline / result / measurement period:
Access test identities and outcomes:
Business acceptance owner and date:
```

## Official technical references

'''
(ROOT/'IMPLEMENTATION_HANDBOOK.md').write_text(handbook+sources,encoding='utf-8')

resume_header = '''# [YOUR FULL NAME]

**Azure Data Engineer | Azure Databricks | Azure Data Factory | Microsoft Fabric**

[City, Country] | [Phone] | [Email] | [LinkedIn URL] | [Portfolio URL]

> Resume preparation template: client/project labels are user supplied. Employment, dates, responsibilities, technology use and impact have not been verified. Keep only work you actually performed; use the reference projects as portfolio designs if they were not client engagements. Remove this note only after checking every claim and replacing all placeholders.

## Professional summary

Azure Data Engineer with [verified years] of experience in [verified domains], delivering data ingestion, transformation, quality and analytical datasets using [technologies actually used]. Experienced in [verified SQL/Python/PySpark scope], incremental processing, dimensional modeling, reconciliation and production support. Contributed to [verified banking/finance/telecom engagements] with responsibility for [your personal scope].

## Technical skills — retain only demonstrated skills

- Cloud and storage: Microsoft Azure, ADLS Gen2, Microsoft Fabric, OneLake.
- Integration: Azure Data Factory, Fabric Data Factory pipelines, supported integration runtimes, REST/file/database ingestion.
- Processing: Azure Databricks, Fabric Spark, PySpark, Python, Spark SQL, Delta Lake.
- Modeling and serving: dimensional modeling, SCD Type 2, Databricks SQL, Azure Synapse Analytics, Azure SQL Database, Power BI.
- Governance and security: Microsoft Purview, Microsoft Entra ID, Azure Key Vault, RBAC/ACLs, Unity Catalog, row-level security.
- Engineering and operations: Git, Azure DevOps, [Bicep/Terraform if used], Azure Monitor, Log Analytics, testing, CI/CD, incident recovery.
- Streaming: Azure Event Hubs, Structured Streaming, event-time processing and checkpointing [only if used].

## Professional experience

### [Actual employer] — [Actual job title]

[City/Remote] | [MM YYYY–MM YYYY or Present]

- Owned [verified pipeline/domain scope] across [verified project phases].
- Developed [specific ADF/Fabric pipelines, notebooks and SQL objects] for [business purpose].
- Implemented [verified quality/reconciliation/security controls] and supported [verified service target].
- Collaborated with [actual teams] to deliver [accepted outputs].
- Achieved [measured result] compared with [baseline] over [measurement period].

Repeat this employer block for every actual employer. Map the client engagements below to the correct employer and dates; do not list client names as employers unless you were employed by them.

## Selected client engagements / projects

'''
full=resume_header
for p in projects:
    full += f"### {p['client']} — {p['title']}\n\n"
    full += '**Employer:** [actual employer] | **Dates:** [MM YYYY–MM YYYY] | **Role:** [actual role]\n\n'
    full += f"**Business scope:** {p['problem']}\n\n**Technology used:** [retain verified technologies from: {p['stack']}]\n\n"
    full += '\n'.join('- '+b for b in p['bullets'])+'\n\n'
    full += f"**Flow:** {p['flow']}\n\n"
    full += '**Evidence to add:** [owned components], [volume], [acceptance controls], [baseline/result], [production responsibilities].\n\n'
full += '''## Education

**[Degree]**, [Institution], [Location] — [Graduation year]

## Certifications

- [Exact certification title], [Issuer], [Award date], [Credential URL/status].

List only credentials actually held, using the title on the credential. Put courses/labs in a separate training section if needed.

## Additional achievements

- [Verified automation, mentoring, award, contribution or publication with evidence].

## Resume finalization

Replace all placeholders; remove technologies you did not use; check overlapping engagement dates and employer mappings; choose two to four strongest projects for a job application. Use the full version as a master inventory and the ATS version as the shorter application draft. Do not copy example architecture into past experience unless it matches the actual engagement.
'''
(RESUMES/'FULL_AZURE_DATA_ENGINEER_RESUME.md').write_text(full,encoding='utf-8')

ats='''# [YOUR FULL NAME]

Azure Data Engineer

[City] | [Phone] | [Email] | [LinkedIn] | [Portfolio]

> Draft template: replace placeholders and retain only verified employment, skills and project contributions before submission.

## Summary

Azure Data Engineer with [years] of experience in [domains]. Built [verified scope] using [verified Azure services], SQL, Python and PySpark. Specialized in [two demonstrated strengths], delivering [one verified outcome].

## Skills

[Keep demonstrated skills only: Azure Data Factory, ADLS Gen2, Azure Databricks, Microsoft Fabric, OneLake, Delta Lake, PySpark, SQL, Python, Synapse Analytics, Azure SQL, Power BI, Purview, Key Vault, Entra ID, Azure DevOps, Azure Monitor, Event Hubs.]

## Experience

**[Employer] — [Role]** | [Dates] | [Location]

- Built [specific solution] for [business need] using [actual technology].
- Processed [verified volume] with [verified freshness/reliability result].
- Implemented [specific correctness/security control] and resolved [actual production issue].
- Improved [metric] from [baseline] to [result], measured over [period].

[Repeat for each actual employer.]

## Selected projects

Select the most relevant two to four projects for the vacancy; the candidate bullets below cover all six for selection. Remove unverified or unused entries.

'''
for p in projects:
    ats+=f"**{p['client']} — {p['title']}** | [Employer / Dates / Role]\n\n- {p['bullets'][0]}\n- {p['bullets'][1]}\n\n"
ats+='''## Education

[Degree] — [Institution], [Year]

## Certifications

[Exact verified credential title] — [Issuer], [Date/status]
'''
(RESUMES/'ATS_AZURE_DATA_ENGINEER_RESUME.md').write_text(ats,encoding='utf-8')

for p in projects:
    targeted=resume_header.split('## Selected client engagements / projects')[0]
    targeted+=f"## Featured project\n\n### {p['client']} — {p['title']}\n\n**Employer:** [actual employer] | **Dates:** [dates] | **Role:** [actual role]\n\n"
    targeted+=f"{p['problem']}\n\n"+'\n'.join('- '+b for b in p['bullets'])+'\n\n'
    targeted+='## Education and certifications\n\n[Actual degree, institution, year and verified certifications.]\n\n'
    targeted+='## Other experience\n\n[Add relevant verified employer achievements and other projects; remove irrelevant skills from this targeted version.]\n'
    (RESUMES/f"{p['id']}_{p['slug']}_RESUME.md").write_text(targeted,encoding='utf-8')

readme='''# Azure Data Engineering Project and Resume Pack

Six detailed Azure/Microsoft reference project designs, a shared technical implementation handbook, a full master resume, an ATS application draft and six project-focused resume variants.

The named clients and project titles come from your request. Their internal architectures, your employment and your achievements were not provided. All proposed source systems, technology choices, flows and responsibilities require confirmation before they become resume claims. A proposed modernization design can be presented as a portfolio project if clearly labeled; it must not be presented as a historical implementation that did not happen.

## Project documents

| Project | Focus | Document |
|---|---|---|
'''
for p in projects:
    readme+=f"| {p['client']} | {p['title']} | [End-to-end design](projects/{p['id']}_{p['slug']}.md) |\n"
readme+='''
## Implementation and resumes

- [Shared implementation handbook](IMPLEMENTATION_HANDBOOK.md): build sequence, metadata tables, ADF orchestration, PySpark validation, Delta upsert, SCD history, streaming, reconciliation, CI/CD and recovery.
- [Full master resume](resumes/FULL_AZURE_DATA_ENGINEER_RESUME.md): all six engagements, technical skills, employer history and education placeholders.
- [ATS resume draft](resumes/ATS_AZURE_DATA_ENGINEER_RESUME.md): concise candidate content for selecting the most relevant verified projects.
'''
for p in projects:
    readme+=f"- [{p['client']} focused resume](resumes/{p['id']}_{p['slug']}_RESUME.md).\n"
readme+='''
## How to finalize

1. Add your name, contact details, employer titles/dates, client engagement dates, education and credentials.
2. Replace illustrative sources and architectures with actual components. Confirm acronyms and historical technology availability against engagement dates.
3. Select only responsibilities you personally performed. Distinguish implementation, contribution, operation and design review accurately.
4. Add metrics with baseline/result, unit, measurement period and evidence. Remove metric bullets if evidence is unavailable.
5. Use project documents for interview preparation; use the master resume as an inventory and trim the ATS version for the target role.

Microsoft Fabric is a Microsoft SaaS analytics platform integrated with the Azure ecosystem; it is not interchangeable with ADF, ADLS or Synapse. The Citi design intentionally uses Fabric, while the other designs use Azure services. The documents are implementation specifications with example code, not deployed projects. Azure deployment and integration tests have not been run.

## Official platform references

'''+sources
(ROOT/'README.md').write_text(readme,encoding='utf-8')
print(f'Created {len(list(ROOT.rglob("*.md")))} Markdown files in {ROOT}')
