# BNP Paribas: Enterprise Datahub and Data Integration Platform

**Single-file project document:** architecture, all 12 flow diagrams, technical notes, examples, controls, deployment and recovery guidance are included in this Markdown file. No separate diagram assets or handbook are required.

> Evidence status: the client and project labels were supplied by the user. Architecture, datasets, responsibilities and implementation below are proposed reference designs for preparation. They are not verified descriptions of a client's internal platform. Replace illustrative details with actual experience before using them as employment claims.

## Project profile

- Target role: Azure Data Engineer / Data Integration Engineer.
- Employer: [actual employer]; client engagement dates: [MM YYYY–MM YYYY].
- Contribution: [what you personally designed/built/operated]; team: [verified size and roles].
- Scale: [verified daily volume, entity count and historical size].
- Outcomes: [baseline, measured result, period and measurement method].

## Business objective

Provide reusable ingestion and standardized data products for multiple enterprise domains with clear contracts, ownership, and controlled consumption.

## Azure and Microsoft technology stack

Azure Data Factory, ADLS Gen2, Azure Databricks/Delta Lake, Azure SQL Database metadata store, Azure Event Hubs for event sources where required, Azure Key Vault, Microsoft Entra ID, Microsoft Purview, Azure Monitor, Azure DevOps; Azure API Management and Azure Functions for narrowly scoped data APIs.

Illustrative sources: customer and account databases, payment files, reference APIs, domain extracts, and optional business-event streams. Specific source products and business rules require confirmation.

## End-to-end architecture

```text
Databases / files / APIs / optional events --> ADF or Event Hubs --> ADLS bronze --> Databricks domain silver --> governed gold data products --> SQL/Power BI/file exports or approved API
Cross-cutting: identity + access | quality + reconciliation | metadata + lineage | CI/CD + monitoring
```

The source owner provides bounded, identifiable deliveries. Engineering preserves raw input, applies explicit business rules, validates the result and releases only an accepted dataset. Consumers receive a defined product with an owner and freshness contract.

## Data model

| Dataset | Grain | Example columns |
|---|---|---|
| entity_contract | One entity contract version | entity_id, version, owner, grain, key_columns, schema_uri, freshness_target |
| customer_crosswalk | One source customer mapped to enterprise identity | source_system, source_customer_id, enterprise_customer_id, match_method |
| payment | One payment lifecycle event | payment_id, event_id, event_ts, status, amount, currency_code |
| data_product_manifest | One released data product version | product_id, version, schema_version, accepted_run_id, owner, published_at |

All names and columns are illustrative. Confirm uniqueness, source precedence, null handling, timezones, history policy and retention before implementing physical tables. A snapshot fact and an event fact require different aggregation rules.

## Technical implementation

### 1. Define contracts and domain ownership

Assign an owner for each domain and specify keys, types, nullable fields, retention, freshness, supported changes, and permitted consumers. Avoid treating similarly named source fields as identical without agreement.

### 2. Create metadata-driven onboarding

Register source connector, validated source object, extraction strategy, target paths, schema version, dependency list, and controls in Azure SQL. ADF orchestrates approved entity configurations; never execute unrestricted configuration text as SQL.

### 3. Handle each ingestion mode

Use Copy activities for supported database/file sources; implement API pagination, rate-limit retry, and cursor handling. For events, use Event Hubs and a dedicated checkpointed Spark stream; do not force streaming sources into a daily file schedule.

### 4. Standardize domain silver

Normalize codes and data types while retaining source identifiers. Build governed crosswalks for customer/account identity. Preserve ambiguous matches for stewardship instead of assigning identities through an unexplained heuristic.

### 5. Publish versioned products

Generate gold datasets with documented grain, compatibility rules, owner, lineage and quality results. Publish a manifest only after validation. Provide SQL and file delivery for bulk use; APIs read a serving store with appropriate request limits.

### 6. Protect consumer contracts

Expose stable views for compatible schema evolution. For breaking changes, release a separate version and deprecation window. Test downstream consumers before retiring the old contract.

### 7. Operate onboarding and lineage

Track source-to-product run IDs, automatically captured lineage where supported, and documented/custom lineage where needed. Alert owners on freshness or contract violations and capture consumer-facing incident status.

## Project-specific SQL example

The snippet illustrates one transformation/control, not an executable project by itself. Create the referenced tables, bind parameters using the selected runtime's supported API, and validate input contracts first.

```sql
-- Example contract metadata in Azure SQL Database.
CREATE TABLE dbo.entity_contract (
 entity_id varchar(100) NOT NULL,
 contract_version int NOT NULL,
 domain_name varchar(100) NOT NULL,
 owner_group varchar(200) NOT NULL,
 schema_uri nvarchar(1000) NOT NULL,
 load_strategy varchar(20) NOT NULL,
 is_active bit NOT NULL,
 CONSTRAINT PK_entity_contract PRIMARY KEY(entity_id, contract_version),
 CONSTRAINT CK_load_strategy CHECK(load_strategy IN ('SNAPSHOT','WATERMARK','CDC','EVENT'))
);
```

## Validation and acceptance

- Validate a new source against the registered contract before it enters the shared domain table.
- Test paginated API failure after page N, replayed events, and a schema that removes a required field.
- Prove every released product has an owner, source lineage, access policy, run ID and quality outcome.
- Check that customer crosswalk changes do not silently rewrite historical identities.
- Replay the same accepted input twice and verify the business output is unchanged.
- Obtain approval from the business owner using source/control evidence before consumer cutover.

## Failure and recovery example

An upstream API adds an optional field and later changes the type of a key. Accept the optional field only under the contract's evolution policy; block the incompatible key change, retain raw payloads, and resume from the saved cursor after a versioned migration.

Do not advance accepted source state when extraction, validation or publication fails. Resume from durable input and the last accepted boundary; do not resolve data differences by blindly rerunning downstream reports.

## Architecture tradeoff to explain in interviews

A generic ingestion framework reduces repeated plumbing but does not replace source-specific semantics. Keep contract validation and orchestration reusable, while domain transformations remain explicit. Purview lineage coverage depends on connector/workload support and must be verified.

## Deployment and production ownership

- Keep development, test, and production resources and identities separate. Provision Azure resources through reviewed Bicep/Terraform and deploy notebooks, SQL, configuration, and pipeline definitions through Azure DevOps.
- Run schema/contract checks and transformation tests on synthetic or approved masked data, followed by integration validation in test. Promote the same reviewed artifact with environment-specific parameters.
- Store supported secrets in Azure Key Vault; prefer managed identity or approved workload identity wherever the connector supports it. Do not embed secrets in notebooks or Markdown.
- Version contracts, business rules and published schemas. Take a recovery point before a destructive schema migration; validate both application rollback and data rollback.
- Record run ID, entity, source boundary, input/output counts, reconciliation result, quality status, execution time and publication ID. Monitor freshness separately from job success.
- Agree actual freshness target, RPO, RTO, support owner and escalation route before go-live. Targets in an interview must be verified, not invented.

## Security implementation

Use Microsoft Entra ID groups and least-privilege workload identities. Apply ADLS RBAC and ACLs, Databricks Unity Catalog grants or Fabric workload/OneLake permissions as appropriate. Limit storage network access through supported private networking, firewalls and validated DNS configuration. Review Fabric connectivity separately; Azure Private Link assumptions do not automatically apply to every Fabric workload. Restrict raw and quarantine zones, mask sensitive attributes in test and consumer datasets, and keep personal data out of logs. Configure Power BI access and row-level security independently of direct data access. Agree residency, retention and deletion requirements with the data owner rather than claiming a platform configuration guarantees compliance.

## Implementation deliverables and release evidence

1. Source inventory, data contract, sample input and expected output.
2. Architecture and identity/connectivity design approved for the environment.
3. Pipeline definitions, notebooks, SQL transformations and configuration metadata.
4. Model dictionary with grain, keys, decimal precision and historical behavior.
5. Test fixtures/results, source reconciliation and signed acceptance record.
6. CI/CD definition, infrastructure code, rollback procedure and cost baseline.
7. Lineage documentation, ownership/access matrix, operating dashboard and runbook.

These documents describe the implementation; they are not a deployed platform or evidence of work performed for the named client. The implementation reference at the end of this file provides code patterns, a build sequence, recovery handling and acceptance templates.


## Interview walkthrough

Use this sequence with your actual details: explain the business requirement; identify sources and their grain; draw the end-to-end flow; explain your personal contribution; describe one transformation and one control; walk through a failure/recovery; explain a measured optimization and its tradeoff; state the accepted result.

Practice these questions:

1. Why were these Azure services selected, and what alternative did you evaluate?
2. How were inserts, updates, deletes, duplicates and late data handled?
3. What proved the published data was complete and financially/operationally correct?
4. How did you prevent exposure through raw files, SQL, BI and exception logs?
5. How did you deploy, roll back, replay and recover the platform?
6. Which parts did you personally implement, and what evidence supports the claimed impact?

## Resume-ready project bullets — use only if verified

- Developed a metadata-driven Azure ingestion framework for [verified source types/entities] using ADF and ADLS Gen2.
- Built domain-level Delta datasets and reusable data products with schema contracts and publication controls.
- Integrated [verified API/file/event sources] with pagination, replay, and incremental processing.
- Established ownership, lineage, and access patterns for [verified number] enterprise data products.

## Technical references

The following official references support the platform patterns, not the named client's implementation.

- [Fabric medallion lakehouse architecture](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture)
- [Fabric end-to-end lakehouse tutorial](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-introduction)
- [ADF incremental ingestion with watermarks](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-portal)
- [Azure Databricks MERGE reference](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)
- [Azure Databricks change data feed](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed)
- [Microsoft Purview governance setup](https://learn.microsoft.com/en-us/purview/data-governance-get-started)

<!-- EXPANDED_FLOW_START -->

## Full flow diagrams and detailed execution narrative

The following diagrams expand the entire reference project lifecycle. Solid arrows indicate the stated data or workflow direction; dotted arrows indicate supporting configuration, catalog or security relationships. These are proposed designs and must be checked against the actual engagement.

### Diagram 1: Complete project data flow

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


**How to read the diagram:** start with the source groups, follow ingestion into durable raw/bronze data, then follow validated transformations into the accepted serving dataset. The rejection paths are part of the production flow: a held run retains its input and evidence so the owner can investigate and engineering can replay the affected scope. Raw inputs, staged output and accepted publications are different artifacts.

### Source-to-output contracts

| Input group | Business grain | Ingestion contract | Result |
|---|---|---|---|
| Contract metadata | Entity + contract version | Reviewed configuration changes | Approved source/schema/ownership contract |
| Customer crosswalk | Source identity + enterprise mapping interval | Stewarded identity decisions | Traceable enterprise joins |
| Payment events | Payment + lifecycle event | Batch extracts or event stream | Ordered payment lifecycle and analytical facts |
| Data products | Product + publication version | Accepted domain processing | SQL/file/API contract and consumer manifest |

For every input, confirm the owner, business key, event/effective timestamp, source change sequence, extraction boundary, deletion semantics and reference dependencies. Choose snapshot, watermark, CDC or event ingestion from those semantics. Do not assume a file delivery is complete merely because the file is readable.

### Diagram 2: Runtime interaction from source to consumer

```mermaid
sequenceDiagram
  autonumber
  participant SRC as Approved source
  participant ORC as Azure Data Factory
  participant CTL as Durable run control
  participant RAW as Immutable landing or bronze
  participant ENG as Azure Databricks job
  participant GATE as Quality and reconciliation
  participant PUB as Accepted publication
  participant USER as Versioned SQL file or API product
  ORC->>CTL: Acquire entity or publication lease
  CTL-->>ORC: Last accepted boundary and run ID
  ORC->>SRC: Request bounded input or validate delivered batch
  SRC-->>RAW: Persist source records and manifest
  RAW-->>CTL: Record durable input and source boundary
  ORC->>ENG: Process identified input and rule version
  ENG->>GATE: Submit staged output and control totals
  alt Critical validation fails
    GATE->>CTL: Hold run with failed controls
    GATE-->>ORC: Alert owner and preserve replay scope
  else Validation accepted
    GATE->>PUB: Release validated publication
    PUB-->>CTL: Save publication ID and accepted boundary
    PUB-->>USER: Expose accepted dataset and as-of status
  end
  ORC->>CTL: Release lease and finalize run status
```


This sequence describes an accepted batch or publication cycle. For streaming, raw events are persisted continuously and product publication follows the chosen microbatch/date policy; an ADF schedule is not required for every event. The control store holds durable state, while the accepted publication records the actual output exposed to consumers. Where these sit in different systems, recovery reconciles their manifests instead of assuming a shared atomic transaction.

### Detailed stage explanations

### Stage 1: Define contracts and domain ownership

Assign an owner for each domain and specify keys, types, nullable fields, retention, freshness, supported changes, and permitted consumers. Avoid treating similarly named source fields as identical without agreement.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Stage 2: Create metadata-driven onboarding

Register source connector, validated source object, extraction strategy, target paths, schema version, dependency list, and controls in Azure SQL. ADF orchestrates approved entity configurations; never execute unrestricted configuration text as SQL.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Stage 3: Handle each ingestion mode

Use Copy activities for supported database/file sources; implement API pagination, rate-limit retry, and cursor handling. For events, use Event Hubs and a dedicated checkpointed Spark stream; do not force streaming sources into a daily file schedule.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Stage 4: Standardize domain silver

Normalize codes and data types while retaining source identifiers. Build governed crosswalks for customer/account identity. Preserve ambiguous matches for stewardship instead of assigning identities through an unexplained heuristic.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Stage 5: Publish versioned products

Generate gold datasets with documented grain, compatibility rules, owner, lineage and quality results. Publish a manifest only after validation. Provide SQL and file delivery for bulk use; APIs read a serving store with appropriate request limits.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Stage 6: Protect consumer contracts

Expose stable views for compatible schema evolution. For breaking changes, release a separate version and deprecation window. Test downstream consumers before retiring the old contract.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Stage 7: Operate onboarding and lineage

Track source-to-product run IDs, automatically captured lineage where supported, and documented/custom lineage where needed. Alert owners on freshness or contract violations and capture consumer-facing incident status.

**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness.

### Diagram 3: Project-specific business transformation

```mermaid
flowchart LR
  A[Domain owner proposes source] --> B[Define versioned data contract]
  B --> C[Review schema keys freshness and permissions]
  C --> D[Register approved connector configuration]
  D --> E[Ingest raw sample and validate]
  E --> F[Build explicit domain transformation]
  F --> G[Run quality and compatibility checks]
  G --> H{Accepted?}
  H -->|No| I[Fix source or contract with owner]
  I --> B
  H -->|Yes| J[Publish product version and manifest]
  J --> K[Grant approved consumer access]
  K --> L[Monitor freshness and contract changes]
```


**Business meaning:** Provide reusable ingestion and standardized data products for multiple enterprise domains with clear contracts, ownership, and controlled consumption. The diagram highlights where the project-specific rules alter the data's meaning, grain or reporting status. Technical success at these stages does not substitute for the business control evidence described below.

### Worked record journey

An illustrative payment product receives `PAY100` with lifecycle events `CREATED`, `AUTHORIZED` and `SETTLED`. Each event has a stable source event key and event time. Bronze preserves the complete event history. Silver validates status membership and preserves lifecycle order; a current-status view may select the latest accepted source sequence, but the underlying event fact still retains all three events.

The product owner decides whether the consumer contract exposes events, current payment state, or a daily settled-payment aggregate. These are different grains. Counting three lifecycle events as three settled payments is incorrect. The released product manifest identifies the contract version, accepted input boundary, rule version and quality result.

If the API fails after page 7, the saved cursor and immutable page manifests make recovery bounded. Deduplication protects against a repeated page. A new optional field can follow the approved compatibility policy, while a key type change requires a reviewed version change and consumer migration. An operational API reads a properly sized serving database with bounded queries rather than scanning raw lake files for every request.

The example is synthetic and demonstrates behavior, not actual client data or a measured client outcome. Trace a record using its source business key, source sequence, raw location, run ID, contract/rule version and accepted publication ID. Avoid putting sensitive payload values in general logs.

### Dependencies, scheduling and publication boundaries

Contracts and permissions precede ingestion. Identity crosswalk/reference versions precede dependent domain joins. Products publish only after all declared dependencies reach an accepted boundary; independent domains can have separate release schedules.

Keep a dependency manifest for each publication. It should identify the accepted source/reference versions, transformed partition scope and resulting output version. A successful upstream run is usable only if its controls passed and its artifact matches the downstream contract. Run independent entities concurrently only within the approved resource/source limits; serialize publication where concurrent writers could conflict.

**Suggested parameter contract:** `entity_id`, `run_id`, `business_date` or bounded change range, `contract_version`, `rule_version`, `input_manifest_uri`, `output_stage_uri`, `environment`, and `replay_mode`. Validate values and allow-list identifiers. Use the same input/rule scope during a replay unless the run explicitly records an approved correction.

### Diagram 4: Lifecycle and acceptance states

```mermaid
stateDiagram-v2
  [*] --> STARTED
  STARTED --> LANDED: Input and manifest durable
  LANDED --> TRANSFORMED: Staged output produced
  TRANSFORMED --> VALIDATED: Critical controls accepted
  VALIDATED --> PUBLISHED: Accepted output exposed
  PUBLISHED --> [*]
  STARTED --> FAILED: Extract failed
  LANDED --> FAILED: Transform failed
  TRANSFORMED --> HELD: Controls failed
  VALIDATED --> FAILED: Publish failed
  FAILED --> STARTED: Resume identified run safely
  HELD --> TRANSFORMED: Correct and replay affected input
```


`STARTED` means a run exists; `LANDED` means its inputs are durable; `TRANSFORMED` means a candidate output exists; `VALIDATED` means the critical checks passed; `PUBLISHED` means consumers can read the accepted output. `HELD` indicates a deliberate business/control stop and `FAILED` indicates an execution failure. Extend this file's example control-table status constraint if you implement these additional states. The diagram is a recommended lifecycle, not a claim that the existing example DDL already includes every state.

Track state transitions with timestamps, actor/workload identity, reason and artifact IDs. A retry is an attempt tied to the original business input. Replaying a publication should not create extra fact rows, duplicate daily aggregates or misleading extra accepted runs.

### Diagram 5: Error handling, late correction and recovery

```mermaid
flowchart TD
  A[Failure late data or reconciliation mismatch] --> B[Identify entity run input and accepted boundary]
  B --> C[Hold affected publication and preserve evidence]
  C --> D{Failure phase?}
  D -->|Extraction| E[Resume bounded copy or missing delivery]
  D -->|Transformation| F[Fix approved code or reference and replay raw input]
  D -->|Quality| G[Owner corrects source rule or mapping]
  D -->|Publication| H[Inspect durable accepted manifest]
  H --> I{Publication already committed?}
  I -->|Yes| J[Reconcile state without duplicate output]
  I -->|No| K[Retry idempotent publication]
  E --> L[Revalidate affected scope]
  F --> L
  G --> L
  J --> L
  K --> L
  L --> M{Critical controls restored?}
  M -->|No| C
  M -->|Yes| N[Release accepted output and confirm freshness]
  N --> O[Close incident with root cause and evidence]
```


**Project recovery scenario:** An upstream API adds an optional field and later changes the type of a key. Accept the optional field only under the contract's evolution policy; block the incompatible key change, retain raw payloads, and resume from the saved cursor after a versioned migration.

Before retrying, determine whether the failure occurred before or after publication. A run can publish successfully and fail while recording its state; a blind repeat can double-count outputs. Inspect the accepted manifest, compare expected key/count/control evidence, and complete or roll back the recorded state safely. Missing or corrupt inputs require source correction; transformation fixes require versioned code; business-control failures require the relevant owner's resolution.

For a late correction, identify affected event dates, historical dimension intervals and dependent aggregate/reporting periods. Recompute the smallest complete business scope rather than updating only an arbitrary file. Preserve old publication metadata and make consumer as-of/revision information clear.

### Diagram 6: Identity, access and governance flow

```mermaid
flowchart LR
  A[Microsoft Entra ID identities and groups] --> B[Workload identities]
  A --> C[Engineering and steward groups]
  A --> D[Approved consumer groups]
  B --> E[Connector and data-plane permissions]
  C --> F[Scoped raw silver and quarantine access]
  D --> G[Approved gold SQL and semantic model access]
  H[Key Vault for supported external secrets] -.-> B
  I[Supported network controls and DNS] -.-> E
  J[Purview catalog classifications and ownership] -.-> F
  J -.-> G
  K[Access tests audit and retention controls] -.-> F
  K -.-> G
```


Permissions are enforced at the workload, storage/catalog and serving layers used by this project. The catalog documents ownership and classification; permissions still need implementation and testing. Validate engineer, workload, steward and consumer paths independently, including raw, quarantine, direct SQL and dashboard exports. A masked dashboard does not justify unrestricted raw access.

Use approved identities for source connections and pipeline execution. Key Vault applies to supported external-secret scenarios; configure Fabric connection credentials through supported mechanisms rather than assuming Azure managed identity works identically for every connector. Network restrictions, retention and residency settings are environment-specific controls to verify during deployment.

### Diagram 7: Development-to-production deployment flow

```mermaid
flowchart TD
  A[Reviewed architecture contracts and changes] --> B[Git pull request]
  B --> C[Code schema and fixture validation]
  C --> D[Versioned build artifact]
  D --> E[Deploy development or test configuration]
  E --> F[Integration replay reconciliation and access tests]
  F --> G{Release evidence accepted?}
  G -->|No| H[Fix and repeat affected checks]
  H --> B
  G -->|Yes| I[Promote same artifact to production]
  I --> J[Controlled smoke load and publish validation]
  J --> K[Monitor freshness performance and quality]
  K --> L{Release issue?}
  L -->|Yes| M[Execute tested code and data recovery plan]
  L -->|No| N[Record accepted release and operating baseline]
```


Create source contracts, physical schemas and fixtures before building the complete pipeline. Deploy infrastructure and configuration first, then compatible tables and transformations, then orchestration and serving objects. Test one vertical slice before adding volume or source variants. Promote reviewed artifacts with separate environment parameters and identities. Confirm the selected Azure/Fabric item's deployment support instead of assuming every object uses the same release mechanism.

Production smoke validation checks source reachability, identity permissions, small bounded processing, accepted publication and consumer reads. If a release changes stored data/schema, the rollback plan must cover those data changes as well as code. Record who owns the decision and where the recovery evidence is stored.

### Consumer request and reporting behavior

A consuming team requests a product version, grain, freshness target and access scope. Bulk consumers use approved SQL/files; operational API consumers use a serving store through controlled endpoints. Deprecation of a breaking contract has an owner, migration date and consumer acknowledgment.

Every product should expose its grain, accepted as-of boundary, revision/contract version, freshness status, business owner and access route. Serving queries should select accepted output; do not expose unvalidated staging by accident. If multiple datasets publish independently, the report must handle and display their differing as-of dates.

### Observability from ingestion through consumption

| Layer | What to record or measure | What the signal establishes |
|---|---|---|
| Source/landing | Boundary, delivery IDs, source counts, manifests, completeness | Whether all expected input arrived |
| Transformation | Rule/code version, input/output scope, rejected rows, duration | Which logic ran on which records |
| Validation | Key coverage, decimal totals, rule results, accepted status | Whether the output meets its contract |
| Publication | Dataset version, accepted boundary, publication ID | Exactly what consumers can read |
| Consumption | Access-test outcomes, serving errors, query latency | Whether authorized users can use the product |
| Recovery | Failed phase, replay input, replacement publication, controls | Whether service was restored correctly |

Measure source/API throughput, domain transformation cost and product query latency separately. Reuse connectors and validators, but retain explicit domain rules. Batch small API requests where supported and respect source rate limits with bounded retry.

Alert on accepted-data age as well as job failure. A pipeline can finish successfully while a source feed is stale or the product remains held. Dashboard a last accepted timestamp and business freshness target, and route each alert to its actual owning team.

### Project-specific completion and interview evidence

- Validate a new source against the registered contract before it enters the shared domain table.
- Test paginated API failure after page N, replayed events, and a schema that removes a required field.
- Prove every released product has an owner, source lineage, access policy, run ID and quality outcome.
- Check that customer crosswalk changes do not silently rewrite historical identities.
- Demonstrate normal flow, rejected flow, duplicate replay and a late correction using synthetic/approved fixtures.
- Verify the diagram against deployed resources, connections, code and actual publication artifacts.
- Keep one accepted-run evidence packet linking manifest, controls, serving dataset and consumer acceptance.
- Replace illustrative names, example dates, sources and targets with verified engagement details before discussing them as past experience.

**Interview explanation:** draw Diagram 1, describe the worked record journey, identify your own implemented stages, explain Diagram 3's business rules, show how the critical gate protects publication, then use Diagram 5 to explain a concrete recovery. Finish with the verified output and a measured result supported by evidence.

### Plain-text fallback flow

All diagrams are embedded directly below their corresponding project sections using Mermaid. Markdown viewers with Mermaid support display them inline. The original architecture section and the following text retain the core flow in those viewers:

```text
Databases / files / APIs / optional events --> ADF or Event Hubs --> ADLS bronze --> Databricks domain silver --> governed gold data products --> SQL/Power BI/file exports or approved API
1. Confirm source contract and accepted dependencies.
2. Persist identifiable raw input and manifest.
3. Apply ordered, versioned business transformations.
4. Validate critical rules and source-to-target controls.
5. On failure: hold -> investigate -> correct -> replay -> revalidate.
6. On acceptance: publish -> record accepted boundary -> expose to consumers.
7. Monitor freshness, correctness, access, performance and recovery.
```

<!-- DEEP_NOTES_START -->

## Extended project notes: source, model, dependencies and serving

### Diagram 8: Individual source-to-bronze ingestion

```mermaid
flowchart TD
  S0[Registered relational source] --> C0[Validate source-specific contract]
  C0 --> R0[Bounded identified raw input]
  R0 --> M[Delivery or event manifest and provenance]
  S1[Paginated approved REST source] --> C1[Validate source-specific contract]
  C1 --> R1[Bounded identified raw input]
  R1 --> M[Delivery or event manifest and provenance]
  S2[Manifested files] --> C2[Validate source-specific contract]
  C2 --> R2[Bounded identified raw input]
  R2 --> M[Delivery or event manifest and provenance]
  S3[Event Hubs business events] --> C3[Validate source-specific contract]
  C3 --> R3[Bounded identified raw input]
  R3 --> M[Delivery or event manifest and provenance]
  M --> B[Bronze with explicit schema and source metadata]
  B --> V{Complete valid input scope?}
  V -->|No| H[Hold or approved restricted quarantine]
  V -->|Yes| T[Versioned domain transformation]
```

Validate each source separately before combining its records. Database changes, manifested files and event deliveries have different completeness/replay semantics. Preserve source keys, boundary and arrival metadata even after standardization.

### Diagram 9: Transformation dependency graph

```mermaid
flowchart LR
  N0[Contract approval]
  N1[Raw ingestion]
  N0 --> N1
  N2[Domain normalization]
  N1 --> N2
  N3[Identity crosswalk]
  N3 --> N2
  N4[Reference versions]
  N4 --> N2
  N5[Product checks]
  N2 --> N5
  N6[Versioned release]
  N5 --> N6
  N7[SQL file and API consumers]
  N6 --> N7
```

An arrow means the downstream stage requires an accepted upstream artifact/version. This is the business dependency graph, not proof that all upstream systems run on a single schedule. Record version/as-of dependencies for independently published data.

### Diagram 10: Logical data relationships

```mermaid
erDiagram
  entity_contract ||--o{ data_product_manifest : "declared product dependency"
  customer_crosswalk ||--o{ payment : "approved enterprise identity mapping"
  entity_contract { string entity_id string version string owner string grain string schema_uri }
  customer_crosswalk { string source_system string source_customer_id string enterprise_customer_id string match_method }
  payment { string payment_id string event_id timestamp event_ts string status decimal amount string currency_code }
  data_product_manifest { string product_id string version string schema_version string accepted_run_id timestamp published_at }
```

The ER view shows logical analytical relationships, not deployed foreign-key enforcement. Some edges express as-of or control-scope relationships rather than direct physical foreign keys. Reconcile this view with the model dictionary and actual physical schemas; composite uniqueness follows the stated grain.

### Diagram 11: Accepted publication-to-consumer flow

```mermaid
flowchart TD
  A[Validated staged output] --> B[Acceptance evidence and dependency manifest]
  B --> C{Product policy satisfied?}
  C -->|No| D[Hold publication and notify owner]
  C -->|Yes| E[Commit supported table or warehouse output]
  E --> F[Record accepted publication and as-of boundary]
  F --> G[Consumer route resolves accepted dataset]
  G --> H[Authorized SQL or semantic model query]
  H --> I[Business report with explicit grain and date]
  J[Identity and permitted access scope] -.-> H
  K[Measure and reporting contract] -.-> I
  F --> L[Freshness and correctness monitoring]
```

The consumer product is versioned domain product, export or operational API serving store. Define how the actual serving route selects accepted data. A manifest alone does not secure or atomically switch readers; implement compatible views/version selection/transactions for the chosen engine and validate concurrent reads.

### Diagram 12: Historical correction and dependent rebuild

```mermaid
sequenceDiagram
  autonumber
  participant SRC as Source or business owner
  participant RAW as Durable raw history
  participant ENG as Versioned transformation
  participant CTL as Critical controls
  participant PUB as Accepted publication
  participant BI as Dependent consumer
  SRC->>RAW: Deliver identified correction with authoritative ordering
  RAW->>ENG: Supply correction and required historical scope
  ENG->>ENG: Resolve affected dates keys and reference versions
  ENG->>CTL: Submit recomputed candidate and control evidence
  alt Controls fail
    CTL-->>SRC: Hold and request owner resolution
  else Controls pass
    CTL->>PUB: Release traceable replacement revision
    PUB->>BI: Expose accepted boundary and refresh affected scope
    BI-->>CTL: Confirm intended reporting result
  end
```

Correction scope includes source entity contract version, identity mapping and dependent product scope. Source arrival time does not automatically determine the historical business period affected. Preserve prior acceptance metadata, use authoritative ordering and verify downstream refresh behavior.

### Detailed implementation decisions and operating notes

#### 1. Onboarding

A domain owner declares grain, key, schema, freshness, retention and consumer permissions. Configuration reuses plumbing, but each source still needs explicit extraction/change semantics and approved object identifiers.

#### 2. Connector behavior

Database extraction needs consistent boundaries, API extraction needs pagination/rate-limit/cursor handling, file extraction needs delivery manifests, and event ingestion needs durable offsets/checkpoints. One generic timestamp pipeline cannot safely replace all four.

#### 3. Identity integration

Preserve original source identity and govern crosswalk assignments. Ambiguous matches remain stewarded exceptions. Changing an enterprise identity mapping can affect historical products and must have a defined correction policy.

#### 4. Lifecycle grain

Payment events and current payment state are distinct products. Three lifecycle events do not imply three settled payments. Define whether the product retains all events, selects authoritative latest status or aggregates accepted settlement activity.

#### 5. Consumer contract

Publish compatible schema additions under an approved policy; introduce a new version for breaking keys/types/semantics. The product manifest identifies contract, inputs, rules, owner and accepted as-of boundary.

#### 6. API serving

Serve bounded operational lookups from an appropriate serving database, with approved API identity/access and pagination. Use lake/SQL/file routes for bulk analytics instead of scanning raw files for every API request.

### Pipeline/notebook contract and evidence packet

Every transformation should receive an identified input scope and produce an identified candidate. Suggested logical fields are `run_id`, `attempt_id`, `entity_id`, source boundary or delivery ID, business-date range, contract version, code/rule version, reference versions and output location. Validate paths/identifiers and bind values using supported APIs. These are recommended control fields, not an existing deployed application interface.

Persist input completeness, accepted/rejected/duplicate/conflict counts and the applicable reconciliation totals. Do not conflate a retried attempt with a new source business delivery. A publish decision records which candidate and dependencies were accepted. If table writes and the control store are separate systems, reconcile the outcome after a crash; avoid claiming a distributed atomic commit that the implementation does not provide.

### Synthetic acceptance fixtures

| Case | Input or fault | Expected behavior |
|---|---|---|
| Repeated API page | Page 7 returns twice | Stable source keys prevent duplicate output |
| Breaking key change | String key becomes incompatible structured value | Contract holds release; versioned migration needed |
| Optional field addition | New nullable field arrives | Accept only under evolution policy |
| Ambiguous identity | Two enterprise matches for one source customer | Steward exception; no arbitrary mapping |
| Payment lifecycle | Created authorized settled events | One settled payment under settlement fact grain |
| Old consumer | Consumer still uses product v1 | v1 stays compatible until approved deprecation |

Retain the input, expected business result, actual result, rule/reference versions and run/publication IDs for each fixture. Cases are proposed tests and have not executed against cloud resources. Add representative volume/concurrency checks after the correctness cases pass.

### Normal-day operating walkthrough

1. Check expected source deliveries/events and the last accepted business boundary.
2. Verify required reference/dependency versions, execution identity and resource availability.
3. Land durable input and record its manifest/provenance.
4. Transform the bounded scope and preserve restricted exception evidence.
5. Evaluate keys, reference coverage, quality and source-to-target totals.
6. Publish only the accepted scope and record the consumer-visible as-of/revision.
7. Verify consumer access and business queries; monitor accepted-data age and resource cost.

### Incident walkthrough and ownership

The source owner resolves missing/corrected deliveries and source business semantics. The engineer resolves extraction/processing/target behavior. The data steward resolves approved reference/quality exceptions. The product/reporting owner accepts the consumer result. Assign actual teams and escalation routes before production; these are responsibilities to fill in, not assumed client organization details.

For an incident, identify its impacted product and last accepted boundary before rerunning anything. Preserve raw input, code/configuration version and the failed control. Determine whether publication already happened. Recover the smallest complete business scope, revalidate, then verify the dependent report/API result. A green pipeline without restored accepted freshness does not close the incident.

### Performance and cost evidence to collect

Measure extraction, source pressure, listing/read throughput, transformation/shuffle time, target writing, reconciliation and serving queries separately. Capture the workload boundary and concurrency with each benchmark. Tune a demonstrated bottleneck, compare equivalent before/after cases, and retain correctness/recovery checks. No volumes, capacity sizes or percentage savings in these notes are verified client metrics.

### Explain the whole flow during an interview

Start with the business output and its grain. Draw the full architecture and the source-specific flow. Explain the dependency order and one historical/reference join. Show the accepted-publication path and a consumer query. Walk through a correction using Diagram 12, then show one acceptance fixture and the evidence that would prove the result. State precisely which parts you personally performed when discussing actual employment.

## Embedded implementation reference

This is a reference implementation guide for the six proposed project designs. Code uses illustrative tables and schemas. It requires Azure resources, approved source access, runtime configuration and synthetic/approved test data; the Markdown files do not provision or run Azure services.

### 1. Build sequence

1. Select one project and define a minimal vertical slice: one source entity, one transformation, one validated gold dataset and one consumer query.
2. Create a development Azure resource group, ADLS Gen2 account with hierarchical namespace, ADF instance, Azure SQL metadata database, Key Vault and Databricks workspace. For the Fabric project create licensed/capacity-backed Fabric workspaces and Lakehouses instead of assuming an Azure storage account is OneLake.
3. Assign workload identity permissions, catalog/table grants, storage ACLs and source access. Validate networking and DNS. Create separate development/test/production configurations before deployment.
4. Create raw paths and bronze/silver/gold Delta tables with explicit schemas. In Databricks use Unity Catalog storage credentials/external locations as appropriate; in Fabric attach the correct Lakehouse to the notebook.
5. Create control tables, register an approved entity and seed its initial boundary. Load a small synthetic snapshot, including intentionally invalid and duplicate records.
6. Build the source extraction pipeline, notebook transformations, reconciliation and publication gate. Record durable input and output locations for every run.
7. Implement one insert, update, delete and late-arrival scenario. Replay input twice. Validate the accepted result and recovery after a simulated failure.
8. Create a serving view/semantic model and validate both its numbers and access with consumer identities.
9. Add monitoring, CI/CD, infrastructure code, deployment parameters, operating procedures and a measured performance/cost baseline.
10. Scale only after correctness passes; use the project-specific acceptance controls before declaring completion.

### 2. Storage and metadata contracts

```text
landing/<source>/<entity>/business_date=YYYY-MM-DD/run_id=<uuid>/
bronze/<domain>/<entity>/                  # raw records plus ingestion metadata
silver/<domain>/<entity>/                  # conformed business records
gold/<product>/<dataset>/                  # accepted analytical datasets
quarantine/<domain>/<entity>/run_id=<uuid>/ # restricted failed records
checkpoints/<stream_name>/                 # one durable path per stream
```

These are ADLS examples. Fabric Files/Tables organization and managed catalog tables have their own locations. Do not manually move files inside a managed Delta table. Avoid subscriber/customer ID partitions; choose partitioning only after measuring date filtering, volume and file sizes.

```sql
-- Azure SQL orchestration metadata; add access, indexing and retention policies.
CREATE TABLE dbo.entity_state (
 entity_id varchar(100) PRIMARY KEY,
 accepted_watermark datetime2(7) NULL,
 accepted_run_id uniqueidentifier NULL,
 state_version rowversion
);
CREATE TABLE dbo.pipeline_run (
 run_id uniqueidentifier PRIMARY KEY,
 entity_id varchar(100) NOT NULL,
 old_watermark datetime2(7) NULL,
 new_watermark datetime2(7) NULL,
 status varchar(20) NOT NULL,
 source_count bigint NULL,
 target_count bigint NULL,
 started_at datetime2(7) NOT NULL,
 ended_at datetime2(7) NULL,
 CONSTRAINT CK_run_status CHECK
  (status IN ('STARTED','LANDED','VALIDATED','PUBLISHED','FAILED'))
);
```

Acquire a per-entity lease or use a serialized scheduler so two runs cannot publish the same boundary concurrently. Restrict configuration changes to reviewed values; table identifiers need allow-list validation because SQL parameters do not parameterize object names.

### 3. ADF incremental orchestration

```text
Lookup approved entity configuration
  -> acquire entity lock
  -> read last accepted boundary
  -> capture bounded source upper boundary
  -> create STARTED run record
  -> Copy bounded source rows into immutable run directory
  -> validate landing manifest / mark LANDED
  -> invoke Databricks notebook
  -> quality checks + reconciliation / mark VALIDATED
  -> publish accepted product
  -> compare-and-set accepted boundary / mark PUBLISHED
  -> release lock
Failure path: mark FAILED + preserve input + alert owner + release lock
```

For Fabric use supported Fabric pipeline/notebook/control-state mechanisms rather than assuming every ADF activity or connector is identical.

```sql
-- Bounded example query; timestamp semantics must be agreed with the source.
SELECT transaction_id, source_sequence, modified_at, amount, currency_code
FROM dbo.source_transaction
WHERE modified_at > @old_watermark
  AND modified_at <= @new_watermark;
```

A timestamp alone is safe only if the source's commit/update behavior guarantees it. Concurrent or late commits can otherwise fall behind the accepted boundary. Prefer source-supported CDC or consistent snapshots with a commit-ordered change boundary. If using a lookback overlap, deduplicate it and document residual risks. Use a timestamp plus key cursor for deterministic page ordering; this does not fix backdated updates or deletes. Timestamp extraction cannot detect hard deletes without a deletion feed or complete-snapshot comparison.

Advance state only after successful acceptance. Publication and Azure SQL state are usually in different transaction systems: use a durable publication manifest and idempotent reconciliation so a crash between them can resume safely. Never claim they are one atomic distributed transaction.

### 4. PySpark validation and deterministic deduplication

```python
from pyspark.sql import functions as F, Window

## `input_path`, `quarantine_path`, `silver_table` and `run_id` are validated job parameters.
schema = ('transaction_id STRING, line_id STRING, source_system STRING, '
          'source_sequence LONG, modified_at TIMESTAMP, '
          'amount DECIMAL(28,6), currency_code STRING')
raw = (spark.read.schema(schema).option('mode', 'FAILFAST')
       .json(input_path).withColumn('run_id', F.lit(run_id)))
## FAILFAST fails the batch for malformed JSON. An alternative permissive
## parser must explicitly capture corrupt records and quarantine them.
invalid = (F.col('transaction_id').isNull() | F.col('line_id').isNull()
           | F.col('source_system').isNull() | F.col('source_sequence').isNull()
           | F.col('modified_at').isNull() | F.col('amount').isNull()
           | F.col('currency_code').isNull())
bad = raw.where(invalid)
good = raw.where(~invalid)
bad.write.format('delta').mode('overwrite').save(quarantine_path)

keys = ['source_system', 'transaction_id', 'line_id']
## Assert one payload per key + source_sequence; contradictory ties fail
## rather than being silently chosen by nondeterministic ordering.
conflicts = (good.groupBy(*(keys + ['source_sequence']))
             .agg(F.countDistinct(F.struct('amount', 'currency_code',
                                          'modified_at')).alias('payloads'))
             .where('payloads > 1'))
if conflicts.limit(1).count():
    raise ValueError('Conflicting payloads for a source sequence')
window = Window.partitionBy(*keys).orderBy(F.col('source_sequence').desc())
latest = (good.dropDuplicates(keys + ['source_sequence'])
          .withColumn('rn', F.row_number().over(window))
          .where('rn = 1').drop('rn'))
latest.createOrReplaceTempView('transaction_latest')
```

Implement format, membership, uniqueness and reconciliation rules separately; null checks alone are not a complete quality framework. The subsequent MERGE target must already exist with a compatible schema. Run the critical quality gate before publication; a valid-row table may be staged even when the batch is held.

### 5. Delta upsert and deletion semantics

```sql
-- Spark SQL / Azure Databricks Delta; source is deduplicated and ordered.
MERGE INTO silver.transaction AS t
USING transaction_latest AS s
ON t.source_system = s.source_system
 AND t.transaction_id = s.transaction_id AND t.line_id = s.line_id
WHEN MATCHED AND s.source_sequence > t.source_sequence THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Keep the source sequence on each current record. A later-arriving older update must not overwrite a newer one. For physical deletes, retain ordering in a tombstone ledger or soft-deleted current row if stale events can be replayed; otherwise an old insert can resurrect a deleted entity. Use delete operations only from an explicit CDC contract or an authoritative complete snapshot, never from absence in a partial batch.

Delta change data feed exposes changes already written to Delta. Enable/configure the supported CDF mode for the chosen Databricks runtime, checkpoint consumers, and plan retention/backfills. Do not promise indefinite history or assume Azure Databricks-specific CDF modes are readable in Fabric.

### 6. SCD Type 2 and historical joins

Choose an entity business key, tracked attributes and effective-time source. Use half-open intervals `[valid_from, valid_to)` and a sentinel or null end date. Assert no overlapping intervals and at most one current row per key.

```sql
-- Spark SQL historical dimension lookup.
SELECT f.transaction_id, f.line_id, d.account_sk, f.amount
FROM silver.transaction f
LEFT JOIN silver.dim_account d
 ON f.account_id = d.account_id
 AND f.event_ts >= d.valid_from
 AND (d.valid_to IS NULL OR f.event_ts < d.valid_to);
```

Count matches: zero requires an approved unknown/suspense policy; more than one is a critical integrity failure. For an out-of-order dimension change, recompute that key's timeline from ordered source history and identify affected facts. A naive close-current-and-insert routine can misrepresent late history. Hashes can compare attributes but are not business keys or proof of equivalence without canonical types/null handling.

### 7. Streaming state and replay

Event Hubs ingestion uses its supported Spark integration for the selected runtime. Persist the original source identifier, event ID, event timestamp and producer sequence. Keep one durable checkpoint per query and environment. Validate connector/authentication options against the installed runtime.

```python
## `events` is an already parsed streaming DataFrame from the approved source.
deduped = (events.withWatermark('event_ts', '2 hours')
           .dropDuplicatesWithinWatermark(['source_system', 'event_id']))
query = (deduped.writeStream.format('delta')
         .option('checkpointLocation', checkpoint_path)
         .outputMode('append').start(bronze_delta_path))
```

The two-hour window is an illustrative configuration, not an SLA. Verify runtime support for `dropDuplicatesWithinWatermark`; if unavailable use an explicitly designed alternative with measured state behavior. Windowed deduplication expires state and can accept replays beyond the horizon. Enforce durable business-key idempotency in silver, retain raw data, and reconcile late partitions. `foreachBatch` handlers must be idempotent because microbatches can execute again; a checkpoint alone does not make arbitrary external writes exactly once.

### 8. Financial and operational reconciliation

Record expected and observed counts and decimal totals at matching grain. Counts alone can miss a duplicated row replacing a missing row. Combine key uniqueness, missing-key comparisons, signed totals, reference coverage and independent samples.

| Control | Expected evidence | Failure action |
|---|---|---|
| Manifest completeness | Declared files/rows vs landed files/rows | Hold batch and request missing delivery |
| Key uniqueness | Distinct business keys equal accepted record count | Resolve source duplicates/conflicts |
| Financial amounts | Decimal totals by date/entity/currency | Hold publication and investigate |
| Dimension resolution | Exactly one historical match per eligible fact | Fix timeline or agreed suspense policy |
| Freshness | Last accepted business timestamp vs target | Alert owner even if jobs succeeded |
| Replay | Same input creates same business output | Fix idempotency before go-live |

Define tolerance from an approved rounding/accounting policy; do not use an arbitrary percentage to suppress differences. Keep rejected-row counts in the balance equation. Test `source = accepted + rejected` where the extract contract and deduplication rules make that equation applicable.

### 9. CI/CD and infrastructure

Suggested repository structure:

```text
infra/                 # Bicep/Terraform, parameters, network/identity declarations
pipelines/             # ADF/Fabric definitions and deployment configuration
notebooks/             # parameterized PySpark transformations
sql/                   # metadata DDL and engine-specific serving objects
contracts/             # reviewed schemas and data-product definitions
tests/fixtures/        # synthetic examples and expected outputs
tests/integration/     # connectivity/replay/reconciliation scenarios
monitoring/            # queries, dashboards and alert definitions
runbooks/              # recovery, access and cutover procedures
```

PR validation checks code/contracts and meaningful fixtures. Test deployment creates resources/configuration and executes the vertical slice. Production promotion uses a reviewed artifact, environment identity, approved parameters and release evidence. Fabric Git/deployment support differs by item type; verify the actual items before promising fully automated promotion. Migration rollback can require recovering data, not just reverting a notebook.

### 10. Performance, costs and observability

Measure extraction bottleneck, shuffle volume, skew, file counts, read amplification, concurrency and serving query latency. Tune one measured bottleneck at a time. Do not apply repartition, caching, broadcast joins, clustering or partitioning mechanically. Avoid tiny files and full-table scans in daily incremental jobs. Run maintenance only under the retention policy; aggressive VACUUM can remove replay/time-travel data still needed by consumers.

Monitor pipeline failure, accepted-data age, reconciliation difference, quarantine rate, streaming lag, execution duration and cost per accepted batch. Use ADF diagnostics and Azure logs where available; use Fabric monitoring and capacity metrics for Fabric workloads rather than assuming all internal events automatically appear in Log Analytics. Benchmark representative data and concurrency and retain before/after results.

### 11. Production recovery runbook

1. Identify the failed run, entity, boundary, input manifest and affected consumers.
2. Prevent concurrent publication for the affected entity; preserve raw input and error evidence.
3. Determine whether landing, transformation, quality, serving publication or state update failed.
4. Resume from the durable phase using the same business input. If publication succeeded but state did not, reconcile the manifest and advance state without appending duplicate facts.
5. Revalidate keys, amounts, quality and access; release only the accepted output.
6. Confirm freshness restored, communicate through the approved incident route, and document root cause and prevention.

Recovery objectives must be backed by tested infrastructure/data restoration. Delta time travel alone is not a complete disaster recovery strategy. Agree source retention, checkpoints, configuration backups, identity/network recovery and regional constraints.

### 12. Completion checklist and evidence form

- [ ] Source owner and data-product owner confirmed.
- [ ] Source snapshot/change semantics documented, including deletes.
- [ ] Reconciliation, critical quality gates and access tests passed.
- [ ] Replay, partial failure, late data and schema-change scenarios passed.
- [ ] Deployment/rollback/recovery demonstrated in the target environment.
- [ ] Freshness, RPO/RTO and cost targets agreed and measured.
- [ ] Consumer acceptance recorded with run/publication IDs.

```text
Project / entity:
Input manifest / source boundary:
Contract / rule version:
Run ID / publication ID:
Source / accepted / rejected counts:
Reconciliation totals / differences:
Failure and replay evidence:
Performance baseline / result / measurement period:
Access test identities and outcomes:
Business acceptance owner and date:
```

### Official technical references

- [Fabric medallion lakehouse architecture](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture)
- [Fabric end-to-end lakehouse tutorial](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-introduction)
- [ADF incremental ingestion with watermarks](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-portal)
- [Azure Databricks MERGE reference](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)
- [Azure Databricks change data feed](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed)
- [Microsoft Purview governance setup](https://learn.microsoft.com/en-us/purview/data-governance-get-started)
