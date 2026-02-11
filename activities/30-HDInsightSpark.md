# HDInsight Spark Activity

## Overview
The **HDInsight Spark** activity runs a **Spark** program on an HDInsight Spark cluster. You can run a Spark JAR, Python file, or reference a Spark job. Used for Spark-based ETL or analytics when using HDInsight instead of Databricks.

## Key Features
- **Spark execution**: Run JAR, .py file, or Spark job; supports Scala, Python, Java.
- **Cluster**: Existing or on-demand HDInsight Spark cluster.
- **Arguments**: Pass arguments (paths, config) to the Spark job.
- **Main class / file**: Specify main class for JAR or path to Python file.

## Common Properties
| Property | Description |
|----------|-------------|
| HDInsight linked service | Spark cluster |
| Root path / JAR / Python file | Path to JAR or Python file in storage |
| Main class name | For JAR, main class |
| Arguments | Job arguments |

## When to Use

### Use Cases
1. **Spark on HDInsight** – Use HDInsight Spark cluster (not Databricks); ADF triggers Spark job (JAR or Python).
2. **Existing Spark jobs** – Team has Spark code for HDInsight; ADF orchestrates and passes parameters.
3. **ETL or analytics** – Spark script for transformation or aggregation; data in Blob/ADLS.
4. **Cost or policy** – Organization standard is HDInsight; Spark activity fits that standard.
5. **Migration** – On-prem Spark (e.g., Hadoop+Spark) moved to HDInsight Spark; ADF for scheduling.
6. **Batch Spark** – Run Spark batch job after Copy lands data; output for downstream activities.

### When NOT to Use
- Prefer Databricks (use **Databricks Notebook/JAR/Python** for richer ecosystem).
- Prefer serverless Spark (use **Synapse Notebook** or **Synapse Spark job**).
- Simple copy (use **Copy**).

## Example Scenarios
- Copy raw data to ADLS; HDInsight Spark runs Python script that aggregates and writes Parquet; ADF runs Validation.
- Nightly Spark JAR run with input/output paths from ADF parameters; on-demand cluster.
- Spark job for Delta or Parquet processing on HDInsight; ADF triggers and waits for completion.
