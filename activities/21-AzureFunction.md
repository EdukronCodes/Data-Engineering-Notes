# Azure Function Activity

## Overview
The **Azure Function** activity invokes an Azure Function (HTTP trigger) from a pipeline. You pass a payload and optional headers; the function runs your custom code (C#, JavaScript, Python, etc.) and can return a response used in later activities.

## Key Features
- **HTTP trigger**: Calls the function’s HTTP endpoint (GET/POST); function key or AAD auth.
- **Payload**: JSON body and headers; can use pipeline variables and activity outputs in expressions.
- **Response**: Function response available as `@activity('AzureFunction1').output` for downstream logic.
- **Custom logic**: Use for logic that is hard to express in ADF (parsing, calling multiple APIs, custom validation).

## Common Properties
| Property | Description |
|----------|-------------|
| Azure Function linked service | App and function name |
| Function name | Name of the Azure Function |
| Method | GET or POST |
| Body | Request body (JSON; can be expression) |
| Headers | Optional headers |

## When to Use

### Use Cases
1. **Custom transformation** – Code that transforms or validates data (e.g., parse complex JSON, apply business rules) before or after Copy.
2. **Multi-API orchestration** – Function calls several APIs, aggregates result, returns single response for pipeline.
3. **Token or secret handling** – Function retrieves token from Key Vault or external auth; pipeline uses it in Web/Copy.
4. **Notifications** – Function sends formatted email/Slack/Teams message with run details.
5. **Data quality or scoring** – Function runs validation logic or ML scoring; pipeline branches on result.
6. **Legacy or proprietary API** – Wrapper around non-REST or complex API that ADF does not support natively.

### When NOT to Use
- Simple REST call (use **Web** activity).
- Heavy data movement (use **Copy**; use function for control/small payloads).
- Logic that fits in Data Flow or Script (avoid unnecessary code).

## Example Scenarios
- After Copy: Azure Function validates file format and returns { valid: true, errors: [] }; If Condition on result decides Fail or continue.
- Azure Function gets SAS token for private Blob; returns URL; next activity uses it in Copy source.
- Azure Function calls external vendor API with retry and parsing; returns list of IDs for ForEach.
