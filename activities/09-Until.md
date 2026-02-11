# Until Activity

## Overview
**Until** is a loop activity that runs its inner activities repeatedly until a condition evaluates to true or a timeout is reached. It is the main “do-while” style loop in ADF.

## Key Features
- **Condition**: Expression that must become true to exit (e.g., `@equals(activity('Check').output.status, 'Succeeded')`).
- **Timeout**: Maximum duration (e.g., 1 hour); loop stops and can fail or continue.
- **Inner activities**: One or more activities inside the loop (e.g., Web to poll, Wait, then check again).
- **Iteration limit**: Optional max iteration count to avoid infinite loops.

## Common Properties
| Property | Description |
|----------|-------------|
| Expression | Condition to evaluate each iteration; loop exits when true |
| Timeout | Max time for the entire Until block |
| Activities | Child activities to run each iteration |

## When to Use

### Use Cases
1. **Poll for completion** – Run a job (e.g., Synapse notebook, Databricks); loop with Wait + GetMetadata or Web until job status is “Succeeded”.
2. **Wait for file** – Check for file/folder (Get Metadata); loop until exists or timeout.
3. **Retry with backoff** – Call API; if failure, Wait 1 min and retry until success or max attempts.
4. **Batch processing** – Process in chunks; loop until no more chunks (e.g., Lookup next batch, process, repeat).
5. **Async job wait** – Start async operation (Web); poll status in loop until completed/failed.
6. **Data availability** – Until source system signals “ready” (e.g., flag file, API response).

### When NOT to Use
- Iterating over a known list (use **ForEach**).
- Single wait with no condition (use **Wait**).
- Fixed number of iterations with no condition (ForEach over a range is clearer).

## Example Scenarios
- Start Synapse notebook via REST; Until loop: Wait 30 sec, GET job status; exit when status = Completed.
- Until loop: Get Metadata on `trigger.txt`; exit when file exists or timeout 2 hours.
- Call API; if 429 (throttle), Wait 60 sec and retry until success or 5 attempts.
