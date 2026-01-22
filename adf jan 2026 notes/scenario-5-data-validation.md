# Scenario 5: Data Validation

## Overview

Data validation is a critical component of any ETL/ELT pipeline to ensure data quality, integrity, and reliability. This scenario covers various methods and approaches for implementing data validation in Azure Data Factory.

## Validation Methods

### 1. Database Level Validation

#### Using Check Constraints
- **Definition**: Constraints defined at the database schema level
- **Enforcement**: Database engine enforces rules automatically
- **Scope**: Applied to all data inserted/updated in the table

#### Advantages
- Automatic enforcement
- No application code needed
- Database-level guarantee
- Performance optimized

#### Disadvantages
- Less flexible than application-level validation
- Harder to customize error messages
- Requires schema changes

#### Example Constraints
```sql
-- Range check
ALTER TABLE orders 
ADD CONSTRAINT chk_price_positive 
CHECK (price > 0);

-- Not null check
ALTER TABLE customers 
ADD CONSTRAINT chk_email_not_null 
CHECK (email IS NOT NULL);

-- Date validation
ALTER TABLE orders 
ADD CONSTRAINT chk_order_date_valid 
CHECK (order_date <= GETDATE());
```

---

### 2. Custom Log in ADF Using Stored Procedure Activity

#### Definition
- Use Azure Data Factory's **Stored Procedure Activity**
- Execute custom validation logic in SQL
- Log validation results to a validation table

#### Implementation Steps
1. Create stored procedure with validation logic
2. Add Stored Procedure Activity to ADF pipeline
3. Execute validation checks
4. Log results to validation table
5. Handle validation failures

#### Advantages
- Flexible validation logic
- Centralized validation rules
- Can use complex SQL queries
- Reusable across pipelines

#### Example Stored Procedure
```sql
CREATE PROCEDURE sp_ValidateOrderData
    @RunId INT,
    @SourceTable NVARCHAR(100)
AS
BEGIN
    -- Validation checks
    INSERT INTO validation_log (
        run_id,
        validation_type,
        record_count,
        status,
        error_message
    )
    SELECT 
        @RunId,
        'Range Check',
        COUNT(*),
        CASE WHEN COUNT(*) > 0 THEN 'FAILED' ELSE 'PASSED' END,
        'Orders with price <= 0 found'
    FROM @SourceTable
    WHERE price <= 0;
    
    -- Additional validations...
END
```

---

### 3. Custom Python Code for Data Validation

#### Definition
- Use **Python Script Activity** in Azure Data Factory
- Implement custom validation logic in Python
- Leverage pandas, numpy, or other libraries

#### Advantages
- Maximum flexibility
- Can use data science libraries
- Complex statistical validations
- Machine learning-based validation

#### Use Cases
- Statistical outlier detection
- Pattern matching
- Complex business rules
- Data profiling

#### Example Python Validation
```python
import pandas as pd
import numpy as np

def validate_data(df):
    validation_results = []
    
    # Range check
    invalid_price = df[df['price'] <= 0]
    if len(invalid_price) > 0:
        validation_results.append({
            'check': 'Price Range',
            'status': 'FAILED',
            'count': len(invalid_price)
        })
    
    # Null check
    null_email = df[df['email'].isnull()]
    if len(null_email) > 0:
        validation_results.append({
            'check': 'Null Email',
            'status': 'FAILED',
            'count': len(null_email)
        })
    
    # Outlier detection
    Q1 = df['order_total'].quantile(0.25)
    Q3 = df['order_total'].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df['order_total'] < (Q1 - 1.5 * IQR)) | 
                  (df['order_total'] > (Q3 + 1.5 * IQR))]
    
    return validation_results
```

---

## Validation Output Destinations

### 1. Validation Table (Azure SQL Database)

#### Structure
- Store validation results in a dedicated SQL table
- Track validation runs, results, and errors
- Enable querying and reporting

#### Example Schema
```sql
CREATE TABLE validation_results (
    validation_id INT IDENTITY(1,1) PRIMARY KEY,
    run_id INT,
    validation_type NVARCHAR(100),
    table_name NVARCHAR(100),
    record_count INT,
    failed_count INT,
    status NVARCHAR(20),
    error_message NVARCHAR(MAX),
    validation_date DATETIME DEFAULT GETDATE()
);
```

#### Advantages
- Structured storage
- Easy querying and reporting
- Historical tracking
- Integration with SQL tools

---

### 2. Bad Records (Azure Blob Storage - CSV)

#### Definition
- Export failed validation records to CSV files
- Store in Azure Blob Storage
- Enable data correction and reprocessing

#### File Naming Convention
```
bad_records_{table_name}_{run_id}_{timestamp}.csv
```

#### Advantages
- Easy to review and correct
- Can be reprocessed after correction
- Human-readable format
- Can be shared with business users

#### Example Structure
```csv
record_id,field_name,field_value,validation_error,row_number
12345,price,-10,Price must be greater than 0,15
12346,email,,Email cannot be null,23
```

---

## Validation Types and Rules

See [Data Validation Rules](./data-validation-rules.md) for detailed validation rules including:
- Range checks
- Null value checks
- Outlier detection
- Duplicate checks
- Format validation
- Business rule validation

---

## Validation Workflow

### Typical Pipeline Flow

```
1. Extract Data
   ↓
2. Run Validation Checks
   ├─ Database Constraints
   ├─ Stored Procedure Validation
   └─ Python Script Validation
   ↓
3. Check Validation Results
   ├─ If PASSED → Continue to Transform/Load
   └─ If FAILED → Log to Validation Table & Bad Records
   ↓
4. Handle Failures
   ├─ Send Alert/Notification
   ├─ Export Bad Records to Blob
   └─ Stop or Continue Pipeline (based on configuration)
```

---

## Best Practices

### 1. Validation Strategy
- **Early Validation**: Validate as early as possible in the pipeline
- **Multiple Layers**: Use multiple validation methods for critical data
- **Fail Fast**: Stop pipeline on critical validation failures
- **Warn on Non-Critical**: Log warnings for non-critical issues

### 2. Performance Considerations
- Use database constraints for simple validations (fastest)
- Use stored procedures for complex SQL validations
- Use Python for statistical/ML-based validations
- Consider sampling for large datasets

### 3. Error Handling
- Log all validation failures
- Provide clear error messages
- Include context (row number, field name, value)
- Enable reprocessing of failed records

### 4. Monitoring
- Track validation pass/fail rates over time
- Monitor validation execution times
- Alert on validation failures
- Generate validation reports

### 5. Data Quality Metrics
- **Completeness**: Percentage of non-null values
- **Accuracy**: Percentage of records passing validation
- **Consistency**: Percentage of records meeting business rules
- **Timeliness**: Data freshness and latency

---

## Implementation Example

### ADF Pipeline Structure

```
Pipeline: DataValidationPipeline
├─ Activity 1: Lookup (Get Last Run ID)
├─ Activity 2: Data Flow (Extract Source Data)
├─ Activity 3: Stored Procedure (Run Validations)
│  └─ Validation Checks:
│     ├─ Range Checks
│     ├─ Null Checks
│     ├─ Duplicate Checks
│     └─ Format Checks
├─ Activity 4: If Condition (Check Validation Status)
│  ├─ True Branch: Continue to Load
│  └─ False Branch: Export Bad Records
│     ├─ Copy Activity (Bad Records to Blob)
│     └─ Send Email (Alert on Failure)
└─ Activity 5: Data Flow (Load Validated Data)
```

---

## Validation Table Schema

For detailed schema of validation tables, see [Log Table Schema](./log-table-schema.md).

---

## Related Topics

- [Data Validation Rules](./data-validation-rules.md) - Detailed validation rules and examples
- [Scenario 6: Log Table](./scenario-6-log-table.md) - Logging and tracking mechanisms
- [Scenario 3: Data Loading Strategies](./scenario-3-data-loading-strategies.md) - When to validate in loading strategies
