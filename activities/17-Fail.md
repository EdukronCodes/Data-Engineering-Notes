# Fail Activity

## Overview
The **Fail** activity deliberately fails the pipeline run with a custom error message and optional error code. It is used to enforce business rules or validation by stopping the pipeline and marking the run as failed.

## Key Features
- **Controlled failure**: Pipeline run status becomes Failed; no further activities run (unless failure path is used).
- **Message**: Custom message shown in run history and logs (e.g., “Row count below threshold”).
- **Error code**: Optional code for downstream handling or monitoring (e.g., “VALIDATION_FAILED”).
- **No retry**: Typically used when retry would not help (business rule violation).

## Common Properties
| Property | Description |
|----------|-------------|
| Message | Error message (required); can use expressions |
| Error code | Optional string code for filtering/alerting |

## When to Use

### Use Cases
1. **Validation failure** – After Validation or row count check: if criteria not met, run Fail with message so run is clearly “Failed” and alerts fire.
2. **Business rule** – If critical condition is not satisfied (e.g., no data, duplicate key detected), Fail with descriptive message.
3. **Safety stop** – If parameter or variable indicates “do not run” (e.g., production guard), Fail before destructive steps.
4. **Data quality gate** – If data quality score or row count is below threshold, Fail to block downstream load.
5. **Explicit error path** – In Switch or If Condition “error” branch, use Fail instead of letting pipeline succeed incorrectly.
6. **Audit and alerting** – Ensure failed runs are visible in monitoring; use consistent error codes for routing alerts.

### When NOT to Use
- Expected “no work” case where pipeline should succeed (use If Condition to skip and succeed).
- Transient errors where retry helps (let activity fail naturally or use retry policy).
- When you want to continue pipeline after “failure” (use Set Variable + branch instead of Fail).

## Example Scenarios
- Validation activity finds row count < expected; If Condition runs Fail with message “Row count 0; expected > 0”.
- If `variables('duplicateCount')` > 0, Fail with code “DUPLICATE_KEYS” and message listing keys.
- If parameter `allowDestructive` is false and activity would truncate, Fail with “Destructive operation not allowed”.
