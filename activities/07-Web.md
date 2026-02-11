# Web Activity

## Overview
The **Web** activity calls a REST API (HTTP/HTTPS) from a pipeline. It can use GET, POST, PUT, PATCH, or DELETE and pass headers/body. The response can be used in later activities.

## Key Features
- **REST calls**: Integrate with any REST API (Azure services, SaaS, custom APIs).
- **Method and body**: Support for JSON/XML body and custom headers (e.g., Authorization).
- **Authentication**: Use pipeline parameters or Key Vault references for secrets.
- **Output**: Response body and status available to subsequent activities (e.g., `@activity('Web1').output`).

## Common Properties
| Property | Description |
|----------|-------------|
| URL | Full endpoint URL (can be parameterized) |
| Method | GET, POST, PUT, PATCH, DELETE |
| Headers | Optional headers (e.g., Authorization, Content-Type) |
| Body | Request body for POST/PUT/PATCH |

## When to Use

### Use Cases
1. **Trigger external process** – Call an API to start a job (e.g., Spark job, ML endpoint) and optionally wait for result.
2. **Get token** – Call OAuth/token endpoint; use token in next Web or Copy (REST) activity.
3. **Ping or health check** – GET to a URL to verify service is up before running Copy/Data Flow.
4. **Webhook-style integration** – POST to external system to notify completion or send payload.
5. **Azure REST APIs** – Call Azure Management or Data APIs (e.g., trigger Synapse job, check run status).
6. **SaaS APIs** – Pull or push data via vendor REST API when no built-in connector exists.

### When NOT to Use
- Need to wait for long-running callback (use **Webhook** for callback-based wait).
- Moving bulk data (use **Copy** with REST connector).
- Complex parsing or retry logic (consider **Azure Function**).

## Example Scenarios
- GET token from Azure AD; use in next Web activity to call Power BI REST API.
- POST to Slack/Dynamics when pipeline succeeds or fails (notification).
- Call Azure Synapse REST API to start a notebook run and poll for completion in Until loop.
