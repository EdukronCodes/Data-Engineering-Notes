# If Condition Activity

## Overview
**If Condition** evaluates an expression and branches the pipeline: one set of activities runs when the condition is true, another when false. It enables conditional logic without multiple pipelines.

## Key Features
- **Boolean expression**: Use pipeline variables, activity outputs, and functions (e.g., `equals`, `greater`, `and`, `or`).
- **Two branches**: “If true” and “If false” activity groups; one or both can be empty.
- **Nesting**: If Condition activities can be nested for multi-way logic (or use **Switch** for many cases).

## Common Properties
| Property | Description |
|----------|-------------|
| Expression | Boolean expression (e.g., `@equals(variables('count'), 0)`) |
| If true activities | Activities when condition is true |
| If false activities | Activities when condition is false |

## When to Use

### Use Cases
1. **Skip when no data** – If Lookup/Get Metadata returns 0 files or rows, skip Copy and maybe send “No data” notification.
2. **Environment branching** – If parameter `env` = 'prod', run extra validation; else skip.
3. **Error handling** – If previous activity failed, run cleanup or alert pipeline; else continue normal path.
4. **Watermark logic** – If watermark exists, run incremental Copy; else run full load.
5. **Feature flags** – If flag “enable_validation” is true, run Validation activity; else skip.
6. **Threshold checks** – If row count or file count above threshold, run different path (e.g., parallel load).

### When NOT to Use
- Many discrete cases (e.g., status = A, B, C, D); **Switch** is clearer.
- Iterating over items (use **ForEach**).
- Only “run or skip” with no false branch (you can still use If Condition with empty false branch).

## Example Scenarios
- If `@activity('LookupFiles').output.count` > 0, run Copy; else run Web to post “No new files”.
- If `@pipeline().RunId` is from trigger type “Manual”, run with debug settings; else production settings.
- If `variables('lastLoadStatus')` = 'Full', run full refresh; else run incremental.
