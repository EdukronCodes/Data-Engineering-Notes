# ForEach Activity

## Overview
**ForEach** iterates over a collection (array) and runs its inner activities once per item. The current item is available as `@item()` (or `@item().property`) in child activities.

## Key Features
- **Iteration**: Loops over array from pipeline variable or activity output (e.g., Lookup result, Get Metadata child items).
- **Sequential or parallel**: Run iterations one-by-one (sequential) or with a defined degree of parallelism (parallel).
- **Batch count**: In parallel mode, limit how many iterations run at once (e.g., 5).
- **Item context**: Use `@item()`, `@item().name`, etc., in child activity settings.

## Common Properties
| Property | Description |
|----------|-------------|
| Items | Expression that returns an array (e.g., `@activity('Lookup1').output.value`) |
| Is sequential | If true, one iteration at a time; if false, parallel |
| Batch count | Max concurrent iterations when parallel (default 20, max 50) |

## When to Use

### Use Cases
1. **Process multiple files** – Get Metadata (child items) or Lookup file list; ForEach runs Copy or Data Flow per file.
2. **Process multiple tables** – Lookup list of table names; ForEach runs Copy or Stored Procedure per table.
3. **Process multiple pipelines** – Array of pipeline names or configs; ForEach runs Execute Pipeline per item.
4. **Partition-based processing** – List of partition values (e.g., dates); ForEach runs load per partition.
5. **Multi-tenant** – List of tenant IDs; ForEach runs tenant-specific Copy or Data Flow.
6. **Retry list** – Array of failed items; ForEach retries each with Copy or Web.

### When NOT to Use
- Waiting until a condition is true (use **Until**).
- Single conditional branch (use **If Condition** or **Switch**).
- When the “collection” is dynamic and not array-shaped (shape it in Lookup or variable first).

## Example Scenarios
- Lookup table names from config table; ForEach runs Copy from SQL to Blob per table.
- Get Metadata child items on folder; ForEach runs Data Flow per CSV file.
- ForEach over array of pipeline parameters; Execute Pipeline for each parameter set.
