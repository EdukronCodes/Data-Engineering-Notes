# Execute SSIS Package Activity

## Overview
The **Execute SSIS Package** activity runs a **SQL Server Integration Services (SSIS)** package hosted in **Azure-SSIS Integration Runtime**. The package can be stored in SSIS Catalog (SSISDB), file system, or Azure SQL Database (MSDB). Used to lift-and-shift existing SSIS workloads to Azure.

## Key Features
- **SSIS execution**: Run packages deployed to Azure-SSIS IR (catalog or file system).
- **Parameters**: Pass project/package parameters and connection manager overrides (e.g., connection strings).
- **Authentication**: Windows auth, or pass credentials for package data sources.
- **Logging**: Execution logs can be written to SSISDB or custom log provider.
- **Environment**: Use SSIS environments (catalog) for parameter values per environment.

## Common Properties
| Property | Description |
|----------|-------------|
| Azure-SSIS IR | Integration Runtime that hosts SSIS |
| Package location | SSISDB, file system, or Azure SQL (MSDB) |
| Package path | Path to package in the store |
| Connection manager overrides | Override connection strings at runtime |
| Property overrides | Override package properties |
| Logging level | None, Basic, Performance, Verbose |

## When to Use

### Use Cases
1. **Lift-and-shift SSIS** – Migrate existing SSIS packages to Azure; run them on Azure-SSIS IR and orchestrate with ADF.
2. **Legacy ETL** – Complex packages (data flow, script task, custom components) that are costly to rewrite; run as-is.
3. **Hybrid** – SSIS package connects to on-premises sources (via IR); ADF schedules and passes parameters.
4. **Parameterized packages** – ADF passes run date, paths, or connection overrides; package uses them for dynamic execution.
5. **Multi-package** – Master package or ADF pipeline that runs several child packages (Execute SSIS Package or Execute Package Task).
6. **Enterprise standard** – Organization standardizes on SSIS; ADF is the scheduler and orchestrator.

### When NOT to Use
- New development (prefer ADF Copy, Data Flow, or Synapse for new pipelines).
- No existing SSIS (use native ADF activities).
- Package requires features not supported on Azure-SSIS (check compatibility).

## Example Scenarios
- Daily pipeline: ADF runs Execute SSIS Package for “Load_DimCustomer.dtsx” with connection override to prod DB; package runs on Azure-SSIS IR.
- ADF passes project parameter (RunDate); package uses it for incremental extract; result in SSISDB.
- ForEach over list of packages; each iteration runs one SSIS package with different parameter set.
