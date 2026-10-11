"""Add detailed Mermaid diagrams and operational flows to existing Markdown files."""
from pathlib import Path
import ast

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'Azure_Data_Engineering_Portfolio'
tree = ast.parse((BASE / 'build_documents.py').read_text(encoding='utf-8'))
assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'projects' for t in n.targets))
namespace = {}
exec(compile(ast.Module(body=[assignment], type_ignores=[]), '<project metadata>', 'exec'), namespace)
projects = namespace['projects']

DETAILS = {
'01': {
'diagram': '''flowchart TD
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
  T --> I''',
'domain': '''flowchart LR
  A[Accepted transaction line] --> B[Resolve account version at event time]
  B --> C[Resolve customer and product attributes]
  C --> D[Preserve original decimal amount and currency]
  D --> E[Join approved FX rate by date and rate type]
  E --> F{Required reference available?}
  F -->|No| G[Hold or approved suspense treatment]
  F -->|Yes| H[Calculate reporting amount under rounding policy]
  H --> I[Gold transaction fact with source and FX identifiers]
  J[Authoritative daily balance extract] --> K[Validate account date and currency grain]
  K --> L[Gold daily balance fact]
  I --> M[Reconcile transaction totals]
  L --> N[Reconcile balance snapshot totals]
  M --> O[Accepted banking publication]
  N --> O''',
'entities': [
('Transactions','Transaction + line + source system','Bounded change feed or approved extract','Signed posted activity; reversals retain their source identity'),
('Accounts and customers','Source key plus effective interval','Snapshot followed by ordered changes','Historical versions used by event-time fact joins'),
('FX rates','Pair + rate date + approved rate type','Validated reference delivery','Original amount plus converted amount and rate provenance'),
('Daily balances','Account + business date + currency','Authoritative daily snapshot','Snapshot totals; no summation across reporting dates')],
'worked': '''Consider an illustrative transaction line `TX100 / 1` for account `A100`, posted at 10:00 UTC on 2026-10-01, with an original amount of EUR 100.00. The account is mapped to the customer version effective at 10:00, and the approved EUR-to-reporting-currency rate for that business date is looked up. If the illustrative rate were 1.10, the converted amount would be 110.00 before any agreed rounding; the actual rate must come from the approved reference feed.

Bronze retains the received row and delivery ID. Silver retains its business key, source sequence, original amount, and historical dimension references. Gold retains both currencies, amounts, and the FX identifier so a reviewer can explain the conversion. A duplicate with the same source sequence does not increase the transaction total. A higher-sequence correction supersedes the current line and triggers reconciliation of the affected day. A reversal is represented according to the source contract, preserving a link to the original transaction.

An account's closing balance comes from the approved snapshot or an agreed balance derivation with an opening value and complete posted activity. The semantic model returns a selected-date snapshot. It must not add ten daily closing balances and present the sum as the account's current balance.''',
'dependencies': 'Customer/account and reference versions must be accepted before dependent transaction facts are resolved. FX availability is required for reporting-currency facts. Balance publication can have its own accepted boundary if its contract is independent; the combined report must display the relevant as-of dates.',
'consumer': 'A banking analyst filters country, product and business date in the semantic model. Measures use accepted transaction facts and selected-date balance facts. An authorized engineer querying the SQL endpoint still needs underlying data permissions; semantic-model row filters are verified separately.',
'optimization': 'Measure Fabric capacity utilization, notebook duration, reference-join volume and BI query latency. Use explicit schemas and incremental affected-date processing first; tune capacity or layout only after identifying the bottleneck.',
'orchestrator': 'Fabric pipeline', 'processor': 'Fabric Spark notebook', 'store': 'OneLake', 'serve': 'Power BI and SQL endpoint',
},
'02': {
'diagram': '''flowchart TD
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
  Q --> R[Approved retirement of legacy jobs]''',
'domain': '''flowchart TD
  A[Document source snapshot semantics] --> B[Capture snapshot and ordered change boundary]
  B --> C[Copy historical chunks with manifests]
  B --> D[Retain subsequent source changes]
  C --> E[Load baseline into Delta]
  D --> F[Apply ordered inserts updates and deletes]
  E --> F
  F --> G[Drain catch-up backlog]
  G --> H[Compare key sets totals and rule outputs]
  H --> I{Parity and freshness accepted?}
  I -->|No| J[Hold cutover and investigate]
  J --> F
  I -->|Yes| K[Freeze accepted publication boundary]
  K --> L[Switch approved consumers]
  L --> M[Monitor with documented rollback route]''',
'entities': [
('Historical facts','Source business key + historical date','Bounded snapshot chunks','Replayable migrated history'),
('Position changes','Position key + source sequence','Source-supported CDC where available','Current or historical position state with deletion semantics'),
('Instrument/account reference','Entity key + effective interval','Snapshot and ordered changes','Stable historical joins'),
('Parity evidence','Entity + date + comparison control','Parallel legacy/Azure execution','Accepted differences and cutover evidence')],
'worked': '''Suppose an illustrative historical migration chunk covers 2026-09-01 through 2026-09-07 for one position entity. The migration log records its snapshot/change boundary, source key range, count and totals. The chunk is copied into a unique immutable location and transformed independently of other weeks. A failed chunk can be retried without recopying every historical date.

Source changes occurring after the consistent boundary are retained and applied after the baseline. For example, a position quantity changing from 100 to 120 at sequence 41 must win over a replayed sequence 40. A subsequent delete at sequence 42 removes or marks the position according to the target contract, while a tombstone/history record prevents an old insert from resurrecting it.

Legacy and Azure outputs are compared at the same accepted business boundary. A discrepancy cannot be explained away by comparing different dates, FX versions, or rule versions. Consumers switch only when historical completeness, catch-up freshness, reconciliation, performance and recovery are accepted. An observation period keeps the documented rollback route usable before legacy jobs are retired.''',
'dependencies': 'Backfill chunks can run independently within approved source limits, but catch-up application depends on a valid baseline and an exact handoff boundary. Consumer cutover depends on parity evidence and the change backlog being drained to an accepted point.',
'consumer': 'A downstream consumer reads the same documented dataset contract through Databricks SQL or the approved reporting connection. During parallel operation, compare consumer outputs using identical parameters and source boundaries. Record a connection switch and a tested rollback route.',
'optimization': 'Benchmark extraction throughput and source pressure separately from Spark transformation time. Tune chunk size, bounded concurrency, file sizes, skew and serving query plans using observed data; avoid accelerating backfill at the expense of source operational workloads.',
'orchestrator': 'Azure Data Factory', 'processor': 'Azure Databricks job', 'store': 'ADLS and Delta Lake', 'serve': 'Databricks SQL and Power BI',
},
'03': {
'diagram': '''flowchart TD
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
  V -.-> O''',
'domain': '''flowchart LR
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
  K --> L[Monitor freshness and contract changes]''',
'entities': [
('Contract metadata','Entity + contract version','Reviewed configuration changes','Approved source/schema/ownership contract'),
('Customer crosswalk','Source identity + enterprise mapping interval','Stewarded identity decisions','Traceable enterprise joins'),
('Payment events','Payment + lifecycle event','Batch extracts or event stream','Ordered payment lifecycle and analytical facts'),
('Data products','Product + publication version','Accepted domain processing','SQL/file/API contract and consumer manifest')],
'worked': '''An illustrative payment product receives `PAY100` with lifecycle events `CREATED`, `AUTHORIZED` and `SETTLED`. Each event has a stable source event key and event time. Bronze preserves the complete event history. Silver validates status membership and preserves lifecycle order; a current-status view may select the latest accepted source sequence, but the underlying event fact still retains all three events.

The product owner decides whether the consumer contract exposes events, current payment state, or a daily settled-payment aggregate. These are different grains. Counting three lifecycle events as three settled payments is incorrect. The released product manifest identifies the contract version, accepted input boundary, rule version and quality result.

If the API fails after page 7, the saved cursor and immutable page manifests make recovery bounded. Deduplication protects against a repeated page. A new optional field can follow the approved compatibility policy, while a key type change requires a reviewed version change and consumer migration. An operational API reads a properly sized serving database with bounded queries rather than scanning raw lake files for every request.''',
'dependencies': 'Contracts and permissions precede ingestion. Identity crosswalk/reference versions precede dependent domain joins. Products publish only after all declared dependencies reach an accepted boundary; independent domains can have separate release schedules.',
'consumer': 'A consuming team requests a product version, grain, freshness target and access scope. Bulk consumers use approved SQL/files; operational API consumers use a serving store through controlled endpoints. Deprecation of a breaking contract has an owner, migration date and consumer acknowledgment.',
'optimization': 'Measure source/API throughput, domain transformation cost and product query latency separately. Reuse connectors and validators, but retain explicit domain rules. Batch small API requests where supported and respect source rate limits with bounded retry.',
'orchestrator': 'Azure Data Factory', 'processor': 'Azure Databricks job', 'store': 'ADLS and Delta Lake', 'serve': 'Versioned SQL file or API product',
},
'04': {
'diagram': '''flowchart TD
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
  Q -.-> K''',
'domain': '''flowchart TD
  A[Identify critical data element] --> B[Owner defines rule and eligibility]
  B --> C[Approve severity threshold and version]
  C --> D[Evaluate pinned input snapshot]
  D --> E[Persist tested and failed counts]
  D --> F[Persist restricted exception references]
  E --> G{Critical rule failed?}
  G -->|Yes| H[Hold product and assign owner]
  G -->|No| I[Apply approved advisory policy]
  I --> J[Publish quality status with product]
  H --> K[Investigate and correct]
  K --> L[Revalidate same affected scope]
  L --> M{Controls restored?}
  M -->|No| H
  M -->|Yes| J''',
'entities': [
('Rule definitions','Rule ID + version','Reviewed metadata updates','Approved deterministic validation'),
('Quality results','Rule + input run + tested scope','Per accepted evaluation','Counts, denominators, status and trend'),
('Exceptions','Input record reference + rule + run','Failed record capture','Restricted accountable remediation'),
('Quality gate','Product + input publication','Critical/advisory policy evaluation','Publish or hold decision with evidence')],
'worked': '''For an illustrative run with 1,000 eligible account rows, a required account-ID rule fails on 5 rows. Its failure rate is 5 / 1,000 = 0.5%. If the approved rule is critical and requires zero missing IDs, publication is held even though 99.5% of rows passed. A quality dashboard must show the numerator, denominator, threshold and rule version so the result can be interpreted.

Separately, a balance-plausibility rule may apply only to a particular product/status combination. Its denominator consists of eligible records, not all rows in the table. A negative balance is not automatically invalid; the business owner defines what the balance means and when a negative value is legitimate.

Exceptions retain restricted record references and reason codes. A steward corrects the source or approves a documented rule/reference revision. Engineering reruns the affected scope, records the new evaluation and resolves the exception after the controls pass. Removing exceptions from a dashboard without fixing/revalidating the data does not constitute remediation.''',
'dependencies': 'An approved rule version and pinned input must exist before evaluation. Quality results are persisted before the publish/hold decision. Exceptions can be worked in parallel by owners, but publication depends on the critical-rule policy and reconciliation acceptance.',
'consumer': 'The product consumer sees data quality status and accepted as-of time. A steward sees restricted exceptions for assigned domains. A general dashboard user sees aggregate results without sensitive failed payloads. Verify these access paths with separate identities.',
'optimization': 'Group compatible rules to avoid repeated full scans, while preserving independent rule counts and eligibility. Measure predicate cost and result volume. Cache only reused datasets that fit the intended execution pattern; do not collect exception payloads to the driver.',
'orchestrator': 'Azure Data Factory', 'processor': 'Databricks quality evaluator', 'store': 'ADLS and Delta Lake', 'serve': 'Governed product and quality scorecard',
},
'05': {
'diagram': '''flowchart TD
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
  S --> G''',
'domain': '''flowchart TD
  A[Journal line with source business key] --> B[Parse debit and credit decimals]
  B --> C[Validate posting date entity and currency]
  C --> D[Resolve historical chart-of-account mapping]
  D --> E{Exactly one approved mapping?}
  E -->|No| F[Controlled suspense and held publication]
  E -->|Yes| G[Reconcile journal and ledger totals]
  G --> H[Load batch-isolated warehouse staging]
  H --> I[Validate dimension and fact references]
  I --> J{Period publication allowed?}
  J -->|Open| K[Publish accepted period output]
  J -->|Closed| L[Authorized correction or reopen workflow]
  L --> K
  K --> M[Retain revision and acceptance evidence]''',
'entities': [
('Journal lines','Source + journal ID + line ID','Approved ledger delivery/change feed','Financial line-level fact'),
('Legal entity and GL dimensions','Business key + effective interval','Versioned reference changes','Historical reporting mapping'),
('Trial balance','Entity + account + currency + period','Authoritative period snapshot','Period totals under agreed sign convention'),
('Reconciliation controls','Run + entity + period + control','Source/stage/fact validation','Accepted warehouse and close evidence')],
'worked': '''An illustrative journal has a debit of GBP 100.00 to one account and a credit of GBP 100.00 to another account. Both source lines retain their source system, journal ID and line ID. The control verifies balancing at the scope agreed with the ledger owner; it does not mix currencies or silently round away a discrepancy.

The posting date resolves the historical legal-entity and chart-of-account versions. If an account is remapped to a reporting line later, the original journal uses the mapping effective for its posting date unless a separately approved restatement policy says otherwise. The transformation exports only an accepted batch to Parquet for warehouse loading.

Synapse staging is isolated by batch so another run cannot overwrite inputs during publication. The fact load is validated before acceptance. A correction to a closed period follows the period correction/reopen workflow and creates traceable reporting revision evidence. Trial balances are snapshots at entity/account/currency/period grain; their reporting aggregation must follow the accounting contract rather than indiscriminately summing periods.''',
'dependencies': 'Reference and effective-dated dimensions must be available before journal fact key resolution. Accepted lake transformations precede Parquet export and Synapse staging. Warehouse reconciliation and period-state approval precede consumer publication.',
'consumer': 'Finance users read approved warehouse views and semantic models with explicit period, legal-entity, currency and revision filters. A warehouse read path must expose the accepted reporting state, not staging tables or an incomplete period load.',
'optimization': 'Measure extraction, Databricks transformation, Parquet export, warehouse load and reporting queries separately. Choose warehouse distribution based on actual join/filter patterns and skew; verify batch loads and update patterns against the selected Synapse engine.',
'orchestrator': 'Azure Data Factory', 'processor': 'Databricks and Synapse load jobs', 'store': 'ADLS Delta and Synapse staging', 'serve': 'Accepted Synapse reporting views',
},
'06': {
'diagram': '''flowchart TD
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
  R --> U''',
'domain': '''flowchart TD
  A[Usage event arrives with stable event key] --> B[Persist raw event and source envelope]
  B --> C[Validate timestamp units and identifiers]
  C --> D{Already applied to silver?}
  D -->|Yes same payload| E[Ignore duplicate business event]
  D -->|Conflicting payload| F[Source ordering or correction workflow]
  D -->|No| G[Apply durable silver event]
  G --> H[Resolve subscriber and tariff at event time]
  H --> I[Identify affected usage date and billing period]
  I --> J[Rebuild aggregate from accepted silver]
  J --> K[Reconcile count duration bytes and charge rules]
  K --> L[Release accepted gold update]
  M[Late event outside streaming horizon] --> B
  F --> G''',
'entities': [
('Usage/CDR events','Source system + event ID','Checkpointed events and approved replay','Durable usage facts with corrected event semantics'),
('Subscriber/tariff versions','Source key + effective interval','ADF reference delivery','Historical plan and tariff enrichment'),
('Daily usage','Subscriber + service + usage date','Rebuild affected date from silver','Count/duration/volume totals'),
('Billing comparison','Account + service + billing period','Approved rating and billing extracts','Traceable expected-vs-billed comparison')],
'worked': '''An illustrative data-session event `CDR100` for subscriber `S100` occurs at 23:59 UTC and contains 1,024 bytes. Bronze stores the envelope and payload. Silver validates the event key and byte unit, resolves the subscriber/plan version effective at 23:59, and retains one accepted usage event.

If the same event is replayed three times, its durable business key ensures the daily count stays one and bytes stay 1,024. A streaming watermark only bounds in-memory state; it does not replace durable protection against a replay that arrives days later. If a correction has a higher approved source sequence, the silver record changes and the affected daily aggregate is rebuilt from the accepted event set.

The usage date follows the agreed UTC or local business-date policy. Billing-period comparison uses the actual approved tariff rules, including bundles, rounding and promotions. The daily usage dataset may be provisionally current while a billing-period product waits for completeness; its consumer status must make that distinction visible. For a broker outage beyond retention, retained raw/archive data and source recovery supply the missing events.''',
'dependencies': 'The stream can persist bronze independently of reference availability. Historical enrichment and billing products require accepted subscriber/tariff versions. Billing comparison also requires complete approved billing-period extracts and rating rules.',
'consumer': 'Network/usage analysts read daily subscriber/service aggregates with accepted as-of and completeness metadata. Billing analysts read period-level comparison products with the relevant tariff/rule version. Subscriber/location fields are masked or restricted according to their approved access scope.',
'optimization': 'Measure broker lag, processing latency, state-store size, checkpoint health, data skew and aggregation cost. Tune stream partitioning and microbatch work based on observed throughput; keep reference-feed scheduling and expensive historical rebuilds from blocking raw event capture.',
'orchestrator': 'ADF and streaming job controller', 'processor': 'Databricks streaming and batch jobs', 'store': 'ADLS and Delta Lake', 'serve': 'Databricks SQL and Power BI',
},
}

def diagram(code):
    return '```mermaid\n' + code + '\n```\n'

def sequence(d):
    return f'''sequenceDiagram
  autonumber
  participant SRC as Approved source
  participant ORC as {d['orchestrator']}
  participant CTL as Durable run control
  participant RAW as Immutable landing or bronze
  participant ENG as {d['processor']}
  participant GATE as Quality and reconciliation
  participant PUB as Accepted publication
  participant USER as {d['serve']}
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
  ORC->>CTL: Release lease and finalize run status'''

recovery = '''flowchart TD
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
  N --> O[Close incident with root cause and evidence]'''

security = '''flowchart LR
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
  K -.-> G'''

deployment = '''flowchart TD
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
  L -->|No| N[Record accepted release and operating baseline]'''

stage_states = '''stateDiagram-v2
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
  HELD --> TRANSFORMED: Correct and replay affected input'''

for p in projects:
    d = DETAILS[p['id']]
    path = ROOT/'projects'/f"{p['id']}_{p['slug']}.md"
    original = path.read_text(encoding='utf-8').split('\n<!-- EXPANDED_FLOW_START -->')[0].rstrip()
    entities = '| Input group | Business grain | Ingestion contract | Result |\n|---|---|---|---|\n'
    entities += '\n'.join('| '+' | '.join(row)+' |' for row in d['entities'])
    stages = '\n\n'.join(
        f"### Stage {i}: {name}\n\n{body}\n\n"
        f"**Execution evidence:** record the input scope, source/run boundary, applicable contract or rule version, produced artifact and acceptance status for this stage. "
        f"The next dependent stage consumes its accepted output; an execution timestamp alone is insufficient evidence of correctness."
        for i,(name,body) in enumerate(p['steps'],1))
    addition = f'''

<!-- EXPANDED_FLOW_START -->

## Full flow diagrams and detailed execution narrative

The following diagrams expand the entire reference project lifecycle. Solid arrows indicate the stated data or workflow direction; dotted arrows indicate supporting configuration, catalog or security relationships. These are proposed designs and must be checked against the actual engagement.

### Diagram 1: Complete project data flow

{diagram(d['diagram'])}

**How to read the diagram:** start with the source groups, follow ingestion into durable raw/bronze data, then follow validated transformations into the accepted serving dataset. The rejection paths are part of the production flow: a held run retains its input and evidence so the owner can investigate and engineering can replay the affected scope. Raw inputs, staged output and accepted publications are different artifacts.

### Source-to-output contracts

{entities}

For every input, confirm the owner, business key, event/effective timestamp, source change sequence, extraction boundary, deletion semantics and reference dependencies. Choose snapshot, watermark, CDC or event ingestion from those semantics. Do not assume a file delivery is complete merely because the file is readable.

### Diagram 2: Runtime interaction from source to consumer

{diagram(sequence(d))}

This sequence describes an accepted batch or publication cycle. For streaming, raw events are persisted continuously and product publication follows the chosen microbatch/date policy; an ADF schedule is not required for every event. The control store holds durable state, while the accepted publication records the actual output exposed to consumers. Where these sit in different systems, recovery reconciles their manifests instead of assuming a shared atomic transaction.

### Detailed stage explanations

{stages}

### Diagram 3: Project-specific business transformation

{diagram(d['domain'])}

**Business meaning:** {p['problem']} The diagram highlights where the project-specific rules alter the data's meaning, grain or reporting status. Technical success at these stages does not substitute for the business control evidence described below.

### Worked record journey

{d['worked']}

The example is synthetic and demonstrates behavior, not actual client data or a measured client outcome. Trace a record using its source business key, source sequence, raw location, run ID, contract/rule version and accepted publication ID. Avoid putting sensitive payload values in general logs.

### Dependencies, scheduling and publication boundaries

{d['dependencies']}

Keep a dependency manifest for each publication. It should identify the accepted source/reference versions, transformed partition scope and resulting output version. A successful upstream run is usable only if its controls passed and its artifact matches the downstream contract. Run independent entities concurrently only within the approved resource/source limits; serialize publication where concurrent writers could conflict.

**Suggested parameter contract:** `entity_id`, `run_id`, `business_date` or bounded change range, `contract_version`, `rule_version`, `input_manifest_uri`, `output_stage_uri`, `environment`, and `replay_mode`. Validate values and allow-list identifiers. Use the same input/rule scope during a replay unless the run explicitly records an approved correction.

### Diagram 4: Lifecycle and acceptance states

{diagram(stage_states)}

`STARTED` means a run exists; `LANDED` means its inputs are durable; `TRANSFORMED` means a candidate output exists; `VALIDATED` means the critical checks passed; `PUBLISHED` means consumers can read the accepted output. `HELD` indicates a deliberate business/control stop and `FAILED` indicates an execution failure. Extend the handbook's minimal control-table status constraint if you implement these additional states. The diagram is a recommended lifecycle, not a claim that the existing example DDL already includes every state.

Track state transitions with timestamps, actor/workload identity, reason and artifact IDs. A retry is an attempt tied to the original business input. Replaying a publication should not create extra fact rows, duplicate daily aggregates or misleading extra accepted runs.

### Diagram 5: Error handling, late correction and recovery

{diagram(recovery)}

**Project recovery scenario:** {p['scenario']}

Before retrying, determine whether the failure occurred before or after publication. A run can publish successfully and fail while recording its state; a blind repeat can double-count outputs. Inspect the accepted manifest, compare expected key/count/control evidence, and complete or roll back the recorded state safely. Missing or corrupt inputs require source correction; transformation fixes require versioned code; business-control failures require the relevant owner's resolution.

For a late correction, identify affected event dates, historical dimension intervals and dependent aggregate/reporting periods. Recompute the smallest complete business scope rather than updating only an arbitrary file. Preserve old publication metadata and make consumer as-of/revision information clear.

### Diagram 6: Identity, access and governance flow

{diagram(security)}

Permissions are enforced at the workload, storage/catalog and serving layers used by this project. The catalog documents ownership and classification; permissions still need implementation and testing. Validate engineer, workload, steward and consumer paths independently, including raw, quarantine, direct SQL and dashboard exports. A masked dashboard does not justify unrestricted raw access.

Use approved identities for source connections and pipeline execution. Key Vault applies to supported external-secret scenarios; configure Fabric connection credentials through supported mechanisms rather than assuming Azure managed identity works identically for every connector. Network restrictions, retention and residency settings are environment-specific controls to verify during deployment.

### Diagram 7: Development-to-production deployment flow

{diagram(deployment)}

Create source contracts, physical schemas and fixtures before building the complete pipeline. Deploy infrastructure and configuration first, then compatible tables and transformations, then orchestration and serving objects. Test one vertical slice before adding volume or source variants. Promote reviewed artifacts with separate environment parameters and identities. Confirm the selected Azure/Fabric item's deployment support instead of assuming every object uses the same release mechanism.

Production smoke validation checks source reachability, identity permissions, small bounded processing, accepted publication and consumer reads. If a release changes stored data/schema, the rollback plan must cover those data changes as well as code. Record who owns the decision and where the recovery evidence is stored.

### Consumer request and reporting behavior

{d['consumer']}

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

{d['optimization']}

Alert on accepted-data age as well as job failure. A pipeline can finish successfully while a source feed is stale or the product remains held. Dashboard a last accepted timestamp and business freshness target, and route each alert to its actual owning team.

### Project-specific completion and interview evidence

{chr(10).join('- '+x for x in p['checks'])}
- Demonstrate normal flow, rejected flow, duplicate replay and a late correction using synthetic/approved fixtures.
- Verify the diagram against deployed resources, connections, code and actual publication artifacts.
- Keep one accepted-run evidence packet linking manifest, controls, serving dataset and consumer acceptance.
- Replace illustrative names, example dates, sources and targets with verified engagement details before discussing them as past experience.

**Interview explanation:** draw Diagram 1, describe the worked record journey, identify your own implemented stages, explain Diagram 3's business rules, show how the critical gate protects publication, then use Diagram 5 to explain a concrete recovery. Finish with the verified output and a measured result supported by evidence.

### Plain-text fallback flow

Some Markdown viewers do not render Mermaid. The original architecture section and the following text retain the core flow in those viewers:

```text
{p['flow']}
1. Confirm source contract and accepted dependencies.
2. Persist identifiable raw input and manifest.
3. Apply ordered, versioned business transformations.
4. Validate critical rules and source-to-target controls.
5. On failure: hold -> investigate -> correct -> replay -> revalidate.
6. On acceptance: publish -> record accepted boundary -> expose to consumers.
7. Monitor freshness, correctness, access, performance and recovery.
```
'''
    path.write_text(original + addition, encoding='utf-8')

atlas = '''# Full project flow diagram atlas

This Markdown document collects the six full data-flow diagrams. Open each detailed project document for its complete runtime sequence, business transformation, lifecycle, recovery, security and deployment diagrams, plus stage explanations and worked examples. All architectures remain proposed reference designs until verified against actual experience.

Mermaid-capable Markdown viewers render the diagrams. Text architecture flows remain available in each project file for viewers without Mermaid support.

'''
for p in projects:
    atlas += f"## {p['client']}: {p['title']}\n\n"
    atlas += diagram(DETAILS[p['id']]['diagram'])+'\n'
    atlas += f"[Open the full project flow and technical explanation](projects/{p['id']}_{p['slug']}.md).\n\n"
(ROOT/'FULL_PROJECT_FLOW_DIAGRAMS.md').write_text(atlas,encoding='utf-8')

index_path = ROOT/'README.md'
index = index_path.read_text(encoding='utf-8').split('\n<!-- FLOW_INDEX_START -->')[0].rstrip()
index += '''

<!-- FLOW_INDEX_START -->

## Expanded full-flow documentation

[Open the full project flow diagram atlas](FULL_PROJECT_FLOW_DIAGRAMS.md).

Each of the six project Markdown files now includes seven Mermaid diagrams: complete data flow, runtime sequence, project-specific business transformation, lifecycle states, failure/replay recovery, security/governance, and development-to-production deployment. Each also includes source-to-output contracts, a detailed stage narrative, a worked record journey, dependencies, publication behavior, consumer flows, observability and acceptance evidence.

The atlas collects the six complete project data-flow diagrams. Mermaid requires a compatible Markdown viewer; plain-text flows are retained in every project document. These files specify reference implementations and have not deployed or executed Azure resources.
'''
index_path.write_text(index,encoding='utf-8')
print('Expanded six project Markdown files with 42 Mermaid diagrams; created six-diagram atlas.')
