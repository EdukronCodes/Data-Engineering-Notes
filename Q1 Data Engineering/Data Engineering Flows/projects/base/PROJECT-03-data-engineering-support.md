# PROJECT 3 — Azure Data Engineering Support: Support Simulation & Runbook Development

### Project Story (Spoken English)

This project is about making `PROJECT-03-data-engineering-support` dependable in real delivery conditions, not only in demos. We orchestrate the end-to-end run through Azure Data Factory so every load starts with a clear trigger, moves through dependency checks, and lands in predictable windows for business users. From there, Azure Databricks notebooks execute the transformation chain in a medallion pattern, where raw inputs are safely captured in Bronze, corrected and standardized in Silver, and published as decision-ready Gold datasets. I explain the flow in an interview style as if I am walking a team lead through what really runs at 2 AM: what starts first, what can fail, what retries automatically, and what gets escalated. The design intentionally includes operational controls like watermarking, checkpointing, schema drift handling, and audit stamps so we can trust both the data and the process timeline. Even if the source system is delayed or noisy, ADF orchestration + ADB notebooks keep the run recoverable and measurable.

In practical terms, this `support` workload for `operations` is built so engineers can rerun any slice without breaking downstream consumers. Each diagram below maps a concrete orchestration path in ADF to named notebook responsibilities in Databricks, then shows exactly how records transition from Bronze to Silver to Gold with storage paths and quality expectations. Instead of generic architecture talk, the sections focus on implementation details teams ask in design reviews: parameter strategy, Delta MERGE behavior, late-arrival handling, reconciliation queries, incident routing, and SLA reporting. This makes the document portfolio-ready and execution-ready at the same time, because a new engineer can read it and understand not only what the architecture looks like, but also how to operate it safely under pressure. The notebook deep-dive and code snippets are included so orchestration logic, Spark logic, and validation logic stay connected as one delivery story across ADF and ADB.

## Detailed Flows

**Detailed Flow 01: Source Ingestion and Landing**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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
    T->>P: Start run 02 (support)
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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
    T->>P: Start run 05 (support)
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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
    T->>P: Start run 09 (support)
    P->>B: Execute with params (load_date, watermark)
    B-->>P: Bronze write complete
    P->>S: Execute cleansing + DQ
    S-->>P: Silver publish complete
    P->>G: Execute MERGE into Gold
    G-->>P: Gold metrics + row counts
    P->>M: Emit status, retries, escalation
```

**Detailed Flow 10: Publishing and Consumer SLA**

- **Purpose:** Drive `operations` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
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

```python
# Retry + rerun token capture for support workflows
try:
    dbutils.notebook.run(nb_path, 0, params)
except Exception as ex:
    spark.sql(f"""
      INSERT INTO ops.incident_log
      VALUES (current_timestamp(), '{nb_path}', '{str(ex)[:180]}', '{params.get('run_id')}')
    """)
    raise
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

> **Reference:** Adapted from [Analytics6/Azure-Data-Engineering-Notes](https://github.com/Analytics6/Azure-Data-Engineering-Notes) — `14-Retail-Support-Project.md`, `09-Enterprise-Data-Governance-Observability-Platform.md`

## Project Overview and Business Context

Operations teams supporting Azure data platforms need standardized runbooks, incident workflows, and observable pipelines. This project simulates L2/L3 production support for ADF + Databricks estates: monitoring pipeline SLAs, triaging failures, executing recovery procedures, and maintaining knowledge base articles aligned to ITIL practices.

**Business outcomes:** Mean time to recovery (MTTR) under 60 minutes for P1 data incidents, 99.5% pipeline SLA, auditable incident history.

Reference support platform scope: operational support for data operations—incident management, runbooks, alerting, automated remediation for common pipeline failures; on-call routing, automated retries, incident tracking, runbook automation via Log Analytics, Logic Apps, and Automation Runbooks.

**Governance tie-in (reference):** Purview catalog/lineage, data quality rules (completeness, timeliness), and observability metrics for SLA compliance and audit trails.

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Platforms
        ADF[Azure Data Factory]
        ADB[Databricks Jobs]
        ADLS[ADLS Gen2]
    end

    subgraph Observability
        LA[Log Analytics]
        AM[Azure Monitor Alerts]
        AG[Action Groups]
        SB[Service Bus / ITSM webhook]
    end

    subgraph Support_Tools
        RUN[Runbook Wiki / Markdown]
        AUTO[Automation Account / Logic Apps]
        PBI[Support Dashboard]
    end

    ADF --> LA
    ADB --> LA
    LA --> AM --> AG --> SB
    AG --> AUTO
    LA --> PBI
    RUN -.-> AUTO
```

---

## Azure Services Used

| Service | Role |
|---------|------|
| Azure Data Factory | Monitored pipelines (simulated failures) |
| Azure Databricks | Job clusters for batch workloads |
| Log Analytics | Centralized diagnostics |
| Azure Monitor | Metric and log alerts |
| Action Groups | Email, SMS, Teams, webhook |
| Azure Automation / Logic Apps | Runbook automation (restart IR, rerun pipeline) |
| Azure Key Vault | Secret rotation procedures |
| Microsoft Sentinel (optional) | SIEM correlation |

---

## Medallion Architecture (Support Telemetry)

Support projects also land **operational telemetry** into a small medallion for analytics on platform health.

### Bronze

- **Sources:** ADF Activity Runs, Pipeline Runs, Databricks cluster events (via diagnostic settings)
- **Path:** `abfss://bronze@stdataops{env}.dfs.core.windows.net/platform/adf_activity_runs/`
- **Schema:** `run_id, pipeline_name, activity_name, status, error_message, start_time, end_time, duration_sec`

### Silver

- Conformed `silver.pipeline_run_summary` — one row per pipeline run with SLA flag
- Joined with configuration table `silver.pipeline_sla_config`

### Gold

- `gold.support_daily_sla` — % success by pipeline, env, owner team
- `gold.incident_metrics` — MTTR, incident count by severity (from ITSM export)

---

## ADF Orchestration (Support & Simulation)

### Pipelines

| Pipeline | Purpose |
|----------|---------|
| `PL_OPS_Ingest_ADF_Logs` | Copy diagnostic export → Bronze |
| `PL_OPS_Silver_SLA_Calc` | Databricks: compute SLA breaches |
| `PL_OPS_Gold_Dashboard_Refresh` | Gold aggregates for Power BI |
| `PL_SIM_Inject_Failure` | Dev/test: Fail activity for training |
| `PL_OPS_Rerun_Failed_Window` | Parameterized rerun with `windowStart`/`windowEnd` |
| `PL_OPS_SHIR_Health_Check` | Until loop + Web ping on-prem gateway |

### Activities

- **Copy:** Log Analytics export or Storage → Bronze
- **Lookup:** Last successful run timestamp
- **If Condition:** `activityStatus == 'Failed'`
- **Web:** POST to Logic App for ticket creation
- **ForEach:** Failed pipelines list → child `Execute Pipeline`
- **Databricks Notebook:** SLA calculations

### Triggers

| Trigger | Schedule |
|---------|----------|
| `TR_OPS_Hourly_Telemetry` | Every hour |
| `TR_OPS_Daily_SLA_Report` | 06:00 UTC |
| `TR_SIM_Weekly_Drill` | Monday 09:00 (test env only) |

### Parameterization

- `g_support_env`, `g_log_analytics_workspace_id`, `g_it_sm_webhook_url`
- Separate ADF instance `adf-contoso-ops-prod` vs. business `adf-contoso-iot-prod`

---

## ADB Notebooks

```
/DataOpsSupport/
├── 01_Bronze/NB_Ingest_ADF_Diagnostics
├── 02_Silver/NB_Conform_Pipeline_Runs
├── 03_Gold/NB_SLA_Aggregates
└── 99_Remediation/NB_Identify_Stale_Watermarks
```

| Notebook | Purpose |
|----------|---------|
| `NB_Conform_Pipeline_Runs` | Parse JSON diagnostics → silver |
| `NB_SLA_Aggregates` | Join config, flag breaches |
| `NB_Identify_Stale_Watermarks` | Find tables with no load > 26h |

**Cluster:** Small job cluster 2–4 workers; daily schedule only.

---

## Incident Workflow (ITIL-Aligned)

```mermaid
stateDiagram-v2
    [*] --> Detect: Alert fires
    Detect --> Triage: L1 on-call
    Triage --> L2: Data engineer
    L2 --> Diagnose: Runbook steps
    Diagnose --> Remediate: Fix/rerun
    Remediate --> Validate: Row counts/SLA
    Validate --> Close: PIR if P1
    Validate --> Escalate: Vendor/Microsoft
    Escalate --> Diagnose
```

### Severity Matrix

| Sev | Criteria | Response | Example |
|-----|----------|----------|---------|
| P1 | Prod Gold stale > 4h | 15 min | Sales mart empty |
| P2 | Single pipeline fail | 1 hr | Bronze load fail |
| P3 | Dev/test issue | Next business day | Parameter typo |

---

## Runbook Catalog (Samples)

1. **RB-ADF-001** — Pipeline failure: diagnose Activity Run error, rerun with same parameters
2. **RB-ADF-002** — SHIR offline: restart service, check port 443, escalate to infra
3. **RB-ADB-003** — Streaming job stopped: verify checkpoint, restart job, check lag
4. **RB-DATA-004** — Watermark corruption: restore from `control.watermark_backup`
5. **RB-KV-005** — Secret expired: rotate secret, update Key Vault reference, warm-up pipeline

Each runbook includes: prerequisites, steps, rollback, validation query, escalation path.

---

## Security

- Support engineers: Reader on prod ADF, Contributor on dev/test
- Runbook automation MI: `Pipeline Contributor` scoped to resource group
- No secrets in runbooks; link to Key Vault secret names only
- PIM for elevated access to prod Databricks

---

## Monitoring

- Alert: `Pipeline Failed` count > 0 in 15 min (prod)
- Alert: `Available Memory < 10%` on SHIR node
- Dashboard: SLA %, failed runs trend, open incidents
- Weekly PIR template for recurring failures

---

## Sample Naming

- `rg-contoso-dataops-prod`
- `adf-contoso-ops-prod`
- `law-contoso-dataops-prod`
- `ag-contoso-data-p1-alerts`

---

## Implementation Phases

| Phase | Deliverable |
|-------|-------------|
| 1 | Log Analytics diagnostics enabled on all ADF/ADB |
| 2 | Bronze/Silver/Gold ops telemetry pipelines |
| 3 | Alert rules + Action Groups |
| 4 | Runbook library (min 10 articles) |
| 5 | Simulation drills in test subscription |
| 6 | Power BI support dashboard |

### Checklist

- [ ] All prod pipelines have owner tags and SLA config rows
- [ ] Runbooks linked from alert descriptions
- [ ] Quarterly game day executed and documented
- [ ] Escalation matrix published to Teams channel
