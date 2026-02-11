# Get Metadata Activity

## Overview
**Get Metadata** retrieves metadata from a dataset or from a specific path (e.g., files/folders in Blob or ADLS). The output is used in expressions for control flow, not for moving data.

## Key Features
- **Metadata only**: No data read; lightweight and fast.
- **Dataset or path**: Can use dataset or a path (e.g., container/folder).
- **Field list**: Choose what to retrieve (e.g., itemName, itemType, size, lastModified, structure/schema).
- **Child items**: Get list of files/subfolders; useful for iteration.

## Common Properties
| Property | Description |
|----------|-------------|
| Dataset / Path | Source to read metadata from |
| Field list | Metadata fields to return (itemName, size, lastModified, structure, etc.) |
| Child items | If true, returns list of child items (files/folders) |

## When to Use

### Use Cases
1. **Check file/folder existence** – Before Copy or Data Flow; fail or branch if file is missing.
2. **Get file list** – List files in a folder; pass to **ForEach** for per-file processing.
3. **Last modified time** – Get `lastModified` of a file to decide if pipeline should run (incremental trigger).
4. **Schema/structure** – Get column list or schema for dynamic mapping or validation.
5. **Partition discovery** – List partition folders (e.g., `year=2024/month=01`) and iterate.
6. **Validation** – Ensure expected columns exist before loading; use with **If Condition** or **Validation**.

### When NOT to Use
- Need full result set from a query (use **Lookup**).
- Need to read actual data (use **Copy** or **Lookup**).
- Need to list items from a database (Lookup with query is more appropriate).

## Example Scenarios
- Get metadata of a Blob folder; if file count = 0, skip Copy and send “No new files” notification.
- List all CSV files in `raw/orders/`; ForEach runs Copy for each file.
- Get `lastModified` of `landing/trigger.txt`; compare with last run time to enable incremental processing.
