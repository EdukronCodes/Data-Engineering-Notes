# Retail Data Pipeline - Azure Data Factory with Medallion Architecture

## Overview
This project implements an end-to-end retail data pipeline using Azure Data Factory (ADF) with a medallion architecture pattern. The pipeline processes retail data from multiple sources into ADLS Gen2, applying bronze, silver, and gold layer transformations for comprehensive data analytics.

## Complete Pipeline Architecture

### End-to-End Pipeline Flow

```mermaid
graph TB
    subgraph "Data Sources"
        A1[POS Systems<br/>SQL Server]
        A2[E-commerce Platform<br/>REST API]
        A3[Inventory Management<br/>SAP HANA]
        A4[Customer Database<br/>Salesforce]
        A5[Payment Gateway<br/>Stripe API]
        A6[Loyalty Program<br/>MongoDB]
        A7[Marketing Platform<br/>HubSpot API]
        A8[Social Media<br/>Twitter/Facebook APIs]
    end
    
    subgraph "Data Ingestion Layer"
        B1[Azure Event Hubs<br/>Real-time Streaming]
        B2[Azure Data Factory<br/>Batch Processing]
        B3[Azure Functions<br/>Event Processing]
        B4[Azure Logic Apps<br/>Workflow Automation]
    end
    
    subgraph "Bronze Layer - Raw Data"
        C1[ADLS Gen2 Container<br/>bronze/pos_transactions/]
        C2[ADLS Gen2 Container<br/>bronze/ecommerce_orders/]
        C3[ADLS Gen2 Container<br/>bronze/inventory_movement/]
        C4[ADLS Gen2 Container<br/>bronze/customer_data/]
        C5[ADLS Gen2 Container<br/>bronze/payment_data/]
        C6[ADLS Gen2 Container<br/>bronze/loyalty_data/]
        C7[ADLS Gen2 Container<br/>bronze/marketing_data/]
        C8[ADLS Gen2 Container<br/>bronze/social_media_data/]
    end
    
    subgraph "Silver Layer - Cleaned Data"
        D1[Data Flow Activities<br/>Transformation Engine]
        D2[Business Rules Engine<br/>Validation Framework]
        D3[Data Quality Checks<br/>Quality Gates]
        D4[ADLS Gen2 Container<br/>silver/clean_transactions/]
        D5[ADLS Gen2 Container<br/>silver/enriched_orders/]
        D6[ADLS Gen2 Container<br/>silver/inventory_snapshot/]
        D7[ADLS Gen2 Container<br/>silver/customer_master/]
        D8[ADLS Gen2 Container<br/>silver/payment_master/]
        D9[ADLS Gen2 Container<br/>silver/loyalty_master/]
        D10[ADLS Gen2 Container<br/>silver/marketing_master/]
        D11[ADLS Gen2 Container<br/>silver/social_media_master/]
    end
    
    subgraph "Gold Layer - Analytics Ready"
        E1[Aggregation Engine<br/>Business Metrics]
        E2[KPI Calculations<br/>Performance Metrics]
        E3[ADLS Gen2 Container<br/>gold/daily_sales_summary/]
        E4[ADLS Gen2 Container<br/>gold/customer_segments/]
        E5[ADLS Gen2 Container<br/>gold/product_performance/]
        E6[ADLS Gen2 Container<br/>gold/inventory_alerts/]
        E7[ADLS Gen2 Container<br/>gold/financial_summary/]
        E8[ADLS Gen2 Container<br/>gold/marketing_performance/]
        E9[ADLS Gen2 Container<br/>gold/social_media_analytics/]
    end
    
    subgraph "Consumption Layer"
        F1[Power BI Dashboards<br/>Executive Reporting]
        F2[Azure Synapse Analytics<br/>Data Warehouse]
        F3[Real-time APIs<br/>Application Integration]
        F4[Machine Learning Models<br/>Predictive Analytics]
        F5[Business Applications<br/>CRM, ERP Integration]
    end
    
    subgraph "Security & Governance"
        G1[Azure Key Vault<br/>Secrets Management]
        G2[Azure Active Directory<br/>RBAC & Authentication]
        G3[Azure Monitor<br/>Pipeline Health]
        G4[Log Analytics<br/>Audit Logs]
        G5[Data Quality Metrics<br/>SLA Monitoring]
        G6[Cost Optimization<br/>Resource Management]
    end
    
    %% Data Flow Connections
    A1 --> B2
    A2 --> B1
    A3 --> B2
    A4 --> B2
    A5 --> B1
    A6 --> B2
    A7 --> B4
    A8 --> B1
    
    B1 --> C1
    B1 --> C2
    B1 --> C5
    B1 --> C8
    B2 --> C1
    B2 --> C3
    B2 --> C4
    B2 --> C6
    B3 --> C2
    B4 --> C7
    
    C1 --> D1
    C2 --> D1
    C3 --> D1
    C4 --> D1
    C5 --> D1
    C6 --> D1
    C7 --> D1
    C8 --> D1
    
    D1 --> D2
    D2 --> D3
    D3 --> D4
    D3 --> D5
    D3 --> D6
    D3 --> D7
    D3 --> D8
    D3 --> D9
    D3 --> D10
    D3 --> D11
    
    D4 --> E1
    D5 --> E1
    D6 --> E1
    D7 --> E1
    D8 --> E1
    D9 --> E1
    D10 --> E1
    D11 --> E1
    
    E1 --> E2
    E2 --> E3
    E2 --> E4
    E2 --> E5
    E2 --> E6
    E2 --> E7
    E2 --> E8
    E2 --> E9
    
    E3 --> F1
    E4 --> F1
    E5 --> F1
    E6 --> F1
    E7 --> F1
    E8 --> F1
    E9 --> F1
    
    E3 --> F2
    E4 --> F2
    E5 --> F2
    E6 --> F2
    E7 --> F2
    E8 --> F2
    E9 --> F2
    
    E3 --> F3
    E4 --> F3
    E5 --> F3
    E6 --> F3
    
    E3 --> F4
    E4 --> F4
    E5 --> F4
    E6 --> F4
    
    E3 --> F5
    E4 --> F5
    E5 --> F5
    E6 --> F5
    
    %% Security Connections
    B1 --> G1
    B2 --> G1
    B3 --> G1
    B4 --> G1
    
    B1 --> G2
    B2 --> G2
    B3 --> G2
    B4 --> G2
    
    D1 --> G3
    E1 --> G3
    D2 --> G4
    E2 --> G4
    D3 --> G5
    E2 --> G5
    G3 --> G6
    G4 --> G6
    G5 --> G6
```

### Detailed Pipeline Processing Flow

```mermaid
sequenceDiagram
    participant Sources as Data Sources
    participant ADF as Azure Data Factory
    participant Bronze as Bronze Layer
    participant Silver as Silver Layer
    participant Gold as Gold Layer
    participant Monitor as Azure Monitor
    participant KV as Key Vault
    
    Note over Sources, KV: Daily Pipeline Execution
    
    Sources->>ADF: 1. Data Available Event
    ADF->>KV: 2. Get Connection Secrets
    KV-->>ADF: 3. Return Secrets
    
    Note over ADF, Bronze: Bronze Layer Processing
    ADF->>Bronze: 4. Ingest Raw Data
    Bronze->>Bronze: 5. Basic Validation
    Bronze->>Monitor: 6. Log Ingestion Metrics
    
    Note over Bronze, Silver: Silver Layer Processing
    Bronze->>Silver: 7. Trigger Transformation
    Silver->>Silver: 8. Apply Business Rules
    Silver->>Silver: 9. Data Quality Checks
    Silver->>Monitor: 10. Log Quality Metrics
    
    Note over Silver, Gold: Gold Layer Processing
    Silver->>Gold: 11. Trigger Aggregation
    Gold->>Gold: 12. Calculate KPIs
    Gold->>Gold: 13. Generate Analytics
    Gold->>Monitor: 14. Log Performance Metrics
    
    Note over Monitor: Monitoring & Alerting
    Monitor->>Monitor: 15. Evaluate SLAs
    Monitor->>Monitor: 16. Check Data Quality
    Monitor->>Monitor: 17. Send Alerts if Needed
```

## Data Sources and Metadata

### 1. POS Systems - SQL Server

**Source Configuration**:
```json
{
  "source_system": "POS_SQL_SERVER",
  "database_name": "RetailPOS",
  "connection_type": "SQL Server",
  "authentication": "SQL Authentication via Key Vault",
  "data_center": "Primary DC - East US",
  "sla_availability": "99.9%",
  "processing_frequency": "Hourly batch",
  "daily_volume": "50M transactions/day",
  "data_size": "2GB/day per store"
}
```

**Entity Relationship Diagram**:

```mermaid
erDiagram
    STORES ||--o{ TRANSACTIONS : has
    STORES ||--o{ INVENTORY : contains
    PRODUCTS ||--o{ TRANSACTION_ITEMS : sold_in
    TRANSACTIONS ||--o{ TRANSACTION_ITEMS : contains
    TRANSACTIONS ||--|| PAYMENTS : processed_with
    CUSTOMERS ||--o{ TRANSACTIONS : makes
    EMPLOYEES ||--o{ TRANSACTIONS : processes
    
    STORES {
        int store_id PK
        string store_code UK
        string store_name
        string address_line1
        string city
        string state
        string postal_code
        string country
        decimal latitude
        decimal longitude
        string phone_number
        string email
        string manager_name
        datetime opening_date
        string status
    }
    
    PRODUCTS {
        int product_id PK
        string sku UK
        string product_name
        string description
        int category_id FK
        decimal unit_price
        decimal cost_price
        decimal margin_percentage
        int min_stock_level
        int max_stock_level
        string status
    }
    
    TRANSACTIONS {
        bigint transaction_id PK
        int store_id FK
        int customer_id FK
        int employee_id FK
        datetime transaction_date
        string transaction_type
        decimal subtotal
        decimal tax_amount
        decimal discount_amount
        decimal total_amount
        string payment_method
        string currency_code
        string receipt_number
        string status
    }
    
    TRANSACTION_ITEMS {
        bigint transaction_item_id PK
        bigint transaction_id FK
        int product_id FK
        int quantity
        decimal unit_price
        decimal total_price
        decimal discount_amount
        decimal tax_amount
    }
    
    CUSTOMERS {
        int customer_id PK
        string customer_code UK
        string first_name
        string last_name
        string email
        string phone_number
        date date_of_birth
        string gender
        string loyalty_member_id
        int loyalty_tier
        decimal loyalty_points
        string status
    }
```

### 2. E-commerce Platform - REST API

**Real-time Processing Architecture**:

```mermaid
graph LR
    A[E-commerce API] --> B[Azure Event Hubs]
    B --> C[Azure Stream Analytics]
    C --> D[Azure Functions]
    D --> E[ADLS Gen2 Bronze]
    E --> F[15-minute Batch Processing]
    F --> G[Silver Layer]
    
    subgraph "Streaming Components"
        B
        C
        D
    end
    
    subgraph "Batch Components"
        E
        F
        G
    end
```

**API Data Model**:

```mermaid
erDiagram
    ORDERS ||--o{ ORDER_ITEMS : contains
    ORDERS ||--|| CUSTOMERS : placed_by
    ORDERS ||--|| SHIPPING_ADDRESS : ships_to
    ORDERS ||--|| BILLING_ADDRESS : billed_to
    ORDERS ||--o{ PAYMENT_METHODS : paid_with
    ORDERS ||--o{ ORDER_STATUS_HISTORY : tracked_by
    
    ORDERS {
        string order_id PK
        string customer_id FK
        datetime order_date
        string order_status
        decimal subtotal
        decimal shipping_cost
        decimal tax_amount
        decimal discount_amount
        decimal total_amount
        string currency_code
        string payment_status
        string shipping_status
        datetime estimated_delivery
        datetime actual_delivery
        string tracking_number
        string source_channel
        string campaign_id
    }
    
    ORDER_ITEMS {
        string order_item_id PK
        string order_id FK
        string product_id FK
        string sku
        string product_name
        int quantity
        decimal unit_price
        decimal total_price
        decimal discount_amount
        string size
        string color
    }
    
    CUSTOMERS {
        string customer_id PK
        string email UK
        string first_name
        string last_name
        string phone_number
        date date_of_birth
        string gender
        string customer_segment
        string acquisition_channel
        datetime first_purchase_date
        datetime last_purchase_date
        decimal lifetime_value
        int total_orders
        string status
    }
```

## Folder Structure

### Bronze Layer Structure
```
adls-gen2-container/
├── bronze/
│   ├── pos_transactions/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── hour=00/
│   │   │   │   │   │   ├── pos_transactions_20240115_000000.parquet
│   │   │   │   │   │   ├── pos_transactions_20240115_000000_metadata.json
│   │   │   │   │   │   └── pos_transactions_20240115_000000_checksum.md5
│   │   │   │   │   ├── hour=01/
│   │   │   │   │   └── hour=23/
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   ├── _metadata/
│   │   │   ├── schema_evolution_log.json
│   │   │   ├── data_quality_reports/
│   │   │   └── ingestion_logs/
│   │   └── _temp/
│   ├── ecommerce_orders/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── hour=00/
│   │   │   │   │   │   ├── minute=00/
│   │   │   │   │   │   │   ├── orders_20240115_000000.json.gz
│   │   │   │   │   │   │   └── orders_20240115_000000_metadata.json
│   │   │   │   │   │   ├── minute=15/
│   │   │   │   │   │   ├── minute=30/
│   │   │   │   │   │   └── minute=45/
│   │   │   │   │   ├── hour=01/
│   │   │   │   │   └── hour=23/
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   ├── _metadata/
│   │   └── _temp/
│   ├── inventory_movement/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── inventory_movement_20240115.parquet
│   │   │   │   │   └── inventory_movement_20240115_metadata.json
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   ├── _metadata/
│   │   └── _temp/
│   └── customer_data/
│       ├── year=2024/
│       │   ├── month=01/
│       │   │   ├── day=15/
│       │   │   │   ├── customer_data_20240115_delta.parquet
│       │   │   │   └── customer_data_20240115_metadata.json
│       │   │   │   ├── day=16/
│       │   │   │   └── day=31/
│       │   │   ├── month=02/
│       │   │   └── month=12/
│       │   │   └── year=2023/
│       ├── _metadata/
│       └── _temp/
```

### Silver Layer Structure
```
adls-gen2-container/
├── silver/
│   ├── clean_transactions/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── clean_transactions_20240115.parquet
│   │   │   │   │   ├── clean_transactions_20240115_quality_report.json
│   │   │   │   │   └── clean_transactions_20240115_audit_log.json
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   │   └── year=2023/
│   │   ├── _metadata/
│   │   │   ├── schema_version.json
│   │   │   ├── business_rules_applied.json
│   │   │   ├── data_quality_metrics/
│   │   │   └── transformation_logs/
│   │   └── _temp/
│   ├── enriched_orders/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── enriched_orders_20240115.parquet
│   │   │   │   │   ├── enriched_orders_20240115_quality_report.json
│   │   │   │   │   └── enriched_orders_20240115_audit_log.json
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   │   └── year=2023/
│   │   ├── _metadata/
│   │   └── _temp/
│   ├── inventory_snapshot/
│   ├── customer_master/
│   ├── payment_master/
│   ├── loyalty_master/
│   ├── marketing_master/
│   └── social_media_master/
```

### Gold Layer Structure
```
adls-gen2-container/
├── gold/
│   ├── daily_sales_summary/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── daily_sales_summary_20240115.parquet
│   │   │   │   │   ├── daily_sales_summary_20240115_kpi_report.json
│   │   │   │   │   └── daily_sales_summary_20240115_audit_log.json
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   │   └── year=2023/
│   │   ├── _metadata/
│   │   │   ├── kpi_definitions.json
│   │   │   ├── aggregation_rules.json
│   │   │   ├── business_metrics/
│   │   │   └── performance_logs/
│   │   └── _temp/
│   ├── customer_segments/
│   │   ├── year=2024/
│   │   │   ├── month=01/
│   │   │   │   ├── day=15/
│   │   │   │   │   ├── customer_segments_20240115.parquet
│   │   │   │   │   ├── customer_segments_20240115_segmentation_report.json
│   │   │   │   │   └── customer_segments_20240115_audit_log.json
│   │   │   │   ├── day=16/
│   │   │   │   └── day=31/
│   │   │   ├── month=02/
│   │   │   └── month=12/
│   │   │   └── year=2023/
│   │   ├── _metadata/
│   │   │   ├── segmentation_rules.json
│   │   │   ├── rfm_parameters.json
│   │   │   ├── customer_analytics/
│   │   │   └── performance_logs/
│   │   └── _temp/
│   ├── product_performance/
│   ├── inventory_alerts/
│   ├── financial_summary/
│   ├── marketing_performance/
│   └── social_media_analytics/
```

## Pipeline Components

### 1. Master Orchestration Pipeline

```mermaid
flowchart TD
    A[Start Pipeline] --> B{System Health Check}
    B -->|Healthy| C[Execute Bronze Ingestion]
    B -->|Unhealthy| Z[Send Alert & Stop]
    
    C --> D{Bronze Data Validation}
    D -->|Pass| E[Execute Silver Transformation]
    D -->|Fail| Y[Log Error & Retry]
    
    E --> F{Silver Data Validation}
    F -->|Pass| G[Execute Gold Aggregation]
    F -->|Fail| X[Log Error & Retry]
    
    G --> H{Gold Data Validation}
    H -->|Pass| I[Send Success Notification]
    H -->|Fail| W[Log Error & Retry]
    
    I --> J[Update Monitoring Dashboard]
    J --> K[End Pipeline]
    
    Y --> C
    X --> E
    W --> G
```

### 2. Bronze Layer Ingestion Pipeline

```mermaid
flowchart LR
    subgraph "Data Sources"
        A1[POS SQL Server]
        A2[E-commerce API]
        A3[SAP HANA]
        A4[Salesforce]
    end
    
    subgraph "Ingestion Process"
        B1[Copy Data Activity]
        B2[Data Quality Checks]
        B3[Metadata Capture]
        B4[Partitioning]
    end
    
    subgraph "Bronze Storage"
        C1[pos_transactions/]
        C2[ecommerce_orders/]
        C3[inventory_movement/]
        C4[customer_data/]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> B2
    B2 --> B3
    B3 --> B4
    
    B4 --> C1
    B4 --> C2
    B4 --> C3
    B4 --> C4
```

### 3. Silver Layer Transformation Pipeline

```mermaid
flowchart TD
    subgraph "Bronze Input"
        A1[Raw Transactions]
        A2[Raw Orders]
        A3[Raw Inventory]
        A4[Raw Customers]
    end
    
    subgraph "Transformation Engine"
        B1[Data Flow Activity]
        B2[Business Rules Engine]
        B3[Data Quality Framework]
        B4[Data Enrichment]
    end
    
    subgraph "Silver Output"
        C1[Clean Transactions]
        C2[Enriched Orders]
        C3[Inventory Snapshot]
        C4[Customer Master]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> B2
    B2 --> B3
    B3 --> B4
    
    B4 --> C1
    B4 --> C2
    B4 --> C3
    B4 --> C4
```

### 4. Gold Layer Aggregation Pipeline

```mermaid
flowchart TD
    subgraph "Silver Input"
        A1[Clean Transactions]
        A2[Enriched Orders]
        A3[Inventory Snapshot]
        A4[Customer Master]
    end
    
    subgraph "Aggregation Engine"
        B1[Daily Sales Summary]
        B2[Customer Segmentation]
        B3[Product Performance]
        B4[Inventory Alerts]
        B5[Financial Summary]
        B6[Marketing Performance]
    end
    
    subgraph "Gold Output"
        C1[Business KPIs]
        C2[Analytics Datasets]
        C3[Executive Dashboards]
    end
    
    A1 --> B1
    A1 --> B2
    A2 --> B1
    A2 --> B2
    A3 --> B3
    A3 --> B4
    A4 --> B2
    A4 --> B5
    A1 --> B5
    A2 --> B6
    
    B1 --> C1
    B2 --> C1
    B3 --> C1
    B4 --> C1
    B5 --> C1
    B6 --> C1
    
    B1 --> C2
    B2 --> C2
    B3 --> C2
    B4 --> C2
    B5 --> C2
    B6 --> C2
    
    C1 --> C3
    C2 --> C3
```

## Business Rules and Transformations

### Data Quality Rules
```json
{
  "data_quality_framework": {
    "bronze_validation": {
      "pos_transactions": {
        "required_fields": ["transaction_id", "store_id", "product_code", "amount"],
        "data_types": {
          "transaction_id": "bigint",
          "store_id": "int",
          "amount": "decimal(18,2)",
          "transaction_date": "datetime"
        },
        "business_rules": {
          "amount_validation": {
            "min_amount": 0.01,
            "max_amount": 10000.00
          },
          "store_validation": {
            "valid_stores": ["STORE001", "STORE002", "STORE003", "STORE004", "STORE005"]
          }
        },
        "completeness_threshold": 95.0,
        "accuracy_threshold": 98.0
      }
    },
    "silver_validation": {
      "completeness_threshold": 98.0,
      "accuracy_threshold": 99.0,
      "consistency_threshold": 99.5
    },
    "gold_validation": {
      "completeness_threshold": 99.0,
      "accuracy_threshold": 99.5,
      "consistency_threshold": 99.8
    }
  }
}
```

### Customer Segmentation Rules
```json
{
  "customer_segmentation": {
    "rfm_analysis": {
      "recency_parameters": {
        "r1_high": 30,
        "r2_medium": 90,
        "r3_low": 180,
        "r4_very_low": 365
      },
      "frequency_parameters": {
        "f1_high": 12,
        "f2_medium": 6,
        "f3_low": 3,
        "f4_very_low": 1
      },
      "monetary_parameters": {
        "m1_high": 1000.00,
        "m2_medium": 500.00,
        "m3_low": 200.00,
        "m4_very_low": 50.00
      },
      "segmentation_matrix": {
        "champions": {"r": [1, 2], "f": [1, 2], "m": [1, 2]},
        "loyal_customers": {"r": [1, 2], "f": [1, 2, 3], "m": [1, 2]},
        "potential_loyalists": {"r": [1, 2], "f": [1, 2], "m": [3, 4]},
        "new_customers": {"r": [1], "f": [1], "m": [1, 2, 3, 4]},
        "at_risk": {"r": [3, 4], "f": [1, 2, 3], "m": [1, 2]},
        "hibernating": {"r": [4], "f": [1, 2, 3, 4], "m": [1, 2, 3, 4]},
        "lost": {"r": [4], "f": [4], "m": [4]}
      }
    }
  }
}
```

## Security and Access Control

### Role-Based Access Control (RBAC)

```mermaid
graph TB
    subgraph "User Roles"
        A1[Data Engineer]
        A2[Data Analyst]
        A3[Business User]
        A4[Data Steward]
    end
    
    subgraph "Permissions"
        B1[Full Pipeline Access]
        B2[Read-Only Data Access]
        B3[Dashboard Access Only]
        B4[Quality Management]
    end
    
    subgraph "Data Classification"
        C1[Public Data]
        C2[Internal Data]
        C3[Confidential Data]
        C4[Restricted Data]
    end
    
    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    
    B1 --> C1
    B1 --> C2
    B1 --> C3
    B1 --> C4
    
    B2 --> C1
    B2 --> C2
    B2 --> C3
    
    B3 --> C1
    B3 --> C2
    
    B4 --> C1
    B4 --> C2
    B4 --> C3
    B4 --> C4
```

### Azure Key Vault Integration

```mermaid
graph LR
    subgraph "Key Vault Secrets"
        A1[Database Connections]
        A2[API Keys]
        A3[Encryption Keys]
        A4[Certificates]
    end
    
    subgraph "Azure Services"
        B1[Data Factory]
        B2[Functions]
        B3[Logic Apps]
        B4[Stream Analytics]
    end
    
    subgraph "Access Control"
        C1[Managed Identity]
        C2[Service Principal]
        C3[RBAC Policies]
    end
    
    A1 --> B1
    A2 --> B1
    A2 --> B2
    A2 --> B3
    A3 --> B1
    A4 --> B1
    
    C1 --> B1
    C2 --> B2
    C3 --> B1
    C3 --> B2
    C3 --> B3
    C3 --> B4
```

## Monitoring and Alerting

### Pipeline Monitoring Dashboard

```mermaid
graph TB
    subgraph "Pipeline Health"
        A1[Success Rate: 99.5%]
        A2[Execution Time: 2.5 hrs]
        A3[Data Volume: 50M records]
        A4[Cost: $1,250/day]
    end
    
    subgraph "Data Quality"
        B1[Completeness: 98.5%]
        B2[Accuracy: 99.2%]
        B3[Consistency: 99.8%]
        B4[Timeliness: 99.9%]
    end
    
    subgraph "Business Metrics"
        C1[Daily Revenue: $2.5M]
        C2[Customer Count: 2.1M]
        C3[Inventory Turns: 6.2]
        C4[Order Fulfillment: 98.7%]
    end
    
    subgraph "Alerts"
        D1[Pipeline Failures]
        D2[Quality Threshold Breach]
        D3[SLA Violations]
        D4[Cost Anomalies]
    end
    
    A1 --> D1
    B1 --> D2
    A2 --> D3
    A4 --> D4
```

## Deployment and Configuration

### Infrastructure Setup
```bash
# Deploy Azure resources
az group create --name rg-retail-data-pipeline --location "East US"

# Deploy Data Factory
az datafactory create --resource-group rg-retail-data-pipeline --name adf-retail-pipeline --location "East US"

# Deploy Storage Account
az storage account create --resource-group rg-retail-data-pipeline --name retaildatalakestg --location "East US" --sku Standard_LRS

# Deploy Key Vault
az keyvault create --resource-group rg-retail-data-pipeline --name retail-data-pipeline-kv --location "East US"
```

### Pipeline Configuration
```json
{
  "pipeline_configuration": {
    "master_orchestration": {
      "name": "99-master-orchestration",
      "schedule": "daily at 6:00 AM EST",
      "timeout": "8 hours",
      "retry_policy": {
        "max_retries": 3,
        "retry_interval": "30 minutes"
      }
    },
    "bronze_ingestion": {
      "name": "01-bronze-ingestion",
      "schedule": "hourly",
      "parallel_execution": true,
      "data_sources": ["pos", "ecommerce", "inventory", "customer"]
    },
    "silver_transformation": {
      "name": "02-silver-transformation",
      "schedule": "after bronze completion",
      "data_flows": ["pos_cleaning", "order_enrichment", "inventory_processing", "customer_master"]
    },
    "gold_aggregation": {
      "name": "03-gold-aggregation",
      "schedule": "after silver completion",
      "aggregations": ["daily_sales", "customer_segments", "product_performance", "inventory_alerts"]
    }
  }
}
```

## Business Value and KPIs

### Key Performance Indicators

```mermaid
graph LR
    subgraph "Financial KPIs"
        A1[Daily Revenue: $2.5M]
        A2[Revenue Growth: +15% YoY]
        A3[Average Order Value: $85]
        A4[Customer Lifetime Value: $1,250]
    end
    
    subgraph "Operational KPIs"
        B1[Order Fulfillment Rate: 98.7%]
        B2[Inventory Turnover: 6.2]
        B3[Data Processing SLA: 99.9%]
        B4[System Uptime: 99.95%]
    end
    
    subgraph "Customer KPIs"
        C1[Customer Retention: 78%]
        C2[Net Promoter Score: 8.2]
        C3[Customer Acquisition Cost: $45]
        C4[Churn Rate: 5.2%]
    end
    
    subgraph "Data Quality KPIs"
        D1[Data Completeness: 98.5%]
        D2[Data Accuracy: 99.2%]
        D3[Processing Time: 2.5 hours]
        D4[Cost per Transaction: $0.025]
    end
```

## Troubleshooting and Support

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Pipeline Timeout | Large data volume | Increase timeout, optimize queries |
| Data Quality Failure | Source system changes | Update validation rules |
| Connection Failures | Network issues | Check firewall, retry logic |
| Cost Spike | Resource over-provisioning | Right-size compute resources |

### Support Contacts
- **Data Engineering Team**: data-eng@company.com
- **Infrastructure Team**: infra@company.com
- **Business Analysts**: analytics@company.com
- **Emergency Support**: +1-800-DATA-HELP

## Version History
- **v1.0**: Initial implementation with basic bronze/silver/gold layers
- **v1.1**: Added monitoring and alerting capabilities
- **v1.2**: Enhanced data quality framework
- **v2.0**: Performance optimizations and cost improvements
- **v2.1**: Added real-time streaming capabilities
- **v2.2**: Enhanced security and compliance features

## License
This project is proprietary and confidential. All rights reserved.

---

*Last Updated: January 15, 2024*
*Document Version: 2.2*
