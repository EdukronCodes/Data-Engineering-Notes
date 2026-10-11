# Azure SQL Database — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Managed relational storage, metadata control, transactional serving and query optimization.

**Audience:** Azure data engineering interviews, from fundamentals through production troubleshooting and design. Each question has exactly two detailed prose paragraphs: the first explains the concept or resolution, and the second develops its practical application and checks. Scenario answers cover the cause, investigation, correction and verification. Check source semantics, engine/runtime, workload identity and acceptance evidence for your actual configuration. Practice scenarios are hypothetical and are not claims about the named client projects.

## Contents

- A. Core interview questions — C01–C10.
- B. Advanced implementation questions — A01–A05.
- C. Scenario-based interview questions — S01–S25.
- D. Practical implementation exercises — P01–P05.
- E. Architecture and project discussion — D01–D05.
- Revision notes, scoring and official references.

## Role in the full project flow

```text
Approved client identity -> parameterized SQL -> relational tables and transaction -> accepted result -> application or orchestration consumer
```

For this guide, the primary unit is **one transactional SQL operation or control-state update**. The engineering artifacts are database schema, procedures, connection configuration and migration scripts. Troubleshooting starts with Query Store plans, database resource metrics, waits and transaction state; durable progress/evidence is represented by transaction commit, entity-state version and accepted run/publication record. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is Azure SQL Database?

A managed relational database service that handles platform functions such as patching and supported backups. Application schemas, queries and access still require design. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Keep schema/query/access ownership explicit even when infrastructure is managed, and distinguish database availability from correct application/control-state behavior.

### C02. How does it differ from SQL Server on a VM?

The managed service removes much infrastructure administration but has service-specific feature/configuration boundaries. A VM provides broader instance/OS control with more operational ownership. Deployment models expose different operational/feature boundaries. Evaluate required instance features, connectivity, recovery and administration rather than assuming complete interchangeability.

An existing SQL Server integration may need redesign before moving from a VM to a managed database. Inventory instance features and operational dependencies first, then validate the supported managed-service migration rather than assuming every VM-based integration transfers unchanged.

### C03. What is an elastic pool?

A set of databases sharing configured resources. It can suit variable database usage, but noisy neighbors and per-database limits must be considered. Shared resources suit variable workloads only when combined peak use and isolation needs are understood. Track individual databases and noisy-neighbor behavior.

Several modest metadata databases can share a pool if concurrent releases/loads remain within accepted service targets. Measure overlapping peaks and per-database resource pressure, and choose sharing only when service targets and isolation remain acceptable under realistic concurrency.

### C04. How do provisioned and serverless compute differ?

Provisioned compute supplies configured capacity; supported serverless configurations scale compute according to the service model. Validate tier eligibility, resume latency and billing behavior. Compute configuration affects latency, scale and cost under supported tier behavior. Validate actual cold/resume and peak patterns, not only average utilization.

An intermittent API database has different requirements from continuously active ingestion metadata. Validate the target tier's supported scaling/resume behavior and include its observed latency/cost tradeoff in the workload decision.

### C05. What is Query Store?

A database feature for retaining query/plan/runtime information useful in regression analysis. It helps compare observed execution behavior over time. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Correlate plan/runtime changes with parameters, statistics and data volume before forcing a fix, and retain comparable before/after execution evidence.

### C06. How do indexes affect reads and writes?

They can improve selected access paths but add storage and write maintenance. Choose from query predicates/joins and measured plans. Index benefit follows the query's access patterns. Excess indexes impose write/maintenance cost and may not address blocking or a bad join.

Index an appropriate entity/status/time lookup after reviewing the actual predicate and plan. Evaluate read benefit against insert/update maintenance, and verify the chosen index addresses the actual predicate or join instead of creating redundant write overhead.

### C07. What are transactions used for?

Grouping compatible changes with atomic commit/rollback and isolation semantics. External storage writes are not automatically included in a database transaction. A database transaction coordinates compatible database changes, not arbitrary cloud files. Cross-system workflows require durable acceptance and recovery reconciliation.

A transaction updates the run record and watermark only after the identified gold publication is validated. Keep transactions short and supported while ensuring the accepted business state is complete; cloud table publication needs a separate durable coordination contract.

### C08. How do you authenticate securely?

Use supported Microsoft Entra/workload identity patterns and least-privilege database grants; store necessary secrets securely when identity-based access is unavailable. Authentication identifies the caller; grants authorize its database actions. Network connectivity is another separate condition.

The ADF identity needs the specific metadata procedure permission, not an administrator's interactive credential. Test the actual caller's authentication, object/execute grants and network route separately, rather than copying administrator access into the runtime configuration.

### C09. What are source consistency requirements for extraction?

The extraction must read a defined snapshot/change boundary. Concurrent updates can make arbitrary paginated reads inconsistent. Consistent extraction requires a source snapshot/change contract under concurrent writes. Deterministic pagination alone cannot find every backdated update or hard delete.

Pair a documented snapshot with retained ordered changes for a migration baseline. Specify change/delete semantics and accepted extraction boundaries with the source owner, because repeated paging over mutable rows can yield inconsistent results.

### C10. How are automated backups different from tested recovery?

Backups provide recovery capabilities under service settings; tested recovery proves the application, identities and consumers can resume within agreed objectives. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection.

Switch approved routing and validate one accepted pipeline/control update after restoration. Validate restored identities, endpoint routing, schema compatibility and downstream state before allowing consumers to treat the database as recovered.

## B. Advanced implementation questions

### A01. How do you diagnose CPU versus blocking issues?

Compare resource metrics with Query Store, waits and active transactions. Query inefficiency and lock contention need different fixes. CPU saturation, waiting on locks and I/O pressure indicate different bottlenecks. Use query/transaction evidence before changing capacity.

A blocked watermark update needs lock/transaction investigation rather than simply more vCores. Use query and wait evidence to identify the bottleneck, then measure one correction under the same concurrency rather than relying only on aggregate utilization.

### A02. How do you coordinate an orchestration watermark?

Use an entity lease or serialized owner and compare-and-set updates, preserving run/publication evidence. Reconcile cross-system commits after failures. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules.

Only the run holding the entity token may advance its accepted watermark from the expected old version. Handle abandoned ownership and expected-state mismatches explicitly, so an old run cannot overwrite a boundary advanced by another accepted execution.

### A03. How should an API paginate mutable records?

Use a documented consistency contract and stable keyset cursor where appropriate. Cursor order does not capture all backdated changes automatically. API pagination must define what remains stable while records change. Keyset cursors improve some access patterns but not all extraction completeness risks.

A mutable customer listing still needs a snapshot or reviewed overlap/change strategy. Retain a consistent snapshot/change strategy and define duplicates/late updates, since cursor ordering alone does not prove complete source capture.

### A04. How do you choose a service tier?

Measure workload latency, concurrency, resource pressure, recovery and cost needs, then validate supported tier features. Avoid quoting unverified current limits. Tier selection is an empirical service/cost decision with feature constraints. Exact current capacities and capabilities need official configuration-specific checks.

Benchmark metadata peaks and recovery requirements before selecting or reducing the database tier. Benchmark representative peaks and recovery targets, and verify configuration-specific current features before quoting service capacity or making a tier recommendation.

### A05. How do you make schema migrations safe?

Deploy compatible changes, validate data/backfills and coordinate consumer versions. DDL rollback alone may not restore transformed data. Compatible migrations reduce downtime while consumers move. Backfills and destructive transformations need data recovery, not merely a reverse DDL command.

Add a nullable reviewed field first, backfill/test it, then migrate readers before removing the old field. Coordinate consumer compatibility and backfill/recovery before destructive changes, since reverting application code may still leave the database in an incompatible state.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A metadata lookup becomes slow as pipeline runs accumulate. What do you inspect?

Check filters/indexes, execution plan and table retention. Keep active state small while preserving appropriately indexed run history. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. Two pipelines claim the same entity. How do you prevent it?

Use a transactional claim/lease or approved serialization and an ownership token; expire/recover abandoned leases safely. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules.

Only the run holding the entity token may advance its accepted watermark from the expected old version. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. CPU is high but adding capacity barely helps. Why?

Inspect query plans, scan volume, expensive expressions and contention. Scaling does not remove inefficient access or incorrect join grain. CPU saturation, waiting on locks and I/O pressure indicate different bottlenecks. Use query/transaction evidence before changing capacity.

A blocked watermark update needs lock/transaction investigation rather than simply more vCores. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A procedure works for an administrator but not a workload identity. What do you test?

Check the effective contained identity and required object/execute privileges, connection token and network route. Authentication identifies the caller; grants authorize its database actions. Network connectivity is another separate condition.

The ADF identity needs the specific metadata procedure permission, not an administrator's interactive credential. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. The database is reachable publicly but not through a private route. What is likely missing?

Validate endpoint/DNS configuration and workload connectivity; authentication alone does not fix routing. Authentication identifies the caller; grants authorize its database actions. Network connectivity is another separate condition.

The ADF identity needs the specific metadata procedure permission, not an administrator's interactive credential. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A watermark update succeeds although gold publication failed. What is wrong?

The acceptance sequence is incorrect. Restore/reconcile the accepted source boundary and advance only after validated publication evidence. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules.

Only the run holding the entity token may advance its accepted watermark from the expected old version. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. An API request retries an insert and creates two rows. What prevents it?

Use a stable idempotency/business key with a supported unique constraint and transaction-aware request handling. A database transaction coordinates compatible database changes, not arbitrary cloud files. Cross-system workflows require durable acceptance and recovery reconciliation.

A transaction updates the run record and watermark only after the identified gold publication is validated. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A point-in-time restore produces a new database. What else needs recovery?

Validate connection routing, identities/grants, schema version, application state and downstream reconciliation before consumer switch. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection.

Switch approved routing and validate one accepted pipeline/control update after restoration. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. Reporting queries block metadata updates. What can you change?

Review query duration/access paths and isolation behavior; isolate workloads or use suitable serving architecture without compromising transaction correctness. CPU saturation, waiting on locks and I/O pressure indicate different bottlenecks. Use query/transaction evidence before changing capacity.

A blocked watermark update needs lock/transaction investigation rather than simply more vCores. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. A scale-down causes unacceptable latency. How do you evaluate it?

Benchmark representative concurrency and active resource pressure, then match tier/capacity to the agreed service target rather than average utilization. Tier selection is an empirical service/cost decision with feature constraints. Exact current capacities and capabilities need official configuration-specific checks.

Benchmark metadata peaks and recovery requirements before selecting or reducing the database tier. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one transactional SQL operation or control-state update to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate Entra/database identity, object grants, firewall/private-route configuration. Compare production with the working configuration using Query Store plans, database resource metrics, waits and transaction state; do not resolve the incident by giving every identity broad access. Authentication identifies the caller; grants authorize its database actions. Network connectivity is another separate condition. Investigate under the real caller rather than the interactive administrator. The relevant path is Entra/database identity, object grants, firewall/private-route configuration. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

The ADF identity needs the specific metadata procedure permission, not an administrator's interactive credential. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Azure SQL Database is available, but the business result has not advanced. What would you check?

Trace the expected operation through application/ADF caller and source or consumer contract and compare progress in transaction commit, entity-state version and accepted run/publication record. Inspect Query Store plans, database resource metrics, waits and transaction state to distinguish a service being reachable from an accepted business operation actually completing. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules. Walk the dependency chain through application/ADF caller and source or consumer contract and locate the last accepted evidence in transaction commit, entity-state version and accepted run/publication record. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

Only the run holding the entity token may advance its accepted watermark from the expected old version. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of database schema, procedures, connection configuration and migration scripts works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual relational schema, unique keys, isolation and API/metadata semantics. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics. Treat the release as a change to database schema, procedures, connection configuration and migration scripts and its dependencies, not just to one code file. Compare relational schema, unique keys, isolation and API/metadata semantics and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one transactional SQL operation or control-state update although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with Query Store plans, database resource metrics, waits and transaction state and inspect CPU, I/O, plan regression, blocking and connection pressure. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes. Use Query Store plans, database resource metrics, waits and transaction state to compare the same business boundary and concurrency against a known-good baseline. Examine CPU, I/O, plan regression, blocking and connection pressure and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Azure SQL Database may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in transaction commit, entity-state version and accepted run/publication record before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. A database transaction coordinates compatible database changes, not arbitrary cloud files. Cross-system workflows require durable acceptance and recovery reconciliation. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by transaction commit, entity-state version and accepted run/publication record and repeat only through a supported safe operation/status mechanism.

A transaction updates the run record and watermark only after the identified gold publication is validated. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one transactional SQL operation or control-state update at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in transaction commit, entity-state version and accepted run/publication record. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules. Define who owns the shared mutation and which state version each caller expected. Preserve transaction commit, entity-state version and accepted run/publication record so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

Only the run holding the entity token may advance its accepted watermark from the expected old version. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Azure SQL Database without prior notice. How do you contain the impact?

Validate against relational schema, unique keys, isolation and API/metadata semantics and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes. Classify the change against relational schema, unique keys, isolation and API/metadata semantics: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some transaction commit, entity-state version and accepted run/publication record evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of transaction commit, entity-state version and accepted run/publication record and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics. Recovery can reconstruct only what still exists and is consistent. Inventory transaction commit, entity-state version and accepted run/publication record, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in Query Store plans, database resource metrics, waits and transaction state. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review Entra/database identity, object grants, firewall/private-route configuration for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read Query Store plans, database resource metrics, waits and transaction state and derived exports; minimizing the source log alone does not remove already copied sensitive output.

Switch approved routing and validate one accepted pipeline/control update after restoration. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Azure SQL Database accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in database schema, procedures, connection configuration and migration scripts, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against transaction commit, entity-state version and accepted run/publication record before restoring normal processing. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection. Environment validation belongs before mutation. Bind database schema, procedures, connection configuration and migration scripts to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

Switch approved routing and validate one accepted pipeline/control update after restoration. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Application/adf caller and source or consumer contract is temporarily unavailable. What retry and recovery policy fits Azure SQL Database?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved transaction commit, entity-state version and accepted run/publication record; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. A database transaction coordinates compatible database changes, not arbitrary cloud files. Cross-system workflows require durable acceptance and recovery reconciliation. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep transaction commit, entity-state version and accepted run/publication record durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

A transaction updates the run record and watermark only after the identified gold publication is validated. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Azure SQL Database rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect CPU, I/O, plan regression, blocking and connection pressure. Remove demonstrated waste while preserving required transaction commit, entity-state version and accepted run/publication record and correctness/access controls. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to CPU, I/O, plan regression, blocking and connection pressure and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

Switch approved routing and validate one accepted pipeline/control update after restoration. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, database schema, procedures, connection configuration and migration scripts is restored but the business path still fails. What else is required?

Restore/validate Entra/database identity, object grants, firewall/private-route configuration, application/ADF caller and source or consumer contract and the appropriate transaction commit, entity-state version and accepted run/publication record. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate Entra/database identity, object grants, firewall/private-route configuration, reconcile transaction commit, entity-state version and accepted run/publication record and execute a normal authorized consumer path before calling the recovery successful.

Switch approved routing and validate one accepted pipeline/control update after restoration. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Azure SQL Database. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with Query Store plans, database resource metrics, waits and transaction state and validate their relational schema, unique keys, isolation and API/metadata semantics. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes. Find the smallest complete failed business scope using keys/objects and Query Store plans, database resource metrics, waits and transaction state. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow relational schema, unique keys, isolation and API/metadata semantics and preserve a clear accounting of accepted versus failed scope.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change database schema, procedures, connection configuration and migration scripts while dependent workloads remain active. What release sequence would you use?

Inventory consumers and relational schema, unique keys, isolation and API/metadata semantics compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain transaction commit, entity-state version and accepted run/publication record and define a tested rollback/correction route for incompatible behavior. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep transaction commit, entity-state version and accepted run/publication record and a tested correction/rollback boundary so a partially applied release remains recoverable.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Validate the accepted result and the intended relational schema, unique keys, isolation and API/metadata semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Build a safe entity-state update procedure.

Require expected previous state/version and an owning run token; transactionally record the new accepted boundary and run result. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules.

Only the run holding the entity token may advance its accepted watermark from the expected old version. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Analyze a query regression with Query Store.

Compare historical/current plan/runtime, data changes, waits and indexes; validate one corrective change with equivalent parameters. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Design a restore-and-cutover rehearsal.

Specify restore boundary, connection/identity validation, application checks, downstream reconciliation and measured recovery time. Recovery success includes usable endpoints, workload grants and downstream state. A restored database can exist while applications still use the old connection.

Switch approved routing and validate one accepted pipeline/control update after restoration. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one transactional SQL operation or control-state update.

Capture the initial transaction commit, entity-state version and accepted run/publication record, introduce one realistic dependency or validation failure and use Query Store plans, database resource metrics, waits and transaction state to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. State ownership and compare-and-set protect the accepted boundary from concurrent callers. Abandoned leases must expire/recover under defined rules.

Only the run holding the entity token may advance its accepted watermark from the expected old version. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Azure SQL Database.

Document database schema, procedures, connection configuration and migration scripts, the relational schema, unique keys, isolation and API/metadata semantics, required Entra/database identity, object grants, firewall/private-route configuration, owner, normal/failure signals and recovery instructions using transaction commit, entity-state version and accepted run/publication record. Include one normal and one failure example plus actual service targets and retention assumptions. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Azure SQL Database fit in an end-to-end Azure data platform?

Use this specific flow: Approved client identity -> parameterized SQL -> relational tables and transaction -> accepted result -> application or orchestration consumer. Explain what this component owns, how application/ADF caller and source or consumer contract connects, and what the accepted consumer/result boundary is. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using Azure SQL Database for Azure orchestration metadata and governed relational serving?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one transactional SQL operation or control-state update meets them, compare a credible alternative and validate using Query Store plans, database resource metrics, waits and transaction state rather than choosing a tool merely because it is on the stack. Historical query evidence helps identify plan and resource regressions. Correlate it with schema, parameter and data-distribution changes.

Compare yesterday's fast metadata lookup with today's slow plan and the new run-history volume. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround Azure SQL Database in a financial or telecom project?

Tie relational schema, unique keys, isolation and API/metadata semantics to accountable business ownership, verify Entra/database identity, object grants, firewall/private-route configuration, preserve transaction commit, entity-state version and accepted run/publication record and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your Azure SQL Database optimization helped?

Record the old/new configuration and comparable workload, measure CPU, I/O, plan regression, blocking and connection pressure with Query Store plans, database resource metrics, waits and transaction state, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. Compute configuration affects latency, scale and cost under supported tier behavior. Validate actual cold/resume and peak patterns, not only average utilization.

An intermittent API database has different requirements from continuously active ingestion metadata. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a Azure SQL Database interview project?

Identify which database schema, procedures, connection configuration and migration scripts you personally built/reviewed/operated, one specific failure you resolved, the evidence in transaction commit, entity-state version and accepted run/publication record and a verified outcome. State team-owned components separately and do not invent scale or savings. Managed infrastructure reduces administration but does not optimize the application's model or queries automatically. Database owners still define schemas, permissions and transaction semantics.

A metadata database needs safe entity-state procedures and indexed run queries even when backups are managed. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain Azure SQL Database's specific responsibility in the flow before naming surrounding tools.
- Use the real relational schema, unique keys, isolation and API/metadata semantics; an accepted request/job does not establish a correct business result.
- Validate Entra/database identity, object grants, firewall/private-route configuration under the actual execution identity, rather than your administrator account.
- Preserve transaction commit, entity-state version and accepted run/publication record and inspect it before retrying uncertain side effects.
- Tune CPU, I/O, plan regression, blocking and connection pressure from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Build a safe entity-state update procedure.**

```sql
-- T-SQL transaction skeleton; expected state and token are parameters.
BEGIN TRANSACTION;
UPDATE dbo.entity_state
SET accepted_watermark = @new_boundary,
    accepted_run_id = @run_id
WHERE entity_id = @entity_id
  AND accepted_watermark = @expected_old_boundary;
IF @@ROWCOUNT <> 1
BEGIN
  ROLLBACK TRANSACTION;
  THROW 50001, 'State changed or entity was not found', 1;
END;
COMMIT TRANSACTION;
-- Production adds lease/token validation, NULL-initial-state handling
-- and the accepted publication check; this is not a complete procedure.
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure SQL Database official documentation](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview).

[Back to all 20 interview guides](README.md).
