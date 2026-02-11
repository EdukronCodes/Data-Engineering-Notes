# HDInsight Streaming Activity

## Overview
The **HDInsight Streaming** activity runs a **Hadoop Streaming** job on an HDInsight cluster. You specify mapper and reducer executables (e.g., Python, shell scripts) and input/output paths. Used for custom map-reduce style processing with non-Java languages.

## Key Features
- **Streaming job**: Mapper and reducer are executables (e.g., Python, Perl, bash); receive input via stdin, emit to stdout.
- **Cluster**: Existing or on-demand HDInsight Hadoop cluster.
- **Input/output**: Standard Hadoop streaming; input and output paths in HDFS or Blob/ADLS.
- **Arguments**: Optional arguments passed to mapper/reducer (e.g., config, thresholds).

## Common Properties
| Property | Description |
|----------|-------------|
| HDInsight linked service | Cluster |
| Mapper / Reducer | Path to mapper and reducer executables (e.g., .py in Blob) |
| Input / Output | Input and output paths |
| Arguments | Optional arguments |

## When to Use

### Use Cases
1. **Python/shell MapReduce** – Use Python or shell as mapper/reducer; no Java; run on HDInsight via streaming.
2. **Legacy streaming jobs** – Existing Hadoop streaming scripts; ADF runs them on schedule.
3. **Text/log processing** – Parse and aggregate logs with custom logic in Python; streaming fits the model.
4. **Migration** – On-prem streaming jobs moved to HDInsight; ADF for orchestration.
5. **Flexible logic** – Any language that can read stdin and write stdout; good for prototypes or simple jobs.
6. **Batch processing** – Large files processed with map-reduce pattern; output to Blob or Hive.

### When NOT to Use
- New development (prefer Spark/Databricks or Synapse).
- Complex or low-latency (use Spark or SQL).
- Simple copy (use **Copy**).

## Example Scenarios
- Copy logs to Blob; HDInsight Streaming runs Python mapper and reducer from Blob; output to Blob; ADF waits.
- Streaming job with parameters (date, input path); ADF passes parameters; on-demand cluster.
- Legacy Perl mapper/reducer run nightly via ADF; output consumed by downstream pipeline.
