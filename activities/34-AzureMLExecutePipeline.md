# Azure ML Execute Pipeline Activity

## Overview
The **Azure ML Execute Pipeline** activity runs an **Azure Machine Learning (Azure ML)** pipeline (job). It submits the pipeline to the Azure ML workspace and can wait for completion. Used to trigger ML training, batch inference, or other Azure ML pipelines from ADF.

## Key Features
- **Azure ML pipeline**: Submit a published or draft pipeline (job) in Azure ML workspace.
- **Parameters**: Pass pipeline parameters (e.g., data path, model version, compute size) from ADF (variables, parameters, or activity output).
- **Wait for completion**: Option to wait until the Azure ML job finishes; pipeline can branch on success/failure.
- **Workspace**: Connect via Azure ML linked service (workspace ID and auth: service principal or managed identity).
- **Output**: Job run ID and status available for logging or downstream activities.

## Common Properties
| Property | Description |
|----------|-------------|
| Azure ML linked service | Azure ML workspace and auth |
| Pipeline / Experiment | Reference to ML pipeline (by ID or name) and experiment name |
| Parameters | Key-value parameters for the ML pipeline |
| Wait on completion | If true, ADF waits for ML job to finish |

## When to Use

### Use Cases
1. **ML training** – After ADF copies training data to Blob/ADLS, run Azure ML training pipeline; wait for model to be registered.
2. **Batch inference** – ADF prepares input data; Azure ML Execute Pipeline runs batch scoring pipeline; ADF continues with post-processing or notification.
3. **Retraining schedule** – ADF runs on schedule; triggers Azure ML pipeline with date or data path parameter; model retrained and promoted.
4. **End-to-end MLOps** – Data prep in ADF → Copy to ML store → Azure ML pipeline (train/score) → ADF moves results or triggers deployment.
5. **Parameterized runs** – ADF passes data path, model name, or environment from variables; ML pipeline uses them.
6. **Conditional ML** – If Condition (e.g., new data arrived); then run Azure ML pipeline; else skip.

### When NOT to Use
- No Azure ML pipeline (use **Azure Function** or **Custom** for custom ML code).
- Real-time inference (use Azure ML endpoint from app; ADF for batch only).
- Simple copy of data (use **Copy**); this activity is for triggering ML jobs.

## Example Scenarios
- Daily: ADF Copy new data to Blob; Azure ML Execute Pipeline runs “Train_Model” pipeline with data path parameter; on success, ADF runs pipeline that deploys model.
- ADF prepares input CSV; Azure ML Execute Pipeline runs batch scoring pipeline; ADF Copy moves output to data warehouse.
- ADF checks if new data exists; If yes, run Azure ML Execute Pipeline for retraining; else send “No retrain” notification.
