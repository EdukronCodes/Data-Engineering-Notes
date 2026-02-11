# Wait Activity

## Overview
The **Wait** activity pauses the pipeline for a specified duration. No condition is evaluated; it simply waits and then continues to the next activity.

## Key Features
- **Fixed duration**: Specify wait time (e.g., 5 minutes, 1 hour) in `HH:MM:SS` format.
- **No polling**: Does not check any condition; purely time-based.
- **Use in loops**: Often used inside **Until** to space out polling (e.g., wait 30 sec between status checks).

## Common Properties
| Property | Description |
|----------|-------------|
| Wait time | Duration to pause (e.g., 00:05:00 for 5 minutes) |

## When to Use

### Use Cases
1. **Delay before next step** – Wait for an external system to finish (e.g., wait 10 min after triggering export).
2. **Polling interval** – Inside **Until**, wait between status checks (e.g., Wait 1 min, then Web to check job status).
3. **Rate limiting** – Space out API calls to avoid throttling (e.g., Wait between Web activities).
4. **Time-based sequencing** – Ensure a downstream process runs at a certain time after start (e.g., wait until 2 AM).
5. **Cool-down** – After a failure path, wait before retry or notification.
6. **Batch windows** – Pause until source system’s batch window completes (fixed delay).

### When NOT to Use
- Waiting until a condition is true (use **Until** with condition + Wait inside).
- Waiting for human approval (use **Webhook**).
- Need to wait for an event (consider trigger or Webhook).

## Example Scenarios
- Trigger on-prem export; Wait 15 min; then Copy from file share.
- Until loop: Web (check job) → if not done, Wait 30 sec → repeat.
- After Copy, Wait 5 min for indexing; then run Validation activity.
