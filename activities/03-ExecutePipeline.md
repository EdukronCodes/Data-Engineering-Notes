# Execute Pipeline Activity

## Overview
**Execute Pipeline** runs another pipeline from within the current pipeline. It enables reuse, modular design, and parent-child orchestration (e.g., master pipeline calling child pipelines).

## Key Features
- **Reuse**: Call the same pipeline with different parameters.
- **Parameters**: Pass pipeline parameters and wait for completion (or fire-and-forget).
- **Wait on completion**: Block until child finishes or run asynchronously.
- **Chaining**: Build complex workflows by composing smaller pipelines.

## Common Properties
| Property | Description |
|----------|-------------|
| Invoked pipeline | Reference to the pipeline to execute |
| Parameters | Key-value parameters for the child pipeline |
| Wait on completion | If true, parent waits for child to finish |

## When to Use

### Use Cases
1. **Modular ETL** – One pipeline per source (e.g., Ingest_Sales, Ingest_Inventory); master pipeline runs all.
2. **Environment-specific runs** – Same pipeline with dev/test/prod parameters (connection strings, table names).
3. **Reusable patterns** – Load_Dimension, Load_Fact pipelines called from a single orchestration pipeline.
4. **Error handling** – Run cleanup or notification pipelines on failure via failure path.
5. **Sequential or parallel execution** – Run multiple child pipelines in sequence or in parallel.
6. **Approval gates** – Child pipeline holds until manual approval; parent continues after completion.

### When NOT to Use
- Single, linear pipeline with no reuse (keep logic in one pipeline).
- Need to pass large in-memory data (use datasets and Copy/Data Flow instead).

## Example Scenarios
- Master pipeline Daily_Load that runs Load_Dim_Customer, Load_Dim_Product, then Load_Fact_Sales.
- Backup_All_Databases pipeline that executes Backup_SQL_DB once per database via ForEach + Execute Pipeline.
- Trigger a Send_Alert pipeline when a Copy activity fails.
