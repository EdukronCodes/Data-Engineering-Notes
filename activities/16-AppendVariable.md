# Append Variable Activity

## Overview
**Append Variable** adds one or more elements to an existing pipeline variable of type **Array**. It does not replace the array; it appends to it. Used to build lists during pipeline execution.

## Key Features
- **Array only**: Variable must be of type Array (defined at pipeline level).
- **Append**: Adds the given value(s) to the end of the array; existing elements remain.
- **Value**: Single value or expression that evaluates to one element (or array to append as elements, depending on design).
- **Build list**: Often used in a loop (e.g., ForEach) to collect processed items or errors.

## Common Properties
| Property | Description |
|----------|-------------|
| Variable name | Name of the array variable |
| Value | Value to append (e.g., `@item()` or `item().name`) |

## When to Use

### Use Cases
1. **Collect processed items** – In ForEach, append each processed file or table name to a variable; use for logging or “processed list” at end.
2. **Collect errors** – Append error message or item to array when an activity fails in loop; after loop, send summary (e.g., Web to post failures).
3. **Build dynamic list** – Start with empty array; append items that pass a condition (alternative to Filter in some designs).
4. **Audit trail** – Append run IDs or timestamps as pipeline progresses through steps.
5. **Retry list** – Append failed items to array; after loop, use array in next pipeline or notification.
6. **Aggregate metadata** – Append row counts or file names from each iteration for final summary.

### When NOT to Use
- Setting a single value (use **Set Variable**).
- Variable is not an array (Append Variable requires array type).
- You have a fixed list from Lookup (use that output directly in ForEach; no need to build array in pipeline).

## Example Scenarios
- ForEach over tables: on success append table name to `processedTables`; at end Web activity posts `@variables('processedTables')`.
- ForEach over files: on failure append `item().name` to `failedFiles`; default path sends `failedFiles` to support.
- Build list of partition values that had errors; pass to downstream pipeline for retry.
