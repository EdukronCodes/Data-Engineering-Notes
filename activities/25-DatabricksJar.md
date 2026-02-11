# Databricks JAR Activity

## Overview
The **Databricks JAR** activity runs a **JAR** (Java/Scala compiled artifact) on a Databricks cluster. You specify the JAR location (DBFS or workspace) and main class; optional parameters can be passed. Used for existing JAR-based Spark jobs.

## Key Features
- **JAR execution**: Run a pre-built JAR (e.g., Spark job written in Scala/Java).
- **Main class**: Specify main class name when JAR has multiple entry points.
- **Parameters**: Pass command-line arguments to the JAR (e.g., input path, date).
- **Cluster**: Existing cluster or job cluster; same cluster options as Databricks Notebook.

## Common Properties
| Property | Description |
|----------|-------------|
| Databricks linked service | Workspace and auth |
| JAR path | DBFS or workspace path to JAR (e.g., dbfs:/libs/etl.jar) |
| Main class name | Optional; required if JAR has multiple mains |
| Parameters | List of arguments passed to the JAR |
| Cluster | Existing or job cluster config |

## When to Use

### Use Cases
1. **Existing Spark jobs** – Team already has JAR-based ETL or batch jobs; ADF orchestrates and triggers on schedule.
2. **Scala/Java Spark** – Logic written in Scala/Java and packaged as JAR; no need to rewrite as notebook.
3. **Libraries and dependencies** – JAR bundles all dependencies; consistent execution on cluster.
4. **CI/CD built artifacts** – JAR built in pipeline; path passed to ADF (e.g., parameter); ADF runs specific version.
5. **Performance-critical code** – Compiled JAR may run faster than interpreted notebook for heavy logic.
6. **Enterprise standards** – Some organizations standardize on JAR for production Spark jobs.

### When NOT to Use
- New development (notebooks are easier to develop and maintain for many teams).
- Simple or ad-hoc logic (use **Databricks Notebook** or **Data Flow**).
- No existing JAR (use Notebook or Data Flow).

## Example Scenarios
- ADF Copy lands data in ADLS; Databricks JAR runs company ETL JAR with args (input path, output path, date).
- Nightly run: ADF triggers Databricks JAR (main class com.company.MergeJob) with parameters from pipeline variables.
- ForEach over partitions: each iteration runs same JAR with different partition parameter.
