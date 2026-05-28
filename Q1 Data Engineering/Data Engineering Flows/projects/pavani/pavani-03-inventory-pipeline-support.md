# Retail Inventory Data Pipeline Support and Incident Management Framework (Pavani)

### Project Story (Spoken English)

This project is about making `pavani-03-inventory-pipeline-support` dependable in real delivery conditions, not only in demos. We orchestrate the end-to-end run through Azure Data Factory so every load starts with a clear trigger, moves through dependency checks, and lands in predictable windows for business users. From there, Azure Databricks notebooks execute the transformation chain in a medallion pattern, where raw inputs are safely captured in Bronze, corrected and standardized in Silver, and published as decision-ready Gold datasets. I explain the flow in an interview style as if I am walking a team lead through what really runs at 2 AM: what starts first, what can fail, what retries automatically, and what gets escalated. The design intentionally includes operational controls like watermarking, checkpointing, schema drift handling, and audit stamps so we can trust both the data and the process timeline. Even if the source system is delayed or noisy, ADF orchestration + ADB notebooks keep the run recoverable and measurable.

In practical terms, this `support` workload for `inventory` is built so engineers can rerun any slice without breaking downstream consumers. Each diagram below maps a concrete orchestration path in ADF to named notebook responsibilities in Databricks, then shows exactly how records transition from Bronze to Silver to Gold with storage paths and quality expectations. Instead of generic architecture talk, the sections focus on implementation details teams ask in design reviews: parameter strategy, Delta MERGE behavior, late-arrival handling, reconciliation queries, incident routing, and SLA reporting. This makes the document portfolio-ready and execution-ready at the same time, because a new engineer can read it and understand not only what the architecture looks like, but also how to operate it safely under pressure. The notebook deep-dive and code snippets are included so orchestration logic, Spark logic, and validation logic stay connected as one delivery story across ADF and ADB.

## Detailed Flows

**Detailed Flow 01: Source Ingestion and Landing**

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_01` starts `PL_INVENTORY_01`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_01` -> `NB_Silver_inventory_position_01` -> `NB_Gold_stockout_risk_01`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 01] --> PIPE[ADF Pipeline PL_INVENTORY_01]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stinventory{env}/inventory_event/)]
    BR --> NB1[ADB NB_Bronze_inventory_event_01]
    NB1 --> SV[(abfss://silver@stinventory{env}/inventory_position/)]
    SV --> NB2[ADB NB_Silver_inventory_position_01]
    NB2 --> NB3[ADB NB_Gold_stockout_risk_01]
    NB3 --> GD[(abfss://gold@stinventory{env}/stockout_risk/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 02: ADF Trigger to Notebook Handshake**

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_02` starts `PL_INVENTORY_02`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_02` -> `NB_Silver_inventory_position_02` -> `NB_Gold_stockout_risk_02`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_03` starts `PL_INVENTORY_03`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_03` -> `NB_Silver_inventory_position_03` -> `NB_Gold_stockout_risk_03`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_04` starts `PL_INVENTORY_04`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_04` -> `NB_Silver_inventory_position_04` -> `NB_Gold_stockout_risk_04`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 04] --> PIPE[ADF Pipeline PL_INVENTORY_04]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stinventory{env}/inventory_event/)]
    BR --> NB1[ADB NB_Bronze_inventory_event_04]
    NB1 --> SV[(abfss://silver@stinventory{env}/inventory_position/)]
    SV --> NB2[ADB NB_Silver_inventory_position_04]
    NB2 --> NB3[ADB NB_Gold_stockout_risk_04]
    NB3 --> GD[(abfss://gold@stinventory{env}/stockout_risk/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 05: CDC Merge into Gold Serving**

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_05` starts `PL_INVENTORY_05`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_05` -> `NB_Silver_inventory_position_05` -> `NB_Gold_stockout_risk_05`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_06` starts `PL_INVENTORY_06`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_06` -> `NB_Silver_inventory_position_06` -> `NB_Gold_stockout_risk_06`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 06] --> PIPE[ADF Pipeline PL_INVENTORY_06]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stinventory{env}/inventory_event/)]
    BR --> NB1[ADB NB_Bronze_inventory_event_06]
    NB1 --> SV[(abfss://silver@stinventory{env}/inventory_position/)]
    SV --> NB2[ADB NB_Silver_inventory_position_06]
    NB2 --> NB3[ADB NB_Gold_stockout_risk_06]
    NB3 --> GD[(abfss://gold@stinventory{env}/stockout_risk/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 07: Checkpoint and Replay Control**

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_07` starts `PL_INVENTORY_07`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_07` -> `NB_Silver_inventory_position_07` -> `NB_Gold_stockout_risk_07`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_08` starts `PL_INVENTORY_08`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_08` -> `NB_Silver_inventory_position_08` -> `NB_Gold_stockout_risk_08`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 08] --> PIPE[ADF Pipeline PL_INVENTORY_08]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stinventory{env}/inventory_event/)]
    BR --> NB1[ADB NB_Bronze_inventory_event_08]
    NB1 --> SV[(abfss://silver@stinventory{env}/inventory_position/)]
    SV --> NB2[ADB NB_Silver_inventory_position_08]
    NB2 --> NB3[ADB NB_Gold_stockout_risk_08]
    NB3 --> GD[(abfss://gold@stinventory{env}/stockout_risk/)]
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

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_09` starts `PL_INVENTORY_09`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_09` -> `NB_Silver_inventory_position_09` -> `NB_Gold_stockout_risk_09`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `inventory` data from source to governed Gold outputs with observable checkpoints. Includes incident routing, rerun protocol, and RCA capture.
- **Trigger/Orchestration in ADF:** `TR_INVENTORY_10` starts `PL_INVENTORY_10`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_inventory_event_10` -> `NB_Silver_inventory_position_10` -> `NB_Gold_stockout_risk_10`.
- **Medallion transitions:** Bronze (`inventory_event` raw + audit columns) -> Silver (`inventory_position` standardized, deduped, DQ-tagged) -> Gold (`stockout_risk` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stinventory{env}/inventory_event/`; writes to `abfss://bronze@stinventory{env}/inventory_event/`, `abfss://silver@stinventory{env}/inventory_position/`, `abfss://gold@stinventory{env}/stockout_risk/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_INVENTORY_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 10] --> PIPE[ADF Pipeline PL_INVENTORY_10]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stinventory{env}/inventory_event/)]
    BR --> NB1[ADB NB_Bronze_inventory_event_10]
    NB1 --> SV[(abfss://silver@stinventory{env}/inventory_position/)]
    SV --> NB2[ADB NB_Silver_inventory_position_10]
    NB2 --> NB3[ADB NB_Gold_stockout_risk_10]
    NB3 --> GD[(abfss://gold@stinventory{env}/stockout_risk/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

## Practical Theory Expansion

### ADF orchestration model in this project
ADF is used as the control-plane. Pipelines are parameterized by `load_date`, `domain`, and `watermark`; trigger decisions and dependency checks happen before Databricks execution. We keep the orchestration explicit: ingest first, then Bronze validation, then Silver transforms, then Gold publish, then reconciliation and notifications.

```adf
@concat('abfss://landing@stinventory', pipeline().globalParameters.g_env, '.dfs.core.windows.net/inventory_event/', formatDateTime(pipeline().parameters.load_date,'yyyy/MM/dd'))
```

### Databricks execution model
Databricks notebooks are grouped by medallion stage so runtime failures are isolated and reruns are granular. Bronze notebooks prioritize schema capture and lineage, Silver notebooks enforce business rules and dedup logic, Gold notebooks build serving marts with deterministic keys.

```python
# Delta MERGE for Silver->Gold publish
from delta.tables import DeltaTable
source_df = spark.table('inventory_silver.inventory_position')
target = DeltaTable.forName(spark, 'inventory_gold.stockout_risk')
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
SELECT 'inventory_position' AS silver_table, 'stockout_risk' AS gold_table,
       (SELECT COUNT(1) FROM inventory_silver.inventory_position) AS silver_count,
       (SELECT COUNT(1) FROM inventory_gold.stockout_risk) AS gold_count;
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

### Notebook `/Projects/inventory/01_Bronze/NB_Bronze_inventory_event`
- **Purpose:** Execute a scoped medallion responsibility in the `inventory` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://landing@stinventory{env}/inventory_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `inventory_bronze.inventory_event` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/inventory/02_Silver/NB_Silver_inventory_position`
- **Purpose:** Execute a scoped medallion responsibility in the `inventory` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `inventory_bronze.inventory_event`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `inventory_silver.inventory_position` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/inventory/03_Gold/NB_Gold_stockout_risk`
- **Purpose:** Execute a scoped medallion responsibility in the `inventory` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `inventory_silver.inventory_position`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `inventory_gold.stockout_risk` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/inventory/04_Validation/NB_Validate_stockout_risk`
- **Purpose:** Execute a scoped medallion responsibility in the `inventory` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `inventory_gold.stockout_risk`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `audit.validation_results` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/inventory/05_Recovery/NB_Backfill_inventory_event`
- **Purpose:** Execute a scoped medallion responsibility in the `inventory` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://bronze@stinventory{env}/inventory_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `inventory_silver.inventory_position` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.


## Preserved Existing Project Notes

> **Reference:** Adapted from [https://github.com/Analytics6/Azure-Data-Engineering-Notes](https://github.com/Analytics6/Azure-Data-Engineering-Notes) — `14-Retail-Support-Project.md`


## Project Overview and Business Context

Production support for inventory/supply chain pipelines (Pavani project 1 & 2). Incident management framework with P1–P3 severities, runbooks, and SLA dashboards specific to **stock accuracy** and **ASN freshness**.

## Platform Concepts (Analytics6 Reference)

**Medallion ADLS layout:** Landing by source → Pre-Bronze (schema validation) → Bronze (immutable Delta) → Silver (cleansed, DQ, SCD) → Gold (business models) → Archive.

**ADF:** Metadata-driven ingestion (Lookup + ForEach), watermark incrementals, CDC, exponential backoff, audit logging. Linked services use MSI + Key Vault; SHIR for on-prem.

**Databricks / Delta:** MERGE incrementals, `OPTIMIZE`/`VACUUM`, partition pruning, Unity Catalog governance.

**Monitoring:** Log Analytics diagnostics, pipeline failure action groups, SLA KQL dashboards.

---

## Architecture Diagram

```mermaid
flowchart TB
    InvPipelines[Inventory ADF Pipelines] --> LA
    LA --> IM[Incident Mgmt - ServiceNow]
    LA --> OpsMedallion[Bronze/Silver/Gold Ops]
    OpsMedallion --> PBI[Support Dashboard]
```

---

## Medallion (Ops)

- Bronze: pipeline logs, `bronze/support/adf_runs/`
- Silver: `silver.inventory_pipeline_health`
- Gold: `gold.asn_freshness_sla`, `gold.stock_accuracy_sla`

---

## ADF Orchestration

`PL_INV_SUP_Telemetry`, `PL_INV_SUP_Rerun_Store_Load` (ForEach `store_id`), `PL_INV_SUP_ASN_Recovery`.

**If Condition:** ASN not loaded by 08:00 → P2 ticket Web activity.

---

## Runbooks

- **RB-INV-01:** WMS snapshot missing — rerun `PL_SC_Bronze_WMS`
- **RB-INV-02:** Stream lag — scale cluster, check checkpoint
- **RB-INV-03:** Vendor SFTP failure — failover to secondary host

---

## ADB

`NB_Ops_Inventory_Freshness`, `NB_Store_Level_Gap_Detection` — daily 2 workers.

---

## Monitoring

Alerts: `stockout_risk` table stale > 2h; open P1 page on-call within 15 min.
