# Data Validation Rules

## Overview

This document provides detailed data validation rules and examples for ensuring data quality in Azure Data Factory pipelines. These rules should be applied during the ETL/ELT process to catch data quality issues early.

---

## 1. Range Checks

Range checks validate that numeric values fall within acceptable boundaries.

### Examples

#### Order Total Validation
**Rule**: `order_total = sum(item_price * quantity)`

**Description**: The order total must equal the sum of all line items (price × quantity).

**Validation Logic**:
```sql
SELECT 
    order_id,
    order_total,
    calculated_total,
    ABS(order_total - calculated_total) AS difference
FROM (
    SELECT 
        o.order_id,
        o.order_total,
        SUM(oi.item_price * oi.quantity) AS calculated_total
    FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id, o.order_total
) AS calc
WHERE ABS(order_total - calculated_total) > 0.01; -- Allow small rounding differences
```

**Error Message**: "Order total does not match sum of line items"

---

#### Price Validation
**Rule**: `price > 0`

**Description**: All prices must be positive numbers (greater than zero).

**Validation Logic**:
```sql
SELECT 
    product_id,
    price,
    'Price must be greater than 0' AS validation_error
FROM products
WHERE price <= 0;
```

**Error Message**: "Price must be greater than 0"

---

#### Quantity Validation
**Rule**: `quantity > 1` (or `quantity >= 1` depending on business rules)

**Description**: Quantity must be at least 1 (or greater than 1 if zero quantities are not allowed).

**Validation Logic**:
```sql
SELECT 
    order_item_id,
    quantity,
    'Quantity must be greater than 1' AS validation_error
FROM order_items
WHERE quantity <= 1; -- or quantity < 1 if zero is not allowed
```

**Error Message**: "Quantity must be greater than 1"

---

### Additional Range Check Examples

#### Age Validation
```sql
-- Age must be between 0 and 150
WHERE age < 0 OR age > 150
```

#### Percentage Validation
```sql
-- Discount percentage must be between 0 and 100
WHERE discount_percentage < 0 OR discount_percentage > 100
```

#### Date Range Validation
```sql
-- Order date must be within last 5 years
WHERE order_date < DATEADD(YEAR, -5, GETDATE())
```

---

## 2. Null Value Checks

Null value checks ensure that required fields are not empty.

### Implementation

#### Single Column Null Check
```sql
SELECT 
    customer_id,
    'Email cannot be null' AS validation_error
FROM customers
WHERE email IS NULL;
```

#### Multiple Column Null Check
```sql
SELECT 
    order_id,
    CASE 
        WHEN customer_id IS NULL THEN 'Customer ID is required'
        WHEN order_date IS NULL THEN 'Order date is required'
        WHEN order_total IS NULL THEN 'Order total is required'
    END AS validation_error
FROM orders
WHERE customer_id IS NULL 
   OR order_date IS NULL 
   OR order_total IS NULL;
```

#### Critical Field Validation
```sql
-- Check for nulls in critical business fields
SELECT 
    'customers' AS table_name,
    COUNT(*) AS null_count,
    'customer_id' AS field_name
FROM customers
WHERE customer_id IS NULL

UNION ALL

SELECT 
    'orders' AS table_name,
    COUNT(*) AS null_count,
    'order_id' AS field_name
FROM orders
WHERE order_id IS NULL;
```

---

## 3. Outliers Check

Outlier detection identifies values that are significantly different from the norm, which may indicate data quality issues.

### Statistical Methods

#### Z-Score Method
**Rule**: Values beyond 3 standard deviations are considered outliers.

```sql
WITH stats AS (
    SELECT 
        AVG(order_total) AS mean,
        STDEV(order_total) AS std_dev
    FROM orders
    WHERE order_date >= DATEADD(MONTH, -3, GETDATE())
)
SELECT 
    o.order_id,
    o.order_total,
    ABS((o.order_total - s.mean) / s.std_dev) AS z_score,
    'Order total is an outlier' AS validation_error
FROM orders o
CROSS JOIN stats s
WHERE ABS((o.order_total - s.mean) / s.std_dev) > 3;
```

#### Interquartile Range (IQR) Method
**Rule**: Values outside Q1 - 1.5×IQR or Q3 + 1.5×IQR are outliers.

```sql
WITH quartiles AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY order_total) AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY order_total) AS Q3
    FROM orders
    WHERE order_date >= DATEADD(MONTH, -3, GETDATE())
)
SELECT 
    o.order_id,
    o.order_total,
    CASE 
        WHEN o.order_total < (q.Q1 - 1.5 * (q.Q3 - q.Q1)) THEN 'Below lower bound'
        WHEN o.order_total > (q.Q3 + 1.5 * (q.Q3 - q.Q1)) THEN 'Above upper bound'
    END AS validation_error
FROM orders o
CROSS JOIN quartiles q
WHERE o.order_total < (q.Q1 - 1.5 * (q.Q3 - q.Q1))
   OR o.order_total > (q.Q3 + 1.5 * (q.Q3 - q.Q1));
```

#### Business Rule Outliers
```sql
-- Orders over $1,000,000 may be outliers (depending on business)
SELECT 
    order_id,
    order_total,
    'Unusually large order total' AS validation_error
FROM orders
WHERE order_total > 1000000;
```

---

## 4. Duplicate Checks

Duplicate checks identify records that should be unique but appear multiple times.

### Primary Key Duplicates
```sql
SELECT 
    customer_id,
    COUNT(*) AS duplicate_count,
    'Duplicate customer ID found' AS validation_error
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;
```

### Composite Key Duplicates
```sql
-- Check for duplicate order items (same order + product)
SELECT 
    order_id,
    product_id,
    COUNT(*) AS duplicate_count,
    'Duplicate order item found' AS validation_error
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;
```

### Business Rule Duplicates
```sql
-- Check for duplicate email addresses (if business rule requires unique emails)
SELECT 
    email,
    COUNT(*) AS duplicate_count,
    'Duplicate email address found' AS validation_error
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;
```

### Date-Based Duplicate Check
**Rule**: `order_date <= current_date`

**Description**: Order dates cannot be in the future.

```sql
SELECT 
    order_id,
    order_date,
    'Order date cannot be in the future' AS validation_error
FROM orders
WHERE order_date > CAST(GETDATE() AS DATE);
```

---

## 5. Format Validation

Format validation ensures data conforms to expected patterns and formats.

### Date Format Validation

#### Incorrect Date Formats
```sql
-- Check for invalid date formats or unparseable dates
SELECT 
    order_id,
    order_date_string,
    'Invalid date format' AS validation_error
FROM orders_staging
WHERE TRY_CAST(order_date_string AS DATE) IS NULL
   AND order_date_string IS NOT NULL;
```

#### Date Logic Validation
**Rule**: `ship_date >= order_date`

**Description**: Ship date must be on or after the order date.

```sql
SELECT 
    order_id,
    order_date,
    ship_date,
    'Ship date cannot be before order date' AS validation_error
FROM orders
WHERE ship_date < order_date;
```

#### Additional Date Validations
```sql
-- Delivery date must be after ship date
WHERE delivery_date < ship_date

-- Return date must be after order date
WHERE return_date < order_date

-- Cancellation date must be after order date
WHERE cancellation_date < order_date
```

---

### Email Format Validation
```sql
SELECT 
    customer_id,
    email,
    'Invalid email format' AS validation_error
FROM customers
WHERE email IS NOT NULL
  AND email NOT LIKE '%_@_%._%'  -- Basic email pattern
  AND email NOT LIKE '%@%@%';    -- No multiple @ symbols
```

### Phone Number Format Validation
```sql
SELECT 
    customer_id,
    phone_number,
    'Invalid phone number format' AS validation_error
FROM customers
WHERE phone_number IS NOT NULL
  AND phone_number NOT LIKE '[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]';
```

### Postal Code Format Validation
```sql
-- US ZIP code format (5 digits or 5+4 format)
SELECT 
    address_id,
    postal_code,
    'Invalid postal code format' AS validation_error
FROM addresses
WHERE postal_code IS NOT NULL
  AND postal_code NOT LIKE '[0-9][0-9][0-9][0-9][0-9]%'
  AND LEN(REPLACE(postal_code, '-', '')) NOT IN (5, 9);
```

---

## 6. Business Rule Validation

Business rule validation enforces domain-specific logic.

### Order Status Progression
**Rule**: Order status must follow valid progression: `created → paid → shipped → delivered`

```sql
SELECT 
    order_id,
    current_status,
    previous_status,
    'Invalid status progression' AS validation_error
FROM (
    SELECT 
        o.order_id,
        o.status AS current_status,
        LAG(o.status) OVER (PARTITION BY o.order_id ORDER BY o.status_date) AS previous_status
    FROM orders o
) AS status_check
WHERE (previous_status = 'delivered' AND current_status IN ('created', 'paid', 'shipped'))
   OR (previous_status = 'shipped' AND current_status IN ('created', 'paid'))
   OR (previous_status = 'paid' AND current_status = 'created');
```

### Inventory Validation
**Rule**: `inventory_should never get into negative`

**Description**: Inventory levels should never be negative.

```sql
SELECT 
    product_id,
    warehouse_id,
    current_inventory,
    'Inventory cannot be negative' AS validation_error
FROM inventory
WHERE current_inventory < 0;
```

### Payment Validation
```sql
-- Payment amount cannot exceed order total
SELECT 
    p.payment_id,
    p.payment_amount,
    o.order_total,
    'Payment amount exceeds order total' AS validation_error
FROM payments p
INNER JOIN orders o ON p.order_id = o.order_id
WHERE p.payment_amount > o.order_total;
```

### Promotion Validation
```sql
-- Promotion end date must be after start date
SELECT 
    promotion_id,
    start_date,
    end_date,
    'Promotion end date must be after start date' AS validation_error
FROM promotions
WHERE end_date < start_date;
```

---

## 7. Referential Integrity Checks

### Foreign Key Validation
```sql
-- Orders must reference valid customers
SELECT 
    o.order_id,
    o.customer_id,
    'Invalid customer reference' AS validation_error
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
```

### Orphaned Records
```sql
-- Order items must reference valid orders
SELECT 
    oi.order_item_id,
    oi.order_id,
    'Orphaned order item - order does not exist' AS validation_error
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;
```

---

## 8. Data Type Validation

### Numeric Field Validation
```sql
-- Ensure numeric fields contain only numbers
SELECT 
    product_id,
    price_string,
    'Price must be numeric' AS validation_error
FROM products_staging
WHERE ISNUMERIC(price_string) = 0
  AND price_string IS NOT NULL;
```

### Boolean Field Validation
```sql
-- Ensure boolean fields contain only valid values
SELECT 
    customer_id,
    is_active,
    'Invalid boolean value' AS validation_error
FROM customers
WHERE is_active NOT IN ('Y', 'N', '1', '0', 'True', 'False');
```

---

## Validation Implementation Template

### SQL Stored Procedure Template
```sql
CREATE PROCEDURE sp_ValidateData
    @TableName NVARCHAR(100),
    @RunId INT
AS
BEGIN
    -- Range checks
    INSERT INTO validation_results (run_id, validation_type, failed_count, error_message)
    SELECT @RunId, 'Range Check', COUNT(*), 'Prices must be greater than 0'
    FROM @TableName
    WHERE price <= 0;
    
    -- Null checks
    INSERT INTO validation_results (run_id, validation_type, failed_count, error_message)
    SELECT @RunId, 'Null Check', COUNT(*), 'Email cannot be null'
    FROM @TableName
    WHERE email IS NULL;
    
    -- Duplicate checks
    INSERT INTO validation_results (run_id, validation_type, failed_count, error_message)
    SELECT @RunId, 'Duplicate Check', COUNT(*), 'Duplicate customer IDs found'
    FROM (
        SELECT customer_id, COUNT(*) AS cnt
        FROM @TableName
        GROUP BY customer_id
        HAVING COUNT(*) > 1
    ) AS dup;
    
    -- Return validation summary
    SELECT 
        validation_type,
        SUM(failed_count) AS total_failures
    FROM validation_results
    WHERE run_id = @RunId
    GROUP BY validation_type;
END
```

---

## Best Practices

1. **Validate Early**: Run validations as soon as data is extracted
2. **Fail Fast**: Stop processing on critical validation failures
3. **Log Everything**: Record all validation failures with context
4. **Provide Context**: Include row numbers, field names, and values in error messages
5. **Categorize Errors**: Classify errors by severity (Critical, Warning, Info)
6. **Enable Reprocessing**: Export bad records for correction and reprocessing
7. **Monitor Trends**: Track validation failure rates over time
8. **Document Rules**: Maintain clear documentation of all validation rules

---

## Related Topics

- [Scenario 5: Data Validation](./scenario-5-data-validation.md) - Validation methods and implementation
- [Scenario 6: Log Table](./scenario-6-log-table.md) - Logging validation results
