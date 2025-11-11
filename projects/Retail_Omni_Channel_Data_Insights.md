# Retail Omni-Channel Data Insights
**Project Duration:** April 2024 – Present

---

## Project Overview
This project focuses on analyzing retail data across multiple channels (online, in-store, mobile app) to provide unified insights into customer behavior, sales performance, inventory optimization, and channel effectiveness.

---

## Business Objectives

### Primary Goals
1. **Unified Customer View**: Create a 360-degree view of customers across all sales channels to understand shopping behaviors and preferences
2. **Revenue Optimization**: Identify high-performing products, channels, and customer segments to maximize revenue growth
3. **Inventory Intelligence**: Reduce stockouts and overstock situations through data-driven inventory management
4. **Channel Performance**: Measure and optimize performance across online, in-store, and mobile channels
5. **Customer Retention**: Increase repeat purchase rates and customer lifetime value through targeted insights

### Key Business Questions to Answer
- Which products drive the most revenue across different channels?
- What are the shopping patterns of our most valuable customers?
- How can we reduce cart abandonment rates in our e-commerce channel?
- Which stores are underperforming and why?
- What is the optimal inventory level for each SKU by location?
- How effective are our promotional campaigns across channels?
- What factors influence customer churn and how can we prevent it?

### Success Metrics
- **15% increase in revenue** through data-driven merchandising decisions
- **20% reduction in inventory carrying costs** via optimization
- **10% improvement in customer retention rate**
- **25% faster reporting** and insights delivery to stakeholders
- **30% increase in cross-channel shopping** participation

### Stakeholders
- **Executive Team**: High-level performance metrics and strategic insights
- **Merchandising Team**: Product performance and inventory optimization
- **Marketing Team**: Customer segmentation and campaign effectiveness
- **Store Operations**: Store-level performance and operational metrics
- **IT Department**: Data infrastructure and system integration
- **Finance Team**: Revenue analysis and profitability metrics

---

## SQL Server Connection in Power BI - Complete Guide

### Overview
SQL Server serves as the primary data source for storing Point of Sale (POS) transactions, inventory data, and customer information. Establishing a robust connection between Power BI and SQL Server is critical for real-time analytics and reporting.

---

## Project Architecture & Data Flow Diagrams

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   POS System │  │  E-commerce  │  │  Mobile App  │  │    CRM     │ │
│  │   (In-Store) │  │   Platform   │  │   Database   │  │  Customer  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                 │                  │                 │        │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  ┌─────┴──────┐ │
│  │  Inventory   │  │   Marketing  │  │   Payment    │  │   Loyalty  │ │
│  │    System    │  │   Campaigns  │  │   Gateway    │  │   Program  │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                 │                  │                 │        │
└─────────┼─────────────────┼──────────────────┼─────────────────┼────────┘
          │                 │                  │                 │
          └─────────────────┴──────────┬───────┴─────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        ETL / DATA INTEGRATION LAYER                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│                      ┌────────────────────────┐                          │
│                      │   Azure Data Factory   │                          │
│                      │    (ETL Orchestration) │                          │
│                      └───────────┬────────────┘                          │
│                                  │                                       │
│              ┌───────────────────┼───────────────────┐                   │
│              ▼                   ▼                   ▼                   │
│      ┌──────────────┐    ┌──────────────┐   ┌──────────────┐           │
│      │   Extract    │    │  Transform   │   │     Load     │           │
│      │  (Pull Data) │───▶│ (Clean/Map)  │──▶│  (To Data    │           │
│      │              │    │              │   │   Warehouse) │           │
│      └──────────────┘    └──────────────┘   └──────┬───────┘           │
│                                                     │                   │
└─────────────────────────────────────────────────────┼───────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       DATA WAREHOUSE LAYER                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│              ┌────────────────────────────────────┐                      │
│              │   SQL Server Data Warehouse        │                      │
│              │   RetailOmniChannel_DW             │                      │
│              ├────────────────────────────────────┤                      │
│              │                                    │                      │
│              │  ┌──────────────────────────────┐ │                      │
│              │  │     FACT TABLES              │ │                      │
│              │  │  • FactSales (10M rows)      │ │                      │
│              │  │  • FactInventory (2M rows)   │ │                      │
│              │  │  • FactCustomerActivity      │ │                      │
│              │  └──────────────────────────────┘ │                      │
│              │                                    │                      │
│              │  ┌──────────────────────────────┐ │                      │
│              │  │   DIMENSION TABLES           │ │                      │
│              │  │  • DimCustomer (485K)        │ │                      │
│              │  │  • DimProduct (25K)          │ │                      │
│              │  │  • DimStore (348)            │ │                      │
│              │  │  • DimDate (3,652)           │ │                      │
│              │  │  • DimChannel (4)            │ │                      │
│              │  └──────────────────────────────┘ │                      │
│              └─────────────────┬──────────────────┘                      │
│                                │                                         │
└────────────────────────────────┼─────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       POWER BI LAYER                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│              ┌────────────────────────────────────┐                      │
│              │    Power BI Desktop                │                      │
│              ├────────────────────────────────────┤                      │
│              │  1. Connect to SQL Server          │                      │
│              │  2. Power Query (Transform)        │                      │
│              │  3. Data Model (Relationships)     │                      │
│              │  4. DAX Measures                   │                      │
│              │  5. Report Visualizations          │                      │
│              └─────────────────┬──────────────────┘                      │
│                                │                                         │
│                                ▼                                         │
│              ┌────────────────────────────────────┐                      │
│              │    Power BI Gateway                │                      │
│              │  (For Scheduled Refresh)           │                      │
│              └─────────────────┬──────────────────┘                      │
│                                │                                         │
│                                ▼                                         │
│              ┌────────────────────────────────────┐                      │
│              │    Power BI Service (Cloud)        │                      │
│              │  • Published Reports               │                      │
│              │  • Scheduled Refresh               │                      │
│              │  • Dashboards                      │                      │
│              │  • Row-Level Security              │                      │
│              └─────────────────┬──────────────────┘                      │
│                                │                                         │
└────────────────────────────────┼─────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       END USERS LAYER                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Executives  │  │ Merchandising│  │   Marketing  │  │   Store    │ │
│  │  (Dashboards)│  │    Team      │  │     Team     │  │  Managers  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                                           │
│         Access via: Web Browser | Mobile App | Embedded Reports          │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### End-to-End Data Flow Process

```
Step 1: DATA COLLECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Multiple retail systems capture transactions
    ↓
    In-Store POS → Transaction completed → SQL Database
    E-commerce → Order placed → API endpoint
    Mobile App → Purchase → App database
    
    
Step 2: DATA EXTRACTION (ETL Process)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Azure Data Factory extracts data every 15 minutes
    ↓
    ┌─ POS Database (SQL Query)
    ├─ E-commerce API (REST calls)
    ├─ Mobile App DB (Direct connection)
    ├─ CRM System (Scheduled export)
    └─ Inventory System (Real-time feed)
    

Step 3: DATA TRANSFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Clean, standardize, and enrich data
    ↓
    • Remove duplicates
    • Standardize date formats
    • Validate data quality
    • Create unified customer IDs
    • Map product SKUs across channels
    • Calculate derived metrics
    

Step 4: DATA LOADING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Load into SQL Server Data Warehouse
    ↓
    Star Schema:
    • Fact tables (Sales, Inventory, Activity)
    • Dimension tables (Customer, Product, Store, Date)
    

Step 5: POWER BI CONNECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Connect Power BI to SQL Server
    ↓
    Import Mode: Load data into Power BI
    DirectQuery: Query database in real-time
    Composite: Mix of both (optimal)
    

Step 6: DATA MODELING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Build relationships and calculations
    ↓
    • Create table relationships
    • Write DAX measures
    • Optimize data types
    • Hide technical columns
    

Step 7: VISUALIZATION & REPORTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Design interactive reports
    ↓
    • Executive Dashboard
    • Channel Performance
    • Customer Analytics
    • Inventory Insights
    • Geographic Analysis
    

Step 8: PUBLISHING & SHARING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Publish to Power BI Service
    ↓
    • Configure scheduled refresh
    • Set up row-level security
    • Share with stakeholders
    • Embed in applications
    

Step 9: MONITORING & MAINTENANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Ongoing optimization and updates
    ↓
    • Monitor refresh status
    • Track usage metrics
    • Gather feedback
    • Update reports as needed
```

---

### Power BI Connection Workflow Diagram

```
START: Open Power BI Desktop
│
├─► Step 1: Click "Get Data"
│       │
│       ├─► Select "SQL Server"
│       │
│       └─► Click "Connect"
│
├─► Step 2: Enter Connection Details
│       │
│       ├─► Server Name: RETAILSQL01\PRODUCTION
│       │
│       ├─► Database Name: RetailOmniChannel_DW
│       │
│       ├─► Choose Mode: Import / DirectQuery / Composite
│       │
│       └─► Click "OK"
│
├─► Step 3: Authentication
│       │
│       ├─► Windows Authentication (Recommended)
│       │       └─► Auto-populated credentials
│       │
│       └─► SQL Server Authentication
│               └─► Enter username/password
│
├─► Step 4: Navigator (Select Tables)
│       │
│       ├─► Expand schemas (Sales, Dimension)
│       │
│       ├─► Check boxes for required tables:
│       │       ├─ ✓ FactSales
│       │       ├─ ✓ FactInventory
│       │       ├─ ✓ FactCustomerActivity
│       │       ├─ ✓ DimCustomer
│       │       ├─ ✓ DimProduct
│       │       ├─ ✓ DimStore
│       │       ├─ ✓ DimDate
│       │       ├─ ✓ DimChannel
│       │       └─ ✓ DimPaymentMethod
│       │
│       └─► Preview data in right pane
│
├─► Step 5: Transform or Load Decision
│       │
│       ├─► Option A: Load (Direct)
│       │       └─► Skip transformations
│       │
│       └─► Option B: Transform Data ✓ (Recommended)
│               └─► Opens Power Query Editor
│
├─► Step 6: Power Query Transformations
│       │
│       ├─► Filter data (date ranges, active records)
│       │
│       ├─► Remove unnecessary columns
│       │
│       ├─► Change data types
│       │
│       ├─► Create calculated columns
│       │
│       ├─► Merge columns (FirstName + LastName)
│       │
│       ├─► Replace null values
│       │
│       └─► Verify query folding
│
├─► Step 7: Close & Apply
│       │
│       ├─► Power BI loads data
│       │
│       ├─► Compresses data (VertiPaq engine)
│       │
│       └─► Creates automatic relationships
│
├─► Step 8: Data Model Setup
│       │
│       ├─► Verify relationships
│       │
│       ├─► Create missing relationships
│       │
│       ├─► Hide technical columns
│       │
│       └─► Create DAX measures
│
├─► Step 9: Build Visualizations
│       │
│       ├─► Create report pages
│       │
│       ├─► Add charts and tables
│       │
│       └─► Configure interactivity
│
├─► Step 10: Publish to Power BI Service
│       │
│       ├─► Sign in to Power BI account
│       │
│       ├─► Select workspace
│       │
│       └─► Publish report
│
└─► Step 11: Configure Scheduled Refresh
        │
        ├─► Install Power BI Gateway (if on-premises)
        │
        ├─► Configure gateway connection
        │
        ├─► Set refresh schedule (Daily at 2:00 AM)
        │
        └─► Configure email notifications
        
END: Report ready for users
```

---

### Prerequisites & Requirements

#### SQL Server Requirements
- **SQL Server Version**: SQL Server 2012 or later (recommended: SQL Server 2019+)
- **Database Access**: Read permissions (SELECT) on required tables/views
- **Network Connectivity**: SQL Server must be accessible from Power BI Desktop/Service
- **Firewall Configuration**: Port 1433 (default) open for SQL Server connections
- **SQL Server Authentication**: Windows Authentication or SQL Server Authentication enabled

#### Power BI Requirements
- **Power BI Desktop**: Latest version installed (download from Microsoft website)
- **User Credentials**: Valid Windows account or SQL Server login credentials
- **Network Access**: VPN connection if accessing on-premises SQL Server remotely
- **Power BI Gateway**: Required for scheduled refresh in Power BI Service (for on-premises SQL Server)

#### Database Structure for Retail Project
```
Database: RetailOmniChannel_DW
├── Sales Schema
│   ├── FactSales (10M+ rows)
│   ├── FactInventory (2M+ rows)
│   ├── FactCustomerActivity (50M+ rows)
├── Dimension Schema
│   ├── DimCustomer (500K rows)
│   ├── DimProduct (25K rows)
│   ├── DimStore (350 rows)
│   ├── DimDate (3,650 rows - 10 years)
│   ├── DimChannel (4 rows)
│   └── DimPaymentMethod (6 rows)
└── Staging Schema
    ├── StagingSales
    └── StagingInventory
```

---

### Step-by-Step Connection Process

#### Step 1: Launch Power BI Desktop
1. Open **Power BI Desktop** application
2. Close the splash screen if it appears
3. You'll see the main Power BI interface with three views: Report, Data, and Model

**Note**: Ensure you're working with a blank report or create a new one (File > New)

---

#### Step 2: Access Get Data Menu
1. Click on **Home** tab in the ribbon (top menu)
2. Click **Get Data** button (located in the left section of the ribbon)
3. Alternatively, you can use keyboard shortcut: **Ctrl + Alt + D**

**Note**: The Get Data menu provides access to 100+ data sources

---

#### Step 3: Select SQL Server Data Source

**Method A: Direct Selection**
1. In the Get Data window, look for **SQL Server** in the list
2. It's usually visible in the top section under "Common data sources"
3. Click on **SQL Server** icon
4. Click **Connect** button at the bottom

**Method B: Search Method**
1. In the Get Data window, use the search box at the top
2. Type "SQL Server"
3. Select **SQL Server** from search results
4. Click **Connect**

**Important Notes**:
- Do NOT select "SQL Server Analysis Services" - that's for SSAS cubes
- For Azure SQL Database, select "Azure SQL Database" instead
- For SQL Server 2005 or earlier, you may need legacy connectors

---

#### Step 4: Enter SQL Server Connection Details

You'll see the **SQL Server Database** dialog box with the following fields:

**Server Name** (Required):
- Enter the SQL Server instance name
- Format options:
  - **Local server**: `localhost` or `(local)` or `.`
  - **Named instance**: `ServerName\InstanceName` (e.g., `SQLSERVER01\RETAIL`)
  - **Default instance**: `ServerName` (e.g., `SQLSERVER01`)
  - **IP Address**: `192.168.1.100` or `192.168.1.100\InstanceName`
  - **Full domain**: `server.company.com` or `server.company.com\InstanceName`
  - **Azure SQL**: `servername.database.windows.net`
  - **Port specification**: `ServerName,1433` (comma separates port)

**Example for our Retail Project**: 
```
RETAILSQL01\PRODUCTION
```

**Database Name** (Optional but Recommended):
- Enter the specific database name: `RetailOmniChannel_DW`
- **Why specify database?**: Improves performance and prevents loading unnecessary databases
- Leave blank to see all databases (not recommended for production)

---

#### Step 5: Configure Data Connectivity Mode

You have two primary options:

**Option 1: Import Mode** (Recommended for this project)
- **Description**: Copies data from SQL Server into Power BI's internal storage (VertiPaq engine)
- **Advantages**:
  - Fastest query performance
  - Works offline after initial load
  - Supports all Power BI features and visualizations
  - Compressed storage (10:1 compression ratio typical)
  - Best for datasets under 1GB uncompressed
  
- **Disadvantages**:
  - Data is not real-time (requires refresh)
  - Dataset size limitations (10GB in Premium, 1GB in Pro)
  - Refresh time increases with data volume

**When to Use Import**: 
- Historical analysis (daily/weekly data updates sufficient)
- Dataset size manageable (our project: ~500MB compressed)
- Need complex DAX calculations
- Want fast dashboard performance

**Option 2: DirectQuery Mode**
- **Description**: Queries SQL Server in real-time, no data stored in Power BI
- **Advantages**:
  - Always shows live data
  - No dataset size limitations
  - No data duplication
  - Security managed at SQL Server level
  
- **Disadvantages**:
  - Slower query performance (depends on SQL Server)
  - Limited DAX functions available
  - Requires constant SQL Server connectivity
  - Puts load on source database

**When to Use DirectQuery**: 
- Need real-time data (e.g., live inventory monitoring)
- Dataset too large for Import (multi-terabyte databases)
- Regulatory requirements to keep data in source system

**Option 3: Composite Mode** (Hybrid - Best for Our Project)
- **Description**: Mix of Import and DirectQuery
- **Example**: Import historical sales data, DirectQuery for current day
- **Configuration**: Set per table in Power BI Desktop

**Our Project Recommendation**:
- **Import Mode** for dimension tables (small, rarely change)
- **Import Mode** for historical fact data (>7 days old)
- **DirectQuery** for current day transactions (real-time dashboard)

**Selection**: For now, keep default **Import** selected

---

## Comparison Tables

### Table 1: Data Connectivity Mode Comparison

| **Criteria** | **Import Mode** | **DirectQuery Mode** | **Composite Mode** |
|-------------|-----------------|---------------------|-------------------|
| **Data Storage** | Stored in Power BI (.pbix file) | No data stored, queries sent to SQL Server | Mixed: Some tables Import, some DirectQuery |
| **Query Performance** | ⭐⭐⭐⭐⭐ Very Fast (milliseconds) | ⭐⭐⭐ Moderate to Slow (depends on SQL Server) | ⭐⭐⭐⭐ Fast (uses best of both) |
| **Data Freshness** | Requires manual/scheduled refresh | ⭐⭐⭐⭐⭐ Real-time (always current) | Mixed: Historical (Import) + Real-time (DirectQuery) |
| **Dataset Size Limit** | 1GB (Pro), 10GB (Premium) | No limit | No limit |
| **Offline Access** | ✓ Works offline | ✗ Requires connection | Partial (Import tables only) |
| **DAX Functions** | ⭐⭐⭐⭐⭐ All functions supported | ⭐⭐⭐ Limited functions | ⭐⭐⭐⭐ Most functions supported |
| **Compression** | 10:1 ratio typical (VertiPaq) | No compression needed | Import tables compressed |
| **SQL Server Load** | Low (one-time load or scheduled) | High (every visual interaction) | Moderate |
| **Refresh Time** | 5-30 minutes (depends on data size) | Not applicable | 2-10 minutes (only Import tables) |
| **Memory Usage** | High (all data in memory) | Low (no data cached) | Moderate |
| **Network Dependency** | Only during refresh | ✓ Always requires connection | Required for DirectQuery tables |
| **Aggregations Support** | ✓ Yes | ✗ No | ✓ Yes (Premium) |
| **Best For** | Historical analysis, complex DAX | Real-time dashboards, huge datasets | Hybrid scenarios (our project!) |
| **Our Project Usage** | Dimension tables, historical facts | Current day transactions | ✓ **RECOMMENDED** |

**Decision Matrix for Our Retail Project:**

```
Use IMPORT for:
├─ DimCustomer (rarely changes, 485K rows)
├─ DimProduct (daily updates, 25K rows)
├─ DimStore (rarely changes, 348 rows)
├─ DimDate (static, 3,652 rows)
├─ DimChannel (static, 4 rows)
├─ DimPaymentMethod (static, 6 rows)
└─ FactSales (historical: >7 days old, 3M rows)

Use DIRECTQUERY for:
├─ FactSales (current day transactions, ~5K rows/day)
└─ FactInventory (real-time stock levels, 24K rows)

Result: Composite Model = Optimal Performance + Real-time Data
```

---

### Table 2: Authentication Methods Comparison

| **Criteria** | **Windows Authentication** | **SQL Server Authentication** | **Azure AD (Microsoft Account)** |
|-------------|---------------------------|------------------------------|--------------------------------|
| **Security Level** | ⭐⭐⭐⭐⭐ Highest (Kerberos) | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ High |
| **Password Management** | Managed by Active Directory | Manual password management | Azure AD managed |
| **Single Sign-On (SSO)** | ✓ Yes | ✗ No | ✓ Yes |
| **Credential Format** | DOMAIN\Username (automatic) | Username + Password | Microsoft account email |
| **Multi-Factor Auth** | Supported via AD | Not available | ✓ Supported |
| **Best For** | On-premises corporate networks | External users, Azure SQL | Azure SQL Database |
| **Expiration Policy** | Based on AD policy (60-90 days) | Manual rotation needed | Azure AD policy |
| **Audit Trail** | Windows Event Logs | SQL Server logs | Azure AD logs |
| **Gateway Support** | ✓ Full support | ✓ Full support | ✓ Full support |
| **Power BI Service** | Requires gateway credentials | Requires stored credentials | Direct Azure AD integration |
| **Our Project** | ✓ **RECOMMENDED** (on-premises) | Backup option | Not applicable |

**Authentication Decision Tree:**

```
Is SQL Server on-premises?
    ├─ YES → Are you on corporate network?
    │         ├─ YES → Use Windows Authentication ✓ (Most Secure)
    │         └─ NO  → Use SQL Server Authentication (VPN required)
    │
    └─ NO (Azure SQL) → Use Azure AD Authentication
```

---

### Table 3: Power Query Transformation Strategy

| **Transformation Type** | **Do in SQL Server** | **Do in Power Query** | **Impact on Performance** |
|------------------------|---------------------|----------------------|--------------------------|
| **Filter Rows (WHERE)** | ✓ Recommended | Acceptable | SQL: Excellent (reduces data transfer) |
| **Remove Columns** | Not needed | ✓ Yes | Power Query: Good (reduces memory) |
| **Join Tables** | ✓ Use Views | Possible | SQL: Better (query folding) |
| **Aggregate Data** | ✓ Use Views | For small tables | SQL: Much better |
| **Change Data Types** | Best in source | ✓ Required | Power Query: Minimal impact |
| **Merge Columns** | Could do either | ✓ Easy in Power Query | Power Query: Minimal impact |
| **Pivot/Unpivot** | ✓ Complex SQL | ✓ Easy in Power Query | Depends on data size |
| **Replace Values** | Not recommended | ✓ Power Query | Power Query: Good |
| **Custom Calculations** | ✓ Computed columns | ✓ Custom columns | SQL: Better for complex logic |
| **Date Filtering** | ✓ Recommended | ✓ Both work well | SQL: Reduces data transfer |

**Best Practice for Our Retail Project:**
- **Heavy filtering** (date ranges): SQL Server via views ✓
- **Column removal**: Power Query ✓
- **Data type changes**: Power Query ✓
- **Complex joins**: SQL Server via views ✓
- **Simple transformations**: Power Query ✓

---

### Table 4: Data Source Comparison for Retail Project

| **Data Source** | **Connection Type** | **Update Frequency** | **Data Volume** | **Complexity** | **Priority** |
|----------------|-------------------|---------------------|-----------------|----------------|-------------|
| **POS System (SQL Server)** | SQL Server Native | Real-time | 10M+ rows | Low | ⭐⭐⭐⭐⭐ Critical |
| **E-commerce Platform** | REST API | Every 15 minutes | 2M rows | Medium | ⭐⭐⭐⭐⭐ Critical |
| **Mobile App Database** | SQL Server / API | Every 15 minutes | 1M rows | Medium | ⭐⭐⭐⭐ High |
| **CRM System** | ODBC / CSV Export | Daily | 500K rows | Low | ⭐⭐⭐⭐ High |
| **Inventory System** | SQL Server | Real-time | 2M rows | Low | ⭐⭐⭐⭐⭐ Critical |
| **Marketing Platforms** | API / CSV | Daily | 100K rows | High | ⭐⭐⭐ Medium |
| **Payment Gateway** | API / Export | Hourly | 500K rows | Medium | ⭐⭐⭐⭐ High |
| **Loyalty Program** | SQL Server | Daily | 200K rows | Low | ⭐⭐⭐ Medium |

**Integration Strategy:**
1. **Primary**: SQL Server Data Warehouse (consolidates all sources)
2. **Secondary**: Direct API connections for real-time validation
3. **Tertiary**: Flat files for ad-hoc analysis

---

### Table 5: Performance Optimization Comparison

| **Optimization Technique** | **Effort** | **Impact** | **When to Apply** | **Retail Project Status** |
|---------------------------|-----------|----------|------------------|-------------------------|
| **Remove Unused Columns** | Low | High | Always | ✓ Implemented (22% size reduction) |
| **Filter Historical Data** | Low | Very High | Large fact tables | ✓ Implemented (2 years only) |
| **Optimize Data Types** | Low | Medium | Always | ✓ Implemented |
| **Create SQL Indexes** | Medium | Very High | Large tables | ✓ Implemented |
| **Incremental Refresh** | Medium | Very High | Large datasets | ✓ Implemented (Premium) |
| **Enable Compression (SQL)** | Low | High | Large tables | ✓ Implemented |
| **Use Composite Models** | High | Very High | Mixed requirements | ✓ Implemented |
| **Create Aggregation Tables** | High | Very High | Complex queries | Planned (Premium feature) |
| **Disable Auto Date/Time** | Low | Medium | All projects | ✓ Implemented |
| **Query Folding Verification** | Low | High | All transformations | ✓ Verified |

**Performance Results:**

| **Metric** | **Before Optimization** | **After Optimization** | **Improvement** |
|-----------|------------------------|------------------------|-----------------|
| **Dataset Size** | 2.1 GB | 420 MB | 80% reduction |
| **Refresh Time** | 45 minutes | 5 minutes | 89% faster |
| **Report Load Time** | 12 seconds | 2 seconds | 83% faster |
| **Memory Usage** | 8 GB | 1.2 GB | 85% reduction |
| **Query Response** | 3-5 seconds | <1 second | 75% faster |

---

### Table 6: Refresh Schedule Comparison

| **Refresh Frequency** | **Power BI Pro** | **Power BI Premium** | **Best For** | **Our Project** |
|----------------------|------------------|---------------------|-------------|-----------------|
| **Manual Only** | ✓ Available | ✓ Available | Development/Testing | ✗ Not suitable |
| **Daily (1x)** | ✓ Available | ✓ Available | Static data | ✗ Not frequent enough |
| **Daily (8x)** | ✓ Available | ✓ Available | Regular updates | ✗ Not frequent enough |
| **Hourly** | ✗ Not available | ✓ Available (48x/day) | Near real-time | Possible |
| **Every 30 minutes** | ✗ Not available | ✓ Available | Near real-time | ✓ **SELECTED** |
| **Real-time (DirectQuery)** | ✓ Available | ✓ Available | Live dashboards | ✓ For current day |
| **Incremental Refresh** | ✗ Not available | ✓ Available | Large datasets | ✓ **ENABLED** |

**Our Retail Project Schedule:**

| **Table** | **Refresh Method** | **Frequency** | **Reason** |
|-----------|-------------------|---------------|-----------|
| FactSales (Historical) | Incremental Refresh | Daily at 2:00 AM | Historical data stable |
| FactSales (Current Day) | DirectQuery | Real-time | Live sales tracking |
| FactInventory | DirectQuery | Real-time | Stock level monitoring |
| FactCustomerActivity | Incremental Refresh | Every 4 hours | Recent activity tracking |
| DimCustomer | Import | Daily at 2:00 AM | Changes infrequent |
| DimProduct | Import | Daily at 2:00 AM | Daily updates (prices) |
| DimStore | Import | Weekly | Rarely changes |
| DimDate | Import | Quarterly | Pre-built dimension |
| DimChannel | Import | As needed | Static |
| DimPaymentMethod | Import | As needed | Static |

---

### Table 7: Security Configuration Comparison

| **Security Feature** | **SQL Server Level** | **Power BI Desktop** | **Power BI Service** | **Our Implementation** |
|---------------------|---------------------|---------------------|---------------------|----------------------|
| **Authentication** | Windows/SQL Auth | Uses data source creds | Gateway credentials | Windows Auth ✓ |
| **Row-Level Security (RLS)** | Database roles | DAX-based roles | Applied in service | DAX roles ✓ |
| **Column Security** | GRANT/DENY | Hide columns | Hidden in model | Hidden columns ✓ |
| **Encryption at Rest** | TDE (SQL Server) | File-level (Windows) | Azure encryption | All layers ✓ |
| **Encryption in Transit** | TLS 1.2+ | HTTPS | HTTPS | TLS 1.2+ ✓ |
| **Audit Logging** | SQL audit logs | Not available | Usage metrics | SQL + Service ✓ |
| **Multi-Factor Auth** | Via AD | Not applicable | Azure AD MFA | Enabled ✓ |
| **Data Masking** | Dynamic masking | Not available | Not available | SQL Server ✓ |

**Security Layers Implemented:**

```
Layer 1: Network Security
├─ Firewall rules (Port 1433)
├─ VPN for remote access
└─ IP whitelisting

Layer 2: Authentication
├─ Windows Authentication (Kerberos)
├─ Service account: pbi_retail_reader
└─ MFA required for Power BI Service

Layer 3: Authorization
├─ Database roles (db_datareader)
├─ Schema-level permissions
└─ View-based access (exclude sensitive columns)

Layer 4: Row-Level Security
├─ Store Managers: Own stores only
├─ Regional Managers: Own regions only
└─ Executives: All data

Layer 5: Encryption
├─ SQL Server TDE (at rest)
├─ TLS 1.2+ (in transit)
└─ Azure Key Vault (Power BI credentials)

Layer 6: Monitoring
├─ SQL audit logs
├─ Power BI usage metrics
└─ Gateway activity logs
```

---

### Table 8: Troubleshooting Quick Reference

| **Error Type** | **Symptom** | **Common Cause** | **Quick Fix** | **Time to Resolve** |
|---------------|------------|------------------|---------------|---------------------|
| **Connection Failed** | Can't connect to server | Firewall/network | Check VPN, ping server | 5-10 minutes |
| **Authentication Failed** | Login failed | Wrong credentials | Verify username/password | 2-5 minutes |
| **Timeout** | Query takes too long | Large dataset/slow network | Increase timeout, add filters | 10-30 minutes |
| **Out of Memory** | Load fails | Too much data | Filter data, remove columns | 15-45 minutes |
| **Slow Refresh** | Refresh >30 minutes | No indexes, no folding | Add SQL indexes, check folding | 1-2 hours |
| **Relationship Errors** | Visuals don't work | Missing relationships | Create in Model view | 5-10 minutes |
| **Data Type Errors** | Calculation errors | Wrong data types | Fix in Power Query | 10-20 minutes |
| **Gateway Issues** | Scheduled refresh fails | Gateway offline | Restart gateway service | 5-15 minutes |
| **Permission Denied** | Can't access table | Insufficient permissions | Grant SELECT permission | 5-10 minutes |
| **Query Folding Break** | Slow performance | Complex transformations | Simplify or use SQL views | 30-60 minutes |

---

### Table 9: Tool Selection Matrix

| **Task** | **Power Query** | **SQL Server** | **DAX** | **Best Choice** |
|---------|----------------|---------------|---------|-----------------|
| Filter rows by date | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | ⭐⭐ Possible | SQL Server (reduces data transfer) |
| Remove columns | ⭐⭐⭐⭐⭐ Best | ⭐⭐ Not needed | ⭐ Not applicable | Power Query |
| Join two tables | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | ⭐⭐ Possible | SQL Server (query folding) |
| Create calculated field | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | DAX (dynamic calculations) |
| Aggregate data | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐⭐⭐ Best | SQL for pre-agg, DAX for reports |
| Text transformation | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐ Good | ⭐⭐ Limited | Power Query (built-in functions) |
| Date manipulation | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | DAX (time intelligence) |
| Conditional logic | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Best | DAX (CALCULATE, FILTER) |
| Merge columns | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐ Good | ⭐⭐⭐ Possible | Power Query (easy interface) |
| Replace values | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐ Good | ⭐⭐ Not ideal | Power Query |

---

### Table 10: Project Comparison - Before vs After Power BI

| **Metric** | **Before Power BI** | **After Power BI** | **Improvement** |
|-----------|---------------------|-------------------|-----------------|
| **Reporting Time** | 3 days (manual Excel) | Real-time (automated) | 100% faster |
| **Data Sources** | 8 separate systems | 1 unified dashboard | Single source of truth |
| **Manual Effort** | 20 hours/week | 2 hours/week | 90% reduction |
| **Report Distribution** | Email (static PDFs) | Web/Mobile (interactive) | Self-service access |
| **Data Refresh** | Weekly (manual) | Daily/Real-time (automatic) | Always current |
| **Historical Analysis** | Last 3 months only | 2 years available | 8x more data |
| **Cross-Channel Insights** | Not available | Full visibility | New capability |
| **User Access** | 5 analysts only | 150+ stakeholders | 30x more users |
| **Decision Speed** | Days to weeks | Minutes to hours | 95% faster |
| **Data Accuracy** | 85% (manual errors) | 99%+ (automated) | 14% improvement |
| **Cost per Report** | $500 (labor) | $50 (automated) | 90% cost reduction |
| **ROI** | N/A | 450% in Year 1 | Significant value |

---

#### Step 6: Advanced Options (Optional)

Click **Advanced Options** to reveal additional settings:

**SQL Statement Box**:
- Write custom SQL query to retrieve data
- **Use Case**: Complex joins, filtering at source, calculated columns
- **Best Practice**: Use views instead of writing SQL here (easier maintenance)

**Example SQL Statement**:
```sql
SELECT 
    s.SalesID,
    s.TransactionDate,
    s.CustomerID,
    s.ProductID,
    s.Quantity,
    s.TotalAmount,
    c.CustomerName,
    c.LoyaltyTier,
    p.ProductName,
    p.Category
FROM Sales.FactSales s
INNER JOIN Dimension.DimCustomer c ON s.CustomerID = c.CustomerID
INNER JOIN Dimension.DimProduct p ON s.ProductID = p.ProductID
WHERE s.TransactionDate >= DATEADD(YEAR, -2, GETDATE())
```

**Command Timeout (minutes)**:
- Default: 10 minutes
- **Our Setting**: Increase to 30 minutes for large data loads
- Prevents timeout errors on slow networks or large datasets

**Include Relationship Columns**:
- Checked by default
- Automatically detects foreign key relationships
- **Recommendation**: Keep checked for automatic relationship detection

**Navigate Using Full Hierarchy**:
- Shows complete database structure including schemas
- **Recommendation**: Check this for better organization

**Enable SQL Server Failover Support**:
- For SQL Server Always On Availability Groups
- Automatically connects to secondary replica if primary fails
- **Our Project**: Enable if using SQL Server clustering

**Example Configuration for Retail Project**:
```
☑ Include relationship columns
☑ Navigate using full hierarchy
☐ Enable SQL Server Failover support (not applicable)
Command timeout: 30 minutes
SQL Statement: (leave blank - we'll select tables)
```

---

#### Step 7: Click OK to Connect

After entering all details, click **OK** button.

**What Happens Next**:
- Power BI attempts to connect to SQL Server
- Validates server name and database
- If successful, proceeds to authentication
- If failed, shows error message (see Troubleshooting section)

---

#### Step 8: Authentication & Credentials

You'll see the **SQL Server Database Authentication** window:

**Authentication Methods**:

**1. Windows Authentication** (Recommended for Domain Environments)
- **Description**: Uses your Windows login credentials
- **Format**: `DOMAIN\Username` (automatically populated)
- **Requirements**: 
  - Your Windows account must have SQL Server access
  - Power BI Desktop must be on same domain
  - Trusted connection to SQL Server
- **Security**: Most secure, uses Kerberos authentication
- **Use Case**: Internal corporate environment

**Selection Steps**:
1. Select **Windows** tab on the left
2. Verify your credentials are shown
3. Click **Connect**

**2. Database (SQL Server Authentication)**
- **Description**: Uses SQL Server login/password
- **Format**: Username and password created in SQL Server
- **Requirements**: 
  - SQL Server Authentication enabled
  - Valid SQL login credentials
- **Security**: Password transmitted (encrypted), but less secure than Windows auth
- **Use Case**: External users, Azure SQL, application accounts

**Example Credentials**:
```
Username: pbi_retail_reader
Password: [SecurePassword123!]
```

**Selection Steps**:
1. Select **Database** tab on the left
2. Enter **User name**: `pbi_retail_reader`
3. Enter **Password**: `[your password]`
4. Click **Connect**

**Best Practices**:
- Create dedicated read-only SQL login for Power BI
- Use strong passwords (12+ characters, mixed case, symbols)
- Grant minimum permissions (SELECT only on required tables)
- Never use SA or admin accounts
- Rotate passwords quarterly

**3. Microsoft Account**
- For Azure SQL Database with Azure AD authentication
- Not typically used for on-premises SQL Server

---

#### Step 9: Select Tables and Views

After successful authentication, you'll see the **Navigator** window:

**Navigator Interface**:
- **Left Pane**: Tree view of database objects (Tables, Views, Functions)
- **Right Pane**: Preview of selected table/view (first 1,000 rows)
- **Search Box**: Filter objects by name
- **Display Options**: Switch between table and list view

**Our Retail Project - Tables to Select**:

**Fact Tables** (Priority 1 - Must Have):
1. ☑ `Sales.FactSales` - Transaction data (10.2M rows)
2. ☑ `Sales.FactInventory` - Daily inventory snapshots (2.4M rows)
3. ☑ `Sales.FactCustomerActivity` - Web/app activity (52M rows)

**Dimension Tables** (Priority 1 - Must Have):
4. ☑ `Dimension.DimCustomer` - Customer master (485K rows)
5. ☑ `Dimension.DimProduct` - Product catalog (24,850 rows)
6. ☑ `Dimension.DimStore` - Store locations (348 rows)
7. ☑ `Dimension.DimDate` - Date dimension (3,652 rows)
8. ☑ `Dimension.DimChannel` - Sales channels (4 rows)
9. ☑ `Dimension.DimPaymentMethod` - Payment types (6 rows)

**Optional Tables** (Priority 2 - Nice to Have):
10. ☐ `Sales.FactReturns` - Product returns (125K rows)
11. ☐ `Marketing.DimCampaign` - Marketing campaigns (850 rows)
12. ☐ `Marketing.FactCampaignPerformance` - Campaign metrics (45K rows)

**Selection Process**:
1. Expand schema folders (Sales, Dimension, etc.)
2. Click checkbox next to each required table
3. Click on table name to preview data in right pane
4. Verify data looks correct (check date ranges, row counts)
5. Repeat for all tables

**Navigator Tips**:
- Use search box to quickly find tables: type "FactSales"
- Preview data to verify it's correct before loading
- Check "Select Related Tables" to auto-select related tables (foreign keys)
- Note the row count shown below preview (estimates)

---

#### Step 10: Transform or Load Decision

At the bottom of Navigator window, you have two options:

**Option 1: Load** (Direct Load)
- **Action**: Immediately loads data into Power BI
- **Use Case**: Data is clean and ready to use
- **Pros**: Fastest way to get started
- **Cons**: No data transformation opportunity
- **Recommendation**: Only for pre-cleaned data warehouse tables

**Option 2: Transform Data** (Opens Power Query Editor)
- **Action**: Opens Power Query Editor for data transformation
- **Use Case**: Need to clean, filter, or transform data
- **Pros**: Apply filters, remove columns, merge queries, data cleansing
- **Cons**: Additional step before loading
- **Recommendation**: **Always use for production projects**

**For Our Retail Project**: Click **Transform Data**

**Why Transform Data**:
- Remove unnecessary columns (reduce dataset size)
- Filter historical data (e.g., last 2 years only)
- Change data types for proper calculations
- Create custom columns (Age groups, Revenue buckets)
- Merge customer first/last name
- Clean product names and categories
- Handle null values appropriately

---

#### Step 11: Power Query Editor - Data Transformation

After clicking Transform Data, **Power Query Editor** opens:

**Interface Overview**:
- **Left Pane**: Queries list (all tables you selected)
- **Center Pane**: Data preview (first 200 rows)
- **Right Pane**: Query Settings (Applied Steps, Properties)
- **Top Ribbon**: Transformation tools (Home, Transform, Add Column, View)

**Essential Transformations for Our Project**:

**A. FactSales Table Transformations**:

1. **Filter Date Range** (Reduce data size):
   - Click dropdown on `TransactionDate` column header
   - Select **Date Filters** > **After**
   - Enter: `1/1/2022` (load 2 years of data)
   - This reduces rows from 10M to 3.5M

2. **Remove Unnecessary Columns**:
   - Right-click column headers to remove
   - Remove: `CreatedBy`, `CreatedDate`, `ModifiedBy`, `ModifiedDate`, `RowVersion`
   - **Why**: These audit columns not needed for analytics
   - **Result**: Reduces memory footprint by 15%

3. **Change Data Types** (Critical):
   - Verify `TransactionDate` is **Date** type
   - Verify `TotalAmount` is **Decimal** or **Currency**
   - Verify `Quantity` is **Whole Number**
   - **How**: Click column header icon, select type

4. **Rename Columns** (Better readability):
   - Right-click `Qty` > Rename > `Quantity`
   - Right-click `Amt` > Rename > `TotalAmount`

5. **Add Custom Columns**:
   - Click **Add Column** tab
   - Click **Custom Column**
   - Create `Revenue` column: `[Quantity] * [UnitPrice]`
   - Create `Profit` column: `[Revenue] - ([Quantity] * [UnitCost])`

**B. DimCustomer Table Transformations**:

1. **Merge Name Columns**:
   - Select `FirstName` and `LastName` columns
   - Right-click > **Merge Columns**
   - Separator: Space
   - New column name: `CustomerName`

2. **Replace Null Values**:
   - Select `Email` column
   - Right-click > **Replace Values**
   - Value to Find: `null`
   - Replace With: `unknown@email.com`

3. **Create Age Groups**:
   - Click **Add Column** > **Conditional Column**
   - Name: `AgeGroup`
   - Conditions:
     - If `Age` < 25 then "18-24"
     - If `Age` < 35 then "25-34"
     - If `Age` < 45 then "35-44"
     - If `Age` < 55 then "45-54"
     - Else "55+"

4. **Format Phone Numbers**:
   - Select `PhoneNumber` column
   - **Transform** tab > **Format** > **Clean**
   - Removes extra spaces and special characters

**C. DimProduct Table Transformations**:

1. **Title Case Product Names**:
   - Select `ProductName` column
   - **Transform** tab > **Format** > **Capitalize Each Word**

2. **Extract Brand from Product Name**:
   - **Add Column** > **Column From Examples**
   - Power BI will detect pattern
   - Example: "Nike Air Max 90" → "Nike"

3. **Remove Duplicates**:
   - Select `ProductID` column
   - Right-click > **Remove Duplicates**

**D. Apply Filters Across Multiple Tables**:

1. **Filter Out Test Data**:
   - In `FactSales`: Filter out `CustomerID` containing "TEST"
   - In `DimCustomer`: Filter out `Email` containing "test@"

2. **Filter Active Records Only**:
   - In `DimProduct`: Filter `IsActive` = TRUE
   - In `DimStore`: Filter `StoreStatus` = "Open"

**E. Optimize Data Types for Performance**:

```
Date columns → Date (not DateTime if time not needed)
Currency columns → Fixed Decimal Number
Integer IDs → Whole Number
Percentages → Percentage
Boolean flags → True/False
Text columns → Text (check for leading/trailing spaces)
```

**F. Query Folding Verification** (Critical for Performance):

1. Right-click on last step in Applied Steps
2. Check if **View Native Query** is enabled
3. If enabled: Transformations push to SQL Server (good!)
4. If disabled: Transformations in Power BI (slower)

**Transformations That Fold** (Good):
- Filtering rows
- Removing columns
- Changing data types
- Renaming columns
- Basic math operations

**Transformations That Break Folding** (Avoid if possible):
- Adding custom columns with complex M code
- Merging queries from different sources
- Using Table.Buffer()

---

#### Step 12: Close & Apply

After all transformations are complete:

1. Review each query in left pane for errors (no error icons)
2. Click **Home** tab in Power Query ribbon
3. Click **Close & Apply** button (top-left)
   - Alternative: **Close & Apply** > **Apply** (keeps editor open)

**What Happens During Load**:
- Power BI reads data from SQL Server
- Applies all Power Query transformations
- Compresses data into VertiPaq engine
- Detects relationships between tables (foreign keys)
- Calculates column statistics for optimization

**Load Progress**:
- You'll see a loading dialog with progress bar
- Shows: "Loading data to the model..."
- Duration varies: 
  - Small datasets (< 100K rows): 10-30 seconds
  - Medium datasets (1M rows): 2-5 minutes
  - Large datasets (10M+ rows): 10-30 minutes

**Our Retail Project Load Time**: Approximately 8-12 minutes for 15M+ total rows

---

### Post-Connection Configuration

#### Verify Data Load Success

1. **Check Data View**:
   - Click **Data** icon (left sidebar, second icon)
   - Verify all tables appear in Fields pane (right side)
   - Click each table to preview data
   - Check row counts match expectations

2. **Verify Table Relationships**:
   - Click **Model** icon (left sidebar, third icon)
   - You should see tables with relationship lines
   - Verify relationships are created automatically:
     - `FactSales[CustomerID]` → `DimCustomer[CustomerID]`
     - `FactSales[ProductID]` → `DimProduct[ProductID]`
     - `FactSales[StoreID]` → `DimStore[StoreID]`
     - `FactSales[DateID]` → `DimDate[DateID]`
     - `FactSales[ChannelID]` → `DimChannel[ChannelID]`

3. **Create Missing Relationships** (if needed):
   - Drag from foreign key field (FactSales) to primary key field (Dimension)
   - Set cardinality: Many to One (*:1)
   - Set cross filter direction: Single (or Both for special cases)
   - Mark relationship as Active

4. **Hide Technical Columns**:
   - In Data view, right-click columns like IDs, audit fields
   - Select **Hide** (removes from Report view, keeps in Model)
   - Hide: `DateID`, `CustomerID`, `ProductID`, `CreatedDate`, etc.

---

### Connection Settings Management

#### Modify Connection Settings Later

**Access Data Source Settings**:
1. Click **Home** tab
2. Click **Transform Data** dropdown
3. Select **Data Source Settings**

**You Can Modify**:
- Server name (point to different SQL Server)
- Database name (switch databases)
- Credentials (update password)
- Privacy levels
- Connection timeout

**Change Credentials**:
1. In Data Source Settings, select your SQL Server connection
2. Click **Edit Permissions**
3. Click **Edit** under Credentials
4. Enter new credentials
5. Click **Save**

---

### Refresh Configuration

#### Manual Refresh in Power BI Desktop

1. **Refresh All Data**:
   - Click **Home** tab > **Refresh**
   - Reloads all tables from SQL Server
   - Use when data changes in SQL Server

2. **Refresh Specific Table**:
   - Right-click table in Fields pane
   - Select **Refresh Data**

#### Scheduled Refresh in Power BI Service

**For On-Premises SQL Server**:

1. **Install Power BI Gateway**:
   - Download from Microsoft website
   - Install on server with SQL Server access
   - Sign in with Power BI account
   - Configure gateway settings

2. **Configure Gateway in Power BI Service**:
   - Publish report to Power BI Service
   - Go to dataset Settings
   - Under Gateway Connection, select your gateway
   - Enter SQL Server credentials

3. **Schedule Refresh**:
   - In dataset Settings, expand **Scheduled Refresh**
   - Toggle **Keep your data up to date** to ON
   - Select refresh frequency:
     - **Our Project**: Daily at 2:00 AM
   - Add time slots (up to 8 per day in Pro, 48 in Premium)
   - Configure failure notifications

**Refresh Schedule for Retail Project**:
```
Frequency: Daily
Time: 2:00 AM (off-peak hours)
Time Zone: Eastern Standard Time
Email notifications: Enabled
Notify on failure: Data Team Distribution List
Incremental refresh: Enabled (see below)
```

#### Incremental Refresh Setup (Large Datasets)

**Purpose**: Only refresh recent data, keep historical data cached

**Configuration**:
1. In Power BI Desktop, right-click table (e.g., FactSales)
2. Select **Incremental Refresh**
3. Configure parameters:
   - **Archive data starting**: 2 years before refresh date
   - **Incrementally refresh data starting**: 7 days before refresh date
   - **Detect data changes**: Select date column for change detection
   - **Only refresh complete days**: Check this option

**Example for FactSales**:
```
Archive Period: 730 days (2 years)
Incremental Period: 7 days
Change Detection Column: TransactionDate
Only Refresh Complete Days: Yes
```

**Benefits**:
- Reduces refresh time from 30 minutes to 2 minutes
- Lower SQL Server load
- More reliable refreshes
- Keeps historical data stable

---

### Security Best Practices

#### SQL Server Security

1. **Create Dedicated Read-Only User**:
```sql
-- Create SQL Server Login
CREATE LOGIN pbi_retail_reader WITH PASSWORD = 'SecureP@ssw0rd!2024';

-- Create Database User
USE RetailOmniChannel_DW;
CREATE USER pbi_retail_reader FOR LOGIN pbi_retail_reader;

-- Grant Read-Only Permissions
ALTER ROLE db_datareader ADD MEMBER pbi_retail_reader;

-- Grant Execute on Stored Procedures (if needed)
GRANT EXECUTE ON SCHEMA::Sales TO pbi_retail_reader;
```

2. **Limit Access to Specific Schemas**:
```sql
-- Grant SELECT only on required schemas
GRANT SELECT ON SCHEMA::Sales TO pbi_retail_reader;
GRANT SELECT ON SCHEMA::Dimension TO pbi_retail_reader;

-- DENY access to sensitive schemas
DENY SELECT ON SCHEMA::HR TO pbi_retail_reader;
DENY SELECT ON SCHEMA::Finance TO pbi_retail_reader;
```

3. **Use Views for Additional Security**:
```sql
-- Create view that excludes sensitive columns
CREATE VIEW Sales.vw_FactSales_PowerBI AS
SELECT 
    SalesID,
    TransactionDate,
    CustomerID,
    ProductID,
    StoreID,
    Quantity,
    TotalAmount
    -- Exclude: CostAmount, Margin, SupplierInfo
FROM Sales.FactSales
WHERE TransactionDate >= DATEADD(YEAR, -2, GETDATE());

-- Grant access to view, not base table
GRANT SELECT ON Sales.vw_FactSales_PowerBI TO pbi_retail_reader;
```

#### Power BI Security

1. **Row-Level Security (RLS)**:
   - Define roles in Power BI Desktop
   - Filter data based on user identity
   - Example: Regional managers see only their region

2. **Credential Encryption**:
   - Power BI encrypts stored credentials
   - Uses Azure Key Vault in Power BI Service
   - Credentials never visible in reports

3. **Privacy Levels**:
   - Set to **Organizational** for corporate SQL Server
   - Prevents data leakage between sources

---

### Performance Optimization

#### SQL Server Optimizations

1. **Create Indexed Views for Power BI**:
```sql
-- Indexed view for commonly accessed sales summary
CREATE VIEW Sales.vw_SalesSummary_Indexed
WITH SCHEMABINDING AS
SELECT 
    DateID,
    ProductID,
    StoreID,
    SUM(Quantity) AS TotalQuantity,
    SUM(TotalAmount) AS TotalRevenue,
    COUNT_BIG(*) AS TransactionCount
FROM Sales.FactSales
GROUP BY DateID, ProductID, StoreID;

-- Create clustered index
CREATE UNIQUE CLUSTERED INDEX IX_SalesSummary 
ON Sales.vw_SalesSummary_Indexed (DateID, ProductID, StoreID);
```

2. **Add Indexes on Join Columns**:
```sql
-- Index foreign keys in fact tables
CREATE NONCLUSTERED INDEX IX_FactSales_CustomerID 
ON Sales.FactSales(CustomerID) INCLUDE (TransactionDate, TotalAmount);

CREATE NONCLUSTERED INDEX IX_FactSales_ProductID 
ON Sales.FactSales(ProductID) INCLUDE (TransactionDate, Quantity);

CREATE NONCLUSTERED INDEX IX_FactSales_DateID 
ON Sales.FactSales(DateID) INCLUDE (TotalAmount);
```

3. **Enable Compression**:
```sql
-- Enable page compression on large tables
ALTER TABLE Sales.FactSales REBUILD WITH (DATA_COMPRESSION = PAGE);
ALTER TABLE Sales.FactCustomerActivity REBUILD WITH (DATA_COMPRESSION = PAGE);
```

#### Power BI Optimizations

1. **Reduce Column Count**:
   - Remove unused columns in Power Query
   - Saves memory and improves performance
   - Our project: Removed 18 unnecessary columns (22% size reduction)

2. **Optimize Data Types**:
   - Use Integer instead of Text for IDs
   - Use Date instead of DateTime when time not needed
   - Use Fixed Decimal instead of Decimal for currency

3. **Disable Auto Date/Time**:
   - File > Options > Data Load
   - Uncheck "Auto date/time"
   - Create explicit date table instead
   - Saves memory on every date column

4. **Create Aggregations** (Premium Only):
   - Build aggregated tables for common queries
   - Example: DailySalesSummary, MonthlySalesByStore
   - Power BI automatically uses aggregations when appropriate

---

### Troubleshooting Common Issues

#### Issue 1: Cannot Connect to SQL Server

**Error Message**: "A network-related or instance-specific error occurred"

**Solutions**:
1. Verify SQL Server name is correct
2. Check SQL Server is running (SQL Server Configuration Manager)
3. Verify SQL Server Browser service is running (for named instances)
4. Check firewall allows port 1433
5. Test connection using SQL Server Management Studio first
6. Verify network connectivity: `ping ServerName`
7. Check VPN connection if remote

**PowerShell Test**:
```powershell
Test-NetConnection -ComputerName RETAILSQL01 -Port 1433
```

---

#### Issue 2: Login Failed for User

**Error Message**: "Login failed for user 'Domain\Username'"

**Solutions**:
1. Verify credentials are correct
2. Check SQL Server Authentication mode (mixed mode required for SQL auth)
3. Verify user has permission on database:
   ```sql
   USE RetailOmniChannel_DW;
   EXEC sp_helpuser 'pbi_retail_reader';
   ```
4. Check if Windows account is locked or expired
5. Verify SQL Server login is not disabled

---

#### Issue 3: Timeout Expired

**Error Message**: "Timeout expired. The timeout period elapsed..."

**Solutions**:
1. Increase Command Timeout in Advanced Options (30-60 minutes)
2. Optimize SQL query (add WHERE clause to filter data)
3. Check SQL Server performance (CPU, memory, disk I/O)
4. Run queries during off-peak hours
5. Consider using views with pre-aggregated data
6. Enable incremental refresh for large tables

---

#### Issue 4: Out of Memory Error

**Error Message**: "Data load error: not enough memory to complete operation"

**Solutions**:
1. Close other applications to free memory
2. Filter data in Power Query (reduce row count)
3. Remove unnecessary columns
4. Load tables one at a time instead of all at once
5. Use 64-bit Power BI Desktop (not 32-bit)
6. Consider DirectQuery for very large tables
7. Upgrade computer RAM (minimum 16GB recommended)

---

#### Issue 5: Slow Refresh Performance

**Symptoms**: Data refresh takes too long (>30 minutes)

**Solutions**:
1. Verify query folding is working (check View Native Query)
2. Add indexes on SQL Server tables
3. Enable incremental refresh (Premium feature)
4. Filter data at source (Power Query filters)
5. Use database views instead of complex Power Query transformations
6. Schedule refresh during off-peak hours
7. Consider DirectQuery for real-time tables

**Performance Comparison**:
```
Before Optimization: 45 minutes
After Adding SQL Indexes: 28 minutes  
After Enabling Incremental Refresh: 8 minutes
After Removing Unused Columns: 5 minutes
```

---

### Connection Best Practices Summary

✅ **DO**:
- Use Windows Authentication when possible (more secure)
- Create dedicated read-only SQL accounts for Power BI
- Filter data at source (SQL Server) rather than Power BI
- Remove unnecessary columns early in Power Query
- Use database views for complex logic
- Test connection with small dataset first
- Document connection parameters and credentials (securely)
- Enable incremental refresh for large tables
- Schedule refreshes during off-peak hours
- Monitor refresh failures and investigate immediately

❌ **DON'T**:
- Use SA or admin accounts for Power BI connections
- Load entire tables without filtering (especially large fact tables)
- Store passwords in plain text
- Ignore query folding warnings
- Use complex calculations in Power Query if they can be done in SQL
- Load test/development data into production reports
- Forget to configure refresh schedules after publishing
- Ignore refresh failure notifications

---

### Documentation for Our Retail Project

#### Connection Details Document

```
PROJECT: Retail Omni-Channel Data Insights
DATABASE: RetailOmniChannel_DW
SQL SERVER: RETAILSQL01\PRODUCTION
AUTHENTICATION: Windows Authentication (Domain\Username)
SERVICE ACCOUNT: pbi_retail_reader (for scheduled refresh)

CONNECTION SETTINGS:
- Data Connectivity Mode: Import (with DirectQuery for current day)
- Command Timeout: 30 minutes
- Incremental Refresh: Enabled on FactSales, FactCustomerActivity
  - Archive Period: 2 years
  - Incremental Period: 7 days

REFRESH SCHEDULE:
- Frequency: Daily at 2:00 AM EST
- Gateway: RETAILPBIGATEWAY01
- Notification Email: dataanalytics@retailcompany.com

TABLES LOADED:
1. Sales.FactSales (3.5M rows after filtering)
2. Sales.FactInventory (2.4M rows)
3. Sales.FactCustomerActivity (52M rows)
4. Dimension.DimCustomer (485K rows)
5. Dimension.DimProduct (24,850 rows)
6. Dimension.DimStore (348 rows)
7. Dimension.DimDate (3,652 rows)
8. Dimension.DimChannel (4 rows)
9. Dimension.DimPaymentMethod (6 rows)

FILTERS APPLIED:
- FactSales: TransactionDate >= January 1, 2022
- DimProduct: IsActive = TRUE
- DimStore: StoreStatus = 'Open'

DATA SIZE:
- Uncompressed: 4.2 GB
- Compressed in Power BI: 420 MB (10:1 ratio)
- Refresh Time: 5-8 minutes

LAST UPDATED: November 11, 2024
MAINTAINED BY: Business Intelligence Team
```

---

## End-to-End Power BI Workflow

### 1. Data Source Identification & Connection

#### Data Sources
- **Point of Sale (POS) System**: In-store transaction data
- **E-commerce Platform**: Online sales data (Shopify/Magento/Custom)
- **Mobile Application**: App-based purchases and user activity
- **Customer Relationship Management (CRM)**: Customer profiles and loyalty data
- **Inventory Management System**: Stock levels, SKU details, warehouse data
- **Marketing Platforms**: Campaign data (Google Ads, Facebook Ads, Email Marketing)
- **Payment Gateway**: Transaction processing data

#### Connection Methods
- SQL Server databases for POS and inventory systems
- REST APIs for e-commerce and mobile app data
- CSV/Excel files for ad-hoc marketing data
- Azure Data Lake for historical data storage

---

### 2. Data Extraction & Preparation

#### Power Query Transformations
```
// Connect to multiple data sources
// Remove duplicate transactions
// Handle null values in customer demographics
// Standardize date formats across channels
// Create unified customer ID across platforms
// Merge product catalogs from different channels
// Clean SKU variations and naming inconsistencies
```

#### Data Quality Checks
- Validate transaction amounts (no negative values)
- Ensure date ranges are consistent
- Check for orphaned records (transactions without customer/product)
- Verify channel attribution accuracy
- Remove test transactions and internal purchases

---

### 3. Data Modeling

#### Star Schema Design

### Visual Star Schema Diagram

```
                        DimDate                         DimChannel
                     ┌────────────┐                   ┌────────────┐
                     │ DateID (PK)│                   │ChannelID PK│
                     │ Date       │                   │ChannelName │
                     │ Year       │                   │ ChannelType│
                     │ Quarter    │                   └──────┬─────┘
                     │ Month      │                          │
                     │ Week       │                          │
                     │ DayOfWeek  │                          │
                     │ IsHoliday  │                          │
                     └──────┬─────┘                          │
                            │                                │
                            │                                │
                            │                                │
    DimCustomer             │                                │              DimProduct
  ┌─────────────┐           │                                │           ┌──────────────┐
  │CustomerID PK│           │                                │           │ ProductID PK │
  │ FirstName   │           │                                │           │ ProductName  │
  │ LastName    │           │                                │           │ Category     │
  │ Email       │           │                                │           │ SubCategory  │
  │ Phone       │           │         ┌──────────────────────┤           │ Brand        │
  │ LoyaltyTier │           │         │                      │           │ SKU          │
  │ Segment     │           │         │                      │           │ UnitCost     │
  └──────┬──────┘           │         │                      │           │ MSRP         │
         │                  │         │   FactSales          │           └──────┬───────┘
         │                  │         │ ┌──────────────────┐ │                  │
         │                  └─────────┼►│ SalesID (PK)     │◄┼──────────────────┘
         │                            │ ├──────────────────┤ │
         └────────────────────────────┼►│ CustomerID (FK)  │ │
                                      │ │ ProductID (FK)   │ │
                                      │ │ StoreID (FK)     │◄┼─────────┐
                     ┌────────────────┼►│ DateID (FK)      │ │         │
                     │                │ │ ChannelID (FK)   │◄┼─────────┤
                     │                │ │ PaymentMethodID  │◄┼─────┐   │
                     │                │ ├──────────────────┤ │     │   │
                     │                │ │ Quantity         │ │     │   │
                     │                │ │ UnitPrice        │ │     │   │
                     │                │ │ DiscountAmount   │ │     │   │
                     │                │ │ TaxAmount        │ │     │   │
                     │                │ │ TotalAmount      │ │     │   │
                     │                │ └──────────────────┘ │     │   │
                     │                └──────────────────────┘     │   │
                     │                                             │   │
                     │                                             │   │
    DimStore        │                 FactInventory               │   │
  ┌─────────────┐   │              ┌──────────────────┐           │   │
  │ StoreID (PK)│───┘              │ InventoryID (PK) │           │   │
  │ StoreName   │                  ├──────────────────┤           │   │
  │ Address     │          ┌───────┤ ProductID (FK)   │           │   │
  │ City        │          │       │ StoreID (FK)     │───────────┘   │
  │ State       │          │       │ DateID (FK)      │───────────────┘
  │ Region      │          │       ├──────────────────┤
  │ StoreType   │          │       │ StockLevel       │
  │ SquareFoot  │          │       │ ReorderPoint     │
  └─────────────┘          │       │ WarehouseID      │
                           │       └──────────────────┘
                           │
                           │       FactCustomerActivity
                           │      ┌──────────────────────┐
                           │      │ ActivityID (PK)      │
                           │      ├──────────────────────┤
                           └──────┤ ProductID (FK)       │
                                  │ CustomerID (FK)      │────────┐
                                  │ DateID (FK)          │────┐   │
                                  │ ChannelID (FK)       │──┐ │   │
                                  ├──────────────────────┤  │ │   │
                                  │ SessionDuration      │  │ │   │
                                  │ PageViews            │  │ │   │
                                  │ DeviceType           │  │ │   │
                                  └──────────────────────┘  │ │   │
                                                            │ │   │
                                  DimPaymentMethod          │ │   │
                                 ┌────────────────┐         │ │   │
                                 │PaymentMethodID │─────────┘ │   │
                                 │ PaymentType    │           │   │
                                 │ (Credit Card)  │           │   │
                                 │ (Debit Card)   │           │   │
                                 │ (Digital Wallet)          │   │
                                 │ (Cash)         │           │   │
                                 └────────────────┘           │   │
                                                              │   │
         Connects to DimChannel ─────────────────────────────┘   │
         Connects to DimDate ─────────────────────────────────────┘
         Connects to DimCustomer (shown above with arrow)


LEGEND:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PK = Primary Key
FK = Foreign Key
───► = One-to-Many Relationship
Fact Tables (Center) = Contain measures and metrics
Dimension Tables (Surrounding) = Contain descriptive attributes
```

---

**Fact Tables:**
- `FactSales`: Transaction-level sales data
  - SalesID, CustomerID, ProductID, StoreID, DateID, ChannelID
  - Quantity, UnitPrice, DiscountAmount, TaxAmount, TotalAmount
  - PaymentMethodID, OrderStatusID

- `FactInventory`: Daily inventory snapshots
  - InventoryID, ProductID, StoreID, DateID
  - StockLevel, ReorderPoint, WarehouseID

- `FactCustomerActivity`: Customer touchpoints
  - ActivityID, CustomerID, DateID, ChannelID
  - SessionDuration, PageViews, DeviceType

**Dimension Tables:**
- `DimCustomer`: Customer master data
  - CustomerID, FirstName, LastName, Email, Phone
  - LoyaltyTier, RegistrationDate, Segment

- `DimProduct`: Product catalog
  - ProductID, ProductName, Category, SubCategory, Brand
  - SKU, UnitCost, MSRP, Size, Color

- `DimStore`: Store locations
  - StoreID, StoreName, Address, City, State, Region
  - StoreType, SquareFootage, OpeningDate

- `DimDate`: Date dimension
  - DateID, Date, Year, Quarter, Month, Week, DayOfWeek
  - IsHoliday, FiscalYear, FiscalQuarter

- `DimChannel`: Sales channels
  - ChannelID, ChannelName, ChannelType
  - (Online, In-Store, Mobile App, Call Center)

- `DimPaymentMethod`: Payment types
  - PaymentMethodID, PaymentType
  - (Credit Card, Debit Card, Digital Wallet, Cash)

#### Relationships
- One-to-Many from all dimension tables to fact tables
- Bi-directional filtering where needed (Customer ↔ Sales)
- Active/Inactive relationships managed for multiple date fields

---

### 4. DAX Measures & Calculated Columns

#### Key Measures

**Sales Metrics:**
```
Total Revenue = SUM(FactSales[TotalAmount])

YTD Revenue = TOTALYTD([Total Revenue], DimDate[Date])

Revenue vs LY = 
VAR CurrentRevenue = [Total Revenue]
VAR LastYearRevenue = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
RETURN CurrentRevenue - LastYearRevenue

Revenue Growth % = 
DIVIDE([Revenue vs LY], 
    CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date])), 
    0)

Average Transaction Value = DIVIDE([Total Revenue], [Transaction Count], 0)

Transaction Count = COUNTROWS(FactSales)

Units Sold = SUM(FactSales[Quantity])

Average Basket Size = DIVIDE([Units Sold], [Transaction Count], 0)
```

**Channel Performance:**
```
Online Revenue = CALCULATE([Total Revenue], DimChannel[ChannelName] = "Online")

In-Store Revenue = CALCULATE([Total Revenue], DimChannel[ChannelName] = "In-Store")

Mobile Revenue = CALCULATE([Total Revenue], DimChannel[ChannelName] = "Mobile App")

Channel Mix % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(DimChannel)),
    0
)

Cross-Channel Customers = 
CALCULATE(
    DISTINCTCOUNT(FactSales[CustomerID]),
    FILTER(
        VALUES(FactSales[CustomerID]),
        CALCULATE(DISTINCTCOUNT(DimChannel[ChannelID])) > 1
    )
)
```

**Customer Metrics:**
```
Total Customers = DISTINCTCOUNT(FactSales[CustomerID])

New Customers = 
CALCULATE(
    DISTINCTCOUNT(FactSales[CustomerID]),
    FILTER(
        FactSales,
        FactSales[DateID] = 
        CALCULATE(MIN(FactSales[DateID]), ALLEXCEPT(FactSales, FactSales[CustomerID]))
    )
)

Repeat Customer Rate = 
VAR RepeatCustomers = 
    CALCULATE(
        DISTINCTCOUNT(FactSales[CustomerID]),
        FILTER(
            VALUES(FactSales[CustomerID]),
            CALCULATE(COUNTROWS(FactSales)) > 1
        )
    )
RETURN DIVIDE(RepeatCustomers, [Total Customers], 0)

Customer Lifetime Value = 
AVERAGEX(
    VALUES(FactSales[CustomerID]),
    CALCULATE([Total Revenue])
)

Churn Rate = 
VAR InactiveCustomers = 
    CALCULATE(
        DISTINCTCOUNT(FactSales[CustomerID]),
        FILTER(
            VALUES(FactSales[CustomerID]),
            CALCULATE(MAX(FactSales[DateID])) < TODAY() - 90
        )
    )
RETURN DIVIDE(InactiveCustomers, [Total Customers], 0)
```

**Inventory Metrics:**
```
Current Stock Value = 
SUMX(
    FactInventory,
    FactInventory[StockLevel] * RELATED(DimProduct[UnitCost])
)

Stock Turnover Ratio = 
DIVIDE(
    [Total Revenue],
    [Current Stock Value],
    0
)

Out of Stock Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(FactInventory), FactInventory[StockLevel] = 0),
    COUNTROWS(FactInventory),
    0
)

Days of Inventory = 
DIVIDE(
    365,
    [Stock Turnover Ratio],
    0
)
```

**Product Performance:**
```
Top Products by Revenue = 
CALCULATE(
    [Total Revenue],
    TOPN(10, ALL(DimProduct[ProductName]), [Total Revenue], DESC)
)

Product Return Rate = 
DIVIDE(
    CALCULATE([Transaction Count], FactSales[OrderStatusID] = "Returned"),
    [Transaction Count],
    0
)

Average Margin % = 
AVERAGEX(
    FactSales,
    DIVIDE(
        FactSales[TotalAmount] - (FactSales[Quantity] * RELATED(DimProduct[UnitCost])),
        FactSales[TotalAmount],
        0
    )
)
```

---

### 5. Report Design & Visualizations

#### Page 1: Executive Dashboard
**Purpose:** High-level overview for leadership

**Visuals:**
- **KPI Cards:**
  - Total Revenue (with YTD comparison)
  - Revenue Growth %
  - Total Transactions
  - Average Transaction Value
  
- **Line Chart:** Revenue Trend by Month (current vs. last year)
- **Donut Chart:** Revenue by Channel
- **Clustered Bar Chart:** Top 10 Products by Revenue
- **Map Visual:** Revenue by Store Location
- **Gauge Chart:** YTD Target Achievement

#### Page 2: Channel Performance Analysis
**Purpose:** Deep dive into omni-channel metrics

**Visuals:**
- **Stacked Area Chart:** Revenue Trend by Channel over Time
- **Matrix Table:** Channel Performance Metrics
  - Revenue, Transactions, AOV, Conversion Rate per Channel
- **Waterfall Chart:** Channel Contribution to Total Revenue
- **Scatter Plot:** Transaction Count vs. Average Order Value by Channel
- **Tree Map:** Product Category Distribution by Channel
- **Funnel Chart:** Customer Journey across Channels

#### Page 3: Customer Analytics
**Purpose:** Customer behavior and segmentation

**Visuals:**
- **KPI Cards:**
  - Total Customers
  - New Customers
  - Repeat Customer Rate
  - Customer Lifetime Value
  
- **Cohort Analysis Matrix:** Customer Retention by Acquisition Month
- **Segmentation Chart:** Customer Distribution by Loyalty Tier
- **Line Chart:** Customer Acquisition Trend
- **Histogram:** Purchase Frequency Distribution
- **Table:** Top Customers by Lifetime Value
- **Ribbon Chart:** Customer Journey Patterns across Channels

#### Page 4: Product & Inventory Insights
**Purpose:** Product performance and inventory optimization

**Visuals:**
- **Clustered Column Chart:** Top/Bottom Products by Revenue & Margin
- **Heat Map:** Product Category Performance across Channels
- **Gauge Charts:** Inventory Turnover vs. Target
- **Table:** Slow-Moving Inventory Alert (Days > 90)
- **Scatter Plot:** Sales Volume vs. Stock Level
- **Decomposition Tree:** Product Category → Subcategory → SKU Analysis

#### Page 5: Geographic Analysis
**Purpose:** Store and regional performance

**Visuals:**
- **Filled Map:** Revenue by State/Region
- **Clustered Bar Chart:** Top Stores by Revenue
- **Matrix:** Store Performance Comparison (Revenue, Traffic, Conversion)
- **Line Chart:** Regional Trends over Time
- **Table:** Store Rankings with Key Metrics

---

### 6. Advanced Features Implementation

#### Row-Level Security (RLS)
```
// Regional Manager Access
[Region] = USERNAME()

// Store Manager Access
[StoreManager] = USERPRINCIPALNAME()
```

#### Bookmarks & Buttons
- Toggle between revenue and profit views
- Switch between daily/weekly/monthly trends
- Filter presets for quick analysis (This Week, Last Month, YTD)

#### Drill-Through Pages
- Transaction detail drill-through from any sales visual
- Customer detail page (all purchases, preferences, activity)
- Product detail page (sales history, inventory status)

#### Tooltips
- Custom tooltip for geographic maps (store details)
- Product tooltip (image, description, current stock)

#### What-If Parameters
- Price optimization scenarios
- Discount impact analysis
- Inventory level adjustments

---

### 7. Data Refresh Strategy

#### Scheduled Refresh
- **Frequency:** Daily at 2:00 AM
- **Incremental Refresh:** 
  - Historical data (> 1 year): Refresh monthly
  - Recent data (< 1 year): Refresh daily
  - Real-time data (current day): Refresh every 30 minutes using DirectQuery

#### Performance Optimization
- Aggregations for large fact tables
- Composite models (Import + DirectQuery)
- Query folding validation
- Remove unused columns in data model

---

### 8. Publishing & Distribution

#### Power BI Service Configuration
- **Workspace:** Retail Analytics Premium
- **App Creation:** Retail Omni-Channel Insights App
- **Access Control:**
  - Executives: Full app access
  - Regional Managers: RLS-filtered access
  - Store Managers: Store-specific access

#### Report Sharing
- Published dashboard URL for stakeholders
- Email subscriptions (daily/weekly summaries)
- Mobile app optimization
- Embedded reports in internal portal

---

### 9. Monitoring & Maintenance

#### Usage Metrics
- Track report views and user engagement
- Monitor query performance
- Identify slow-loading visuals

#### Continuous Improvement
- Monthly stakeholder feedback sessions
- A/B testing of dashboard layouts
- New KPI additions based on business needs
- Data quality monitoring and alerts

---

## Key Performance Indicators (KPIs)

### KPI Summary Dashboard Matrix

| **KPI Category** | **# of KPIs** | **Update Frequency** | **Target Achievement** | **Priority** | **Stakeholder** |
|-----------------|--------------|---------------------|----------------------|--------------|----------------|
| Sales Performance | 5 | Daily | 92% on target | ⭐⭐⭐⭐⭐ Critical | Executive, Finance |
| Channel-Specific | 5 | Daily | 88% on target | ⭐⭐⭐⭐⭐ Critical | Marketing, Operations |
| Customer Metrics | 6 | Weekly | 85% on target | ⭐⭐⭐⭐ High | Marketing, CRM |
| Product & Inventory | 6 | Daily | 90% on target | ⭐⭐⭐⭐⭐ Critical | Merchandising, Supply Chain |
| Operational | 4 | Daily | 87% on target | ⭐⭐⭐⭐ High | Operations |
| Marketing | 4 | Weekly | 78% on target | ⭐⭐⭐ Medium | Marketing |
| **Total** | **30** | **Mixed** | **87% Overall** | - | All Teams |

---

### Detailed KPI Comparison Table

| **KPI Name** | **Current Value** | **Target** | **Status** | **Trend** | **DAX Complexity** | **Report Page** |
|-------------|------------------|-----------|-----------|----------|-------------------|----------------|
| **Total Revenue** | $48.5M | $50M | ⚠️ 97% | ↗️ +12% YoY | Low | Executive Dashboard |
| **Revenue Growth %** | 12.3% | 15% | ⚠️ 82% | ↗️ Improving | Medium | Executive Dashboard |
| **Average Transaction Value** | $73.50 | $75.00 | ⚠️ 98% | ↗️ +5% | Low | Executive Dashboard |
| **Sales per Square Foot** | $485 | $500 | ⚠️ 97% | → Stable | Medium | Geographic Analysis |
| **Same-Store Sales Growth** | 7.2% | 8% | ⚠️ 90% | ↗️ +2% | High | Geographic Analysis |
| **Channel Revenue Mix** | 41/44/15 | 40/45/15 | ✅ On track | → As expected | Low | Channel Performance |
| **Online Conversion Rate** | 3.8% | 3.5% | ✅ 109% | ↗️ Exceeding | Medium | Channel Performance |
| **In-Store Conversion** | 23% | 25% | ⚠️ 92% | ↗️ Improving | Low | Channel Performance |
| **Mobile App Active Users** | 142K | 150K | ⚠️ 95% | ↗️ +18% | Low | Channel Performance |
| **Cross-Channel Rate** | 28% | 30% | ⚠️ 93% | ↗️ +8% | High | Customer Analytics |
| **Customer Acquisition Cost** | $42 | $45 | ✅ Better | ↘️ -12% | Medium | Customer Analytics |
| **Customer Lifetime Value** | $892 | $850 | ✅ 105% | ↗️ Exceeding | High | Customer Analytics |
| **Repeat Customer Rate** | 47% | 45% | ✅ 104% | ↗️ +5% | Medium | Customer Analytics |
| **Customer Churn Rate** | 13.5% | <15% | ✅ Better | ↘️ -3% | High | Customer Analytics |
| **Net Promoter Score** | 54 | >50 | ✅ 108% | ↗️ +6 pts | N/A (Survey) | Customer Analytics |
| **Customer Satisfaction** | 4.3 | 4.2+ | ✅ 102% | → Stable | N/A (Survey) | Customer Analytics |
| **Inventory Turnover** | 6.2x | 6x | ✅ 103% | ↗️ Improving | Medium | Inventory Insights |
| **Out-of-Stock Rate** | 2.8% | <3% | ✅ Better | ↘️ -0.5% | Low | Inventory Insights |
| **Gross Margin %** | 46.2% | 45% | ✅ 103% | ↗️ +1.2% | Low | Executive Dashboard |
| **Product Return Rate** | 4.2% | <5% | ✅ Better | ↘️ -0.8% | Low | Product Performance |
| **Sell-Through Rate** | 82% | 80% | ✅ 103% | ↗️ +4% | Medium | Inventory Insights |
| **Days Sales Inventory** | 56 days | <60 | ✅ Better | ↘️ -6 days | Medium | Inventory Insights |
| **Order Fulfillment Time** | 22 hrs | <24 hrs | ✅ Better | ↘️ -3 hrs | Low | Operations |
| **Click & Collect Rate** | 37% | 35% | ✅ 106% | ↗️ +8% | Low | Operations |
| **Ship-from-Store %** | 22% | 20% | ✅ 110% | ↗️ +5% | Medium | Operations |
| **Average Delivery Time** | 3.2 days | 3.5 days | ✅ Better | ↘️ -0.4 days | Low | Operations |
| **Marketing ROI** | 520% | 500% | ✅ 104% | ↗️ +45% | Medium | Marketing Performance |
| **Email Conversion** | 2.3% | 2.5% | ⚠️ 92% | → Stable | Low | Marketing Performance |
| **Social Engagement** | 3.1% | 3% | ✅ 103% | ↗️ +0.4% | Low | Marketing Performance |
| **Ad Click-Through Rate** | 2.4% | 2.2% | ✅ 109% | ↗️ +0.5% | Low | Marketing Performance |

**Status Legend:**
- ✅ On target or exceeding
- ⚠️ Below target but within acceptable range (>85%)
- ❌ Significantly below target (<85%)

**Trend Legend:**
- ↗️ Improving / Moving in right direction
- → Stable / Maintaining current level
- ↘️ Declining (can be good for cost metrics, bad for revenue metrics)

---

### KPI Performance Scorecard by Department

| **Department** | **Total KPIs** | **✅ On Target** | **⚠️ At Risk** | **❌ Off Track** | **Overall Score** | **Action Required** |
|---------------|--------------|-----------------|---------------|-----------------|------------------|-------------------|
| **Executive/Finance** | 5 | 3 (60%) | 2 (40%) | 0 (0%) | 🟡 87% | Monitor revenue targets |
| **Marketing** | 10 | 7 (70%) | 3 (30%) | 0 (0%) | 🟢 91% | Improve email conversion |
| **Merchandising** | 6 | 6 (100%) | 0 (0%) | 0 (0%) | 🟢 103% | Excellent performance |
| **Operations** | 4 | 4 (100%) | 0 (0%) | 0 (0%) | 🟢 105% | Excellent performance |
| **Store Management** | 5 | 3 (60%) | 2 (40%) | 0 (0%) | 🟡 92% | Focus on in-store conversion |
| **Overall Company** | 30 | 23 (77%) | 7 (23%) | 0 (0%) | 🟢 94% | Strong performance |

---

### Sales Performance KPIs

1. **Total Revenue**
   - **Definition:** Sum of all completed transactions
   - **Target:** $50M annually
   - **Frequency:** Daily monitoring

2. **Revenue Growth Rate (YoY)**
   - **Definition:** (Current Year Revenue - Prior Year Revenue) / Prior Year Revenue
   - **Target:** 15% YoY growth
   - **Frequency:** Monthly review

3. **Average Transaction Value (ATV)**
   - **Definition:** Total Revenue / Number of Transactions
   - **Target:** $75
   - **Frequency:** Daily monitoring

4. **Sales per Square Foot**
   - **Definition:** Store Revenue / Store Square Footage
   - **Target:** $500/sq ft annually
   - **Frequency:** Monthly review (in-store only)

5. **Same-Store Sales Growth**
   - **Definition:** Revenue growth for stores open > 1 year
   - **Target:** 8% annually
   - **Frequency:** Quarterly review

---

### Channel-Specific KPIs

6. **Channel Revenue Mix**
   - **Definition:** % Revenue contribution by each channel
   - **Target:** Online (40%), In-Store (45%), Mobile (15%)
   - **Frequency:** Weekly monitoring

7. **Online Conversion Rate**
   - **Definition:** (Completed Purchases / Website Visits) × 100
   - **Target:** 3.5%
   - **Frequency:** Daily monitoring

8. **In-Store Foot Traffic to Conversion**
   - **Definition:** (Transactions / Store Visitors) × 100
   - **Target:** 25%
   - **Frequency:** Daily monitoring

9. **Mobile App Active Users**
   - **Definition:** Unique users with activity in last 30 days
   - **Target:** 150,000 users
   - **Frequency:** Weekly monitoring

10. **Cross-Channel Shopping Rate**
    - **Definition:** % Customers who purchase via multiple channels
    - **Target:** 30%
    - **Frequency:** Monthly review

---

### Customer KPIs

11. **Customer Acquisition Cost (CAC)**
    - **Definition:** Total Marketing Spend / New Customers
    - **Target:** $45 per customer
    - **Frequency:** Monthly review

12. **Customer Lifetime Value (CLV)**
    - **Definition:** Average revenue per customer over lifetime
    - **Target:** $850
    - **Frequency:** Quarterly review

13. **Repeat Customer Rate**
    - **Definition:** (Customers with >1 purchase / Total Customers) × 100
    - **Target:** 45%
    - **Frequency:** Monthly review

14. **Customer Churn Rate**
    - **Definition:** % Customers with no purchase in last 90 days
    - **Target:** <15%
    - **Frequency:** Monthly review

15. **Net Promoter Score (NPS)**
    - **Definition:** % Promoters - % Detractors
    - **Target:** >50
    - **Frequency:** Quarterly survey

16. **Customer Satisfaction Score (CSAT)**
    - **Definition:** Average satisfaction rating (1-5 scale)
    - **Target:** 4.2+
    - **Frequency:** Post-transaction surveys

---

### Product & Inventory KPIs

17. **Inventory Turnover Ratio**
    - **Definition:** Cost of Goods Sold / Average Inventory Value
    - **Target:** 6x annually
    - **Frequency:** Monthly review

18. **Out-of-Stock Rate**
    - **Definition:** (SKUs Out of Stock / Total Active SKUs) × 100
    - **Target:** <3%
    - **Frequency:** Daily monitoring

19. **Gross Margin %**
    - **Definition:** (Revenue - COGS) / Revenue × 100
    - **Target:** 45%
    - **Frequency:** Weekly monitoring

20. **Product Return Rate**
    - **Definition:** (Returned Items / Total Items Sold) × 100
    - **Target:** <5%
    - **Frequency:** Weekly monitoring

21. **Sell-Through Rate**
    - **Definition:** (Units Sold / Units Received) × 100
    - **Target:** 80% within 90 days
    - **Frequency:** Monthly review

22. **Days Sales of Inventory (DSI)**
    - **Definition:** 365 / Inventory Turnover Ratio
    - **Target:** <60 days
    - **Frequency:** Monthly review

---

### Operational KPIs

23. **Order Fulfillment Time**
    - **Definition:** Average hours from order to shipment (online)
    - **Target:** <24 hours
    - **Frequency:** Daily monitoring

24. **Click & Collect Adoption Rate**
    - **Definition:** % Online orders picked up in-store
    - **Target:** 35%
    - **Frequency:** Weekly monitoring

25. **Ship-from-Store Success Rate**
    - **Definition:** % Store inventory fulfilled for online orders
    - **Target:** 20% of online orders
    - **Frequency:** Weekly monitoring

26. **Average Delivery Time**
    - **Definition:** Days from order to customer receipt
    - **Target:** 3.5 days
    - **Frequency:** Daily monitoring

---

### Marketing KPIs

27. **Marketing ROI**
    - **Definition:** (Revenue from Marketing - Marketing Cost) / Marketing Cost
    - **Target:** 500% (5:1 ratio)
    - **Frequency:** Monthly review

28. **Email Marketing Conversion Rate**
    - **Definition:** (Email-driven Purchases / Emails Sent) × 100
    - **Target:** 2.5%
    - **Frequency:** Weekly monitoring

29. **Social Media Engagement Rate**
    - **Definition:** (Likes + Comments + Shares) / Followers × 100
    - **Target:** 3%
    - **Frequency:** Weekly monitoring

30. **Paid Advertising Click-Through Rate (CTR)**
    - **Definition:** (Ad Clicks / Ad Impressions) × 100
    - **Target:** 2.2%
    - **Frequency:** Daily monitoring

---

## Business Impact

### Achievements
- **360-degree customer view:** Unified customer profiles across all channels
- **Real-time inventory visibility:** Reduced out-of-stock by 40%
- **Channel optimization:** Identified mobile app as fastest-growing channel (65% YoY)
- **Personalization:** Enabled targeted marketing based on cross-channel behavior
- **Executive decision-making:** Reduced reporting time from 3 days to real-time

### ROI Metrics
- **15% increase in revenue** attributed to data-driven promotions
- **$2.3M cost savings** from inventory optimization
- **25% improvement in customer retention** through targeted engagement
- **30% reduction in reporting hours** across analytics team

---

## Technical Stack

- **Data Sources:** SQL Server, REST APIs, Azure Data Lake, Flat Files
- **ETL/Data Prep:** Power Query, Azure Data Factory
- **Data Modeling:** Power BI Desktop, DAX
- **Visualization:** Power BI Service, Mobile App
- **Security:** Row-Level Security, Azure AD Integration
- **Refresh:** Incremental Refresh, DirectQuery for real-time data

---

## Future Enhancements

1. **Predictive Analytics:** Implement ML models for demand forecasting
2. **Customer Segmentation:** Advanced RFM analysis with clustering
3. **Dynamic Pricing:** Real-time price optimization based on demand
4. **Sentiment Analysis:** Integrate social media and review sentiment
5. **Supply Chain Integration:** End-to-end visibility from vendor to customer
6. **AI-Powered Insights:** Implement Power BI Q&A and Key Influencers

---

*Last Updated: November 2024*
