# Validation Activity

## Overview
**Validation** checks that data exists at a specified location (dataset/path) before continuing. It can validate existence of child items (e.g., files), row count, or that a path exists. It does not move or transform data.

## Key Features
- **Existence check**: Verify dataset or path exists (e.g., folder, file, table).
- **Child items**: Optionally require minimum count of child items (e.g., at least one file in folder).
- **Timeout**: Maximum time to wait for condition; can be used with **Until** for “wait until file appears”.
- **Fail or continue**: Pipeline can fail or take a different path based on validation result (e.g., If Condition after Validation).

## Common Properties
| Property | Description |
|----------|-------------|
| Dataset / Path | What to validate (e.g., Blob path, folder) |
| Minimum size | Minimum size (e.g., file size) |
| Child items | Validate count of child items (e.g., minimum 1 file) |
| Timeout | How long to wait (for “wait until ready” scenarios) |

## When to Use

### Use Cases
1. **Pre-load check** – Ensure source folder or file exists before Copy; fail early with clear message if missing.
2. **Row count gate** – Validate that source has expected minimum rows before loading to warehouse.
3. **File count** – Ensure at least N files landed (e.g., from upstream system); fail or alert if not.
4. **Wait for data** – Use with timeout: wait until file(s) appear (e.g., Validation in Until loop or with long timeout).
5. **Post-load verification** – After Copy, validate sink has expected file/row count before marking success.
6. **Pipeline dependency** – Ensure another pipeline or process has produced output before this pipeline continues.

### When NOT to Use
- Reading or moving data (use **Copy** or **Lookup**).
- Complex business rules (use **Script** or **Data Flow** + **If Condition**).
- When you only need metadata for branching (**Get Metadata** + If Condition may be enough).

## Example Scenarios
- Before Copy: Validation on `landing/orders/` with minimum 1 child item; if 0 files, Fail with “No source files”.
- After Copy: Validation on sink folder for minimum size or child count to confirm write succeeded.
- Until loop: Validation with timeout on `trigger.txt`; exit when file exists so pipeline can proceed.
