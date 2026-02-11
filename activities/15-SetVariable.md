# Set Variable Activity

## Overview
**Set Variable** sets the value of an existing pipeline variable to a single value. The variable must be defined at pipeline level; this activity overwrites its value for the current run.

## Key Features
- **Overwrite**: Replaces the variable’s value (does not append).
- **Pipeline scope**: Variable is available to all subsequent activities in the pipeline.
- **Value**: Can be literal, expression, or output from another activity (e.g., `@activity('Lookup1').output.value`).
- **Type**: Variable type (String, Bool, Array, etc.) is defined at pipeline level; value must be compatible.

## Common Properties
| Property | Description |
|----------|-------------|
| Variable name | Name of the pipeline variable to set |
| Value | New value (expression or literal) |

## When to Use

### Use Cases
1. **Store watermark** – Set variable to `max(ModifiedDate)` or last ID after incremental load for next run.
2. **Store row/file count** – Set variable from Copy or Lookup output; use in If Condition or logging.
3. **Config override** – Set batch size or table name from Lookup result for downstream activities.
4. **Status or flag** – Set “load completed” or “validation passed” for use in Switch or If Condition.
5. **Accumulate single value** – In a loop, set variable to current item or result (e.g., last processed ID).
6. **Dynamic path** – Set variable to constructed path (e.g., `concat('folder/', formatDateTime(utcnow(), 'yyyy-MM-dd'))`) for use in Copy/Data Flow.

### When NOT to Use
- Adding items to a list (use **Append Variable**).
- Setting a value that is only needed inside one activity (expression in that activity may be enough).
- Variables must exist; create them in pipeline definition first.

## Example Scenarios
- After incremental Copy: Set Variable `watermark` = `@activity('Copy1').output.rowsRead` or last row value.
- Lookup config; Set Variable `batchSize` = `@activity('Lookup1').output.value[0].BatchSize`.
- Set Variable `runDate` = `@formatDateTime(utcnow(), 'yyyy-MM-dd')` for use in dataset path.
