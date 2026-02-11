# Databricks Python Activity

## Overview
The **Databricks Python** activity runs a **Python file** (e.g., `.py`) on a Databricks cluster. The file can be stored in DBFS or workspace. Used for script-based Spark or Python logic without using a notebook.

## Key Features
- **Python script**: Execute a single .py file (e.g., Spark or plain Python).
- **Parameters**: Pass command-line arguments (e.g., `--date 2024-01-01`, `--env prod`).
- **Cluster**: Existing or job cluster; Python environment on cluster runs the script.
- **Libraries**: Cluster can have PyPI or custom libraries; script uses them at runtime.

## Common Properties
| Property | Description |
|----------|-------------|
| Databricks linked service | Workspace and auth |
| Python file path | Path to .py file (DBFS or workspace) |
| Parameters | Arguments to the script |
| Cluster | Existing or job cluster |

## When to Use

### Use Cases
1. **Script-based ETL** – Python script that uses PySpark or pandas; no notebook UI needed; easy to version in Git.
2. **CI/CD friendly** – Single .py file in repo; ADF runs it on Databricks; same as local or other runners.
3. **Reusable logic** – Same script for batch and for testing; parameters for paths and dates.
4. **Lightweight** – No notebook metadata; just code; good for automation.
5. **Libraries** – Script can rely on cluster-installed packages (pandas, ML libs); ADF only triggers.
6. **Migration** – Existing Python batch scripts can be run on Databricks with minimal change.

### When NOT to Use
- Interactive or exploratory work (notebooks are better).
- Complex multi-step with different languages (use **Databricks Notebook**).
- Simple copy or ADF-native transform (use **Copy** or **Data Flow**).

## Example Scenarios
- ADF passes date parameter; Databricks Python runs transform.py from DBFS with --date and --output path.
- Nightly: Copy to ADLS; Databricks Python runs aggregate.py; output used in next ADF activity.
- Python script reads config from Blob, runs Spark job, writes to Delta; ADF triggers and waits.
