# Databricks Notebook Activity

## Overview
The **Databricks Notebook** activity runs an existing **Databricks notebook** on a Databricks cluster (existing or job cluster). It is used to run Spark-based transformations, ML, or analytics written in Python, Scala, SQL, or R inside the notebook.

## Key Features
- **Notebook execution**: Specify workspace path to notebook (e.g., `/path/to/notebook`).
- **Parameters**: Pass base parameters (string, number, etc.) to the notebook; notebook reads them via `dbutils.widgets`.
- **Cluster**: Use existing cluster (by ID) or job cluster (config in activity); job cluster is created per run and torn down after.
- **Output**: Notebook can write results to widgets or external store; ADF can use run status and optionally output in subsequent activities.

## Common Properties
| Property | Description |
|----------|-------------|
| Databricks linked service | Workspace URL and auth (token or AAD) |
| Notebook path | Path in workspace (e.g., /Analytics/Transform) |
| Base parameters | Key-value parameters for the notebook |
| Cluster | Existing cluster ID or job cluster specification |
| Python/Scala/Jar libraries | Optional libraries to install on cluster |

## When to Use

### Use Cases
1. **Spark ETL** – Complex transformations (joins, window functions, Delta) implemented in notebook; ADF triggers and waits.
2. **ML training or scoring** – Run MLlib or other ML code in notebook; read from Blob/ADLS, write model or scores.
3. **Delta Lake operations** – Merge, vacuum, optimize Delta tables; notebook encapsulates logic.
4. **Data quality or profiling** – Notebook runs profiling or validation; result (e.g., pass/fail) can drive pipeline branch.
5. **Reusable analytics** – Same notebook used by ADF and by data scientists interactively; parameters for date, table, env.
6. **Orchestration from ADF** – ADF handles schedule, parameters, and dependencies; Databricks handles compute and logic.

### When NOT to Use
- Simple copy (use **Copy**).
- Logic that fits in ADF Data Flow (use **Data Flow**).
- One-off ad-hoc runs (run from Databricks UI or workflow).

## Example Scenarios
- Daily pipeline: Copy raw data to ADLS; Databricks Notebook runs ETL notebook with parameters (date, env); notebook writes to Delta; ADF runs Validation.
- ADF passes batch_id and run_date; notebook loads from Blob, runs ML scoring, writes to Synapse.
- Databricks Notebook runs Delta merge and OPTIMIZE; ADF triggers after Copy lands new Parquet.
