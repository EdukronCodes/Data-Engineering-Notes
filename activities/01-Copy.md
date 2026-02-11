# Copy Activity

## Overview
The **Copy** activity is the primary data movement activity in Azure Data Factory. It copies data between source and sink data stores with support for 90+ connectors (Azure, on-premises, file systems, databases, SaaS apps).

## Key Features
- **Schema mapping**: Map source columns to sink columns; supports automatic schema detection.
- **Partition options**: Optimize with dynamic range or physical partitions.
- **Fault tolerance**: Skip incompatible rows, log them, or fail the run.
- **Data flow conversion**: Type conversion, format conversion (e.g., CSV ↔ Parquet).
- **Integration Runtime**: Use Azure IR for cloud sources/sinks; Self-hosted IR for on-premises or private networks.

## Common Properties
| Property | Description |
|----------|-------------|
| Source | Dataset or linked service defining source (e.g., Blob, SQL, REST) |
| Sink | Dataset or linked service defining destination |
| Enable Staging | Use staging (e.g., Blob) for PolyBase or faster bulk load |
| Parallel Copies | Control degree of parallelism for throughput |

## When to Use

### Use Cases
1. **ETL/ELT ingestion** – Load raw data from Blob/ADLS, SQL, Cosmos DB, etc., into a data lake or warehouse.
2. **Database migration** – Copy tables or full databases between SQL Server, Azure SQL, PostgreSQL, etc.
3. **File sync** – Replicate files/folders between Blob, ADLS, S3, or on-premises file shares.
4. **SaaS to warehouse** – Ingest from Salesforce, Dynamics, Marketo, etc., into Azure Synapse or SQL.
5. **Incremental loads** – Use watermark columns or change data capture (CDC) with Copy + Filter.
6. **Backup/archival** – Copy production data to cold storage or another region.

### When NOT to Use
- For complex transformations (use **Data Flow** or **Synapse Notebook**).
- For in-database only operations (use **Stored Procedure**).
- For orchestration only (use **Execute Pipeline**, **Until**, **If Condition**).

## Example Scenarios
- Copy CSV from Azure Blob to Azure SQL Database with column mapping.
- Incremental copy from SQL Server to Synapse using a `LastModifiedDate` watermark.
- Copy Parquet from ADLS to Snowflake with staging and partition by date.
