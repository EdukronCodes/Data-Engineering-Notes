# HDInsight Hive Activity

## Overview
The **HDInsight Hive** activity runs a **Hive** script on an HDInsight cluster (or on-demand cluster). Hive provides SQL-like queries over data in HDFS or Azure Storage (e.g., Blob, ADLS). Used for batch SQL-style processing on big data.

## Key Features
- **Hive script**: Inline script or script in Azure Blob; HiveQL statements (CREATE TABLE, SELECT, INSERT, etc.).
- **Cluster**: Use existing HDInsight (Hadoop) cluster or create on-demand cluster for the run.
- **Storage**: Script and data typically in Blob or ADLS; Hive reads/writes via external tables or paths.
- **Output**: Activity completes when Hive job finishes; output can be used for control flow (e.g., row count in logs).

## Common Properties
| Property | Description |
|----------|-------------|
| HDInsight linked service | Cluster (existing or on-demand) |
| Script linked service | Storage where script is stored (if not inline) |
| Script path / Inline script | Hive script location or inline HiveQL |
| Arguments | Variables passed to script (e.g., date, path) |

## When to Use

### Use Cases
1. **Legacy Hive workloads** – Existing Hive scripts and tables; ADF runs them on schedule on HDInsight.
2. **Batch SQL on raw data** – Large files in Blob/ADLS; Hive queries for aggregation, filter, join.
3. **Data lake SQL** – Hive external tables over Blob/ADLS; run reports or ETL via Hive activity.
4. **Migration** – Move on-prem Hive jobs to Azure; keep Hive, change cluster to HDInsight.
5. **Partition management** – Hive scripts to add/drop partitions on large tables.
6. **Cost control** – Use on-demand HDInsight so cluster exists only during activity run.

### When NOT to Use
- New projects (prefer **Synapse Spark** or **Databricks** for modern SQL and Spark).
- Simple copy (use **Copy**).
- Low-latency or interactive queries (use Synapse SQL or interactive engines).

## Example Scenarios
- Copy raw CSV to Blob; HDInsight Hive runs script that creates external table and INSERT INTO summary table.
- Nightly Hive script that aggregates logs by date and writes to Blob; ADF triggers and waits.
- On-demand HDInsight cluster runs Hive script with parameterized date; cluster torn down after run.
