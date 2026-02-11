# Azure Batch Activity

## Overview
**Azure Batch** activity (in the context of ADF) typically refers to running tasks on an **Azure Batch** pool. In ADF, this is usually done via the **Custom** activity, which submits a job to Azure Batch and runs your custom executable or script on pool nodes.

## Key Features
- **Batch pool**: Uses VMs in your Batch pool; you manage pool size and OS.
- **Task submission**: ADF submits one or more tasks to the Batch job; Batch handles scheduling and retries.
- **Integration**: Often used with **Custom** activity; Batch linked service points to Batch account and pool.
- **Scale**: Run many tasks in parallel; each task can process a subset of data (e.g., one file per task).

## Common Properties
| Property | Description |
|----------|-------------|
| Batch linked service | Batch account and pool ID |
| Command / Custom activity | Command and reference objects (see Custom activity) |
| Parallelism | Number of parallel tasks (if applicable) |

## When to Use

### Use Cases
1. **Parallel custom processing** – Many files or partitions; each Batch task processes one item (e.g., Custom activity with ForEach over file list).
2. **Compute-heavy workload** – Run R, Python, or .NET code that needs substantial CPU/memory on dedicated VMs.
3. **Package-based execution** – Run code that depends on specific OS or installed software on Batch nodes.
4. **Large-scale batch jobs** – 100s of tasks; Batch manages queue and execution; ADF triggers and waits.
5. **Hybrid with ADF** – ADF does Copy/orchestration; Batch does transformation or scoring.
6. **Cost control** – Use low-priority VMs in Batch for non-urgent work; ADF still orchestrates schedule.

### When NOT to Use
- No custom code (use **Copy**, **Data Flow**, **Script**).
- Prefer serverless (use **Azure Function** or **Synapse/Databricks**).
- One-off script (Azure Function or Script/Stored Procedure may be simpler).

## Example Scenarios
- ForEach over list of files; Custom (Azure Batch) runs Python script per file; aggregate results in pipeline.
- Single Custom activity submits Batch job with 50 tasks; each task processes one day of data; ADF waits for job completion.
- Run legacy C# ETL on Batch pool; ADF Copy loads raw data to Blob; Custom runs executable; ADF Copy moves results to SQL.
