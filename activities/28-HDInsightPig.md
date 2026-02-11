# HDInsight Pig Activity

## Overview
The **HDInsight Pig** activity runs a **Pig** script on an HDInsight cluster. Pig uses Pig Latin to express data flows (load, transform, filter, group, store) and compiles to MapReduce or Tez. Used for ETL-style pipelines on large data in HDFS or Azure Storage.

## Key Features
- **Pig script**: Inline or stored in Blob; Pig Latin (LOAD, FILTER, GROUP, FOREACH, STORE).
- **Cluster**: Existing or on-demand HDInsight cluster (Hadoop).
- **Storage**: Read/write from Blob or ADLS via paths or Hive catalog.
- **Output**: Activity completes when Pig job finishes; useful for orchestration.

## Common Properties
| Property | Description |
|----------|-------------|
| HDInsight linked service | Cluster (existing or on-demand) |
| Script path / Inline script | Pig script location or inline Pig Latin |
| Arguments | Parameters for the script |

## When to Use

### Use Cases
1. **Legacy Pig workloads** – Existing Pig scripts; ADF runs them on HDInsight on schedule.
2. **ETL data flows** – Multi-step transform (load → clean → group → join → store) expressed in Pig Latin.
3. **Semi-structured data** – Parse and flatten log or text data; aggregate and load to structured store.
4. **Migration** – On-prem Pig jobs moved to Azure HDInsight; ADF for scheduling and parameters.
5. **Batch processing** – Large files in Blob/ADLS processed with Pig; output to Blob or Hive table.
6. **Team expertise** – Team familiar with Pig; maintain existing scripts while orchestrating with ADF.

### When NOT to Use
- New development (prefer Spark/Databricks or Synapse for modern pipelines).
- Simple copy or filter (use **Copy** or **Data Flow**).
- Interactive or low-latency (use Spark or SQL engines).

## Example Scenarios
- Copy logs to Blob; HDInsight Pig runs script that parses, groups by user, and stores to Blob.
- Pig script with parameters (input path, output path, date) run on on-demand cluster; ADF passes parameters.
- Legacy Pig ETL run nightly via ADF; output consumed by downstream Copy or Hive activity.
