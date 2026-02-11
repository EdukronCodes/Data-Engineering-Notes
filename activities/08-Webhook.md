# Webhook Activity

## Overview
The **Webhook** activity calls a URL and passes an optional payload, then waits for an external system to call back with a callback URL. It is used when you need the pipeline to pause until an external process completes (e.g., manual approval, external job).

## Key Features
- **Call and wait**: Pipeline passes a callback URL to your endpoint; pipeline resumes when callback is invoked.
- **Timeout**: Maximum wait time; pipeline fails if no callback received.
- **Payload**: Optional JSON body sent to your URL (e.g., run ID, pipeline name).
- **One-way**: No immediate response body from your URL is used to resume; only the callback matters.

## Common Properties
| Property | Description |
|----------|-------------|
| URL | Endpoint that receives the webhook (must call back to continue) |
| Timeout | Max wait (e.g., 00:10:00) |
| Body | Optional payload sent to URL |

## When to Use

### Use Cases
1. **Manual approval** – Send approval request to a tool (e.g., Logic App, Power Automate); pipeline continues when user approves and calls back.
2. **External job completion** – Start an external process (e.g., on-prem job); that process calls back when done.
3. **Human-in-the-loop** – Pause for data validation or sign-off before destructive or sensitive steps.
4. **Third-party workflow** – Integrate with systems that support webhook callbacks (e.g., custom app, SaaS).
5. **Long-running external process** – Avoid polling; external system calls back when job finishes.

### When NOT to Use
- Simple HTTP call without waiting for callback (use **Web** activity).
- You can poll for status in a loop (use **Until** + **Web**).
- Need to pass large data (callback is typically just “done” or small payload).

## Example Scenarios
- Pipeline pauses for approval; Logic App sends email with “Approve” link that calls ADF callback URL.
- Trigger on-premises ETL job; that job calls ADF callback when export completes so pipeline can continue with Copy.
- Wait for data steward to confirm data quality in a custom app; app calls back to resume pipeline.
