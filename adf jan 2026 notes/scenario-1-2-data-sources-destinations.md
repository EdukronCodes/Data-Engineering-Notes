# Scenario 1 & 2: Data Sources and Destinations

## Overview

These scenarios cover different combinations of data sources and destinations in Azure Data Factory pipelines.

## Scenario 1: Blob to Blob

### Configuration
- **Source**: Azure Blob Storage
- **Destination**: Azure Blob Storage

### Use Cases
- Data transformation and staging
- Data format conversion (e.g., CSV to Parquet)
- Data archiving and backup
- Intermediate data processing steps

### Implementation Notes
- Both source and destination are in Azure Blob Storage
- Useful for data lake scenarios
- Can be used for data partitioning and optimization

---

## Scenario 2: SQL to Blob

### Configuration
- **Source**: SQL Server / Azure SQL Database
- **Destination**: Azure Blob Storage

### Context
- **Container**: Same container for related data
- **Data Types**: Transaction Data, Promotions, Productions, Supply Chain

### Use Cases
- Extracting data from relational databases to data lakes
- Creating data backups
- Preparing data for analytics and reporting
- Data archival from operational databases

### Implementation Notes
- Source data comes from SQL Server (relational database)
- Destination is Azure Blob Storage (object storage)
- Common pattern for modern data architectures
- Enables separation of operational and analytical workloads

### Example Data Flow
```
SQL Server → Azure Data Factory → Azure Blob Storage
```

### Related Data Sets
- **Transaction Data**: Customer transactions, orders, payments
- **Promotions**: Marketing campaigns, discount data
- **Productions**: Manufacturing and production records
- **Supply Chain**: Inventory, logistics, supplier data

### Best Practices
1. Use appropriate file formats (Parquet for analytics, CSV for compatibility)
2. Implement partitioning strategies for large datasets
3. Consider compression to reduce storage costs
4. Implement incremental loading where possible
5. Add metadata tags for better data governance
