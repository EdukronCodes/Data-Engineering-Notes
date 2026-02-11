# Data Flow Activity

## Overview
**Data Flow** runs data transformation logic in a visual, code-free (or low-code) designer. It executes on Spark clusters managed by ADF and supports complex transformations like joins, aggregations, pivots, and schema drift.

## Key Features
- **Visual design**: No Spark code required; built-in transformations (Source, Sink, Derived Column, Aggregate, Join, Lookup, etc.).
- **Schema drift**: Handle columns that appear or change at runtime.
- **Partitioning**: Optimize with hash, round-robin, or key-based partitioning.
- **Debug mode**: Test with sample data in the designer.
- **Parameterization**: Pass pipeline parameters into data flow parameters.

## Common Transformations
| Transformation | Purpose |
|----------------|---------|
| Source / Sink | Define input and output datasets |
| Derived Column | Add or modify columns with expressions |
| Select | Rename, drop, or reorder columns |
| Filter | Filter rows by condition |
| Aggregate | Group by and aggregate (sum, count, etc.) |
| Join / Lookup | Combine or enrich data |
| Surrogate Key | Generate unique keys |
| Pivot / Unpivot | Reshape data |

## When to Use

### Use Cases
1. **Complex ETL** – Multi-step transformations (clean → join → aggregate → load) without writing Spark code.
2. **Data cleansing** – Standardize formats, handle nulls, split/merge columns.
3. **Dimensional modeling** – Build star/snowflake dimensions and facts with joins and aggregates.
4. **Data quality** – Apply rules, derive quality scores, filter bad rows.
5. **Slowly changing dimensions (SCD)** – Type 1/2 logic with conditional updates.
6. **Multi-source merge** – Combine data from different sources with different schemas.

### When NOT to Use
- Simple copy only (use **Copy** activity).
- Heavy custom logic or ML (consider **Synapse Notebook** or **Databricks**).
- Trivial one-step filter (Copy with query/filter may be enough).

## Example Scenarios
- Clean and aggregate clickstream data from Blob, then load into Synapse.
- Join customer CSV with reference table from SQL and write to Cosmos DB.
- Flatten JSON, apply business rules, and write to Delta Lake.
