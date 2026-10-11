# Azure Data Factory (ADF) — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Source ingestion, orchestration, scheduling and controlled ETL/ELT execution.

**Audience:** Azure data engineering interviews, from fundamentals through production troubleshooting and design. Each answer explains the concept, its practical use and implementation context. Scenario answers cover the cause, investigation, correction and verification. Check source semantics, engine/runtime, workload identity and acceptance evidence for your actual configuration. Practice scenarios are hypothetical and are not claims about the named client projects.

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

**Answer:** A pipeline groups activities into an orchestrated workflow. A pipeline run is one execution with a specific parameter set and run identity.

**Explanation:** The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

**Practical example:** A daily account pipeline can have one source delivery and three attempts without representing three business loads.

### C02. What are linked services and datasets?

**Answer:** A linked service defines connectivity/authentication to a data store or compute service; a dataset identifies the data structure or location used by an activity.

**Explanation:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Practical example:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

### C03. What is an integration runtime?

**Answer:** It provides the execution/connectivity bridge for integration work. Choose Azure, self-hosted or Azure-SSIS runtime based on the workload and network requirements.

**Explanation:** The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

**Practical example:** Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations.

### C04. When do you use Copy activity versus Mapping Data Flow?

**Answer:** Copy moves supported data between sources and sinks. Mapping Data Flow performs visual Spark-based transformations; external activities can invoke custom compute such as Databricks.

**Explanation:** Data movement and transformation are different responsibilities. Copy success establishes transferred data, while joins, historical resolution and reconciliation require explicit processing and controls.

**Practical example:** Copy journal extracts to raw storage, then invoke a transformation and validate signed ledger totals.

### C05. How do ETL and ELT differ?

**Answer:** ETL transforms before the analytical destination; ELT lands data and transforms within the destination platform. Select based on data volume, engine capabilities and control needs.

**Explanation:** ELT retains replayable source context before applying business rules, but requires governance of raw data. ETL can reduce destination payload while increasing upstream processing coupling.

**Practical example:** A banking lake can retain immutable raw deliveries and rebuild gold facts after a rule correction.

### C06. How do parameters differ from variables?

**Answer:** Parameters supply read-only run configuration. Variables hold mutable pipeline state; avoid shared mutable variables in parallel iterations.

**Explanation:** Concurrent iterations must not modify one shared variable as if it were thread-local. Use per-entity parameters, isolated outputs and a later controlled aggregation.

**Practical example:** Each entity iteration writes its own run/control row; the parent summarizes accepted child results afterward.

### C07. What trigger patterns should you know?

**Answer:** Schedule triggers start time-based runs, tumbling windows represent bounded recurring windows, and supported event triggers respond to events. Choose based on replay, dependency and timing requirements.

**Explanation:** Scheduling must define business windows, not merely clock times. Understand catch-up, overlapping executions and dependencies before choosing the trigger pattern.

**Practical example:** A finance load uses an explicit period boundary so replaying a missed window targets the same business scope.

### C08. How do Lookup and Get Metadata differ?

**Answer:** Lookup reads configuration or query results; Get Metadata reads supported object/file metadata. Their output size and connector constraints matter for large workloads.

**Explanation:** Small configuration queries and object metadata checks serve different purposes. Avoid materializing enormous entity/file lists through orchestration outputs when they exceed supported limits.

**Practical example:** Read a bounded active-entity configuration, then validate each delivery manifest through the appropriate processing path.

### C09. How do you process multiple entities?

**Answer:** Read reviewed metadata and iterate with parameterized datasets/pipelines. Bound concurrency to protect the source and avoid conflicting target publications.

**Explanation:** Metadata-driven frameworks need stable configuration fields and source-specific semantics. Reusability covers orchestration, while CDC, deletion and domain rules remain explicit.

**Practical example:** Customer snapshots and journal CDC can share logging and scheduling while using different extraction methods.

### C10. What proves a pipeline succeeded?

**Answer:** Execution status proves activities completed. Business success also requires manifest completeness, quality/reconciliation controls and accepted consumer publication.

**Explanation:** Technical completion and business acceptance must be separate states. Check file completeness, key coverage and source totals before allowing consumer publication.

**Practical example:** A Copy run transfers all available files but remains held when the expected source manifest lists a missing file.

## B. Advanced implementation questions

### A01. How do you make incremental ingestion safe?

**Answer:** Use a source-consistent bounded change boundary, retain raw input and advance accepted state after publication. Timestamp-only extraction requires explicit assumptions and cannot detect hard deletes by itself.

**Explanation:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Practical example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

### A02. How do you build restartable pipelines?

**Answer:** Persist phase state, source boundaries and manifests. Make target operations idempotent and reconcile cases where publication succeeds but state recording fails.

**Explanation:** Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

**Practical example:** If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load.

### A03. How do you parameterize dynamic SQL safely?

**Answer:** Bind values using supported parameters and allow-list object identifiers. Metadata-driven ingestion must not execute unrestricted configuration as SQL.

**Explanation:** Values and identifiers require different protection. Parameter binding handles values; table/schema names require reviewed allow-lists or safe engine-specific handling.

**Practical example:** A registered entity can select an approved source table but cannot submit arbitrary SQL through metadata.

### A04. How do you deploy ADF across environments?

**Answer:** Version source definitions, produce deployable artifacts, use environment parameters and separate identities, and validate trigger behavior during promotion.

**Explanation:** Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

**Practical example:** Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling.

### A05. How do you tune Copy performance?

**Answer:** Inspect source, network, runtime and sink throughput; adjust partitioning/concurrency only at a measured bottleneck. Higher parallelism can overload the source.

**Explanation:** Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

**Practical example:** Compare extraction duration, transfer rate and sink write time before adjusting concurrency.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. An on-premises SQL connection fails while cloud copies work. What do you check?

**Answer:** Inspect self-hosted runtime availability, service credentials, outbound connectivity, DNS and source permissions. Reproduce with the runtime identity rather than your interactive account.

**Why this happens and what matters:** The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

**Related practical example:** Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. A file event starts before all delivery files arrive. How do you prevent incomplete processing?

**Answer:** Treat the event as a signal, then validate an expected manifest or completion marker. Publish only after the complete delivery is present.

**Why this happens and what matters:** Small configuration queries and object metadata checks serve different purposes. Avoid materializing enormous entity/file lists through orchestration outputs when they exceed supported limits.

**Related practical example:** Read a bounded active-entity configuration, then validate each delivery manifest through the appropriate processing path.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. Two runs update the same watermark. How do you fix it?

**Answer:** Serialize the entity or acquire a durable lease; use compare-and-set state updates. Preserve distinct run IDs and prevent competing publication.

**Why this happens and what matters:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Related practical example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A source hard-deletes rows. Will your timestamp query capture this?

**Answer:** No. Use source-supported CDC, a tombstone feed or an authoritative full-snapshot comparison with explicit deletion rules.

**Why this happens and what matters:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Related practical example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. Copy succeeds but the notebook fails. What do you rerun?

**Answer:** Reuse the durable landed input and same boundary for transformation. Do not re-extract a changing source without recording a new input version.

**Why this happens and what matters:** Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

**Related practical example:** If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. Parallel ForEach produces incorrect shared totals. Why?

**Answer:** Pipeline variables are shared mutable state. Return per-iteration outputs or persist isolated results and aggregate after the parallel work.

**Why this happens and what matters:** Concurrent iterations must not modify one shared variable as if it were thread-local. Use per-entity parameters, isolated outputs and a later controlled aggregation.

**Related practical example:** Each entity iteration writes its own run/control row; the parent summarizes accepted child results afterward.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. REST pagination repeats a page after a timeout. What is your strategy?

**Answer:** Persist cursor/page identity, bound retries and deduplicate stable source keys. Verify whether the API supports a consistent snapshot while pages are fetched.

**Why this happens and what matters:** Metadata-driven frameworks need stable configuration fields and source-specific semantics. Reusability covers orchestration, while CDC, deletion and domain rules remain explicit.

**Related practical example:** Customer snapshots and journal CDC can share logging and scheduling while using different extraction methods.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A tumbling-window backfill overloads the database. What changes?

**Answer:** Lower approved concurrency, chunk the ranges and measure database pressure. Keep backfill separate from the live freshness workload where necessary.

**Why this happens and what matters:** Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

**Related practical example:** Compare extraction duration, transfer rate and sink write time before adjusting concurrency.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A Databricks activity times out after the job finished. Should you submit a new job immediately?

**Answer:** Inspect the external job/run status and target publication before retrying. Use correlation IDs and idempotency to avoid duplicated side effects.

**Why this happens and what matters:** Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

**Related practical example:** If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. Triggers run during deployment and read half-updated configuration. How do you prevent that?

**Answer:** Use a controlled deployment sequence for affected triggers and dependencies, validate the release, then resume scheduling and reconcile missed windows.

**Why this happens and what matters:** Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

**Related practical example:** Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one scheduled entity pipeline to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Answer:** Capture the effective caller and exact error, then validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants. Compare production with the working configuration using activity output, integration-runtime diagnostics and source/sink throughput; do not resolve the incident by giving every identity broad access.

**Why this happens and what matters:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Investigation and correction:** Investigate under the real caller rather than the interactive administrator. The relevant path is linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

**Related practical example:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Azure Data Factory (ADF) is available, but the business result has not advanced. What would you check?

**Answer:** Trace the expected operation through source system and invoked Databricks/SQL transformation and compare progress in source watermark, immutable delivery manifest and accepted run record. Inspect activity output, integration-runtime diagnostics and source/sink throughput to distinguish a service being reachable from an accepted business operation actually completing.

**Why this happens and what matters:** The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

**Investigation and correction:** Walk the dependency chain through source system and invoked Databricks/SQL transformation and locate the last accepted evidence in source watermark, immutable delivery manifest and accepted run record. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

**Related practical example:** Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of pipeline JSON, linked services, trigger definitions and parameterized datasets works in test but breaks a dependent production consumer. How do you diagnose it?

**Answer:** Compare versions, environment settings and the actual source schema, extraction boundary and sink dataset schema. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Why this happens and what matters:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Investigation and correction:** Treat the release as a change to pipeline JSON, linked services, trigger definitions and parameterized datasets and its dependencies, not just to one code file. Compare source schema, extraction boundary and sink dataset schema and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

**Related practical example:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one scheduled entity pipeline although the request or data volume is unchanged. What is your investigation sequence?

**Answer:** Compare a known-good baseline with activity output, integration-runtime diagnostics and source/sink throughput and inspect source query duration, Copy throughput and transformation activity duration. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Why this happens and what matters:** Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

**Investigation and correction:** Use activity output, integration-runtime diagnostics and source/sink throughput to compare the same business boundary and concurrency against a known-good baseline. Examine source query duration, Copy throughput and transformation activity duration and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

**Related practical example:** Compare extraction duration, transfer rate and sink write time before adjusting concurrency.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Azure Data Factory (ADF) may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Answer:** Inspect the durable outcome in source watermark, immutable delivery manifest and accepted run record before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Why this happens and what matters:** Restartability requires durable inputs and known phase completion. Cross-system publication and state recording can disagree after a crash and need reconciliation.

**Investigation and correction:** Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by source watermark, immutable delivery manifest and accepted run record and repeat only through a supported safe operation/status mechanism.

**Related practical example:** If gold published but Azure SQL state update failed, inspect the accepted manifest before repeating the fact load.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one scheduled entity pipeline at the same time. How do you prevent lost or inconsistent state?

**Answer:** Identify the shared resource and ownership boundary in source watermark, immutable delivery manifest and accepted run record. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Why this happens and what matters:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Investigation and correction:** Define who owns the shared mutation and which state version each caller expected. Preserve source watermark, immutable delivery manifest and accepted run record so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

**Related practical example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Azure Data Factory (ADF) without prior notice. How do you contain the impact?

**Answer:** Validate against source schema, extraction boundary and sink dataset schema and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Why this happens and what matters:** Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

**Investigation and correction:** Classify the change against source schema, extraction boundary and sink dataset schema: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

**Related practical example:** Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some source watermark, immutable delivery manifest and accepted run record evidence has expired. What can you recover and what should change?

**Answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of source watermark, immutable delivery manifest and accepted run record and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Why this happens and what matters:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Investigation and correction:** Recovery can reconstruct only what still exists and is consistent. Inventory source watermark, immutable delivery manifest and accepted run record, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

**Related practical example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in activity output, integration-runtime diagnostics and source/sink throughput. How would you fix the logging and access design?

**Answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Why this happens and what matters:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Investigation and correction:** Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read activity output, integration-runtime diagnostics and source/sink throughput and derived exports; minimizing the source log alone does not remove already copied sensitive output.

**Related practical example:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Azure Data Factory (ADF) accidentally points to production while rehearsing in development. What controls would you add?

**Answer:** Validate environment/resource identifiers in pipeline JSON, linked services, trigger definitions and parameterized datasets, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against source watermark, immutable delivery manifest and accepted run record before restoring normal processing.

**Why this happens and what matters:** Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

**Investigation and correction:** Environment validation belongs before mutation. Bind pipeline JSON, linked services, trigger definitions and parameterized datasets to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

**Related practical example:** Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Source system and invoked databricks/sql transformation is temporarily unavailable. What retry and recovery policy fits Azure Data Factory (ADF)?

**Answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved source watermark, immutable delivery manifest and accepted run record; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Why this happens and what matters:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Investigation and correction:** Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep source watermark, immutable delivery manifest and accepted run record durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

**Related practical example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Azure Data Factory (ADF) rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect source query duration, Copy throughput and transformation activity duration. Remove demonstrated waste while preserving required source watermark, immutable delivery manifest and accepted run record and correctness/access controls.

**Why this happens and what matters:** The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

**Investigation and correction:** Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to source query duration, Copy throughput and transformation activity duration and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

**Related practical example:** A daily account pipeline can have one source delivery and three attempts without representing three business loads.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, pipeline JSON, linked services, trigger definitions and parameterized datasets is restored but the business path still fails. What else is required?

**Answer:** Restore/validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, source system and invoked Databricks/SQL transformation and the appropriate source watermark, immutable delivery manifest and accepted run record. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Why this happens and what matters:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Investigation and correction:** Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, reconcile source watermark, immutable delivery manifest and accepted run record and execute a normal authorized consumer path before calling the recovery successful.

**Related practical example:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Azure Data Factory (ADF). How do you isolate it without silently accepting incomplete results?

**Answer:** Correlate failing business keys/objects with activity output, integration-runtime diagnostics and source/sink throughput and validate their source schema, extraction boundary and sink dataset schema. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Why this happens and what matters:** The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

**Investigation and correction:** Find the smallest complete failed business scope using keys/objects and activity output, integration-runtime diagnostics and source/sink throughput. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow source schema, extraction boundary and sink dataset schema and preserve a clear accounting of accepted versus failed scope.

**Related practical example:** A daily account pipeline can have one source delivery and three attempts without representing three business loads.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change pipeline JSON, linked services, trigger definitions and parameterized datasets while dependent workloads remain active. What release sequence would you use?

**Answer:** Inventory consumers and source schema, extraction boundary and sink dataset schema compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain source watermark, immutable delivery manifest and accepted run record and define a tested rollback/correction route for incompatible behavior.

**Why this happens and what matters:** Environment promotion changes endpoints and identities without changing reviewed business logic. Trigger activation and connection configuration belong in release validation.

**Investigation and correction:** Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep source watermark, immutable delivery manifest and accepted run record and a tested correction/rollback boundary so a partially applied release remains recoverable.

**Related practical example:** Deploy the tested artifact with production resource references, then validate a bounded load before resuming scheduling.

**How to verify the resolution:** Validate the accepted result and the intended source schema, extraction boundary and sink dataset schema. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises include implementation reasoning, solution requirements and selected code or flow examples. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a metadata-driven ingestion pipeline.

**Answer:** Show entity configuration, validated identifiers, extraction boundary, Copy, notebook dispatch, controls, publication and state update. Demonstrate one failed-run replay.

**Implementation reasoning:** Metadata-driven frameworks need stable configuration fields and source-specific semantics. Reusability covers orchestration, while CDC, deletion and domain rules remain explicit.

**Example to work through:** Customer snapshots and journal CDC can share logging and scheduling while using different extraction methods.

**Illustrative implementation:**

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

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P02. Write a bounded incremental extraction query.

**Answer:** Use old < boundary <= new under a documented source contract. Include a deletion strategy and explain why backdated updates need more than a timestamp.

**Implementation reasoning:** Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

**Example to work through:** Compare extraction duration, transfer rate and sink write time before adjusting concurrency.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Implement a file completeness gate.

**Answer:** Compare expected manifest paths/counts/checksums against landed objects and preserve run evidence. Test a missing and a duplicate delivery.

**Implementation reasoning:** Technical completion and business acceptance must be separate states. Check file completeness, key coverage and source totals before allowing consumer publication.

**Example to work through:** A Copy run transfers all available files but remains held when the expected source manifest lists a missing file.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one scheduled entity pipeline.

**Answer:** Capture the initial source watermark, immutable delivery manifest and accepted run record, introduce one realistic dependency or validation failure and use activity output, integration-runtime diagnostics and source/sink throughput to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

**Implementation reasoning:** The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

**Example to work through:** A daily account pipeline can have one source delivery and three attempts without representing three business loads.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Azure Data Factory (ADF).

**Answer:** Document pipeline JSON, linked services, trigger definitions and parameterized datasets, the source schema, extraction boundary and sink dataset schema, required linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, owner, normal/failure signals and recovery instructions using source watermark, immutable delivery manifest and accepted run record. Include one normal and one failure example plus actual service targets and retention assumptions.

**Implementation reasoning:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Example to work through:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Azure Data Factory (ADF) fit in an end-to-end Azure data platform?

**Answer:** Use this specific flow: Source -> linked service and integration runtime -> Copy activity -> ADLS landing -> transformation activity -> validation -> accepted serving dataset. Explain what this component owns, how source system and invoked Databricks/SQL transformation connects, and what the accepted consumer/result boundary is.

**Project explanation:** The runtime must reach both endpoints and support the selected activity. A self-hosted runtime requires host/service maintenance; it is not a transformation cluster substitute.

**Concrete example:** Use a reachable self-hosted runtime for an approved on-premises database and separate Databricks compute for business transformations.

### D02. How would you justify using Azure Data Factory (ADF) for banking transaction ingestion and restartable lake modernization?

**Answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one scheduled entity pipeline meets them, compare a credible alternative and validate using activity output, integration-runtime diagnostics and source/sink throughput rather than choosing a tool merely because it is on the stack.

**Project explanation:** Performance tuning starts with locating the slow segment. More parallel copies can saturate source I/O or sink limits rather than improve accepted throughput.

**Concrete example:** Compare extraction duration, transfer rate and sink write time before adjusting concurrency.

### D03. What controls must surround Azure Data Factory (ADF) in a financial or telecom project?

**Answer:** Tie source schema, extraction boundary and sink dataset schema to accountable business ownership, verify linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, preserve source watermark, immutable delivery manifest and accepted run record and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

**Project explanation:** Connectivity can be reused across datasets, but dataset paths and schemas should be parameterized under reviewed contracts. Authentication is determined by the actual linked-service configuration.

**Concrete example:** One ADLS connection can support transaction and customer datasets with separate entity paths and permissions.

### D04. Which measures would prove your Azure Data Factory (ADF) optimization helped?

**Answer:** Record the old/new configuration and comparable workload, measure source query duration, Copy throughput and transformation activity duration with activity output, integration-runtime diagnostics and source/sink throughput, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

**Project explanation:** An accepted watermark is a recovery boundary, not a value to advance after extraction alone. Source commit semantics determine whether timestamp boundaries are reliable.

**Concrete example:** A failed gold transformation reuses landed input and leaves the last accepted source boundary unchanged.

### D05. How would you explain your own contribution to a Azure Data Factory (ADF) interview project?

**Answer:** Identify which pipeline JSON, linked services, trigger definitions and parameterized datasets you personally built/reviewed/operated, one specific failure you resolved, the evidence in source watermark, immutable delivery manifest and accepted run record and a verified outcome. State team-owned components separately and do not invent scale or savings.

**Project explanation:** The pipeline defines dependency and failure paths, while the run records an actual bounded business execution. Separate definition identity from delivery and attempt identity.

**Concrete example:** A daily account pipeline can have one source delivery and three attempts without representing three business loads.

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

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Data Factory (ADF) official documentation](https://learn.microsoft.com/en-us/azure/data-factory/introduction).
- [Integration runtime concepts](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime).

[Back to all 20 interview guides](README.md).
