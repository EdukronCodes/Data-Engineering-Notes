# Scenario 6: Log Table

## Overview

Log tables are essential for tracking and monitoring data pipeline execution in Azure Data Factory. They maintain a complete history of pipeline runs, including processed rows, columns, execution times, and status information.

## Purpose

The log table serves to:
- **Maintain history of rows processed**: Track how many records were processed in each run
- **Track columns processed**: Monitor which columns/fields were handled
- **Monitor pipeline execution**: Track start times, end times, and duration
- **Error tracking**: Record errors, error codes, and error messages
- **Audit trail**: Provide complete audit information for compliance
- **Performance monitoring**: Track execution times and identify bottlenecks
- **Retry management**: Track retry attempts and success/failure

## Storage Options

### 1. Azure SQL Database

#### Advantages
- Structured querying capabilities
- Easy integration with reporting tools
- ACID compliance
- Relational data model
- Indexing for performance

#### Use Cases
- Enterprise data warehouses
- When SQL querying is required
- Integration with existing SQL infrastructure
- Complex reporting needs

#### Implementation
```sql
CREATE TABLE pipeline_log (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    process_name NVARCHAR(100),
    run_id UNIQUEIDENTIFIER,
    job_type NVARCHAR(50),
    start_time DATETIME,
    end_time DATETIME,
    duration_seconds INT,
    total_rows_count BIGINT,
    total_column_count INT,
    status NVARCHAR(20),
    error_code NVARCHAR(50),
    error_message NVARCHAR(MAX),
    retry_count INT,
    created_date DATETIME DEFAULT GETDATE()
);
```

---

### 2. Azure Blob Storage (CSV)

#### Advantages
- Cost-effective storage
- Easy to export and share
- No database licensing required
- Suitable for large volumes
- Can be processed by various tools

#### Use Cases
- High-volume logging
- Cost optimization
- Data lake scenarios
- Long-term archival
- Integration with big data tools

#### File Naming Convention
```
pipeline_log_{process_name}_{run_id}_{timestamp}.csv
```

#### CSV Structure
```csv
log_id,process_name,run_id,job_type,start_time,end_time,duration_seconds,total_rows_count,total_column_count,status,error_code,error_message,retry_count
1,LoadCustomerData,abc-123,Full Load,2024-01-15 10:00:00,2024-01-15 10:05:30,330,50000,15,Success,,,0
```

---

## Log Table Schema

For detailed field descriptions, see [Log Table Schema](./log-table-schema.md).

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `log_id` | INT/UNIQUEID | Unique identifier for each log entry |
| `process_name` | NVARCHAR | Name of the pipeline/process |
| `run_id` | UNIQUEIDENTIFIER | Unique identifier for each pipeline run |
| `job_type` | NVARCHAR | Type of job (Full Load, Incremental, etc.) |
| `start_time` | DATETIME | Pipeline execution start time |
| `end_time` | DATETIME | Pipeline execution end time |
| `duration_seconds` | INT | Total execution time in seconds |
| `total_rows_count` | BIGINT | Number of rows processed |
| `total_column_count` | INT | Number of columns processed |
| `status` | NVARCHAR | Execution status (Success, Failed, In Progress) |
| `error_code` | NVARCHAR | Error code if execution failed |
| `error_message` | NVARCHAR(MAX) | Detailed error message |
| `retry_count` | INT | Number of retry attempts |

---

## Implementation in Azure Data Factory

### 1. Logging at Pipeline Start

#### Using Stored Procedure Activity
```sql
CREATE PROCEDURE sp_LogPipelineStart
    @ProcessName NVARCHAR(100),
    @RunId UNIQUEIDENTIFIER,
    @JobType NVARCHAR(50)
AS
BEGIN
    INSERT INTO pipeline_log (
        process_name,
        run_id,
        job_type,
        start_time,
        status
    )
    VALUES (
        @ProcessName,
        @RunId,
        @JobType,
        GETDATE(),
        'In Progress'
    );
END
```

---

### 2. Logging at Pipeline End

#### Success Logging
```sql
CREATE PROCEDURE sp_LogPipelineSuccess
    @RunId UNIQUEIDENTIFIER,
    @TotalRowsCount BIGINT,
    @TotalColumnCount INT
AS
BEGIN
    UPDATE pipeline_log
    SET 
        end_time = GETDATE(),
        duration_seconds = DATEDIFF(SECOND, start_time, GETDATE()),
        total_rows_count = @TotalRowsCount,
        total_column_count = @TotalColumnCount,
        status = 'Success'
    WHERE run_id = @RunId;
END
```

#### Failure Logging
```sql
CREATE PROCEDURE sp_LogPipelineFailure
    @RunId UNIQUEIDENTIFIER,
    @ErrorCode NVARCHAR(50),
    @ErrorMessage NVARCHAR(MAX),
    @RetryCount INT
AS
BEGIN
    UPDATE pipeline_log
    SET 
        end_time = GETDATE(),
        duration_seconds = DATEDIFF(SECOND, start_time, GETDATE()),
        status = 'Failed',
        error_code = @ErrorCode,
        error_message = @ErrorMessage,
        retry_count = @RetryCount
    WHERE run_id = @RunId;
END
```

---

### 3. Logging Row Counts

#### Using Data Flow Activity
- Use **Aggregate** transformation to count rows
- Store count in a variable
- Log to table using Stored Procedure Activity

#### Example
```sql
CREATE PROCEDURE sp_LogRowCount
    @RunId UNIQUEIDENTIFIER,
    @TableName NVARCHAR(100),
    @RowCount BIGINT
AS
BEGIN
    INSERT INTO pipeline_log_detail (
        run_id,
        table_name,
        row_count,
        logged_at
    )
    VALUES (
        @RunId,
        @TableName,
        @RowCount,
        GETDATE()
    );
END
```

---

## Log Table Use Cases

### 1. Monitoring and Alerting
- Track pipeline success/failure rates
- Monitor execution times
- Identify slow-running pipelines
- Set up alerts for failures

### 2. Performance Analysis
- Identify bottlenecks
- Track processing volumes over time
- Analyze duration trends
- Optimize pipeline performance

### 3. Audit and Compliance
- Complete audit trail
- Regulatory compliance
- Data lineage tracking
- Change tracking

### 4. Troubleshooting
- Error investigation
- Retry analysis
- Failure pattern identification
- Root cause analysis

### 5. Reporting
- Executive dashboards
- Operational reports
- SLA monitoring
- Capacity planning

---

## Best Practices

### 1. Logging Strategy
- **Log at key milestones**: Start, major steps, completion
- **Include context**: Process name, run ID, timestamps
- **Log errors immediately**: Don't wait until end
- **Log row counts**: Track data volumes processed

### 2. Performance Considerations
- Use batch inserts for high-volume logging
- Index log tables on frequently queried columns
- Archive old logs periodically
- Consider partitioning for large log tables

### 3. Error Handling
- Always log failures, even if pipeline crashes
- Include detailed error messages
- Log retry attempts
- Track error patterns

### 4. Data Retention
- Define retention policies
- Archive old logs to blob storage
- Purge logs older than retention period
- Maintain compliance requirements

### 5. Query Optimization
- Index on `run_id`, `process_name`, `status`
- Index on `start_time` for time-based queries
- Use filtered indexes for common queries
- Consider materialized views for reporting

---

## Example Queries

### Get Latest Run Status
```sql
SELECT TOP 1 
    process_name,
    run_id,
    status,
    start_time,
    end_time,
    duration_seconds
FROM pipeline_log
WHERE process_name = 'LoadCustomerData'
ORDER BY start_time DESC;
```

### Get Failed Runs in Last 24 Hours
```sql
SELECT 
    process_name,
    run_id,
    error_code,
    error_message,
    retry_count,
    start_time
FROM pipeline_log
WHERE status = 'Failed'
    AND start_time >= DATEADD(HOUR, -24, GETDATE())
ORDER BY start_time DESC;
```

### Get Average Execution Time by Process
```sql
SELECT 
    process_name,
    AVG(duration_seconds) AS avg_duration_seconds,
    MIN(duration_seconds) AS min_duration_seconds,
    MAX(duration_seconds) AS max_duration_seconds,
    COUNT(*) AS total_runs
FROM pipeline_log
WHERE status = 'Success'
GROUP BY process_name
ORDER BY avg_duration_seconds DESC;
```

### Get Total Rows Processed Today
```sql
SELECT 
    SUM(total_rows_count) AS total_rows_processed,
    COUNT(*) AS total_runs
FROM pipeline_log
WHERE CAST(start_time AS DATE) = CAST(GETDATE() AS DATE)
    AND status = 'Success';
```

---

## Related Topics

- [Log Table Schema](./log-table-schema.md) - Detailed field descriptions
- [Scenario 5: Data Validation](./scenario-5-data-validation.md) - Validation logging
- [Scenario 3: Data Loading Strategies](./scenario-3-data-loading-strategies.md) - Logging for different load types
