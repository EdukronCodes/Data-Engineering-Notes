# Stored Procedure Activity

## Overview
The **Stored Procedure** activity invokes a stored procedure on a database (Azure SQL, Synapse, SQL Server, etc.). You can pass parameters (e.g., from pipeline variables or previous activity output) and optionally capture result sets or return values.

## Key Features
- **Call stored proc**: Execute by name; supports parameter passing (input/output).
- **Parameters**: Map pipeline expressions to procedure parameters (e.g., `@watermark`, `@batchId`).
- **No data movement**: Used for control logic, cleanup, or in-database ETL (procedure does the work).
- **Result**: Output parameters or first result set can be used in subsequent activities (depending on linked service support).

## Common Properties
| Property | Description |
|----------|-------------|
| Linked service | Database connection |
| Stored procedure name | Name of the procedure (can be expression) |
| Table value parameters | Optional table-valued parameters |
| Stored procedure parameters | Name, type, value (expression) for each parameter |

## When to Use

### Use Cases
1. **In-database ETL** – Procedure that transforms or aggregates data inside the database (e.g., populate fact table from staging).
2. **Watermark or control** – Procedure that reads/updates watermark or batch control table; pass batch ID or run time.
3. **Merge/upsert logic** – Procedure that implements complex merge, SCD, or deduplication.
4. **Post-load processing** – After Copy, call procedure to refresh indexes, update stats, or run business rules.
5. **Pre-load setup** – Procedure to create partitions, switch tables, or prepare staging.
6. **Reusable logic** – Centralize logic in database; ADF only orchestrates and passes parameters.

### When NOT to Use
- One-off or simple SQL (use **Script** activity).
- Moving bulk data (use **Copy**).
- Logic that belongs in ADF (branching, loops) – keep in pipeline; use procedure for database-only work.

## Example Scenarios
- Copy to staging; Stored Procedure runs dbo.MergeOrders(@BatchId, @RunDate) with parameters from pipeline.
- Stored Procedure dbo.GetWatermark(@TableName) returns next range; use output in Copy source query.
- After load: Stored Procedure dbo.RefreshAggregates() to rebuild summary tables.
