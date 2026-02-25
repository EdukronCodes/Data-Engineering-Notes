### Project 4 — Unified Customer Master Data Platform (Flow)

### Goal
Create a governed, enterprise-grade **golden customer record** by unifying customer data across source systems, resolving identities, enforcing data quality, and publishing mastered customer profiles to analytics and operational applications.

### Objectives
- Create a single, trusted **golden customer record** with cross-system linkage and survivorship rules.
- Improve data quality with measurable DQ KPIs (completeness, validity, uniqueness) and stewardship workflows.
- Enable identity resolution with transparent match scores and auditability for merges/splits.
- Provide governed access to customer data with privacy controls (PII handling, masking, consent).
- Publish mastered customers to analytics and operational systems via DW tables, APIs, and change events.

### Primary users and outputs
- **Sales/CRM**: consolidated customer profile, deduplicated accounts/contacts, hierarchy (household/enterprise)
- **Marketing**: consent-aware audiences and segments
- **Finance/Risk**: standardized identifiers and KYC/credit attributes (as applicable)
- **Analytics**: curated customer dimension + history (SCD) and link tables
- **Downstream apps**: mastered customer API + event notifications on changes

### Reference architecture (high-level)
```mermaid
flowchart LR
  subgraph Sources
    CRM[CRM (Salesforce/Dynamics)]
    ERP[ERP (SAP/Oracle)]
    WEB[Web/App registrations]
    SUPPORT[Support/Call center]
    BILL[Billing/Subscriptions]
    PARTNER[Partner feeds]
  end

  subgraph Ingest
    ADF[ADF / Pipelines]
    SHIR[Self-hosted IR (if on-prem)]
  end

  subgraph Lakehouse
    ADLS[(ADLS Gen2)]
    BR[Bronze: raw]
    SL[Silver: standardized]
    GL[Gold: mastered]
  end

  subgraph Mastering
    DQ[Data Quality rules]
    ID[Identity resolution + matching]
    MR[Master record & survivorship]
    SCD[SCD Type 2 history]
  end

  subgraph Serve
    DW[(SQL/DW)]
    API[Customer Master API]
    EVT[Change events (Event Grid/Service Bus)]
    PBI[Power BI]
    CAT[Catalog/Lineage (Purview)]
  end

  Sources --> Ingest
  CRM --> ADF
  ERP --> ADF
  WEB --> ADF
  SUPPORT --> ADF
  BILL --> ADF
  PARTNER --> ADF
  SHIR --> ADF
  ADF --> ADLS --> BR --> SL
  SL --> DQ --> ID --> MR --> SCD --> GL
  GL --> DW --> PBI
  GL --> API
  GL --> EVT
  GL --> CAT
```

### End-to-end platform flow (detailed)
- **0) Foundations (security + governance)**
  - Entra ID groups/RBAC, managed identities, secrets in Key Vault
  - Data catalog, glossary terms (customer, account, party, contact), stewardship model
  - Define privacy rules: PII classification, masking/tokenization where required, consent handling

- **1) Source onboarding & canonical model**
  - Identify customer domains: person, organization, household, account, contact points (email/phone/address)
  - Define canonical entities and required keys:
    - `party_id` (golden), source ids, crosswalk mapping, match confidence
  - Define SLAs and CDC strategy per source (watermarks, change tables, API deltas)

- **2) Ingestion to Bronze**
  - Copy from sources to ADLS Bronze (partition by load date/run id)
  - Capture metadata: source watermark, row counts, schema version

- **3) Standardization to Silver**
  - Normalize formats:
    - Names (case/diacritics), phones (E.164), addresses (standard components), emails
  - Apply reference data:
    - Country/state codes, address validation provider outputs (optional)
  - Create conforming “source customer” tables with consistent columns

- **4) Data quality (DQ)**
  - Rule types:
    - Completeness (required fields), validity (email/phone formats), referential integrity
    - Uniqueness constraints by source, freshness checks
  - Route failures to quarantine with reason codes; create stewardship queues

- **5) Identity resolution & matching**
  - Generate candidate matches using:
    - Deterministic rules (exact email/phone, known ids)
    - Probabilistic/fuzzy matching (name + address similarity), blocking strategies for scale
  - Produce:
    - Match clusters, match score, explainability fields (which rules matched)

- **6) Survivorship & golden record creation**
  - Survivorship rules:
    - Source system precedence, recency, completeness scoring
    - Field-level survivorship (best email, best address, best legal name)
  - Create:
    - `gold_party` (mastered attributes)
    - `party_xref` (source-to-golden crosswalk)
    - `party_relationships` (household, parent-child org)
    - `contact_points` (email/phone/address with history)

- **7) History & auditability**
  - Implement **SCD Type 2** for mastered customer attributes (effective_from/to)
  - Keep full lineage:
    - Which sources contributed to which fields, match decision records

- **8) Publishing & consumption**
  - Analytics:
    - Publish Gold to DW/semantic model for reporting
  - Operational:
    - Customer Master API for lookups/search and downstream sync
    - Change events on create/merge/split/update for subscribers
  - Data access controls:
    - PII masking in serving layers; role-based exposure for sensitive attributes

- **9) Operations & monitoring**
  - Data pipeline monitoring: load failures, late sources, volume anomalies
  - DQ monitoring: rule failure rates, top offending sources, steward backlog
  - Mastering monitoring: match rate, merge/split counts, false positive review samples

### Orchestration pattern
- ADF orchestrates:
  - Ingest → Standardize → DQ → Match → Master → Publish → Notify
- Use run id + idempotent patterns to support safe reprocessing.

### Notes (design choices + common pitfalls)
- **Define “customer” explicitly**: person vs organization vs household; avoid mixing these without a clear party model.
- **Golden ID strategy**: generate `party_id` centrally and keep a durable crosswalk to every source identifier (never overwrite source ids).
- **Merges and splits are normal**: support unmerge/split workflows; keep merge decision logs and effective dates.
- **Matching transparency**: store match features and rule hits (why records matched) for explainability and steward trust.
- **Field-level survivorship**: decide winners per attribute, not just per record (e.g., best email from CRM, best legal name from ERP).
- **SCD2 vs “current only”**: analytics typically needs SCD2; operational lookups often need current + audit trail.
- **PII and consent**: apply masking and purpose-based access; enforce consent in downstream audience exports.
- **Data stewardship**: create queues for “needs review” clusters; track backlog and false positive/negative rates.

### Deliverables
- Canonical customer model + glossary
- Ingestion pipelines + standardized Silver schemas
- Matching/survivorship rulebook + stewardship workflow
- Gold mastered tables + crosswalk + SCD2 history
- Customer Master API spec + change event schema
- Monitoring dashboards (DQ, match metrics, pipeline SLAs)
