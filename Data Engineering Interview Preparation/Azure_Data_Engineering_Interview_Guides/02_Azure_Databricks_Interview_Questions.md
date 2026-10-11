# Azure Databricks — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Distributed lakehouse transformations, orchestration of Spark workloads and governed analytical serving.

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
ADF or event source -> ADLS/Delta bronze -> Databricks job -> silver transformations -> gold Delta -> Databricks SQL or reporting
```

For this guide, the primary unit is **one Databricks job or notebook task**. The engineering artifacts are job definition, notebook/package version and compute configuration. Troubleshooting starts with Spark UI stages, task skew, job logs and Delta operation history; durable progress/evidence is represented by Delta table version, job run ID and streaming checkpoint where relevant. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is Azure Databricks?

An Azure-integrated data/AI platform used for distributed processing and lakehouse workloads. Distinguish the platform from Apache Spark, which is one processing engine it uses. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Keep workload identity, data location and execution engine explicit so platform features are not confused with Spark's distributed processing behavior.

### C02. What is the driver versus an executor?

The driver coordinates application execution and planning; executors process distributed tasks. Collecting large data to the driver defeats distributed memory scaling. Driver memory and executor memory solve different problems. Distributed transformations scale across executors; collecting an unbounded result centralizes data on the driver.

Write a large usage aggregation directly to a table and collect only a bounded diagnostic sample. Driver-side diagnostics should remain bounded; executor memory, shuffle pressure and partition sizes need separate investigation when distributed tasks fail.

### C03. How do jobs differ from exploratory notebooks?

Jobs provide scheduled/triggered production tasks, parameters and execution controls. Notebooks support development; production requires versioning, ownership and reproducible deployment. Production execution should not depend on cells previously run by a human. Package dependencies, parameters and task order make the job reproducible.

A scheduled job receives an immutable input manifest and rule version instead of reading an interactive variable. Define dependencies, retries and publication gates in the job graph, and capture the input/rule versions needed to reproduce its accepted result.

### C04. What is a Delta table?

A table with transaction-log metadata over data files, providing supported transactional and schema behavior. It is not merely a folder of Parquet files. The transaction log defines active table state, including updates and removed files. Compatible readers use that state rather than reading every physical Parquet file.

After a corrected transaction MERGE, the active table contains the accepted line while obsolete files may remain for retention. Validate the active table snapshot and schema through supported readers; directly scanning storage files can include records removed from current table state.

### C05. What are bronze, silver and gold layers?

Bronze preserves raw/source context, silver conforms business records, and gold serves defined analytical products. They are design conventions, not required platform names. Layer names matter less than clear contracts. Preserve raw provenance, conform business semantics, then publish grain-specific products with acceptance evidence.

Bronze CDRs retain payloads; silver resolves durable events; gold contains subscriber/day/service totals. Each layer should declare grain, permitted changes, ownership and acceptance controls rather than treating directory names alone as a complete architecture.

### C06. How do SQL warehouses differ from Spark job compute?

SQL warehouses serve SQL workloads; Spark compute executes distributed jobs/notebooks. Match compute to workload, isolation and measured concurrency. Serving concurrency and transformation throughput have different resource patterns. Compute separation can reduce interference, but it introduces cost and operational configuration.

A heavy backfill should not automatically share the same execution resource as latency-sensitive BI queries. Measure workload contention and query latency before deciding compute isolation, and include startup/utilization costs when comparing serving and processing configurations.

### C07. What does lazy execution mean?

Spark transformations build a plan and actions trigger computation. Several actions can recompute the same lineage unless reuse is deliberately materialized or persisted. An action can execute the same logical lineage again. Persisting is useful only when actual reuse justifies its resource footprint and lifecycle.

A validated intermediate reused by several downstream calculations may be persisted, then released after those actions. Repeated actions may repeat source reads and wide transformations; cache only genuinely reused data and release it when downstream work completes.

### C08. What should a production notebook accept?

Validated input/output identifiers, run ID, bounded processing scope and rule/configuration version. Return meaningful status without embedding credentials. Input/output parameters must identify an approved scope and remain valid under retry. Arbitrary target names and paths should not become unrestricted execution instructions.

The notebook accepts entity and run IDs and resolves approved target tables from reviewed configuration. Use a run manifest to identify input files/boundaries and target scope, and fail closed when a supplied identifier is outside approved configuration.

### C09. How do you govern access?

Use Unity Catalog object grants and approved storage credentials/external locations where appropriate, plus platform identity/workspace policies. Platform access, catalog grants and cloud storage permissions form different layers. Test the effective workload identity and eliminate unintended direct-storage bypasses.

A production job reads its domain tables through the approved catalog storage abstraction with narrowly scoped grants. Review inherited grants and direct ADLS access as well as table permissions, since broad cloud access can bypass the intended governed table path.

### C10. What does the Spark UI reveal?

Stages, task duration, shuffle volume, skew, spills and execution plans help identify bottlenecks. Correlate them with job input and output evidence. Task-level evidence identifies skew and spill better than overall runtime alone. Compare successful and slow runs with the same data boundary and workload.

A join with one unusually long task suggests a hot key rather than insufficient capacity everywhere. Look at task distributions rather than only averages; one hot-key task can explain why a larger cluster produces little improvement.

## B. Advanced implementation questions

### A01. When should you broadcast a dimension?

When the actual serialized relation is small enough for executor memory and the join plan benefits. Verify size, skew and runtime behavior instead of forcing broadcasts universally. Broadcasting replicates the build-side data where supported, trading shuffle for memory. Estimates, actual relation size and executor pressure determine whether it helps.

A genuinely small approved reference can broadcast; a unexpectedly expanded dimension may require another join strategy. Check actual relation size, serialization and executor capacity; a dimension that was small last month may no longer be safe to broadcast.

### A02. How do you handle late dimension changes?

Maintain effective intervals, reconstruct affected key timelines and re-resolve impacted facts. Closing only the current row may mishandle out-of-order history. Historical integrity requires reconstructing intervals for late changes, not only updating current attributes. Then determine which existing facts used the affected interval.

A backdated account segment correction can require re-resolving last month's transaction facts. Keep source effective history so a correction can reconstruct the timeline, and identify all gold facts that joined to the changed interval.

### A03. How do you make foreachBatch safe?

Design the handler to be idempotent using batch/business keys and transactional target operations where supported. The function can execute more than once. Microbatch handlers can repeat after recovery. Durable target keys, version ordering and accepted batch evidence must make repetition safe.

A replayed microbatch MERGE does not append another daily usage total. Apply only authoritative new source versions and verify that repeated batches leave keys and aggregates unchanged even after a crash between write and checkpoint.

### A04. How do you tune cost and performance together?

Measure cost per accepted workload, startup/runtime, utilization, shuffle and query latency. Select compute and scaling from these measures, not only job duration. Cost improvements must preserve freshness and correctness. Measure startup, runtime, utilization and accepted output rather than reporting only a smaller cluster bill.

An idle-heavy job may benefit from different scheduling/compute configuration while retaining the agreed completion target. Compare cost per accepted run and freshness under representative concurrency; an inexpensive run that misses its business deadline is not an equivalent improvement.

### A05. How do you upgrade runtimes safely?

Pin dependencies, validate API/connector compatibility and run correctness/performance/replay fixtures in test. Promote with a rollback and data compatibility plan. Runtime upgrades can change APIs, connectors and execution behavior. Fixtures should validate values and recovery as well as whether code still imports.

Test decimal rounding, timestamp parsing, MERGE duplicates and stream restart before promoting a new runtime. Retain the previous runtime/package configuration and confirm that any schema/protocol changes still allow a compatible recovery or rollback.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A Spark job spends most time in one task. What do you investigate?

Check skewed keys and partition sizes in task metrics. Filter early, redesign keys or use supported skew handling, then compare the new plan. Task-level evidence identifies skew and spill better than overall runtime alone. Compare successful and slow runs with the same data boundary and workload.

A join with one unusually long task suggests a hot key rather than insufficient capacity everywhere. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. Executors fail after a forced broadcast. What do you do?

Confirm relation size and memory pressure, remove the forced hint if unsuitable, and evaluate a shuffle join with appropriate partitioning. Broadcasting replicates the build-side data where supported, trading shuffle for memory. Estimates, actual relation size and executor pressure determine whether it helps.

A genuinely small approved reference can broadcast; a unexpectedly expanded dimension may require another join strategy. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. The driver crashes during collect(). What is the fix?

Remove large driver materialization. Write distributed output or use bounded samples; increasing driver size alone preserves the faulty scaling design. Driver memory and executor memory solve different problems. Distributed transformations scale across executors; collecting an unbounded result centralizes data on the driver.

Write a large usage aggregation directly to a table and collect only a bounded diagnostic sample. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A job creates thousands of tiny Delta files. How do you improve it?

Measure batch sizes and writer partitions, use suitable compaction/layout maintenance and verify retention. Avoid arbitrary repartitioning without workload evidence. Cost improvements must preserve freshness and correctness. Measure startup, runtime, utilization and accepted output rather than reporting only a smaller cluster bill.

An idle-heavy job may benefit from different scheduling/compute configuration while retaining the agreed completion target. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. Two tasks MERGE the same target partition. How do you respond to conflicts?

Partition ownership or serialize conflicting writes, handle supported optimistic conflicts with bounded retry and verify idempotent results. Input/output parameters must identify an approved scope and remain valid under retry. Arbitrary target names and paths should not become unrestricted execution instructions.

The notebook accepts entity and run IDs and resolves approved target tables from reviewed configuration. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A reference change arrives after gold facts were published. What must change?

Rebuild the affected dimension timeline and identify dependent fact dates. Publish a reconciled revision rather than only changing the current dimension. Historical integrity requires reconstructing intervals for late changes, not only updating current attributes. Then determine which existing facts used the affected interval.

A backdated account segment correction can require re-resolving last month's transaction facts. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. A notebook works interactively but not in a job. What do you compare?

Compare execution identity, runtime, dependencies, parameters, catalog/context and network permissions. Reproduce under the job identity. Input/output parameters must identify an approved scope and remain valid under retry. Arbitrary target names and paths should not become unrestricted execution instructions.

The notebook accepts entity and run IDs and resolves approved target tables from reviewed configuration. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A stream checkpoint is deleted. Is restart from latest safe?

Not automatically. Identify recoverable offsets/raw input and target idempotency; plan controlled replay instead of silently skipping data. Microbatch handlers can repeat after recovery. Durable target keys, version ordering and accepted batch evidence must make repetition safe.

A replayed microbatch MERGE does not append another daily usage total. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. SQL warehouse queries slow during a batch workload. What would you isolate?

Measure concurrency and resource contention; separate serving and transformation compute where justified and tune the expensive query plan. Serving concurrency and transformation throughput have different resource patterns. Compute separation can reduce interference, but it introduces cost and operational configuration.

A heavy backfill should not automatically share the same execution resource as latency-sensitive BI queries. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. A runtime upgrade changes output decimal rounding. How do you detect and prevent it?

Run explicit decimal/null/timezone fixtures and financial reconciliation before promotion. Record the runtime/rule version and roll back incompatible outputs. Runtime upgrades can change APIs, connectors and execution behavior. Fixtures should validate values and recovery as well as whether code still imports.

Test decimal rounding, timestamp parsing, MERGE duplicates and stream restart before promoting a new runtime. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one Databricks job or notebook task to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate job identity, Unity Catalog grants, storage credential and network connectivity. Compare production with the working configuration using Spark UI stages, task skew, job logs and Delta operation history; do not resolve the incident by giving every identity broad access. Platform access, catalog grants and cloud storage permissions form different layers. Test the effective workload identity and eliminate unintended direct-storage bypasses. Investigate under the real caller rather than the interactive administrator. The relevant path is job identity, Unity Catalog grants, storage credential and network connectivity. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

A production job reads its domain tables through the approved catalog storage abstraction with narrowly scoped grants. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Azure Databricks is available, but the business result has not advanced. What would you check?

Trace the expected operation through ADLS source, Unity Catalog metadata and upstream orchestration and compare progress in Delta table version, job run ID and streaming checkpoint where relevant. Inspect Spark UI stages, task skew, job logs and Delta operation history to distinguish a service being reachable from an accepted business operation actually completing. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted. Walk the dependency chain through ADLS source, Unity Catalog metadata and upstream orchestration and locate the last accepted evidence in Delta table version, job run ID and streaming checkpoint where relevant. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of job definition, notebook/package version and compute configuration works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual input schema, source keys and silver/gold table contract. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted. Treat the release as a change to job definition, notebook/package version and compute configuration and its dependencies, not just to one code file. Compare input schema, source keys and silver/gold table contract and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one Databricks job or notebook task although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with Spark UI stages, task skew, job logs and Delta operation history and inspect shuffle spill, skewed tasks, scan volume and compute utilization. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted. Use Spark UI stages, task skew, job logs and Delta operation history to compare the same business boundary and concurrency against a known-good baseline. Examine shuffle spill, skewed tasks, scan volume and compute utilization and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Azure Databricks may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in Delta table version, job run ID and streaming checkpoint where relevant before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. Driver memory and executor memory solve different problems. Distributed transformations scale across executors; collecting an unbounded result centralizes data on the driver. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by Delta table version, job run ID and streaming checkpoint where relevant and repeat only through a supported safe operation/status mechanism.

Write a large usage aggregation directly to a table and collect only a bounded diagnostic sample. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one Databricks job or notebook task at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in Delta table version, job run ID and streaming checkpoint where relevant. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. The transaction log defines active table state, including updates and removed files. Compatible readers use that state rather than reading every physical Parquet file. Define who owns the shared mutation and which state version each caller expected. Preserve Delta table version, job run ID and streaming checkpoint where relevant so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

After a corrected transaction MERGE, the active table contains the accepted line while obsolete files may remain for retention. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Azure Databricks without prior notice. How do you contain the impact?

Validate against input schema, source keys and silver/gold table contract and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Layer names matter less than clear contracts. Preserve raw provenance, conform business semantics, then publish grain-specific products with acceptance evidence. Classify the change against input schema, source keys and silver/gold table contract: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

Bronze CDRs retain payloads; silver resolves durable events; gold contains subscriber/day/service totals. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some Delta table version, job run ID and streaming checkpoint where relevant evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of Delta table version, job run ID and streaming checkpoint where relevant and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. The transaction log defines active table state, including updates and removed files. Compatible readers use that state rather than reading every physical Parquet file. Recovery can reconstruct only what still exists and is consistent. Inventory Delta table version, job run ID and streaming checkpoint where relevant, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

After a corrected transaction MERGE, the active table contains the accepted line while obsolete files may remain for retention. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in Spark UI stages, task skew, job logs and Delta operation history. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review job identity, Unity Catalog grants, storage credential and network connectivity for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Platform access, catalog grants and cloud storage permissions form different layers. Test the effective workload identity and eliminate unintended direct-storage bypasses. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read Spark UI stages, task skew, job logs and Delta operation history and derived exports; minimizing the source log alone does not remove already copied sensitive output.

A production job reads its domain tables through the approved catalog storage abstraction with narrowly scoped grants. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Azure Databricks accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in job definition, notebook/package version and compute configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against Delta table version, job run ID and streaming checkpoint where relevant before restoring normal processing. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted. Environment validation belongs before mutation. Bind job definition, notebook/package version and compute configuration to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Adls source, unity catalog metadata and upstream orchestration is temporarily unavailable. What retry and recovery policy fits Azure Databricks?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved Delta table version, job run ID and streaming checkpoint where relevant; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep Delta table version, job run ID and streaming checkpoint where relevant durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Azure Databricks rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect shuffle spill, skewed tasks, scan volume and compute utilization. Remove demonstrated waste while preserving required Delta table version, job run ID and streaming checkpoint where relevant and correctness/access controls. Cost improvements must preserve freshness and correctness. Measure startup, runtime, utilization and accepted output rather than reporting only a smaller cluster bill. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to shuffle spill, skewed tasks, scan volume and compute utilization and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

An idle-heavy job may benefit from different scheduling/compute configuration while retaining the agreed completion target. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, job definition, notebook/package version and compute configuration is restored but the business path still fails. What else is required?

Restore/validate job identity, Unity Catalog grants, storage credential and network connectivity, ADLS source, Unity Catalog metadata and upstream orchestration and the appropriate Delta table version, job run ID and streaming checkpoint where relevant. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Platform access, catalog grants and cloud storage permissions form different layers. Test the effective workload identity and eliminate unintended direct-storage bypasses. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate job identity, Unity Catalog grants, storage credential and network connectivity, reconcile Delta table version, job run ID and streaming checkpoint where relevant and execute a normal authorized consumer path before calling the recovery successful.

A production job reads its domain tables through the approved catalog storage abstraction with narrowly scoped grants. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Azure Databricks. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with Spark UI stages, task skew, job logs and Delta operation history and validate their input schema, source keys and silver/gold table contract. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted. Find the smallest complete failed business scope using keys/objects and Spark UI stages, task skew, job logs and Delta operation history. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow input schema, source keys and silver/gold table contract and preserve a clear accounting of accepted versus failed scope.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change job definition, notebook/package version and compute configuration while dependent workloads remain active. What release sequence would you use?

Inventory consumers and input schema, source keys and silver/gold table contract compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain Delta table version, job run ID and streaming checkpoint where relevant and define a tested rollback/correction route for incompatible behavior. Input/output parameters must identify an approved scope and remain valid under retry. Arbitrary target names and paths should not become unrestricted execution instructions. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep Delta table version, job run ID and streaming checkpoint where relevant and a tested correction/rollback boundary so a partially applied release remains recoverable.

The notebook accepts entity and run IDs and resolves approved target tables from reviewed configuration. Validate the accepted result and the intended input schema, source keys and silver/gold table contract. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Create a parameterized bronze-to-silver notebook.

Use explicit schemas, bad-record handling, ordered deduplication and target controls. Prove replay produces the same business output. Layer names matter less than clear contracts. Preserve raw provenance, conform business semantics, then publish grain-specific products with acceptance evidence.

Bronze CDRs retain payloads; silver resolves durable events; gold contains subscriber/day/service totals. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Diagnose a slow Spark join from a plan.

Identify join type, shuffle boundaries, estimates and task skew; propose a measured change and explain its tradeoff. Task-level evidence identifies skew and spill better than overall runtime alone. Compare successful and slow runs with the same data boundary and workload.

A join with one unusually long task suggests a hot key rather than insufficient capacity everywhere. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Build a multi-task job dependency graph.

Separate independent tasks, reference dependencies and critical publication gates. Include durable run IDs and failure recovery. Production execution should not depend on cells previously run by a human. Package dependencies, parameters and task order make the job reproducible.

A scheduled job receives an immutable input manifest and rule version instead of reading an interactive variable. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one Databricks job or notebook task.

Capture the initial Delta table version, job run ID and streaming checkpoint where relevant, introduce one realistic dependency or validation failure and use Spark UI stages, task skew, job logs and Delta operation history to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Azure Databricks.

Document job definition, notebook/package version and compute configuration, the input schema, source keys and silver/gold table contract, required job identity, Unity Catalog grants, storage credential and network connectivity, owner, normal/failure signals and recovery instructions using Delta table version, job run ID and streaming checkpoint where relevant. Include one normal and one failure example plus actual service targets and retention assumptions. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Azure Databricks fit in an end-to-end Azure data platform?

Use this specific flow: ADF or event source -> ADLS/Delta bronze -> Databricks job -> silver transformations -> gold Delta -> Databricks SQL or reporting. Explain what this component owns, how ADLS source, Unity Catalog metadata and upstream orchestration connects, and what the accepted consumer/result boundary is. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using Azure Databricks for lake modernization, banking transformations and telecom usage processing?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one Databricks job or notebook task meets them, compare a credible alternative and validate using Spark UI stages, task skew, job logs and Delta operation history rather than choosing a tool merely because it is on the stack. Task-level evidence identifies skew and spill better than overall runtime alone. Compare successful and slow runs with the same data boundary and workload.

A join with one unusually long task suggests a hot key rather than insufficient capacity everywhere. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround Azure Databricks in a financial or telecom project?

Tie input schema, source keys and silver/gold table contract to accountable business ownership, verify job identity, Unity Catalog grants, storage credential and network connectivity, preserve Delta table version, job run ID and streaming checkpoint where relevant and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. Layer names matter less than clear contracts. Preserve raw provenance, conform business semantics, then publish grain-specific products with acceptance evidence.

Bronze CDRs retain payloads; silver resolves durable events; gold contains subscriber/day/service totals. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your Azure Databricks optimization helped?

Record the old/new configuration and comparable workload, measure shuffle spill, skewed tasks, scan volume and compute utilization with Spark UI stages, task skew, job logs and Delta operation history, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. Cost improvements must preserve freshness and correctness. Measure startup, runtime, utilization and accepted output rather than reporting only a smaller cluster bill.

An idle-heavy job may benefit from different scheduling/compute configuration while retaining the agreed completion target. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a Azure Databricks interview project?

Identify which job definition, notebook/package version and compute configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in Delta table version, job run ID and streaming checkpoint where relevant and a verified outcome. State team-owned components separately and do not invent scale or savings. The platform coordinates compute, governance and serving, while Spark distributes computation. Explain which workload uses which engine and where its data is persisted.

A Databricks Spark job creates silver Delta tables and a SQL warehouse serves the accepted gold product. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain Azure Databricks's specific responsibility in the flow before naming surrounding tools.
- Use the real input schema, source keys and silver/gold table contract; an accepted request/job does not establish a correct business result.
- Validate job identity, Unity Catalog grants, storage credential and network connectivity under the actual execution identity, rather than your administrator account.
- Preserve Delta table version, job run ID and streaming checkpoint where relevant and inspect it before retrying uncertain side effects.
- Tune shuffle spill, skewed tasks, scan volume and compute utilization from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Create a parameterized bronze-to-silver notebook.**

```python
# Illustrative notebook setup; paths and tables are reviewed job parameters.
from pyspark.sql import functions as F
raw = (spark.read.schema(input_schema).json(input_path)
       .withColumn("run_id", F.lit(run_id)))
raw.createOrReplaceTempView("staged_input")
# Next: validate the approved schema/business rules, detect contradictory
# source ties, select latest records by authoritative sequence, and MERGE
# into an existing compatible Delta target. Publish only after controls.
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Databricks official documentation](https://learn.microsoft.com/en-us/azure/databricks/introduction/).
- [Structured Streaming with Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/unity-catalog).

[Back to all 20 interview guides](README.md).
