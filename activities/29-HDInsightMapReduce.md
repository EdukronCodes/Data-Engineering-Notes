# HDInsight MapReduce Activity

## Overview
The **HDInsight MapReduce** activity runs a **MapReduce** (or **Hadoop streaming**) job on an HDInsight cluster. You specify JAR and class (or streaming command); used for custom Java MapReduce or streaming (e.g., Python mapper/reducer) jobs.

## Key Features
- **JAR or streaming**: Run a Hadoop JAR (Mapper/Reducer classes) or streaming job (e.g., Python scripts as mapper/reducer).
- **Cluster**: Existing or on-demand HDInsight Hadoop cluster.
- **Arguments**: Pass arguments to the job (input path, output path, parameters).
- **Output**: Activity completes when MapReduce job succeeds or fails.

## Common Properties
| Property | Description |
|----------|-------------|
| HDInsight linked service | Cluster |
| Class name / JAR / Streaming | JAR path and main class, or streaming command and scripts |
| Arguments | Job arguments (paths, config) |

## When to Use

### Use Cases
1. **Legacy MapReduce** – Existing Java MapReduce jobs; run on HDInsight and orchestrate with ADF.
2. **Custom logic** – Logic that is best expressed as map-reduce (custom partitioning, grouping).
3. **Hadoop streaming** – Python or other language as mapper/reducer; HDInsight MapReduce activity runs streaming job.
4. **Migration** – On-prem MapReduce moved to Azure; ADF for schedule and parameters.
5. **Batch processing** – Large-scale batch job that fits MapReduce model (read from HDFS/Blob, write results).
6. **Libraries** – JAR bundles custom or third-party MapReduce code; run without rewriting.

### When NOT to Use
- New pipelines (prefer Spark/Databricks or Synapse).
- Simple copy or SQL (use **Copy** or **HDInsight Hive**).
- Interactive or low-latency (use Spark or SQL).

## Example Scenarios
- ADF Copy lands data in Blob; HDInsight MapReduce runs custom JAR with input/output paths; result in Blob.
- Streaming job: Python mapper and reducer in Blob; MapReduce activity runs with streaming config; ADF waits.
- Nightly MapReduce job for log processing; ADF triggers on-demand cluster and passes date parameter.
