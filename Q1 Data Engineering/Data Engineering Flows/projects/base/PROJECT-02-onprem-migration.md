# PROJECT 2 — Azure Data Engineering Migration: On-Premises Database to Azure Cloud

### Project Story (Spoken English)

This project is about making `PROJECT-02-onprem-migration` dependable in real delivery conditions, not only in demos. We orchestrate the end-to-end run through Azure Data Factory so every load starts with a clear trigger, moves through dependency checks, and lands in predictable windows for business users. From there, Azure Databricks notebooks execute the transformation chain in a medallion pattern, where raw inputs are safely captured in Bronze, corrected and standardized in Silver, and published as decision-ready Gold datasets. I explain the flow in an interview style as if I am walking a team lead through what really runs at 2 AM: what starts first, what can fail, what retries automatically, and what gets escalated. The design intentionally includes operational controls like watermarking, checkpointing, schema drift handling, and audit stamps so we can trust both the data and the process timeline. Even if the source system is delayed or noisy, ADF orchestration + ADB notebooks keep the run recoverable and measurable.

In practical terms, this `migration` workload for `operations` is built so engineers can rerun any slice without breaking downstream consumers. Each diagram below maps a concrete orchestration path in ADF to named notebook responsibilities in Databricks, then shows exactly how records transition from Bronze to Silver to Gold with storage paths and quality expectations. Instead of generic architecture talk, the sections focus on implementation details teams ask in design reviews: parameter strategy, Delta MERGE behavior, late-arrival handling, reconciliation queries, incident routing, and SLA reporting. This makes the document portfolio-ready and execution-ready at the same time, because a new engineer can read it and understand not only what the architecture looks like, but also how to operate it safely under pressure. The notebook deep-dive and code snippets are included so orchestration logic, Spark logic, and validation logic stay connected as one delivery story across ADF and ADB.

## Detailed Flows

**Detailed Flow 01: Source Ingestion and Landing**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_01` starts `PL_OPERATIONS_01`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_01` -> `NB_Silver_ops_curated_01` -> `NB_Gold_ops_kpi_01`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 01] --> PIPE[ADF Pipeline PL_OPERATIONS_01]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stoperations{env}/ops_event/)]
    BR --> NB1[ADB NB_Bronze_ops_event_01]
    NB1 --> SV[(abfss://silver@stoperations{env}/ops_curated/)]
    SV --> NB2[ADB NB_Silver_ops_curated_01]
    NB2 --> NB3[ADB NB_Gold_ops_kpi_01]
    NB3 --> GD[(abfss://gold@stoperations{env}/ops_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 02: ADF Trigger to Notebook Handshake**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_02` starts `PL_OPERATIONS_02`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_02` -> `NB_Silver_ops_curated_02` -> `NB_Gold_ops_kpi_02`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 02 (migration)
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_03` starts `PL_OPERATIONS_03`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_03` -> `NB_Silver_ops_curated_03` -> `NB_Gold_ops_kpi_03`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_04` starts `PL_OPERATIONS_04`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_04` -> `NB_Silver_ops_curated_04` -> `NB_Gold_ops_kpi_04`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 04] --> PIPE[ADF Pipeline PL_OPERATIONS_04]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stoperations{env}/ops_event/)]
    BR --> NB1[ADB NB_Bronze_ops_event_04]
    NB1 --> SV[(abfss://silver@stoperations{env}/ops_curated/)]
    SV --> NB2[ADB NB_Silver_ops_curated_04]
    NB2 --> NB3[ADB NB_Gold_ops_kpi_04]
    NB3 --> GD[(abfss://gold@stoperations{env}/ops_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 05: CDC Merge into Gold Serving**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_05` starts `PL_OPERATIONS_05`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_05` -> `NB_Silver_ops_curated_05` -> `NB_Gold_ops_kpi_05`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 05 (migration)
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_06` starts `PL_OPERATIONS_06`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_06` -> `NB_Silver_ops_curated_06` -> `NB_Gold_ops_kpi_06`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 06] --> PIPE[ADF Pipeline PL_OPERATIONS_06]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stoperations{env}/ops_event/)]
    BR --> NB1[ADB NB_Bronze_ops_event_06]
    NB1 --> SV[(abfss://silver@stoperations{env}/ops_curated/)]
    SV --> NB2[ADB NB_Silver_ops_curated_06]
    NB2 --> NB3[ADB NB_Gold_ops_kpi_06]
    NB3 --> GD[(abfss://gold@stoperations{env}/ops_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 07: Checkpoint and Replay Control**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_07` starts `PL_OPERATIONS_07`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_07` -> `NB_Silver_ops_curated_07` -> `NB_Gold_ops_kpi_07`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_08` starts `PL_OPERATIONS_08`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_08` -> `NB_Silver_ops_curated_08` -> `NB_Gold_ops_kpi_08`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 08] --> PIPE[ADF Pipeline PL_OPERATIONS_08]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stoperations{env}/ops_event/)]
    BR --> NB1[ADB NB_Bronze_ops_event_08]
    NB1 --> SV[(abfss://silver@stoperations{env}/ops_curated/)]
    SV --> NB2[ADB NB_Silver_ops_curated_08]
    NB2 --> NB3[ADB NB_Gold_ops_kpi_08]
    NB3 --> GD[(abfss://gold@stoperations{env}/ops_kpi/)]
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_09` starts `PL_OPERATIONS_09`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_09` -> `NB_Silver_ops_curated_09` -> `NB_Gold_ops_kpi_09`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 09 (migration)
    P->>B: Execute with params (load_date, watermark)
    B-->>P: Bronze write complete
    P->>S: Execute cleansing + DQ
    S-->>P: Silver publish complete
    P->>G: Execute MERGE into Gold
    G-->>P: Gold metrics + row counts
    P->>M: Emit status, retries, escalation
```

**Detailed Flow 10: Publishing and Consumer SLA**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes legacy parity checks, cutover gates, and rollback path.
- **Trigger/Orchestration in ADF:** `TR_OPERATIONS_10` starts `PL_OPERATIONS_10`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ops_event_10` -> `NB_Silver_ops_curated_10` -> `NB_Gold_ops_kpi_10`.
- **Medallion transitions:** Bronze (`ops_event` raw + audit columns) -> Silver (`ops_curated` standardized, deduped, DQ-tagged) -> Gold (`ops_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stoperations{env}/ops_event/`; writes to `abfss://bronze@stoperations{env}/ops_event/`, `abfss://silver@stoperations{env}/ops_curated/`, `abfss://gold@stoperations{env}/ops_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_OPERATIONS_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 10] --> PIPE[ADF Pipeline PL_OPERATIONS_10]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stoperations{env}/ops_event/)]
    BR --> NB1[ADB NB_Bronze_ops_event_10]
    NB1 --> SV[(abfss://silver@stoperations{env}/ops_curated/)]
    SV --> NB2[ADB NB_Silver_ops_curated_10]
    NB2 --> NB3[ADB NB_Gold_ops_kpi_10]
    NB3 --> GD[(abfss://gold@stoperations{env}/ops_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

## Practical Theory Expansion

### ADF orchestration model in this project
ADF is used as the control-plane. Pipelines are parameterized by `load_date`, `domain`, and `watermark`; trigger decisions and dependency checks happen before Databricks execution. We keep the orchestration explicit: ingest first, then Bronze validation, then Silver transforms, then Gold publish, then reconciliation and notifications.

```adf
@concat('abfss://landing@stoperations', pipeline().globalParameters.g_env, '.dfs.core.windows.net/ops_event/', formatDateTime(pipeline().parameters.load_date,'yyyy/MM/dd'))
```

### Databricks execution model
Databricks notebooks are grouped by medallion stage so runtime failures are isolated and reruns are granular. Bronze notebooks prioritize schema capture and lineage, Silver notebooks enforce business rules and dedup logic, Gold notebooks build serving marts with deterministic keys.

```python
# Delta MERGE for Silver->Gold publish
from delta.tables import DeltaTable
source_df = spark.table('operations_silver.ops_curated')
target = DeltaTable.forName(spark, 'operations_gold.ops_kpi')
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
SELECT 'ops_curated' AS silver_table, 'ops_kpi' AS gold_table,
       (SELECT COUNT(1) FROM operations_silver.ops_curated) AS silver_count,
       (SELECT COUNT(1) FROM operations_gold.ops_kpi) AS gold_count;
```

```sql
-- Cutover parity check before old system freeze
SELECT src.table_name, src.row_cnt AS legacy_rows, tgt.row_cnt AS gold_rows,
       (src.row_cnt - tgt.row_cnt) AS variance
FROM audit.legacy_snapshot_counts src
JOIN audit.gold_counts tgt ON src.table_name = tgt.table_name
WHERE ABS(src.row_cnt - tgt.row_cnt) > 0;
```


## Detailed Notebook Playbook

### Notebook `/Projects/operations/01_Bronze/NB_Bronze_ops_event`
- **Purpose:** Execute a scoped medallion responsibility in the `operations` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://landing@stoperations{env}/ops_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `operations_bronze.ops_event` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/operations/02_Silver/NB_Silver_ops_curated`
- **Purpose:** Execute a scoped medallion responsibility in the `operations` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `operations_bronze.ops_event`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `operations_silver.ops_curated` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/operations/03_Gold/NB_Gold_ops_kpi`
- **Purpose:** Execute a scoped medallion responsibility in the `operations` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `operations_silver.ops_curated`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `operations_gold.ops_kpi` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/operations/04_Validation/NB_Validate_ops_kpi`
- **Purpose:** Execute a scoped medallion responsibility in the `operations` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `operations_gold.ops_kpi`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `audit.validation_results` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/operations/05_Recovery/NB_Backfill_ops_event`
- **Purpose:** Execute a scoped medallion responsibility in the `operations` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://bronze@stoperations{env}/ops_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `operations_silver.ops_curated` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.


## Preserved Existing Project Notes

> **Reference:** Adapted from [Analytics6/Azure-Data-Engineering-Notes](https://github.com/Analytics6/Azure-Data-Engineering-Notes) — `15-Retail-Migration-OnPrem-to-Azure.md`

## Project Overview and Business Context

A mid-size enterprise runs critical OLTP and reporting databases on-premises (SQL Server, Oracle, flat-file exports). This certification project delivers a governed migration to Azure: landing raw data in Bronze, building a modern lakehouse in Silver/Gold on Databricks, orchestrating cutover-safe loads with ADF, and validating row counts and business rules before decommissioning on-prem systems.

**Business outcomes:** Reduce data center footprint, enable elastic analytics, meet RPO/RTO targets, and establish a repeatable migration factory pattern.

Per reference migration notes: lift-and-shift plus modernization migrating on-prem ETL, reporting, and data stores to Azure with minimal downtime and validated data parity—rehost or refactor ETL, migrate historical data, ensure report parity, run reconciliation, and comply with data residency.

---

## Platform Concepts (from reference notes)

**Medallion ADLS layout:** Landing (`/landing/`) by source → Pre-Bronze (schema-validated) → Bronze (immutable Delta, full audit) → Silver (cleansed, DQ rules, SCD2) → Gold (star schema, KPIs) → Archive (compliance).

**ADF metadata-driven ingestion:** Centralized metadata for sources/transforms; Lookup + ForEach; watermarking for incrementals; CDC where supported; exponential backoff on transients; audit tables for job metrics.

**Silver (Databricks):** Cleansing, dedup via window functions, type casting, enrichment, MERGE for incrementals, reconciliation with Bronze row counts.

**Gold:** Fact/dimension tables, pre-computed aggregations, Synapse external tables, Power BI semantic models with RLS.

**Delta optimization:** `OPTIMIZE` by high-selectivity columns, `VACUUM` old snapshots, auto-compaction, partition pruning, schema evolution.

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph OnPrem
        SQL[(SQL Server)]
        Ora[(Oracle)]
        Files[CSV/Flat Files]
    end

    subgraph Network
        SHIR[Self-Hosted IR]
        VPN[ExpressRoute / VPN]
    end

    subgraph Azure
        ADF[Azure Data Factory]
        ADLS[(ADLS Gen2 Bronze/Silver/Gold)]
        ADB[Databricks]
        SQLA[Azure SQL / Synapse]
        KV[Key Vault]
        PUR[Azure Purview]
    end

  SQL --> SHIR --> ADF
  Ora --> SHIR --> ADF
  Files --> SHIR --> ADF
  ADF --> ADLS
  ADF --> ADB
  ADB --> ADLS
  ADB --> SQLA
  ADF --> PUR
  ADF --> KV
```

---

## Azure Services Used

| Service | Role |
|---------|------|
| Azure Data Factory | Primary orchestration, incremental loads |
| Self-Hosted Integration Runtime | On-prem connectivity |
| ADLS Gen2 | Medallion lake |
| Azure Databricks | Transformations, SCD, data quality |
| Azure SQL Database / Synapse | Gold serving / mart |
| Azure Key Vault | Credentials |
| Azure Purview | Scan, lineage, glossary |
| Azure DevOps | CI/CD for ARM/JSON pipelines |

---

## Medallion Architecture

### Bronze Layer

| Attribute | Detail |
|-----------|--------|
| **Sources** | SQL Server (`Sales`, `HR`, `Inventory` schemas), Oracle (`FIN_AP`), file shares |
| **Ingestion** | ADF Copy with incremental watermark (`ModifiedDate`) or CDC |
| **Paths** | `abfss://bronze@stmigration{env}.dfs.core.windows.net/{source_system}/{table}/load_date=YYYY-MM-DD/` |
| **Format** | Parquet (Copy) or CSV; append-only |
| **Schema** | Source-faithful + `_adf_load_id`, `_adf_loaded_at` metadata columns |

### Silver Layer

| Attribute | Detail |
|-----------|--------|
| **Cleansing** | Trim strings, standardize dates to UTC, type casting |
| **Dedup** | Primary-key based `dropDuplicates` |
| **Conforming** | Surrogate keys, unified `customer_id` across systems |
| **SCD** | Type 2 on `dim_customer`, `dim_product` |
| **Paths** | `abfss://silver@.../enterprise/{entity}/` |
| **Quality** | Great Expectations / Databricks constraints |

### Gold Layer

| Attribute | Detail |
|-----------|--------|
| **Marts** | `gold.fact_sales`, `gold.fact_inventory_daily`, `gold.dim_date` |
| **Serving** | Synapse dedicated pool external tables or Azure SQL for BI |
| **Aggregates** | Monthly sales by region, inventory turnover |

---

## ADF Orchestration

### Pipelines

| Pipeline | Purpose |
|----------|---------|
| `PL_MIG_Assessment_Inventory` | Metadata-driven table list from SQL metadata |
| `PL_MIG_Bronze_Full_Load` | Initial full copy on-prem → Bronze |
| `PL_MIG_Bronze_Incremental` | Daily incremental by watermark |
| `PL_MIG_Silver_Gold_Transform` | Databricks notebook chain |
| `PL_MIG_Validation` | Lookup row counts; If Condition fail → notify |
| `PL_MIG_Cutover_Final` | Parallel full load + switch connection strings |
| `PL_MIG_Reconcile_Report` | Execute SSRS replacement notebook export |

### Linked Services

| Name | Type |
|------|------|
| `LS_SQL_OnPrem_Sales` | SQL Server via SHIR |
| `LS_Oracle_OnPrem_FIN` | Oracle via SHIR |
| `LS_ADLS_Migration` | ADLS Gen2 MSI |
| `LS_Databricks_Migration` | Databricks |
| `LS_AzureSQL_Gold` | Azure SQL |
| `LS_KeyVault_Migration` | Key Vault |

### Key Activities

- **Copy:** On-prem → Bronze Parquet (partitioned)
- **Lookup:** Control table `migration.table_watermark`
- **If Condition:** `rowsCopied >= expectedMinRows`
- **ForEach:** Table list from metadata dataset
- **Databricks Notebook:** Silver/Gold transforms
- **Stored Procedure:** Update watermark post-success
- **Web:** Trigger Purview scan (optional)

### Triggers

| Trigger | Type | Schedule |
|---------|------|----------|
| `TR_Incremental_Daily` | Schedule | 01:00 local |
| `TR_Validation_Post_Load` | Tumbling window | 1 hour after incremental |
| `TR_Cutover` | Manual / one-time | Migration weekend |

### Dependencies

```mermaid
flowchart TD
    A[PL_MIG_Bronze_Incremental] --> B[PL_MIG_Silver_Gold_Transform]
    B --> C[PL_MIG_Validation]
    C --> D{Pass?}
    D -->|Yes| E[Update Gold serving]
    D -->|No| F[Incident email]
```

### Environment Strategy

- **dev:** Subset of tables (10%), synthetic data masking
- **test:** Full schema, 30-day history, parallel run with on-prem
- **prod:** Cutover after sign-off; read-only on-prem post-cutover

Global parameters: `g_watermark_column`, `g_batch_id`, `g_env`, `g_storage_account`.

---

## ADB Notebooks

### Folder Structure

```
/Migration/
├── 00_Metadata/NB_Table_Registry
├── 01_Bronze/NB_Bronze_Register_Ingest
├── 02_Silver/
│   ├── NB_Silver_Cleanse_Sales
│   ├── NB_Silver_SCD2_Customer
│   └── NB_Silver_Conform_Product
├── 03_Gold/
│   ├── NB_Gold_Fact_Sales
│   └── NB_Gold_Load_Synapse
├── 04_Validation/NB_Reconcile_Rowcounts
└── 05_Cutover/NB_Final_Delta_Sync
```

| Notebook | Inputs | Outputs |
|----------|--------|---------|
| `NB_Silver_Cleanse_Sales` | `bronze.sqlserver_sales` | `silver.sales_orders` |
| `NB_Silver_SCD2_Customer` | Bronze customer tables | `silver.dim_customer` SCD2 |
| `NB_Gold_Fact_Sales` | Silver facts/dims | `gold.fact_sales` |
| `NB_Reconcile_Rowcounts` | Bronze vs on-prem export | Validation report Delta |
| `NB_Final_Delta_Sync` | Last watermark window | Gold sync before cutover |

### Cluster Recommendations

- **Initial load:** 16 workers `Standard_DS5_v2`, optimized shuffle partitions
- **Incremental:** 4–8 workers autoscale job cluster
- **Unity Catalog:** `prod_migration` catalog, schemas per layer

---

## Migration Methodology

| Phase | Lift-Shift vs Refactor |
|-------|------------------------|
| **Assessment** | DMA / SSMA inventory, dependency graph, complexity scoring |
| **Bronze** | Lift-shift extracts (minimal change) |
| **Silver/Gold** | Refactor: star schema, SCD, remove staging procs |
| **Validation** | Row count, checksum hash on keys, aggregate reconciliation |
| **Cutover** | Freeze window, final incremental, DNS/connection string swap |

---

## Security and Monitoring

- SHIR service account: least privilege on source DBs
- Key Vault references in ADF linked services (no plain text passwords)
- Managed Identity for Azure-to-Azure
- ADF alerts on pipeline failure; Purview for PII classification
- Log Analytics workspace: `log-migration-prod`

---

## Sample Naming

- `adf-contoso-migration-prod`
- `stcontosomigrationprod` containers: `bronze`, `silver`, `gold`, `staging`
- `adb-contoso-migration-prod`

---

## Implementation Checklist

- [ ] SHIR installed and tested (latency < 100ms to SQL)
- [ ] Watermark control table deployed
- [ ] Full load completed for all priority-1 tables
- [ ] Reconciliation report signed by business owner
- [ ] Cutover runbook executed and rollback tested
- [ ] On-prem decommission plan approved
