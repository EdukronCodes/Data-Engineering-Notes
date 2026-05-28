# Customer Recommendation and Market Basket Analysis Platform

### Project Story (Spoken English)

This project is about making `vikitha-01-customer-recommendation` dependable in real delivery conditions, not only in demos. We orchestrate the end-to-end run through Azure Data Factory so every load starts with a clear trigger, moves through dependency checks, and lands in predictable windows for business users. From there, Azure Databricks notebooks execute the transformation chain in a medallion pattern, where raw inputs are safely captured in Bronze, corrected and standardized in Silver, and published as decision-ready Gold datasets. I explain the flow in an interview style as if I am walking a team lead through what really runs at 2 AM: what starts first, what can fail, what retries automatically, and what gets escalated. The design intentionally includes operational controls like watermarking, checkpointing, schema drift handling, and audit stamps so we can trust both the data and the process timeline. Even if the source system is delayed or noisy, ADF orchestration + ADB notebooks keep the run recoverable and measurable.

In practical terms, this `streaming` workload for `customer` is built so engineers can rerun any slice without breaking downstream consumers. Each diagram below maps a concrete orchestration path in ADF to named notebook responsibilities in Databricks, then shows exactly how records transition from Bronze to Silver to Gold with storage paths and quality expectations. Instead of generic architecture talk, the sections focus on implementation details teams ask in design reviews: parameter strategy, Delta MERGE behavior, late-arrival handling, reconciliation queries, incident routing, and SLA reporting. This makes the document portfolio-ready and execution-ready at the same time, because a new engineer can read it and understand not only what the architecture looks like, but also how to operate it safely under pressure. The notebook deep-dive and code snippets are included so orchestration logic, Spark logic, and validation logic stay connected as one delivery story across ADF and ADB.

## Detailed Flows

**Detailed Flow 01: Source Ingestion and Landing**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_01` starts `PL_CUSTOMER_01`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_01` -> `NB_Silver_customer_curated_01` -> `NB_Gold_engagement_kpi_01`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 01] --> PIPE[ADF Pipeline PL_CUSTOMER_01]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stcustomer{env}/customer_event/)]
    BR --> NB1[ADB NB_Bronze_customer_event_01]
    NB1 --> SV[(abfss://silver@stcustomer{env}/customer_curated/)]
    SV --> NB2[ADB NB_Silver_customer_curated_01]
    NB2 --> NB3[ADB NB_Gold_engagement_kpi_01]
    NB3 --> GD[(abfss://gold@stcustomer{env}/engagement_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 02: ADF Trigger to Notebook Handshake**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_02` starts `PL_CUSTOMER_02`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_02` -> `NB_Silver_customer_curated_02` -> `NB_Gold_engagement_kpi_02`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 02 (streaming)
    P->>B: Execute with params (load_date, watermark)
    B-->>P: Bronze write complete
    P->>S: Execute cleansing + DQ
    S-->>P: Silver publish complete
    P->>G: Execute MERGE into Gold
    G-->>P: Gold metrics + row counts
    P->>M: Emit status, retries, escalation
```

```python
# ADF notebook parameter payload example
params = {
  "env": dbutils.widgets.get("env"),
  "load_date": dbutils.widgets.get("load_date"),
  "run_id": dbutils.widgets.get("run_id")
}
```

**Detailed Flow 03: Bronze Quality Gate**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_03` starts `PL_CUSTOMER_03`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_03` -> `NB_Silver_customer_curated_03` -> `NB_Gold_engagement_kpi_03`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
stateDiagram-v2
    [*] --> ADF_Queued
    ADF_Queued --> Bronze_Loaded: Trigger accepted
    Bronze_Loaded --> Silver_Validated: ADB notebook success
    Silver_Validated --> Gold_Published: ADB MERGE success
    Gold_Published --> SLA_Reported: ADF post-validation
    Bronze_Loaded --> Retry_Path: Copy/Notebook transient failure
    Retry_Path --> Bronze_Loaded: Exponential retry in ADF
    Retry_Path --> Incident_Raised: Retry exhausted
    Incident_Raised --> [*]
    SLA_Reported --> [*]
```

**Detailed Flow 04: Silver Standardization and Dedup**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_04` starts `PL_CUSTOMER_04`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_04` -> `NB_Silver_customer_curated_04` -> `NB_Gold_engagement_kpi_04`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 04] --> PIPE[ADF Pipeline PL_CUSTOMER_04]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stcustomer{env}/customer_event/)]
    BR --> NB1[ADB NB_Bronze_customer_event_04]
    NB1 --> SV[(abfss://silver@stcustomer{env}/customer_curated/)]
    SV --> NB2[ADB NB_Silver_customer_curated_04]
    NB2 --> NB3[ADB NB_Gold_engagement_kpi_04]
    NB3 --> GD[(abfss://gold@stcustomer{env}/engagement_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 05: CDC Merge into Gold Serving**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_05` starts `PL_CUSTOMER_05`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_05` -> `NB_Silver_customer_curated_05` -> `NB_Gold_engagement_kpi_05`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 05 (streaming)
    P->>B: Execute with params (load_date, watermark)
    B-->>P: Bronze write complete
    P->>S: Execute cleansing + DQ
    S-->>P: Silver publish complete
    P->>G: Execute MERGE into Gold
    G-->>P: Gold metrics + row counts
    P->>M: Emit status, retries, escalation
```

```python
# ADF notebook parameter payload example
params = {
  "env": dbutils.widgets.get("env"),
  "load_date": dbutils.widgets.get("load_date"),
  "run_id": dbutils.widgets.get("run_id")
}
```

**Detailed Flow 06: Late Arrival and Watermark Reprocess**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_06` starts `PL_CUSTOMER_06`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_06` -> `NB_Silver_customer_curated_06` -> `NB_Gold_engagement_kpi_06`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 06] --> PIPE[ADF Pipeline PL_CUSTOMER_06]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stcustomer{env}/customer_event/)]
    BR --> NB1[ADB NB_Bronze_customer_event_06]
    NB1 --> SV[(abfss://silver@stcustomer{env}/customer_curated/)]
    SV --> NB2[ADB NB_Silver_customer_curated_06]
    NB2 --> NB3[ADB NB_Gold_engagement_kpi_06]
    NB3 --> GD[(abfss://gold@stcustomer{env}/engagement_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 07: Checkpoint and Replay Control**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_07` starts `PL_CUSTOMER_07`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_07` -> `NB_Silver_customer_curated_07` -> `NB_Gold_engagement_kpi_07`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
stateDiagram-v2
    [*] --> ADF_Queued
    ADF_Queued --> Bronze_Loaded: Trigger accepted
    Bronze_Loaded --> Silver_Validated: ADB notebook success
    Silver_Validated --> Gold_Published: ADB MERGE success
    Gold_Published --> SLA_Reported: ADF post-validation
    Bronze_Loaded --> Retry_Path: Copy/Notebook transient failure
    Retry_Path --> Bronze_Loaded: Exponential retry in ADF
    Retry_Path --> Incident_Raised: Retry exhausted
    Incident_Raised --> [*]
    SLA_Reported --> [*]
```

**Detailed Flow 08: Validation and Reconciliation**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_08` starts `PL_CUSTOMER_08`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_08` -> `NB_Silver_customer_curated_08` -> `NB_Gold_engagement_kpi_08`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 08] --> PIPE[ADF Pipeline PL_CUSTOMER_08]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stcustomer{env}/customer_event/)]
    BR --> NB1[ADB NB_Bronze_customer_event_08]
    NB1 --> SV[(abfss://silver@stcustomer{env}/customer_curated/)]
    SV --> NB2[ADB NB_Silver_customer_curated_08]
    NB2 --> NB3[ADB NB_Gold_engagement_kpi_08]
    NB3 --> GD[(abfss://gold@stcustomer{env}/engagement_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

```python
# ADF notebook parameter payload example
params = {
  "env": dbutils.widgets.get("env"),
  "load_date": dbutils.widgets.get("load_date"),
  "run_id": dbutils.widgets.get("run_id")
}
```

**Detailed Flow 09: Retry and Incident Escalation**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_09` starts `PL_CUSTOMER_09`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_09` -> `NB_Silver_customer_curated_09` -> `NB_Gold_engagement_kpi_09`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 09 (streaming)
    P->>B: Execute with params (load_date, watermark)
    B-->>P: Bronze write complete
    P->>S: Execute cleansing + DQ
    S-->>P: Silver publish complete
    P->>G: Execute MERGE into Gold
    G-->>P: Gold metrics + row counts
    P->>M: Emit status, retries, escalation
```

**Detailed Flow 10: Publishing and Consumer SLA**

- **Purpose:** Drive `customer` data from source to governed Gold outputs with observable checkpoints. Includes micro-batch checkpointing and late-arrival replay.
- **Trigger/Orchestration in ADF:** `TR_CUSTOMER_10` starts `PL_CUSTOMER_10`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_customer_event_10` -> `NB_Silver_customer_curated_10` -> `NB_Gold_engagement_kpi_10`.
- **Medallion transitions:** Bronze (`customer_event` raw + audit columns) -> Silver (`customer_curated` standardized, deduped, DQ-tagged) -> Gold (`engagement_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stcustomer{env}/customer_event/`; writes to `abfss://bronze@stcustomer{env}/customer_event/`, `abfss://silver@stcustomer{env}/customer_curated/`, `abfss://gold@stcustomer{env}/engagement_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_CUSTOMER_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 10] --> PIPE[ADF Pipeline PL_CUSTOMER_10]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stcustomer{env}/customer_event/)]
    BR --> NB1[ADB NB_Bronze_customer_event_10]
    NB1 --> SV[(abfss://silver@stcustomer{env}/customer_curated/)]
    SV --> NB2[ADB NB_Silver_customer_curated_10]
    NB2 --> NB3[ADB NB_Gold_engagement_kpi_10]
    NB3 --> GD[(abfss://gold@stcustomer{env}/engagement_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

## Practical Theory Expansion

### ADF orchestration model in this project
ADF is used as the control-plane. Pipelines are parameterized by `load_date`, `domain`, and `watermark`; trigger decisions and dependency checks happen before Databricks execution. We keep the orchestration explicit: ingest first, then Bronze validation, then Silver transforms, then Gold publish, then reconciliation and notifications.

```adf
@concat('abfss://landing@stcustomer', pipeline().globalParameters.g_env, '.dfs.core.windows.net/customer_event/', formatDateTime(pipeline().parameters.load_date,'yyyy/MM/dd'))
```

### Databricks execution model
Databricks notebooks are grouped by medallion stage so runtime failures are isolated and reruns are granular. Bronze notebooks prioritize schema capture and lineage, Silver notebooks enforce business rules and dedup logic, Gold notebooks build serving marts with deterministic keys.

```python
# Delta MERGE for Silver->Gold publish
from delta.tables import DeltaTable
source_df = spark.table('customer_silver.customer_curated')
target = DeltaTable.forName(spark, 'customer_gold.engagement_kpi')
(target.alias('t')
 .merge(source_df.alias('s'), 't.business_key = s.business_key')
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())
```

### Delta and medallion rationale
Bronze protects source fidelity, Silver creates reusable conformed entities, and Gold serves consumption with SLA contracts. This separation avoids mixing ingestion noise with analytics quality and gives predictable recovery points.

### Reliability patterns applied
Common controls include watermark-based incrementals, checkpoint persistence, idempotent Delta MERGE, ADF retries with backoff, dead-letter quarantine, and reconciliation gates before publish success is declared.

```sql
-- Reconciliation query between Silver and Gold
SELECT 'customer_curated' AS silver_table, 'engagement_kpi' AS gold_table,
       (SELECT COUNT(1) FROM customer_silver.customer_curated) AS silver_count,
       (SELECT COUNT(1) FROM customer_gold.engagement_kpi) AS gold_count;
```

```python
# Structured Streaming pattern for Bronze ingestion
(spark.readStream.format("cloudFiles")
 .option("cloudFiles.format", "json")
 .option("cloudFiles.schemaLocation", "abfss://bronze@stcustomer{env}/_schemas/customer_event")
 .load("abfss://landing@stcustomer{env}/customer_event/")
 .withColumn("_ingest_ts", current_timestamp())
 .writeStream
 .option("checkpointLocation", "abfss://silver@stcustomer{env}/_checkpoints/customer_event")
 .trigger(processingTime="5 minutes")
 .toTable("customer_bronze.customer_event"))
```


## Detailed Notebook Playbook

### Notebook `/Projects/customer/01_Bronze/NB_Bronze_customer_event`
- **Purpose:** Execute a scoped medallion responsibility in the `customer` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://landing@stcustomer{env}/customer_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `customer_bronze.customer_event` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/customer/02_Silver/NB_Silver_customer_curated`
- **Purpose:** Execute a scoped medallion responsibility in the `customer` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `customer_bronze.customer_event`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `customer_silver.customer_curated` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/customer/03_Gold/NB_Gold_engagement_kpi`
- **Purpose:** Execute a scoped medallion responsibility in the `customer` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `customer_silver.customer_curated`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `customer_gold.engagement_kpi` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/customer/04_Validation/NB_Validate_engagement_kpi`
- **Purpose:** Execute a scoped medallion responsibility in the `customer` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `customer_gold.engagement_kpi`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `audit.validation_results` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/customer/05_Recovery/NB_Backfill_customer_event`
- **Purpose:** Execute a scoped medallion responsibility in the `customer` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://bronze@stcustomer{env}/customer_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `customer_silver.customer_curated` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.


## Preserved Existing Project Notes

> **Reference:** Adapted from [https://github.com/Analytics6/Azure-Data-Engineering-Notes](https://github.com/Analytics6/Azure-Data-Engineering-Notes) — `03-Customer-Behavior-Analytics-Engine.md, 10-Retail-Customer-Analytics-Platform.md`


## Project Overview and Business Context

A national retailer wants personalized product recommendations and market basket insights (affinity, lift, confidence) across web, mobile, and in-store channels. Batch and near-real-time order events feed a lakehouse where ML features and Gold marts power recommendation APIs and merchant dashboards.

**Outcomes:** Increase average order value 8–12%, optimize cross-sell campaigns, reduce manual merchandising analysis.

## Platform Concepts (Analytics6 Reference)

**Medallion ADLS layout:** Landing by source → Pre-Bronze (schema validation) → Bronze (immutable Delta) → Silver (cleansed, DQ, SCD) → Gold (business models) → Archive.

**ADF:** Metadata-driven ingestion (Lookup + ForEach), watermark incrementals, CDC, exponential backoff, audit logging. Linked services use MSI + Key Vault; SHIR for on-prem.

**Databricks / Delta:** MERGE incrementals, `OPTIMIZE`/`VACUUM`, partition pruning, Unity Catalog governance.

**Monitoring:** Log Analytics diagnostics, pipeline failure action groups, SLA KQL dashboards.

---

## Architecture Diagram

```mermaid
flowchart LR
    POS[POS / E-comm] --> EH[Event Hubs]
    CRM[CRM API] --> ADF[ADF]
    EH --> ADB[Databricks]
    ADF --> ADLS[(Delta Lake)]
    ADB --> ADLS
    ADLS --> ML[Azure ML / MLflow]
    ADLS --> PBI[Power BI]
    ML --> API[Recommendation API]
```

---

## Azure Services

ADF, Databricks, ADLS Gen2, Event Hubs, Delta Lake, Unity Catalog, Azure ML, Key Vault, Azure SQL (feature store cache), Power BI, Log Analytics.

---

## Medallion Architecture

### Bronze
- **Sources:** E-commerce clickstream (JSON), POS transactions (Parquet exports), CRM customer profiles (REST via ADF)
- **Paths:** `bronze/ecomm/events/`, `bronze/pos/transactions/`, `bronze/crm/customers/`
- **Schema (orders):** `order_id, customer_id, product_id, qty, unit_price, channel, event_time`

### Silver
- Cleansed `silver.fact_order_line`, unified `silver.dim_customer`, `silver.dim_product`
- Market basket pairs: `silver.product_cooccurrence_staging` (session window 30 min)
- Dedup on `order_id` + `line_id`

### Gold
- `gold.market_basket_metrics` (support, confidence, lift)
- `gold.customer_product_affinity`
- `gold.recommendation_candidates` (top-N per customer)
- Serving: Azure SQL indexed views for low-latency API reads

---

## ADF Orchestration

| Pipeline | Purpose |
|----------|---------|
| `PL_REC_Bronze_CRM_Daily` | Copy/API → Bronze CRM |
| `PL_REC_Bronze_POS_Incremental` | SHIR or blob → Bronze POS |
| `PL_REC_Silver_Gold_Daily` | Databricks chain |
| `PL_REC_MBA_Weekly` | Market basket full recompute |
| `PL_REC_ML_Feature_Publish` | Trigger Azure ML pipeline |

**Triggers:** Daily 03:00 (`TR_REC_Daily`), Weekly Sunday (`TR_REC_MBA`).

**Activities:** Copy, Lookup (watermark), ForEach (stores), Databricks Notebook, If Condition (row threshold), Web (ML endpoint).

**Environments:** `dev/test/prod` via `g_storage_account`, `g_catalog_name`.

---

## ADB Notebooks

```
/Recommendation/
├── 01_Bronze/NB_Ingest_Ecomm_Events
├── 02_Silver/NB_Conform_Orders, NB_Build_Basket_Pairs
├── 03_Gold/NB_Market_Basket_Metrics, NB_Customer_Affinity
└── 04_ML/NB_Export_Features_MLflow
```

| Notebook | I/O |
|----------|-----|
| `NB_Build_Basket_Pairs` | Silver orders → cooccurrence staging |
| `NB_Market_Basket_Metrics` | Staging → Gold MBA table |

**Cluster:** Batch 8 workers DS4_v2; weekly MBA 16 workers. **Unity Catalog:** `retail_rec_{env}`.

---

## End-to-End Flow

`POS/E-comm → Bronze → Silver orders/dims → Gold MBA + affinity → ML/API + Power BI`

---

## Security & Monitoring

MI for ADF/ADB; Key Vault for CRM API keys; mask PII in dev. Alerts on daily pipeline failure and Gold row count anomaly.

---

## Naming & Phases

`adf-vikitha-rec-prod`, `adb-vikitha-rec-prod`, `stvikitharecprod`. Phases: ingest → conform → MBA → ML integration → API cutover.
