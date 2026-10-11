# Full project flow diagram atlas

This Markdown document collects the six full data-flow diagrams. Open each detailed project document for its complete runtime sequence, business transformation, lifecycle, recovery, security and deployment diagrams, plus stage explanations and worked examples. All architectures remain proposed reference designs until verified against actual experience.

Mermaid-capable Markdown viewers render the diagrams. Text architecture flows remain available in each project file for viewers without Mermaid support.

## Citi Bank (EMEA): Enterprise Banking Data Analytics Platform on Microsoft Fabric

```mermaid
flowchart TD
  subgraph Sources[Approved EMEA source deliveries]
    A[Core banking transaction lines]
    B[Customer and account master]
    C[Balance snapshots and ledger totals]
    D[Product branch and dated FX reference]
  end
  A --> E[Supported source connection or gateway]
  B --> E
  C --> E
  D --> E
  E --> F[Fabric Data Factory pipeline]
  F --> G[Immutable landing files and delivery manifest]
  G --> H[OneLake bronze Delta tables]
  H --> I[Fabric Spark validation and source-key deduplication]
  I --> J{Critical source controls pass?}
  J -->|No| Q[Restricted quarantine and held run]
  J -->|Yes| K[Silver transactions and effective-dated dimensions]
  K --> L[Historical account lookup and dated FX conversion]
  L --> M[Gold transaction facts and daily balance snapshots]
  M --> N{Currency and ledger reconciliation passes?}
  N -->|No| Q
  N -->|Yes| O[Release accepted publication]
  O --> P[Power BI semantic model]
  O --> R[SQL analytics endpoint for approved queries]
  P --> S[Regional banking analytics consumers]
  Q --> T[Owner investigation and replay from landing]
  T --> I
```

[Open the full project flow and technical explanation](projects/01_citi_fabric_banking_analytics.md).

## Barclays (RFT-UKC Gen3): Azure Data Lake Modernization

```mermaid
flowchart TD
  A[Legacy warehouse tables and historical files] --> B[Inventory and approved migration mappings]
  B --> C[Consistent snapshot and change boundary]
  C --> D[ADF historical backfill by bounded chunk]
  C --> E[ADF source CDC or approved incremental ingestion]
  D --> F[ADLS immutable landing with chunk manifests]
  E --> F
  F --> G[Databricks bronze Delta]
  G --> H[Silver normalized types keys and history]
  H --> I[Gold finance and risk datasets]
  I --> J[Azure candidate outputs]
  A --> K[Legacy comparison outputs]
  K --> L{Parallel reconciliation passes?}
  J --> L
  L -->|No| M[Difference analysis and rule correction]
  M --> H
  L -->|Yes| N[Cutover readiness and backlog check]
  N --> O[Approved consumer switch]
  O --> P[Databricks SQL and Power BI]
  O --> Q[Rollback observation period]
  Q --> R[Approved retirement of legacy jobs]
```

[Open the full project flow and technical explanation](projects/02_barclays_rft_ukc_gen3_modernization.md).

## BNP Paribas: Enterprise Datahub and Data Integration Platform

```mermaid
flowchart TD
  A[Relational databases] --> E[ADF metadata-driven extraction]
  B[Files and reference deliveries] --> E
  C[Approved paginated APIs] --> E
  D[Business event producers] --> F[Azure Event Hubs]
  F --> G[Databricks checkpointed ingestion]
  E --> H[ADLS raw landing and manifests]
  G --> I[Bronze Delta event records]
  H --> I
  I --> J[Contract validation and domain standardization]
  J --> K{Schema and critical controls pass?}
  K -->|No| L[Quarantine and source owner workflow]
  K -->|Yes| M[Silver customer account and payment domains]
  M --> N[Identity crosswalk and effective reference joins]
  N --> O[Gold versioned data products]
  O --> P[Accepted product manifest]
  P --> Q[SQL and Power BI consumption]
  P --> R[Approved batch exports]
  P --> S[Serving database for API use]
  S --> T[Azure Functions and API Management]
  U[Azure SQL contracts and entity metadata] -.-> E
  U -.-> J
  V[Purview supported catalog and lineage] -.-> M
  V -.-> O
```

[Open the full project flow and technical explanation](projects/03_bnp_enterprise_datahub.md).

## Synchrony Financial: Enterprise Data Quality and Governance

```mermaid
flowchart TD
  A[Customer account statement and payment feeds] --> B[ADF bounded ingestion]
  B --> C[ADLS landing and bronze Delta]
  D[Azure SQL approved rule versions] --> E[Databricks quality evaluation]
  C --> E
  E --> F[Rule results with denominators and input version]
  E --> G[Restricted record-level exceptions]
  F --> H{Critical controls and reconciliation pass?}
  H -->|No| I[Hold data-product publication]
  H -->|Yes| J[Accepted silver and gold datasets]
  J --> K[Consumer reporting views]
  F --> L[Power BI quality scorecards]
  G --> M[Steward triage and accountable remediation]
  I --> M
  M --> N[Source correction or approved rule revision]
  N --> O[Replay pinned input and revalidate]
  O --> E
  P[Microsoft Purview catalog and ownership] -.-> C
  P -.-> J
  Q[Storage catalog and serving permissions] -.-> G
  Q -.-> K
```

[Open the full project flow and technical explanation](projects/04_synchrony_data_quality_governance.md).

## Barclays (RFTBSL & SRP): Financial Data Warehouse Integration

```mermaid
flowchart TD
  A[General ledger and subledger extracts] --> E[ADF delivery ingestion]
  B[Trial balance snapshots] --> E
  C[Legal entity chart of accounts and reporting mappings] --> E
  D[Approved FX reference] --> E
  E --> F[ADLS immutable raw and bronze]
  F --> G[Databricks silver standardization]
  G --> H[Historical legal entity and account resolution]
  H --> I{Source and accounting controls pass?}
  I -->|No| Q[Restricted suspense and held batch]
  I -->|Yes| J[Accepted curated Parquet batch]
  J --> K[Synapse COPY INTO isolated staging]
  K --> L[Load effective-dated dimensions]
  L --> M[Load journal and trial balance facts]
  M --> N{Warehouse reconciliation passes?}
  N -->|No| Q
  N -->|Yes| O[Commit accepted warehouse publication]
  O --> P[Reporting views and Power BI]
  O --> R[Period close and revision evidence]
  Q --> S[Owner correction and affected-period replay]
  S --> G
```

[Open the full project flow and technical explanation](projects/05_barclays_rftbsl_srp_warehouse.md).

## Mobistar: Telecom Data Warehouse Transformation

```mermaid
flowchart TD
  A[CDR and data-session producers] --> B[Azure Event Hubs]
  B --> C[Databricks streaming reader and durable checkpoint]
  C --> D[Bronze raw event Delta]
  E[Subscriber tariff cell and billing files] --> F[ADF batch ingestion]
  F --> G[ADLS delivery manifests and bronze reference tables]
  D --> H[Parse validate and apply event-key deduplication]
  H --> I{Event valid and ordering resolved?}
  I -->|No| Q[Restricted malformed or conflicting events]
  I -->|Yes| J[Silver durable usage facts]
  G --> K[Effective-dated subscriber and tariff dimensions]
  J --> L[Historical enrichment by event time]
  K --> L
  L --> M[Daily usage aggregates and billing comparisons]
  M --> N{Completeness and source controls pass?}
  N -->|No| R[Hold affected analytical publication]
  N -->|Yes| O[Accepted gold datasets]
  O --> P[Databricks SQL and Power BI]
  S[Late arrivals and retained raw archive] --> T[Reconcile and rebuild affected days]
  T --> J
  Q --> U[Owner investigation]
  R --> U
```

[Open the full project flow and technical explanation](projects/06_mobistar_telecom_warehouse.md).

