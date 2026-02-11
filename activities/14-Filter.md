# Filter Activity

## Overview
**Filter** takes an array (from variable or activity output) and applies a condition to each item, returning only items that satisfy the condition. The output array can be used in **ForEach** or other activities.

## Key Features
- **Input**: Array (e.g., from Lookup, Get Metadata, or variable).
- **Condition**: Expression evaluated per item; use `@item()` or `@item().property` in the condition.
- **Output**: New array containing only items where condition is true; original array is not modified.
- **No side effects**: Filter does not run other activities; it only produces a filtered list.

## Common Properties
| Property | Description |
|----------|-------------|
| Items | Expression that returns an array |
| Condition | Boolean expression per item (e.g., `@greater(item().size, 0)`) |

## When to Use

### Use Cases
1. **Process only new or changed files** – Get Metadata child items; Filter where `lastModified` > last run time; ForEach over result.
2. **Process only failed items** – Array of run results; Filter where status = 'Failed'; ForEach retry.
3. **File type filter** – List of files; Filter where extension = '.csv'; pass to ForEach.
4. **Size or row filter** – Filter items where size > 0 or rowCount > 0 to skip empty files/tables.
5. **Priority subset** – Filter list where priority = 'High'; process high-priority first in ForEach.
6. **Exclude already processed** – Filter out items that exist in a “processed” list (e.g., by name or ID).

### When NOT to Use
- Filtering rows inside a dataset (use **Data Flow** Filter transformation or **Copy** with query).
- Single true/false for whole pipeline (use **If Condition**).
- When you need to transform items, not just filter (use **Set Variable** with expression or Data Flow).

## Example Scenarios
- Get Metadata files; Filter where `lastModified` > `variables('lastRun')`; ForEach Copy for each new file.
- Lookup list of tables; Filter where `tableName` not in 'exclude_list'; ForEach Copy for each table.
- Filter array of partitions where `rowCount` > 0; ForEach process only non-empty partitions.
