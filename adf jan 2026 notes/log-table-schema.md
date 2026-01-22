# Log Table Schema

## Overview

This document provides detailed specifications for the log table schema used to track Azure Data Factory pipeline execution, data processing metrics, and error information.

---

## Main Log Table Schema

### Table Name: `pipeline_log`

### Complete Schema Definition

```sql
CREATE TABLE pipeline_log (
    -- Primary Key
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Process Identification
    process_name NVARCHAR(100) NOT NULL,
    run_id UNIQUEIDENTIFIER NOT NULL,
    job_type NVARCHAR(50),
    
    -- Execution Timing
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_seconds INT,
    
    -- Data Processing Metrics
    total_rows_count BIGINT,
    total_column_count INT,
    
    -- Status and Error Information
    status NVARCHAR(20) NOT NULL,  -- Success, Failed, In Progress, Cancelled
    error_code NVARCHAR(50),
    error_message NVARCHAR(MAX),
    
    -- Retry Information
    retry_count INT DEFAULT 0,
    
    -- Metadata
    created_date DATETIME DEFAULT GETDATE(),
    updated_date DATETIME DEFAULT GETDATE(),
    
    -- Indexes
    INDEX idx_run_id (run_id),
    INDEX idx_process_name (process_name),
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
);
```

---

## Field Descriptions

### 1. `log_id`
- **Type**: `INT IDENTITY(1,1)`
- **Primary Key**: Yes
- **Description**: Unique identifier for each log entry. Auto-incremented.
- **Example**: `1`, `2`, `3`, ...

---

### 2. `process_name`
- **Type**: `NVARCHAR(100)`
- **Nullable**: No
- **Description**: Name of the pipeline or process being executed.
- **Examples**: 
  - `"LoadCustomerData"`
  - `"IncrementalOrderLoad"`
  - `"SCDType2CustomerDimension"`
- **Use Cases**: 
  - Filter logs by process
  - Group execution statistics
  - Identify which pipeline failed

---

### 3. `run_id`
- **Type**: `UNIQUEIDENTIFIER`
- **Nullable**: No
- **Description**: Unique identifier for each pipeline execution run. Used to correlate all activities within a single pipeline execution.
- **Example**: `"550e8400-e29b-41d4-a716-446655440000"`
- **Use Cases**:
  - Track all activities in a single run
  - Link to detailed activity logs
  - Correlate errors across activities

---

### 4. `job_type`
- **Type**: `NVARCHAR(50)`
- **Nullable**: Yes
- **Description**: Type of job or load strategy being executed.
- **Possible Values**:
  - `"Full Load"`
  - `"Incremental Load"`
  - `"Batch Load"`
  - `"Live Streaming"`
  - `"SCD Type 1"`
  - `"SCD Type 2"`
  - `"Data Validation"`
- **Use Cases**:
  - Categorize execution types
  - Compare performance across job types
  - Filter by load strategy

---

### 5. `start_time`
- **Type**: `DATETIME`
- **Nullable**: No
- **Description**: Timestamp when the pipeline execution started.
- **Format**: `YYYY-MM-DD HH:MM:SS`
- **Example**: `"2024-01-15 10:00:00"`
- **Use Cases**:
  - Calculate duration
  - Schedule analysis
  - Time-based filtering
  - Performance trending

---

### 6. `end_time`
- **Type**: `DATETIME`
- **Nullable**: Yes
- **Description**: Timestamp when the pipeline execution completed (successfully or with failure).
- **Format**: `YYYY-MM-DD HH:MM:SS`
- **Example**: `"2024-01-15 10:05:30"`
- **Note**: `NULL` if pipeline is still running or was cancelled before completion.
- **Use Cases**:
  - Calculate duration
  - Identify long-running processes
  - Schedule optimization

---

### 7. `duration_seconds`
- **Type**: `INT`
- **Nullable**: Yes
- **Description**: Total execution time in seconds. Calculated as difference between `end_time` and `start_time`.
- **Example**: `330` (for 5 minutes 30 seconds)
- **Calculation**: `DATEDIFF(SECOND, start_time, end_time)`
- **Use Cases**:
  - Performance monitoring
  - SLA tracking
  - Identifying slow processes
  - Capacity planning

---

### 8. `total_rows_count`
- **Type**: `BIGINT`
- **Nullable**: Yes
- **Description**: Total number of rows processed during the pipeline execution.
- **Example**: `50000`, `1000000`
- **Note**: May represent rows read, transformed, or loaded depending on the process.
- **Use Cases**:
  - Volume tracking
  - Throughput calculation (rows/second)
  - Data growth monitoring
  - Capacity planning

---

### 9. `total_column_count`
- **Type**: `INT`
- **Nullable**: Yes
- **Description**: Total number of columns/fields processed.
- **Example**: `15`, `50`
- **Use Cases**:
  - Schema tracking
  - Data structure monitoring
  - Transformation validation

---

### 10. `status`
- **Type**: `NVARCHAR(20)`
- **Nullable**: No
- **Description**: Current status of the pipeline execution.
- **Possible Values**:
  - `"Success"` - Pipeline completed successfully
  - `"Failed"` - Pipeline execution failed
  - `"In Progress"` - Pipeline is currently running
  - `"Cancelled"` - Pipeline was cancelled
  - `"Warning"` - Pipeline completed with warnings
- **Use Cases**:
  - Filter successful/failed runs
  - Calculate success rates
  - Alerting and monitoring
  - Dashboard status indicators

---

### 11. `error_code`
- **Type**: `NVARCHAR(50)`
- **Nullable**: Yes
- **Description**: Standardized error code for categorization and automated handling.
- **Examples**:
  - `"VALIDATION_FAILED"`
  - `"CONNECTION_TIMEOUT"`
  - `"INSUFFICIENT_PERMISSIONS"`
  - `"DATA_TYPE_MISMATCH"`
  - `"NULL_VIOLATION"`
- **Use Cases**:
  - Error categorization
  - Automated error handling
  - Error trend analysis
  - Alert routing

---

### 12. `error_message`
- **Type**: `NVARCHAR(MAX)`
- **Nullable**: Yes
- **Description**: Detailed error message describing what went wrong. May include stack traces, SQL errors, or custom messages.
- **Example**: 
  ```
  "Validation failed: 150 records failed price range check. 
   Error at activity 'ValidateData' in pipeline 'LoadOrders'. 
   SQL Error: Invalid column name 'order_totl'"
  ```
- **Use Cases**:
  - Troubleshooting
  - Root cause analysis
  - Developer debugging
  - Support ticket information

---

### 13. `retry_count`
- **Type**: `INT`
- **Default**: `0`
- **Nullable**: No
- **Description**: Number of retry attempts made for this pipeline run.
- **Example**: `0` (first attempt), `1` (first retry), `2` (second retry)
- **Use Cases**:
  - Retry strategy monitoring
  - Identifying persistent failures
  - Performance impact analysis
  - Alerting on excessive retries

---

### 14. `created_date`
- **Type**: `DATETIME`
- **Default**: `GETDATE()`
- **Nullable**: No
- **Description**: Timestamp when the log record was created.
- **Use Cases**:
  - Audit trail
  - Data retention policies
  - Historical analysis

---

### 15. `updated_date`
- **Type**: `DATETIME`
- **Default**: `GETDATE()`
- **Nullable**: No
- **Description**: Timestamp when the log record was last updated.
- **Use Cases**:
  - Track record modifications
  - Audit trail
  - Data freshness

---

## Additional Log Tables

### Activity-Level Log Table

For detailed tracking of individual activities within a pipeline:

```sql
CREATE TABLE pipeline_activity_log (
    activity_log_id INT IDENTITY(1,1) PRIMARY KEY,
    run_id UNIQUEIDENTIFIER NOT NULL,
    activity_name NVARCHAR(100) NOT NULL,
    activity_type NVARCHAR(50),
    start_time DATETIME,
    end_time DATETIME,
    duration_seconds INT,
    rows_processed BIGINT,
    status NVARCHAR(20),
    error_message NVARCHAR(MAX),
    FOREIGN KEY (run_id) REFERENCES pipeline_log(run_id)
);
```

### Validation Log Table

For tracking data validation results:

```sql
CREATE TABLE validation_log (
    validation_id INT IDENTITY(1,1) PRIMARY KEY,
    run_id UNIQUEIDENTIFIER NOT NULL,
    validation_type NVARCHAR(50),
    table_name NVARCHAR(100),
    total_records_checked BIGINT,
    failed_records_count BIGINT,
    passed_records_count BIGINT,
    validation_status NVARCHAR(20),
    error_summary NVARCHAR(MAX),
    validated_at DATETIME DEFAULT GETDATE()
);
```

---

## Indexing Strategy

### Recommended Indexes

```sql
-- Primary index on run_id for fast lookups
CREATE INDEX idx_pipeline_log_run_id 
ON pipeline_log(run_id);

-- Index on process_name for filtering by process
CREATE INDEX idx_pipeline_log_process_name 
ON pipeline_log(process_name);

-- Index on status for filtering successful/failed runs
CREATE INDEX idx_pipeline_log_status 
ON pipeline_log(status);

-- Composite index for time-based queries
CREATE INDEX idx_pipeline_log_start_time_status 
ON pipeline_log(start_time, status);

-- Index for date range queries
CREATE INDEX idx_pipeline_log_created_date 
ON pipeline_log(created_date);
```

---

## Sample Queries

### Get Latest Run for a Process
```sql
SELECT TOP 1 *
FROM pipeline_log
WHERE process_name = 'LoadCustomerData'
ORDER BY start_time DESC;
```

### Get Failed Runs in Last 24 Hours
```sql
SELECT 
    process_name,
    run_id,
    start_time,
    error_code,
    error_message
FROM pipeline_log
WHERE status = 'Failed'
  AND start_time >= DATEADD(HOUR, -24, GETDATE())
ORDER BY start_time DESC;
```

### Calculate Success Rate
```sql
SELECT 
    process_name,
    COUNT(*) AS total_runs,
    SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) AS successful_runs,
    CAST(SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS success_rate_percent
FROM pipeline_log
WHERE start_time >= DATEADD(DAY, -30, GETDATE())
GROUP BY process_name;
```

### Get Average Execution Time
```sql
SELECT 
    process_name,
    AVG(duration_seconds) AS avg_duration_seconds,
    MIN(duration_seconds) AS min_duration_seconds,
    MAX(duration_seconds) AS max_duration_seconds
FROM pipeline_log
WHERE status = 'Success'
  AND start_time >= DATEADD(DAY, -7, GETDATE())
GROUP BY process_name;
```

---

## Data Retention and Archival

### Retention Policy
- **Active Logs**: Keep last 90 days in main table
- **Archived Logs**: Move to archive table after 90 days
- **Purge Policy**: Delete logs older than 2 years

### Archival Script
```sql
-- Archive old logs
INSERT INTO pipeline_log_archive
SELECT *
FROM pipeline_log
WHERE created_date < DATEADD(DAY, -90, GETDATE());

-- Delete archived records
DELETE FROM pipeline_log
WHERE created_date < DATEADD(DAY, -90, GETDATE());
```

---

## Related Topics

- [Scenario 6: Log Table](./scenario-6-log-table.md) - Implementation and use cases
- [Scenario 5: Data Validation](./scenario-5-data-validation.md) - Validation logging
