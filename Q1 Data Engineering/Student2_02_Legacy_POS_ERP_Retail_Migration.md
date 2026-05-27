# Student 2 - Project 2
## Legacy POS and ERP Retail Platform Migration to Azure (Migration Project)
### Stack
Azure Data Factory, Azure Databricks, ADLS Gen2, Delta Lake, Azure SQL, Microsoft Fabric, Power BI, Python, PySpark, SQL

### Step 1: Requirement Gathering
Collected migration goals from finance, operations, and analytics teams for replacing legacy reporting workflows. Identified priority subject areas: sales, inventory, pricing, promotions, and vendor settlements. Defined migration constraints for cutover window, reconciliation tolerance, and rollback procedures.

### Step 2: Architecture and Migration Strategy
Designed target Azure architecture with Medallion data zones and phased migration waves. Selected coexistence approach where legacy and Azure pipelines run in parallel during validation. Defined extraction, transformation, reconciliation, and cutover checkpoints for each wave.

### Step 3: Environment and Landing Zone Setup
Provisioned isolated dev, test, and prod environments with policy-compliant networking and identity controls. Configured storage hierarchy, Databricks clusters, and orchestration resources. Established naming conventions and tagging for traceability across migration phases.

### Step 4: Legacy Source Discovery and Profiling
Profiled POS and ERP schemas, stored procedures, flat-file exports, and scheduler dependencies. Documented data quality issues such as code inconsistencies, date format drift, and orphan keys. Mapped source entities to standardized target domain models.

### Step 5: Initial Data Extraction Pipelines
Built ADF pipelines for full historical extraction from legacy databases and file shares. Implemented secure connectivity and throttled extraction strategies to avoid production impact. Captured source control totals and extraction logs for reconciliation.

### Step 6: Bronze Zone Historical Landing
Loaded raw historical snapshots into Bronze with source lineage, extraction batch IDs, and timestamps. Preserved source-native data formats to support audit and replay. Partitioned storage to improve downstream reprocessing and validation workflows.

### Step 7: Transformation and Standardization
Implemented Databricks transformations for datatype alignment, code harmonization, and business rule standardization. Rebuilt key legacy logic in PySpark and SQL with deterministic outputs. Added exception handling for malformed records and missing reference mappings.

### Step 8: Silver Conformed Data Model
Created conformed Silver tables for customers, products, stores, transactions, and inventory events. Applied SCD handling for slowly changing retail dimensions. Enforced data quality contracts on key uniqueness, referential integrity, and mandatory fields.

### Step 9: Gold Reporting Models
Built Gold marts aligned to legacy report outputs for sales, margin, stock movement, and settlement analytics. Implemented star schema design for high-performance BI consumption. Produced parallel-run output datasets to compare legacy and target results.

### Step 10: Legacy Report Mapping and Parity Testing
Mapped existing legacy reports and KPI definitions to Power BI semantic models. Validated row-level and aggregate parity for agreed reporting periods. Logged and resolved metric deltas through controlled change review with business stakeholders.

### Step 11: Incremental Load and CDC Setup
Implemented incremental extraction and CDC-based loads to keep Azure and legacy systems synchronized. Added watermark, delete handling, and late update processing rules. Validated near-real-time and daily refresh behavior under production-like load.

### Step 12: User Acceptance and Business Sign-off
Conducted UAT cycles with finance, merchandising, and operations users on migrated reports and data services. Captured feedback on metric interpretation, drill paths, and usability. Closed defects and obtained formal sign-off for migration wave cutover.

### Step 13: CI/CD and Release Controls
Established Git-based versioning and automated deployment pipelines for ADF and Databricks assets. Added environment-specific parameterization and secure secret references. Included pre-deploy checks and post-deploy validation for each migration release.

### Step 14: Monitoring and Operational Controls
Configured centralized monitoring for pipeline runs, cluster jobs, data freshness, and reconciliation status. Created alerts for load failures, CDC lag, and SLA risk conditions. Published operational views for migration command center tracking.

### Step 15: Security and Compliance
Applied access control, data classification, and masking policies for sensitive customer and payment fields. Used encryption-at-rest and in-transit with enterprise-managed key policies where required. Documented compliance evidence for audit and governance teams.

### Step 16: Cutover and Performance Tuning
Executed phased cutover plan with go/no-go checkpoints and rollback readiness. Tuned Spark execution plans, partitioning, and storage optimization to meet SLA targets. Stabilized workload concurrency for business-hour reporting and overnight processing.

### Step 17: Hypercare and Steady-State Support
Ran post-cutover hypercare for defect triage, reconciliation exceptions, and user onboarding. Transitioned runbooks, ownership matrices, and SOPs to the support team. Planned backlog enhancements for additional legacy decommission opportunities.

