# Scenario 4: Slowly Changing Dimensions (SCD Types)

## Overview

Slowly Changing Dimensions (SCD) are techniques used in data warehousing to manage and track changes to dimension data over time. Different SCD types provide different approaches to handling historical data.

## What are Slowly Changing Dimensions?

Dimensions are descriptive attributes that provide context to facts in a data warehouse. When these attributes change over time, we need strategies to handle these changes while maintaining data integrity and historical accuracy.

---

## SCD Type 0: Fixed / Retain Original

### Characteristic
**Attribute never changes** - Any incoming change is ignored.

### Behavior
- Original value is retained permanently
- New values are rejected or ignored
- No updates allowed
- Simplest SCD type

### Use Cases
- Employee ID numbers
- Social Security Numbers
- Product SKUs (when they should never change)
- Immutable identifiers

### Example
```
Customer ID: 101
Name: John Doe
Original DOB: 1990-01-15

If source sends DOB: 1995-03-20 → IGNORED
Original DOB: 1990-01-15 is retained
```

### Implementation
- No update logic required
- Reject changes at ETL level
- Log rejected changes for monitoring

---

## SCD Type 1: Overwrite / No History

### Characteristic
**Old value is overwritten** - No history is maintained.

### Behavior
- New values replace old values
- Historical data is lost
- Current state only
- Simple update operation

### Use Cases
- Email addresses
- Phone numbers
- Current addresses
- Correction of data errors
- Non-critical attributes

### Example Fields
- `customer_id`
- `name`
- `DOB` / `dob` (Date of Birth)
- `type of promotion`
- `b1g1` (Buy 1 Get 1 promotion type)
- `email`
- `phone number`

### Example
```
Before Update:
Customer ID: 101
Email: john@oldemail.com
Phone: 555-0100

After Update:
Customer ID: 101
Email: john@newemail.com  ← Overwritten
Phone: 555-0200           ← Overwritten
```

### Implementation
- Simple UPDATE statement
- No additional tables needed
- Fastest processing
- Use when history is not required

---

## SCD Type 2: Full History / Complete History

### Characteristic
**Maintain complete history** - Every change creates a new record.

### Behavior
- New record created for each change
- Original record marked as historical
- Current record identified with flag
- Complete audit trail maintained

### Key Fields
- `start_date`: When this version became active
- `end_date`: When this version became inactive (or 9999-12-31 for current)
- `is_current`: Flag indicating current record (Y/N)

### Example

#### Customer Dimension Table

| Cust ID | Address    | Start Date | End Date   | Is Current |
|---------|------------|------------|------------|------------|
| 101     | Bangalore  | 2020-01-20 | 2025-01-25 | N          |
| 101     | Hyderabad  | 2025-01-25 | 9999-12-31 | Y          |

### Explanation
- Customer 101 originally lived in Bangalore (Jan 2020 - Jan 2025)
- Moved to Hyderabad in January 2025
- Old record: `is_current = N`, `end_date = 2025-01-25`
- New record: `is_current = Y`, `end_date = 9999-12-31` (indicates current)

### Use Cases
- Customer addresses
- Employee job titles
- Product categories
- Organizational hierarchies
- Any attribute where full history is critical

### Implementation
1. Identify changed records
2. Update `end_date` and `is_current` on old record
3. Insert new record with new values
4. Set `start_date = current_date`, `end_date = 9999-12-31`, `is_current = Y`

### Advantages
- Complete historical tracking
- Can query "as of" any point in time
- Full audit trail
- Regulatory compliance support

### Disadvantages
- Increased storage requirements
- More complex queries (need to filter by date)
- Slower lookups (need to check current flag)

---

## SCD Type 3: Partial History / Previous Value

### Characteristic
**Maintain partial history** - Stores current value and previous value only.

### Behavior
- Current value in one column
- Previous value in another column
- Only one level of history
- Limited historical tracking

### Example

#### Product Dimension Table

| Product ID | Current Category | Previous Category |
|------------|------------------|-------------------|
| p0001      | Electronics      | Home Appliance    |

### Explanation
- Product p0001 is currently in "Electronics" category
- Previously was in "Home Appliance" category
- Only the most recent change is tracked

### Use Cases
- When only recent history is needed
- Limited storage requirements
- Simple "what changed" queries
- Department changes
- Status changes

### Implementation
- Add `previous_` prefix columns for changed attributes
- Update both current and previous columns on change
- Simpler than Type 2, more history than Type 1

### Advantages
- Simpler than Type 2
- Some historical context
- Easier queries than Type 2
- Less storage than Type 2

### Disadvantages
- Limited history (only one previous value)
- Cannot track multiple changes
- Not suitable for detailed audit trails

---

## SCD Type 4: History Table / Separate History

### Characteristic
**Separate history table** - Current data in main table, history in separate table.

### Behavior
- Main table contains current state only
- History table contains all historical records
- Two-table approach
- Clean separation of current and historical data

### Example

#### Current Product Table

| Product ID | Price |
|------------|-------|
| p001       | 30    |
| p002       | 40    |
| p003       | 50    |

#### Product History Table

| Product ID | Price | Start Date | End Date   |
|------------|-------|------------|------------|
| p001       | 25    | 2020-01-01 | 2023-06-15 |
| p001       | 28    | 2023-06-15 | 2024-01-10 |
| p001       | 30    | 2024-01-10 | 9999-12-31 |
| p002       | 35    | 2020-01-01 | 2023-12-01 |
| p002       | 40    | 2023-12-01 | 9999-12-31 |

### Use Cases
- When current queries are performance-critical
- Large dimension tables
- Frequent historical queries on separate system
- Data archival requirements

### Implementation
1. Main table: Simple Type 1 updates
2. History table: Insert records with timestamps
3. Join tables when historical data needed

### Advantages
- Fast current data queries
- Complete history available
- Can archive history table separately
- Clean separation of concerns

### Disadvantages
- More complex queries (joins required)
- Two tables to maintain
- More storage overall
- Synchronization complexity

---

## SCD Type 5: Hybrid (Type 1 + Type 4)

### Characteristic
**Combines Type 1 + Type 4** - Current data + historical data in separate table.

### Behavior
- Main dimension table: Type 1 (current values only)
- Separate history table: Type 4 (all historical changes)
- Best of both worlds
- Optimized for both current and historical queries

### Use Cases
- High-performance current queries needed
- Complete history also required
- Large-scale data warehouses
- Mixed query patterns

### Implementation
1. Update main table with Type 1 logic (overwrite)
2. Insert historical record into history table
3. Maintain both tables in sync

### Advantages
- Fast current lookups (Type 1)
- Complete history available (Type 4)
- Flexible querying
- Performance optimized

### Disadvantages
- Most complex implementation
- Two tables to maintain
- Higher storage costs
- Synchronization overhead

---

## SCD Type 6: Ultimate Hybrid (Type 1 + Type 2 + Type 3)

### Characteristic
**Combines Type 1 + Type 2 + Type 3** - Overwrite, history, and previous values all maintained.

### Behavior
- **Type 1 aspect**: Some attributes overwritten (current values)
- **Type 2 aspect**: Complete history maintained with versioning
- **Type 3 aspect**: Previous values stored alongside current
- Most comprehensive approach

### Key Features
- **Overwrite**: Current values updated in place
- **History**: Full version history with start/end dates
- **Previous Values**: Previous value columns for quick reference

### Example Structure

| Product ID | Current Price | Previous Price | Start Date | End Date   | Is Current | Version |
|------------|---------------|----------------|------------|------------|------------|---------|
| p001       | 30            | 28             | 2024-01-10 | 9999-12-31 | Y          | 3       |
| p001       | 28            | 25             | 2023-06-15 | 2024-01-10 | N          | 2       |
| p001       | 25            | NULL           | 2020-01-01 | 2023-06-15 | N          | 1       |

### Use Cases
- Complex analytical requirements
- Regulatory compliance needs
- Complete audit trails
- Mixed query patterns
- Enterprise data warehouses

### Advantages
- Maximum flexibility
- Complete historical tracking
- Quick access to previous values
- Supports all query patterns

### Disadvantages
- Most complex to implement
- Highest storage requirements
- Most expensive to maintain
- Requires sophisticated ETL logic

---

## SCD Type Comparison Summary

| Type | History | Complexity | Storage | Use Case |
|------|---------|------------|---------|----------|
| **0** | None (fixed) | Low | Low | Immutable attributes |
| **1** | None (overwrite) | Low | Low | Non-critical changes |
| **2** | Complete | Medium | High | Full audit trail |
| **3** | Partial (one previous) | Medium | Medium | Recent history only |
| **4** | Complete (separate table) | Medium | High | Performance + history |
| **5** | Complete (Type 1 + 4) | High | High | Optimized queries |
| **6** | Complete (all methods) | Very High | Very High | Maximum flexibility |

---

## Choosing the Right SCD Type

### Choose Type 0 When:
- Attribute should never change
- Data quality enforcement needed
- Immutable identifiers

### Choose Type 1 When:
- History not required
- Simplicity is key
- Current state only needed
- Non-critical attributes

### Choose Type 2 When:
- Complete history required
- Regulatory compliance needed
- "As of" date queries needed
- Audit trail critical

### Choose Type 3 When:
- Only recent history needed
- Limited storage available
- Simple "what changed" queries

### Choose Type 4 When:
- Performance-critical current queries
- History needed but queried separately
- Large dimension tables

### Choose Type 5 When:
- Need both fast current queries and complete history
- Mixed query patterns
- Enterprise-scale requirements

### Choose Type 6 When:
- Maximum flexibility required
- Complex analytical needs
- Regulatory compliance critical
- Budget allows for complexity

---

## Implementation in Azure Data Factory

### General Approach
1. **Data Flow Activity**: Use for SCD transformations
2. **Stored Procedure Activity**: For complex SCD logic
3. **Lookup Activity**: To identify existing records
4. **Conditional Logic**: To determine SCD type behavior

### Best Practices
- Document SCD type chosen for each dimension
- Implement proper error handling
- Monitor data quality
- Test with sample data
- Consider performance implications
- Plan for storage growth (especially Type 2, 4, 5, 6)
