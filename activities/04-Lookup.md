# Lookup Activity

## Overview
The **Lookup** activity reads data from a source (dataset) and returns the result to the pipeline. The output can be consumed by subsequent activities (e.g., ForEach, If Condition, or dynamic content in other activities).

## Key Features
- **Read-only**: No data is written; used for control flow and parameterization.
- **Single result or array**: Returns first row only or full result set.
- **Query or table**: Use a query (SQL, etc.) or full table/list (e.g., list Blob files).
- **Output**: Available as `@activity('LookupActivityName').output` in expressions.

## Common Properties
| Property | Description |
|----------|-------------|
| Source | Dataset (e.g., SQL, REST, file) |
| Query / Table | Query string or table/list name |
| First row only | If true, returns first row; otherwise full result set |

## When to Use

### Use Cases
1. **Get list for iteration** – Lookup list of tables, files, or partitions; pass to **ForEach** to process each item.
2. **Watermark / last value** – Lookup max `LastModifiedDate` or last ID from a control table for incremental loads.
3. **Configuration** – Read config table (e.g., source connection, batch size) and pass to Copy or Data Flow.
4. **Conditional branching** – Lookup a flag or count; use result in **If Condition** to choose path.
5. **REST API** – Call REST API via Lookup (GET); use response in next activity (e.g., token, list of IDs).
6. **File existence / metadata** – List files in a folder; check if any exist before running Copy.

### When NOT to Use
- Moving large data (use **Copy**).
- Transforming data (use **Data Flow** or **Script**).
- When you only need metadata (e.g., file count, schema) – **Get Metadata** may be simpler.

## Example Scenarios
- Lookup list of table names from SQL; ForEach runs Copy per table.
- Lookup `MAX(ModifiedDate)` from watermark table; use in Copy source query for incremental load.
- Lookup API token from Key Vault-backed REST dataset; use in Web activity header.
