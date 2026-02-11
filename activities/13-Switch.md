# Switch Activity

## Overview
**Switch** evaluates an expression once and runs the first matching case (or default). It is like a multi-way If-Else: one expression, multiple possible values and corresponding activity groups.

## Key Features
- **Single expression**: One expression is evaluated (e.g., `variables('status')` or `activity('Lookup1').output.value`).
- **Cases**: Each case has a value (or set of values); first match runs that case’s activities.
- **Default**: Optional default case when no other case matches.
- **One case runs**: Only one case executes per run (no fall-through).

## Common Properties
| Property | Description |
|----------|-------------|
| On | Expression to evaluate (e.g., `variables('fileType')`) |
| Cases | List of case value(s) and associated activities |
| Default | Activities when no case matches |

## When to Use

### Use Cases
1. **File type routing** – Switch on file extension or naming pattern; CSV path (Copy to SQL), JSON path (Data Flow), Parquet path (Copy to lake).
2. **Status-based flow** – Switch on job status (Success, Failed, Cancelled); each runs different notification or cleanup.
3. **Region or environment** – Switch on `region` or `env` parameter; run region-specific or env-specific activities.
4. **Priority or tier** – Switch on priority (High, Normal, Low); different concurrency or resources.
5. **Error code handling** – Switch on error code from previous activity; different recovery or alert path.
6. **Load type** – Switch on load type (Full, Incremental, Delta); run corresponding pipeline or parameters.

### When NOT to Use
- Only two outcomes (use **If Condition**).
- Iterating over a list (use **ForEach**).
- Condition is complex (multiple variables); consider nested If or variable that resolves to simple value for Switch.

## Example Scenarios
- Switch on `item().type`: case 'customer' → Copy to DimCustomer; case 'product' → Copy to DimProduct; default → Log unknown.
- Switch on `activity('GetStatus').output.status`: case 'Completed' → run Validation; case 'Failed' → run Alert; default → Wait and retry.
