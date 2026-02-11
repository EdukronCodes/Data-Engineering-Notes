# Script Activity

## Overview
The **Script** activity runs a SQL script against a database linked service (e.g., Azure SQL, Synapse, SQL Server). It is used for DDL, DML, or procedural logic (e.g., truncate, merge, call procedures) without moving data through ADF datasets.

## Key Features
- **Database execution**: Script runs in the context of the linked service (Azure SQL, Synapse, SQL Server, etc.).
- **Single script**: One script per activity; can be parameterized with pipeline variables/parameters.
- **No dataset for data**: Script is for execution only; for bulk data use **Copy** or **Stored Procedure**.
- **Logging**: Query result (e.g., row count) can be captured in output for downstream activities.

## Common Properties
| Property | Description |
|----------|-------------|
| Linked service | Database connection (Azure SQL, Synapse, etc.) |
| Script | Inline SQL or stored script; can use expressions |
| Log level | None, Basic, or Verbose for logging |

## When to Use

### Use Cases
1. **Truncate before load** – Run TRUNCATE or DELETE on staging/target table before Copy loads new data.
2. **DDL** – Create/drop tables, indexes, or partitions (e.g., create partition for today).
3. **Merge/upsert** – Run MERGE or custom UPDATE/INSERT logic after Copy to staging.
4. **Control table updates** – Update watermark or batch control table (e.g., set last run time, status).
5. **Data cleanup** – DELETE old rows for retention; drop temporary tables.
6. **Multi-statement logic** – Run several SQL statements in sequence (where supported) without separate Stored Procedure.

### When NOT to Use
- Moving large data (use **Copy**).
- Complex transformation in ADF (use **Data Flow**).
- Reusable procedural logic with parameters (use **Stored Procedure** activity and call a stored proc).
- Script that returns large result sets for use in pipeline (prefer **Lookup** for small result sets).

## Example Scenarios
- Before Copy: Script TRUNCATE TABLE staging.Orders; then Copy loads from Blob to staging.Orders.
- After Copy: Script MERGE target.Orders FROM staging.Orders ON key.
- Script UPDATE control.Watermark SET LastValue = @p1 WHERE TableName = 'Orders' (parameter from variable).
