# Loans & Collections Enterprise Reporting Data Mart (Karthik)

### Project Story (Spoken English)

This project is about making `karthik-02-loans-collections-datamart` dependable in real delivery conditions, not only in demos. We orchestrate the end-to-end run through Azure Data Factory so every load starts with a clear trigger, moves through dependency checks, and lands in predictable windows for business users. From there, Azure Databricks notebooks execute the transformation chain in a medallion pattern, where raw inputs are safely captured in Bronze, corrected and standardized in Silver, and published as decision-ready Gold datasets. I explain the flow in an interview style as if I am walking a team lead through what really runs at 2 AM: what starts first, what can fail, what retries automatically, and what gets escalated. The design intentionally includes operational controls like watermarking, checkpointing, schema drift handling, and audit stamps so we can trust both the data and the process timeline. Even if the source system is delayed or noisy, ADF orchestration + ADB notebooks keep the run recoverable and measurable.

In practical terms, this `batch` workload for `finance` is built so engineers can rerun any slice without breaking downstream consumers. Each diagram below maps a concrete orchestration path in ADF to named notebook responsibilities in Databricks, then shows exactly how records transition from Bronze to Silver to Gold with storage paths and quality expectations. Instead of generic architecture talk, the sections focus on implementation details teams ask in design reviews: parameter strategy, Delta MERGE behavior, late-arrival handling, reconciliation queries, incident routing, and SLA reporting. This makes the document portfolio-ready and execution-ready at the same time, because a new engineer can read it and understand not only what the architecture looks like, but also how to operate it safely under pressure. The notebook deep-dive and code snippets are included so orchestration logic, Spark logic, and validation logic stay connected as one delivery story across ADF and ADB.

## Detailed Flows

**Detailed Flow 01: Source Ingestion and Landing**

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_01` starts `PL_FINANCE_01`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_01` -> `NB_Silver_ledger_curated_01` -> `NB_Gold_risk_kpi_01`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 01] --> PIPE[ADF Pipeline PL_FINANCE_01]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stfinance{env}/ledger_event/)]
    BR --> NB1[ADB NB_Bronze_ledger_event_01]
    NB1 --> SV[(abfss://silver@stfinance{env}/ledger_curated/)]
    SV --> NB2[ADB NB_Silver_ledger_curated_01]
    NB2 --> NB3[ADB NB_Gold_risk_kpi_01]
    NB3 --> GD[(abfss://gold@stfinance{env}/risk_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 02: ADF Trigger to Notebook Handshake**

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_02` starts `PL_FINANCE_02`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_02` -> `NB_Silver_ledger_curated_02` -> `NB_Gold_risk_kpi_02`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 02 (batch)
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

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_03` starts `PL_FINANCE_03`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_03` -> `NB_Silver_ledger_curated_03` -> `NB_Gold_risk_kpi_03`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_04` starts `PL_FINANCE_04`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_04` -> `NB_Silver_ledger_curated_04` -> `NB_Gold_risk_kpi_04`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 04] --> PIPE[ADF Pipeline PL_FINANCE_04]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stfinance{env}/ledger_event/)]
    BR --> NB1[ADB NB_Bronze_ledger_event_04]
    NB1 --> SV[(abfss://silver@stfinance{env}/ledger_curated/)]
    SV --> NB2[ADB NB_Silver_ledger_curated_04]
    NB2 --> NB3[ADB NB_Gold_risk_kpi_04]
    NB3 --> GD[(abfss://gold@stfinance{env}/risk_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 05: CDC Merge into Gold Serving**

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_05` starts `PL_FINANCE_05`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_05` -> `NB_Silver_ledger_curated_05` -> `NB_Gold_risk_kpi_05`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 05 (batch)
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

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_06` starts `PL_FINANCE_06`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_06` -> `NB_Silver_ledger_curated_06` -> `NB_Gold_risk_kpi_06`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 06] --> PIPE[ADF Pipeline PL_FINANCE_06]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stfinance{env}/ledger_event/)]
    BR --> NB1[ADB NB_Bronze_ledger_event_06]
    NB1 --> SV[(abfss://silver@stfinance{env}/ledger_curated/)]
    SV --> NB2[ADB NB_Silver_ledger_curated_06]
    NB2 --> NB3[ADB NB_Gold_risk_kpi_06]
    NB3 --> GD[(abfss://gold@stfinance{env}/risk_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

**Detailed Flow 07: Checkpoint and Replay Control**

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_07` starts `PL_FINANCE_07`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_07` -> `NB_Silver_ledger_curated_07` -> `NB_Gold_risk_kpi_07`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

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

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_08` starts `PL_FINANCE_08`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_08` -> `NB_Silver_ledger_curated_08` -> `NB_Gold_risk_kpi_08`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 08] --> PIPE[ADF Pipeline PL_FINANCE_08]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stfinance{env}/ledger_event/)]
    BR --> NB1[ADB NB_Bronze_ledger_event_08]
    NB1 --> SV[(abfss://silver@stfinance{env}/ledger_curated/)]
    SV --> NB2[ADB NB_Silver_ledger_curated_08]
    NB2 --> NB3[ADB NB_Gold_risk_kpi_08]
    NB3 --> GD[(abfss://gold@stfinance{env}/risk_kpi/)]
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

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_09` starts `PL_FINANCE_09`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_09` -> `NB_Silver_ledger_curated_09` -> `NB_Gold_risk_kpi_09`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
sequenceDiagram
    participant T as ADF Trigger
    participant P as ADF Pipeline
    participant B as ADB Bronze Notebook
    participant S as ADB Silver Notebook
    participant G as ADB Gold Notebook
    participant M as Monitor/Alerts
    T->>P: Start run 09 (batch)
    P->>B: Execute with params (load_date, watermark)
    B-->>P: Bronze write complete
    P->>S: Execute cleansing + DQ
    S-->>P: Silver publish complete
    P->>G: Execute MERGE into Gold
    G-->>P: Gold metrics + row counts
    P->>M: Emit status, retries, escalation
```

**Detailed Flow 10: Publishing and Consumer SLA**

- **Purpose:** Drive `finance` data from source to governed Gold outputs with observable checkpoints. Includes dependency gating and deterministic daily windows.
- **Trigger/Orchestration in ADF:** `TR_FINANCE_10` starts `PL_FINANCE_10`; Lookup -> IfCondition -> Copy -> Databricks activity chain with retry policy `(count=3, interval=120s)`.
- **Databricks notebook(s):** `NB_Bronze_ledger_event_10` -> `NB_Silver_ledger_curated_10` -> `NB_Gold_risk_kpi_10`.
- **Medallion transitions:** Bronze (`ledger_event` raw + audit columns) -> Silver (`ledger_curated` standardized, deduped, DQ-tagged) -> Gold (`risk_kpi` business serving model).
- **Inputs/Outputs and storage:** Input from `abfss://landing@stfinance{env}/ledger_event/`; writes to `abfss://bronze@stfinance{env}/ledger_event/`, `abfss://silver@stfinance{env}/ledger_curated/`, `abfss://gold@stfinance{env}/risk_kpi/`.
- **Monitoring/Retry/Error handling:** ADF activity run IDs stamped into Delta audit table; failed notebooks route to `PL_FINANCE_INCIDENT` with Logic App/Pager alert and rerun token.

```mermaid
flowchart LR
    TRG[ADF Trigger 10] --> PIPE[ADF Pipeline PL_FINANCE_10]
    PIPE --> COPY[Copy/Landing to Bronze]
    COPY --> BR[(abfss://bronze@stfinance{env}/ledger_event/)]
    BR --> NB1[ADB NB_Bronze_ledger_event_10]
    NB1 --> SV[(abfss://silver@stfinance{env}/ledger_curated/)]
    SV --> NB2[ADB NB_Silver_ledger_curated_10]
    NB2 --> NB3[ADB NB_Gold_risk_kpi_10]
    NB3 --> GD[(abfss://gold@stfinance{env}/risk_kpi/)]
    GD --> MON[ADF Monitor + Retry + Alert]
```

## Practical Theory Expansion

### ADF orchestration model in this project
ADF is used as the control-plane. Pipelines are parameterized by `load_date`, `domain`, and `watermark`; trigger decisions and dependency checks happen before Databricks execution. We keep the orchestration explicit: ingest first, then Bronze validation, then Silver transforms, then Gold publish, then reconciliation and notifications.

```adf
@concat('abfss://landing@stfinance', pipeline().globalParameters.g_env, '.dfs.core.windows.net/ledger_event/', formatDateTime(pipeline().parameters.load_date,'yyyy/MM/dd'))
```

### Databricks execution model
Databricks notebooks are grouped by medallion stage so runtime failures are isolated and reruns are granular. Bronze notebooks prioritize schema capture and lineage, Silver notebooks enforce business rules and dedup logic, Gold notebooks build serving marts with deterministic keys.

```python
# Delta MERGE for Silver->Gold publish
from delta.tables import DeltaTable
source_df = spark.table('finance_silver.ledger_curated')
target = DeltaTable.forName(spark, 'finance_gold.risk_kpi')
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
SELECT 'ledger_curated' AS silver_table, 'risk_kpi' AS gold_table,
       (SELECT COUNT(1) FROM finance_silver.ledger_curated) AS silver_count,
       (SELECT COUNT(1) FROM finance_gold.risk_kpi) AS gold_count;
```


## Detailed Notebook Playbook

### Notebook `/Projects/finance/01_Bronze/NB_Bronze_ledger_event`
- **Purpose:** Execute a scoped medallion responsibility in the `finance` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://landing@stfinance{env}/ledger_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `finance_bronze.ledger_event` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/finance/02_Silver/NB_Silver_ledger_curated`
- **Purpose:** Execute a scoped medallion responsibility in the `finance` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `finance_bronze.ledger_event`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `finance_silver.ledger_curated` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/finance/03_Gold/NB_Gold_risk_kpi`
- **Purpose:** Execute a scoped medallion responsibility in the `finance` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `finance_silver.ledger_curated`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `finance_gold.risk_kpi` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/finance/04_Validation/NB_Validate_risk_kpi`
- **Purpose:** Execute a scoped medallion responsibility in the `finance` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `finance_gold.risk_kpi`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `audit.validation_results` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.

### Notebook `/Projects/finance/05_Recovery/NB_Backfill_ledger_event`
- **Purpose:** Execute a scoped medallion responsibility in the `finance` pipeline.
- **Parameters/widgets:** `env`, `load_date`, `run_id`, `watermark`, `rerun_mode` (widget defaults validated at start).
- **Input tables/paths:** `abfss://bronze@stfinance{env}/ledger_event/`.
- **Transformation logic:** Enforce schema, derive surrogate keys, deduplicate by business key + event time, and apply business-rule flags.
- **Output tables/paths:** `finance_silver.ledger_curated` with audit columns `_run_id`, `_adf_pipeline_run_id`, `_processed_ts`.
- **Expectations/checks:** Row-count thresholds, null checks on mandatory columns, duplicate ratio threshold, and freshness SLA check.
- **Failure handling:** Write failed records to quarantine path, log exception context to `audit.pipeline_errors`, return non-zero status to ADF for controlled retry/escalation.


## Preserved Existing Project Notes

> **Reference:** Adapted from [https://github.com/Analytics6/Azure-Data-Engineering-Notes](https://github.com/Analytics6/Azure-Data-Engineering-Notes) — `02-Financial-Data-Processing-System.md, 11-Banking-Risk-Management-System.md`

## Project Overview and Business Context

Financial data mart for loans, collections, and risk KPIs with SOX audit trails.

**Karthik focus:** Collections/regulatory reporting mart (lighter than Shiva core banking DW).


## Platform Concepts (Analytics6 Reference)

**Medallion ADLS layout:** Landing by source → Pre-Bronze (schema validation) → Bronze (immutable Delta) → Silver (cleansed, DQ, SCD) → Gold (business models) → Archive.

**ADF:** Metadata-driven ingestion (Lookup + ForEach), watermark incrementals, CDC, exponential backoff, audit logging. Linked services use MSI + Key Vault; SHIR for on-prem.

**Databricks / Delta:** MERGE incrementals, `OPTIMIZE`/`VACUUM`, partition pruning, Unity Catalog governance.

**Monitoring:** Log Analytics diagnostics, pipeline failure action groups, SLA KQL dashboards.


---

## Architecture Diagram

```mermaid
flowchart TB
    Sources[Source Systems] --> ADF[Azure Data Factory]
    ADF --> Bronze[(Bronze Delta)]
    Bronze --> ADB[Databricks]
    ADB --> Silver --> Gold
    Gold --> PBI[Power BI / Synapse]
    ADF --> KV[Key Vault]
    ADB --> UC[Unity Catalog]
```

---

## Medallion Architecture

### Bronze
- Source-faithful ingest with `_adf_loaded_at`, `batch_id` metadata
- Paths: `abfss://bronze@st{org}{env}.dfs.core.windows.net/{domain}/`

### Silver
- Cleansing, dedup, SCD where applicable; DQ quarantine tables per reference pre-bronze validation patterns

### Gold
- `gold.fact_loan_balance`
- `gold.collections_aging`
- `gold.risk_exposure`

---

## ADF Orchestration

| Pipeline | Purpose |
|----------|---------|
| `PL_KAR_LOAN_Bronze` | See ADF orchestration below |
| `PL_KAR_LOAN_Gold` | See ADF orchestration below |
| `PL_KAR_Risk_Weekly` | See ADF orchestration below |

**Linked services:** `LS_ADLS`, `LS_Databricks`, `LS_KeyVault`, `LS_SHIR` (on-prem if needed).

**Triggers:** Schedule + tumbling window for validation; environment global parameters `g_env`, `g_storage_account`.

---

## ADB Notebooks

```
/Karthik/Loans/NB_Silver_Conform
NB_Gold_Collections
NB_Risk_Summary
```

**Cluster:** Job clusters for batch; autoscaling streaming cluster where applicable. **Delta:** `delta.autoOptimize.optimizeWrite` on Silver/Gold.

---

## Security & Monitoring

- MSI + Key Vault; private endpoints in prod
- ADF failure → Action Group; Log Analytics KQL for SLA and row-count drift (per reference monitoring sections)

---

## Implementation Phases

| Phase | Focus |
|-------|-------|
| 1 | Foundation (RG, ADLS, Key Vault, ADF, Databricks) |
| 2 | Bronze ingest |
| 3 | Silver/Gold transforms |
| 4 | Consumption & monitoring |
| 5 | Hardening & runbooks |
