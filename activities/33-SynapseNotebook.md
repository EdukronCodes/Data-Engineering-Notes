# Synapse Notebook Activity

## Overview
The **Synapse Notebook** activity runs an **Apache Spark notebook** in **Azure Synapse Analytics** (Synapse workspace). The notebook can be written in PySpark, Spark SQL, Scala, or .NET for Spark. Used for Spark-based ETL, analytics, or ML inside Synapse with ADF orchestration.

## Key Features
- **Notebook in Synapse**: Run notebook by path in Synapse workspace (e.g., folder/notebook name).
- **Parameters**: Pass base parameters (string, number) to the notebook; notebook reads via `mssparkutils.notebook.run` or widget equivalents.
- **Spark pool**: Use existing Spark pool or specify pool name/size; pool can be auto-scaled or fixed.
- **Output**: Notebook output (e.g., return value from last cell or `mssparkutils`) can be used in subsequent ADF activities (where supported).
- **Integration**: Same workspace as Synapse SQL and Pipelines; easy to chain with Copy and other Synapse/ADF activities.

## Common Properties
| Property | Description |
|----------|-------------|
| Synapse linked service | Synapse workspace connection |
| Notebook path | Path to notebook in workspace |
| Base parameters | Key-value parameters for the notebook |
| Spark pool | Target Spark pool (by name or config) |
| Configuration | Spark config, executor size, etc. |

## When to Use

### Use Cases
1. **Spark ETL in Synapse** – Transform data in Spark (PySpark/SQL); read from lake, write to lake or SQL pool; ADF triggers and passes parameters.
2. **Data lake processing** – Notebook for Delta, Parquet, or CSV processing; merge, aggregate, or curate; ADF for schedule and dependencies.
3. **ML scoring or training** – Run ML model in notebook (e.g., Synapse ML, MLlib); read from table/lake, write scores; ADF orchestrates.
4. **Data quality or profiling** – Notebook runs checks or profiling; returns pass/fail or metrics; ADF branches on result.
5. **Unified pipeline** – ADF Copy + Synapse Notebook + Synapse SQL stored proc in one pipeline; single workspace.
6. **Reusable notebooks** – Same notebook for interactive and batch; parameters for date, table, environment.

### When NOT to Use
- Simple copy only (use **Copy**).
- Logic that fits in ADF Data Flow (use **Data Flow**).
- No Synapse workspace (use **Databricks Notebook** or **Custom** activity).

## Example Scenarios
- ADF Copy lands raw data in Synapse lake; Synapse Notebook runs transform notebook with date parameter; notebook writes to curated zone; ADF runs Validation.
- Pipeline passes batch_id and run_date; notebook loads from table, runs ML scoring, writes to scoring table.
- Synapse Notebook runs Delta merge and OPTIMIZE; ADF triggers after Copy; same workspace, no data movement out.
