# Custom Activity

## Overview
The **Custom** activity runs custom code (e.g., .NET or Python) on **Azure Batch** pool (VMs). It is used when you need full control over execution environment, libraries, or long-running logic that does not fit other activities.

## Key Features
- **Azure Batch**: Code runs on Batch pool nodes (Windows or Linux); you provide the executable or script.
- **Flexible**: Any language or framework that can run on the VM (e.g., .NET, Python, R, executable).
- **Input/output**: Pass linked service references (e.g., Blob paths) as input; write results to Blob or database from your code.
- **Scalable**: Batch can run multiple tasks in parallel; ADF invokes the Batch job.

## Common Properties
| Property | Description |
|----------|-------------|
| Azure Batch linked service | Batch account and pool |
| Command | Command line to run (e.g., python main.py) |
| Folder path | Blob path containing script and dependencies |
| Reference objects | Linked services (e.g., Blob) passed to the executable as JSON |
| Extended properties | Additional key-value passed to the process |

## When to Use

### Use Cases
1. **Custom ETL** – Logic in R, Python, or .NET that is not practical in Data Flow or Script (e.g., specialized libraries).
2. **ML inference** – Run scoring or training script that needs specific runtime and packages on Batch.
3. **File or format conversion** – Proprietary format or tool (e.g., legacy executable) that runs on VM.
4. **Heavy computation** – Long-running or CPU-heavy work that should not run on ADF or Synapse Spark.
5. **On-premises-like workload** – Replicate logic that today runs on-prem; package as script and run on Batch.
6. **Multiple outputs** – Code that reads from one store, processes, writes to several sinks with custom logic.

### When NOT to Use
- Simple REST or SQL (use **Web**, **Script**, or **Stored Procedure**).
- Standard connectors and transformations (use **Copy** and **Data Flow**).
- When Azure Functions or Databricks/Synapse can do the job (simpler operations).

## Example Scenarios
- Custom activity runs Python script from Blob; script reads CSV from Blob, applies R-based model, writes results to SQL.
- Run legacy .NET ETL tool as executable on Batch; input/output paths passed via reference objects.
- Custom activity runs R script for statistical validation; output file path used in next activity.
