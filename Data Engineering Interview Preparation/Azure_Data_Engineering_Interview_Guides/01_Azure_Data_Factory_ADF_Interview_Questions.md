# Azure Data Factory (ADF) — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Source ingestion, orchestration, scheduling and controlled ETL/ELT execution.

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
Source -> linked service and integration runtime -> Copy activity -> ADLS landing -> transformation activity -> validation -> accepted serving dataset
```

For this guide, the primary unit is **one scheduled entity pipeline**. The engineering artifacts are pipeline JSON, linked services, trigger definitions and parameterized datasets. Troubleshooting starts with activity output, integration-runtime diagnostics and source/sink throughput; durable progress/evidence is represented by source watermark, immutable delivery manifest and accepted run record. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is an ADF pipeline?

A pipeline groups activities into an orchestrated workflow. A pipeline run is one execution with a specific parameter set and run identity. The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

A daily account pipeline can have one source delivery and three attempts without representing three business loads. The activity dependencies determine which steps run after success, failure or completion; run parameters identify the entity and business window being processed.

### C02. What are linked services and datasets?

A linked service defines connectivity/authentication to a data store or compute service; a dataset identifies the data structure or location used by an activity. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Changing the entity path should not require changing authentication. Validate the connection under the pipeline identity and the dataset under its approved schema.

### C03. What is an integration runtime?

It provides the execution/connectivity bridge for integration work. Choose Azure, self-hosted or Azure-SSIS runtime based on the workload and network requirements. The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations. Runtime availability, host capacity and source connectivity should be monitored separately from the business transformation that the pipeline dispatches.

### C04. When do you use Copy activity versus Mapping Data Flow?

Copy moves supported data between sources and sinks. Mapping Data Flow performs visual Spark-based transformations; external activities can invoke custom compute such as Databricks. Data movement and transformation are different responsibilities. Copy success establishes transferred data, while joins, historical resolution and reconciliation require explicit processing and controls.

Copy journal extracts to raw storage, then invoke a transformation and validate signed ledger totals. Choose Mapping Data Flow for supported visual transformation requirements, or Databricks when code-based rules and distributed processing justify it; validate the resulting business output.

### C05. How do ETL and ELT differ?

ETL transforms before the analytical destination; ELT lands data and transforms within the destination platform. Select based on data volume, engine capabilities and control needs. ELT retains replayable source context before applying business rules, but requires governance of raw data. ETL can reduce destination payload while increasing upstream processing coupling.

A banking lake can retain immutable raw deliveries and rebuild gold facts after a rule correction. Retaining raw data makes rule changes replayable, while placing transformations earlier may reduce transferred volume but adds source-side operational dependence.

### C06. How do parameters differ from variables?

Parameters supply read-only run configuration. Variables hold mutable pipeline state; avoid shared mutable variables in parallel iterations. Concurrent iterations must not modify one shared variable as if it were thread-local. Use per-entity parameters, isolated outputs and a later controlled aggregation.

Each entity iteration writes its own run/control row; the parent summarizes accepted child results afterward. Store per-iteration outcomes with isolated entity/run keys, and aggregate them after the parallel activity finishes instead of mutating shared counters.

### C07. What trigger patterns should you know?

Schedule triggers start time-based runs, tumbling windows represent bounded recurring windows, and supported event triggers respond to events. Choose based on replay, dependency and timing requirements. Scheduling must define business windows, not merely clock times. Understand catch-up, overlapping executions and dependencies before choosing the trigger pattern.

A finance load uses an explicit period boundary so replaying a missed window targets the same business scope. Specify the window's start/end and timezone explicitly so missed-window recovery processes the intended business date without accidentally overlapping an accepted load.

### C08. How do Lookup and Get Metadata differ?

Lookup reads configuration or query results; Get Metadata reads supported object/file metadata. Their output size and connector constraints matter for large workloads. Small configuration queries and object metadata checks serve different purposes. Avoid materializing enormous entity/file lists through orchestration outputs when they exceed supported limits.

Read a bounded active-entity configuration, then validate each delivery manifest through the appropriate processing path. Keep orchestration results bounded; processing a huge file inventory can require a dedicated compute step rather than one oversized metadata response.

### C09. How do you process multiple entities?

Read reviewed metadata and iterate with parameterized datasets/pipelines. Bound concurrency to protect the source and avoid conflicting target publications. Metadata-driven frameworks need stable configuration fields and source-specific semantics. Reusability covers orchestration, while CDC, deletion and domain rules remain explicit.

Customer snapshots and journal CDC can share logging and scheduling while using different extraction methods. An approved configuration includes source object, extraction mode, schema, target, owner and controls, while connector-specific change semantics remain explicit.

### C10. What proves a pipeline succeeded?

Execution status proves activities completed. Business success also requires manifest completeness, quality/reconciliation controls and accepted consumer publication. Technical completion and business acceptance must be separate states. Check file completeness, key coverage and source totals before allowing consumer publication.

A Copy run transfers all available files but remains held when the expected source manifest lists a missing file. Record landed, validated and published states separately so operations can distinguish successful movement from a held or incomplete analytical product.

## B. Advanced implementation questions

### A01. How do you make incremental ingestion safe?

Use a source-consistent bounded change boundary, retain raw input and advance accepted state after publication. Timestamp-only extraction requires explicit assumptions and cannot detect hard deletes by itself. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. An overlap window needs stable-key deduplication and documented residual risk; source-supported CDC is required where timestamp extraction cannot meet completeness needs.

### A02. How do you build restartable pipelines?

Persist phase state, source boundaries and manifests. Make target operations idempotent and reconcile cases where publication succeeds but state recording fails. Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load. Check the published batch identity and counts before retrying, then advance state only when the accepted output matches the saved source boundary.

### A03. How do you parameterize dynamic SQL safely?

Bind values using supported parameters and allow-list object identifiers. Metadata-driven ingestion must not execute unrestricted configuration as SQL. Values and identifiers require different protection. Parameter binding handles values; table/schema names require reviewed allow-lists or safe engine-specific handling.

A registered entity can select an approved source table but cannot submit arbitrary SQL through metadata. Apply identifier allow-lists before constructing a query and keep credentials/configuration editing separate from business users supplying ordinary runtime values.

### A04. How do you deploy ADF across environments?

Version source definitions, produce deployable artifacts, use environment parameters and separate identities, and validate trigger behavior during promotion. Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling. Review linked-service endpoints, identity grants and trigger state in the target environment; source-code parity does not establish working production connectivity.

### A05. How do you tune Copy performance?

Inspect source, network, runtime and sink throughput; adjust partitioning/concurrency only at a measured bottleneck. Higher parallelism can overload the source. Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

Compare extraction duration, transfer rate and sink write time before adjusting concurrency. Compare throughput and source load with the same volume and concurrency, and preserve reconciliation results so optimization does not disguise missing records.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. An on-premises SQL connection fails while cloud copies work. What do you check?

Inspect self-hosted runtime availability, service credentials, outbound connectivity, DNS and source permissions. Reproduce with the runtime identity rather than your interactive account. The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. A file event starts before all delivery files arrive. How do you prevent incomplete processing?

Treat the event as a signal, then validate an expected manifest or completion marker. Publish only after the complete delivery is present. Small configuration queries and object metadata checks serve different purposes. Avoid materializing enormous entity/file lists through orchestration outputs when they exceed supported limits.

Read a bounded active-entity configuration, then validate each delivery manifest through the appropriate processing path. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. Two runs update the same watermark. How do you fix it?

Serialize the entity or acquire a durable lease; use compare-and-set state updates. Preserve distinct run IDs and prevent competing publication. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A source hard-deletes rows. Will your timestamp query capture this?

No. Use source-supported CDC, a tombstone feed or an authoritative full-snapshot comparison with explicit deletion rules. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. Copy succeeds but the notebook fails. What do you rerun?

Reuse the durable landed input and same boundary for transformation. Do not re-extract a changing source without recording a new input version. Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. Parallel ForEach produces incorrect shared totals. Why?

Pipeline variables are shared mutable state. Return per-iteration outputs or persist isolated results and aggregate after the parallel work. Concurrent iterations must not modify one shared variable as if it were thread-local. Use per-entity parameters, isolated outputs and a later controlled aggregation.

Each entity iteration writes its own run/control row; the parent summarizes accepted child results afterward. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. REST pagination repeats a page after a timeout. What is your strategy?

Persist cursor/page identity, bound retries and deduplicate stable source keys. Verify whether the API supports a consistent snapshot while pages are fetched. Metadata-driven frameworks need stable configuration fields and source-specific semantics. Reusability covers orchestration, while CDC, deletion and domain rules remain explicit.

Customer snapshots and journal CDC can share logging and scheduling while using different extraction methods. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A tumbling-window backfill overloads the database. What changes?

Lower approved concurrency, chunk the ranges and measure database pressure. Keep backfill separate from the live freshness workload where necessary. Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

Compare extraction duration, transfer rate and sink write time before adjusting concurrency. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A Databricks activity times out after the job finished. Should you submit a new job immediately?

Inspect the external job/run status and target publication before retrying. Use correlation IDs and idempotency to avoid duplicated side effects. Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. Triggers run during deployment and read half-updated configuration. How do you prevent that?

Use a controlled deployment sequence for affected triggers and dependencies, validate the release, then resume scheduling and reconcile missed windows. Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one scheduled entity pipeline to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants. Compare production with the working configuration using activity output, integration-runtime diagnostics and source/sink throughput; do not resolve the incident by giving every identity broad access. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration. Investigate under the real caller rather than the interactive administrator. The relevant path is linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Azure Data Factory (ADF) is available, but the business result has not advanced. What would you check?

Trace the expected operation through source system and invoked Databricks/SQL transformation and compare progress in source watermark, immutable delivery manifest and accepted run record. Inspect activity output, integration-runtime diagnostics and source/sink throughput to distinguish a service being reachable from an accepted business operation actually completing. The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute. Walk the dependency chain through source system and invoked Databricks/SQL transformation and locate the last accepted evidence in source watermark, immutable delivery manifest and accepted run record. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of pipeline JSON, linked services, trigger definitions and parameterized datasets works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual source schema, extraction boundary and sink dataset schema. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration. Treat the release as a change to pipeline JSON, linked services, trigger definitions and parameterized datasets and its dependencies, not just to one code file. Compare source schema, extraction boundary and sink dataset schema and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one scheduled entity pipeline although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with activity output, integration-runtime diagnostics and source/sink throughput and inspect source query duration, Copy throughput and transformation activity duration. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput. Use activity output, integration-runtime diagnostics and source/sink throughput to compare the same business boundary and concurrency against a known-good baseline. Examine source query duration, Copy throughput and transformation activity duration and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

Compare extraction duration, transfer rate and sink write time before adjusting concurrency. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Azure Data Factory (ADF) may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in source watermark, immutable delivery manifest and accepted run record before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by source watermark, immutable delivery manifest and accepted run record and repeat only through a supported safe operation/status mechanism.

If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one scheduled entity pipeline at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in source watermark, immutable delivery manifest and accepted run record. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable. Define who owns the shared mutation and which state version each caller expected. Preserve source watermark, immutable delivery manifest and accepted run record so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Azure Data Factory (ADF) without prior notice. How do you contain the impact?

Validate against source schema, extraction boundary and sink dataset schema and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation. Classify the change against source schema, extraction boundary and sink dataset schema: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some source watermark, immutable delivery manifest and accepted run record evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of source watermark, immutable delivery manifest and accepted run record and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable. Recovery can reconstruct only what still exists and is consistent. Inventory source watermark, immutable delivery manifest and accepted run record, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in activity output, integration-runtime diagnostics and source/sink throughput. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read activity output, integration-runtime diagnostics and source/sink throughput and derived exports; minimizing the source log alone does not remove already copied sensitive output.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Azure Data Factory (ADF) accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in pipeline JSON, linked services, trigger definitions and parameterized datasets, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against source watermark, immutable delivery manifest and accepted run record before restoring normal processing. Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation. Environment validation belongs before mutation. Bind pipeline JSON, linked services, trigger definitions and parameterized datasets to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Source system and invoked databricks/sql transformation is temporarily unavailable. What retry and recovery policy fits Azure Data Factory (ADF)?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved source watermark, immutable delivery manifest and accepted run record; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep source watermark, immutable delivery manifest and accepted run record durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Azure Data Factory (ADF) rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect source query duration, Copy throughput and transformation activity duration. Remove demonstrated waste while preserving required source watermark, immutable delivery manifest and accepted run record and correctness/access controls. The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to source query duration, Copy throughput and transformation activity duration and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

A daily account pipeline can have one source delivery and three attempts without representing three business loads. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, pipeline JSON, linked services, trigger definitions and parameterized datasets is restored but the business path still fails. What else is required?

Restore/validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, source system and invoked Databricks/SQL transformation and the appropriate source watermark, immutable delivery manifest and accepted run record. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, reconcile source watermark, immutable delivery manifest and accepted run record and execute a normal authorized consumer path before calling the recovery successful.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Azure Data Factory (ADF). How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with activity output, integration-runtime diagnostics and source/sink throughput and validate their source schema, extraction boundary and sink dataset schema. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity. Find the smallest complete failed business scope using keys/objects and activity output, integration-runtime diagnostics and source/sink throughput. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow source schema, extraction boundary and sink dataset schema and preserve a clear accounting of accepted versus failed scope.

A daily account pipeline can have one source delivery and three attempts without representing three business loads. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change pipeline JSON, linked services, trigger definitions and parameterized datasets while dependent workloads remain active. What release sequence would you use?

Inventory consumers and source schema, extraction boundary and sink dataset schema compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain source watermark, immutable delivery manifest and accepted run record and define a tested rollback/correction route for incompatible behavior. Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep source watermark, immutable delivery manifest and accepted run record and a tested correction/rollback boundary so a partially applied release remains recoverable.

Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling. Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a metadata-driven ingestion pipeline.

Show entity configuration, validated identifiers, extraction boundary, Copy, notebook dispatch, controls, publication and state update. Demonstrate one failed-run replay. Metadata-driven frameworks need stable configuration fields and source-specific semantics. Reusability covers orchestration, while CDC, deletion and domain rules remain explicit.

Customer snapshots and journal CDC can share logging and scheduling while using different extraction methods. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Write a bounded incremental extraction query.

Use old < boundary <= new under a documented source contract. Include a deletion strategy and explain why backdated updates need more than a timestamp. Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

Compare extraction duration, transfer rate and sink write time before adjusting concurrency. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Implement a file completeness gate.

Compare expected manifest paths/counts/checksums against landed objects and preserve run evidence. Test a missing and a duplicate delivery. Technical completion and business acceptance must be separate states. Check file completeness, key coverage and source totals before allowing consumer publication.

A Copy run transfers all available files but remains held when the expected source manifest lists a missing file. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one scheduled entity pipeline.

Capture the initial source watermark, immutable delivery manifest and accepted run record, introduce one realistic dependency or validation failure and use activity output, integration-runtime diagnostics and source/sink throughput to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

A daily account pipeline can have one source delivery and three attempts without representing three business loads. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Azure Data Factory (ADF).

Document pipeline JSON, linked services, trigger definitions and parameterized datasets, the source schema, extraction boundary and sink dataset schema, required linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, owner, normal/failure signals and recovery instructions using source watermark, immutable delivery manifest and accepted run record. Include one normal and one failure example plus actual service targets and retention assumptions. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Azure Data Factory (ADF) fit in an end-to-end Azure data platform?

Use this specific flow: Source -> linked service and integration runtime -> Copy activity -> ADLS landing -> transformation activity -> validation -> accepted serving dataset. Explain what this component owns, how source system and invoked Databricks/SQL transformation connects, and what the accepted consumer/result boundary is. The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using Azure Data Factory (ADF) for banking transaction ingestion and restartable lake modernization?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one scheduled entity pipeline meets them, compare a credible alternative and validate using activity output, integration-runtime diagnostics and source/sink throughput rather than choosing a tool merely because it is on the stack. Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

Compare extraction duration, transfer rate and sink write time before adjusting concurrency. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround Azure Data Factory (ADF) in a financial or telecom project?

Tie source schema, extraction boundary and sink dataset schema to accountable business ownership, verify linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, preserve source watermark, immutable delivery manifest and accepted run record and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

One ADLS connection can support transaction and customer datasets with separate entity paths and permissions. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your Azure Data Factory (ADF) optimization helped?

Record the old/new configuration and comparable workload, measure source query duration, Copy throughput and transformation activity duration with activity output, integration-runtime diagnostics and source/sink throughput, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a Azure Data Factory (ADF) interview project?

Identify which pipeline JSON, linked services, trigger definitions and parameterized datasets you personally built/reviewed/operated, one specific failure you resolved, the evidence in source watermark, immutable delivery manifest and accepted run record and a verified outcome. State team-owned components separately and do not invent scale or savings. The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

A daily account pipeline can have one source delivery and three attempts without representing three business loads. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain Azure Data Factory (ADF)'s specific responsibility in the flow before naming surrounding tools.
- Use the real source schema, extraction boundary and sink dataset schema; an accepted request/job does not establish a correct business result.
- Validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants under the actual execution identity, rather than your administrator account.
- Preserve source watermark, immutable delivery manifest and accepted run record and inspect it before retrying uncertain side effects.
- Tune source query duration, Copy throughput and transformation activity duration from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Design a metadata-driven ingestion pipeline.**

```text
Lookup approved entity metadata
-> claim entity with an owning run token
-> capture source-consistent old/new boundaries
-> Copy into source/entity/date/run_id
-> verify delivery manifest
-> execute parameterized transformation
-> validate critical quality and reconciliation
-> publish the accepted candidate
-> record accepted boundary and release ownership
Failure: preserve input, mark failed/held and recover the identified phase
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Data Factory (ADF) official documentation](https://learn.microsoft.com/en-us/azure/data-factory/introduction).
- [Integration runtime concepts](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime).

[Back to all 20 interview guides](README.md).
