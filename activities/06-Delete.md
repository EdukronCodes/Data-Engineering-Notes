# Delete Activity

## Overview
The **Delete** activity deletes files or folders from a store (e.g., Azure Blob, ADLS Gen1/Gen2, on-premises file share). It is used for cleanup, retention, or pre-load truncation.

## Key Features
- **Store-based**: Works with file-system-like stores (Blob, ADLS, File Share); not for deleting rows in databases.
- **Recursive**: Can delete a single file, a folder, or folder and all contents recursively.
- **Wildcards**: Optional file filter (e.g., `*.csv`) to delete only matching files.
- **Safety**: Can be limited to single-level or recursive; use with care in production.

## Common Properties
| Property | Description |
|----------|-------------|
| Dataset / Path | Store and path (folder or file) to delete from |
| Recursive | If true, deletes folder and all contents |
| Wildcard | Optional filter (e.g., *.tmp, *backup*) |

## When to Use

### Use Cases
1. **Pre-load cleanup** – Delete files in a staging folder before Copy writes new data.
2. **Retention policy** – Delete files older than N days (e.g., raw files after successful load).
3. **Landing zone cleanup** – Remove processed files from landing container after move to archive.
4. **Staging cleanup** – Delete staging Blob files used by Copy activity after load completes.
5. **Failed run cleanup** – In failure path, delete partial/incomplete files before retry.
6. **Archive pruning** – Delete from hot tier after copy to cold/archive.

### When NOT to Use
- Deleting rows in SQL/database (use **Stored Procedure** or **Script** with DELETE statement).
- Deleting items in Cosmos DB (use custom code or **Azure Function**).
- When you need to move instead of delete (use **Copy** then Delete, or Copy with move option if supported).

## Example Scenarios
- Before daily load: delete all files in `staging/orders/` so Copy can write fresh data.
- After successful load: delete source files in `landing/` that are older than 7 days.
- In pipeline failure path: delete partial Parquet files in `staging/` before triggering retry.
