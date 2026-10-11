# Microsoft Fabric — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Integrated ingestion, engineering, OneLake lakehouses, warehouse analytics and Power BI serving.

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
Source connection -> Fabric pipeline -> OneLake bronze -> Spark silver -> validated gold -> semantic model or SQL serving
```

For this guide, the primary unit is **one Fabric pipeline and analytical publication**. The engineering artifacts are workspace items, notebook/pipeline definitions and semantic-model contract. Troubleshooting starts with Fabric run monitoring, capacity metrics and consumer query behavior; durable progress/evidence is represented by OneLake table versions, delivery manifests and accepted product boundary. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is Microsoft Fabric?

A Microsoft SaaS analytics platform with integrated workloads and OneLake. Distinguish its services from separately provisioned Azure ADF, ADLS and Synapse resources. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Use a documented item/workspace architecture so orchestration, Spark, SQL and BI ownership remain clear even though they belong to an integrated platform.

### C02. What is OneLake?

The logical data lake for Fabric tenant data. It is not a user-created ADLS account, even though supported integration can connect to external storage. OneLake organization is tied to Fabric items/workspaces. External ADLS remains a separate resource with its own access, networking and lifecycle controls.

An external landing shortcut references storage rather than converting the external account into OneLake. External storage retains its own security and availability contract; a shortcut or connection does not remove the need to validate that dependency.

### C03. What is a Fabric Lakehouse?

An analytical item that organizes files and tables for engineering/analytics workloads. Delta tables support Spark transformations and supported SQL/BI access. A lakehouse's files and tables have different consumption semantics. Structured table access must use supported table readers and validated schemas.

Raw banking files are preserved while accepted transactions become typed Delta tables. Keep immutable source provenance alongside curated tables, and expose analytical products only after their critical controls and consumer schemas are accepted.

### C04. How do Lakehouse and Warehouse choices differ?

A Lakehouse emphasizes Spark/data-file engineering; a Warehouse emphasizes relational SQL warehouse work. Choose from transformation and serving requirements. Choose from required transformation and serving capabilities. A workload centered on Spark/file engineering can favor a Lakehouse; SQL warehouse write behavior needs its own design.

Do not choose the Lakehouse SQL endpoint for a project that expects it to perform warehouse-style table DML. Document SQL write needs, Spark transformations and expected consumers first, then compare supported functionality and operational tradeoffs for each item type.

### C05. What does the Lakehouse SQL analytics endpoint do?

It provides SQL querying over supported Lakehouse tables. Do not use its read-oriented table access as a substitute for Spark Delta mutations. Querying a Lakehouse through its SQL endpoint and mutating its Delta tables are distinct paths. Use the supported engineering engine for the write.

Run transaction upserts in a Fabric Spark notebook, then validate their query-visible accepted state. After the engineering write, verify the intended query-visible schema and accepted table state rather than assuming every reader updates identically.

### C06. What are shortcuts?

References to supported data locations that can reduce copying. Availability, identity, freshness and source permissions still depend on the target connection. A reference can avoid duplication while increasing dependency on the target's availability/permissions. Check credentials, freshness and supported connection behavior.

If an external reference location disappears, dependent notebook/report behavior needs a defined incident route. Track referenced locations and connection identities so a source access change has an accountable owner and an identifiable downstream impact.

### C07. How does Fabric Data Factory relate to ADF?

Both support integration/orchestration, but connectors, activities, execution and deployment capabilities are not guaranteed identical. Product similarity does not prove connector/activity equivalence. A migration needs an inventory of supported behavior and explicit rewrites for gaps.

Validate REST pagination, scheduling and deployed connections when moving an ADF design into Fabric pipelines. Test scheduling, retry, connector and deployment equivalence explicitly; replacing a product name is not a migration plan for the existing pipeline.

### C08. What is a semantic model?

A governed analytical model of tables, relationships and measures for BI consumption. Its security and aggregation behavior must match the business contract. The semantic model expresses relationships and measure semantics. Correct table rows can still produce incorrect reporting when grains or context are wrong.

Separate daily balance snapshots from transaction activity and create date-aware balance measures. Use known fact/dimension fixtures to validate relationships and measures, and test consumer security separately from direct underlying data access.

### C09. What is Direct Lake conceptually?

A Power BI storage mode designed to use lake-backed data under supported conditions. Validate the model/endpoint type and actual query behavior rather than assuming every model stays on the same path. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Measure actual queries and permissions for the chosen configuration, including any mode-specific behavior relevant to freshness and resource consumption.

### C10. What should separate workspaces achieve?

Environment isolation, ownership and access boundaries. Workspace structure should follow deployment and governance needs, with tested cross-workspace dependencies. Workspace ownership and deployment boundaries should follow the environment and product. Cross-workspace references need tested grants and dependency versions.

Separate development and production artifacts and confirm the production job cannot accidentally use test reference tables. Promote compatible dependent items together and test the target environment with its own identities, connections and reference datasets.

## B. Advanced implementation questions

### A01. How do you control capacity contention?

Measure capacity/workload utilization, execution patterns and consumer latency. Isolate or reschedule heavy workloads and size capacity from evidence. Capacity pressure can affect multiple integrated workloads. Correlate run timing and consumer latency before buying capacity or rescheduling jobs.

A historical banking backfill overlapping morning reports can reveal contention requiring workload/schedule changes. Measure notebook load, BI query latency and overall capacity pressure at matching times, then isolate or schedule the dominant workloads deliberately.

### A02. How do you prevent mixed publication versions?

Use accepted boundaries/manifests and a consumer contract that selects the intended release. Independent table writes are not automatically an atomic product release. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary.

A report should not mix new transaction facts with an old unmarked balance snapshot. Expose the accepted as-of and dependency versions to consumers so intentionally independent publications do not silently appear to be one synchronized snapshot.

### A03. How do you verify underlying data security?

Test OneLake/item/workload permissions and direct SQL/file access independently of Power BI row filters. The effective identity varies by access mode. BI filters do not secure every other data path. Test underlying item/OneLake/SQL access with the relevant identities and effective mode.

A regional consumer must not obtain all countries by bypassing the semantic model and directly querying gold. Validate permitted and denied SQL/file/model routes with actual users, including elevated roles whose effective access can differ from ordinary report consumers.

### A04. How do you deploy Fabric items?

Use supported Git/deployment/API mechanisms for the actual item types and validate dependencies/parameters. Do not assume every item supports the same promotion workflow. Deployment coverage differs by item type and platform support. Maintain an inventory and validate connection/model dependencies after promotion.

An omitted pipeline or semantic-model dependency can make a workspace release incomplete despite a successful deployment step. Inventory unsupported or separately promoted item types and include their connection/configuration checks in the release evidence.

### A05. How do you integrate external Azure storage?

Use supported connections/shortcuts or controlled copying according to security and freshness requirements. Verify external target permissions and network support. External integration preserves external security/freshness obligations. Decide between shortcuts and copying from actual availability, isolation and replay needs.

Copying an accepted dated FX delivery may provide stronger replay evidence than relying only on a changing external reference. Choose copying versus referencing from replay, isolation, latency and ownership requirements, and preserve the accepted external version where historical reproducibility matters.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. The SQL endpoint will not accept your Delta MERGE. What do you do?

Run compatible Delta mutations through Spark notebooks for Lakehouse tables, or choose a SQL Warehouse implementation where the workload requires warehouse DML. Querying a Lakehouse through its SQL endpoint and mutating its Delta tables are distinct paths. Use the supported engineering engine for the write.

Run transaction upserts in a Fabric Spark notebook, then validate their query-visible accepted state. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. A shortcut suddenly becomes unreadable. What do you inspect?

Check external target availability, connection identity/permissions, network support and changes to the referenced location. A reference can avoid duplication while increasing dependency on the target's availability/permissions. Check credentials, freshness and supported connection behavior.

If an external reference location disappears, dependent notebook/report behavior needs a defined incident route. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. Power BI is slow during notebook runs. How do you diagnose it?

Correlate capacity contention, notebook timing, query workload and model behavior; isolate or schedule based on measured resource pressure. Capacity pressure can affect multiple integrated workloads. Correlate run timing and consumer latency before buying capacity or rescheduling jobs.

A historical banking backfill overlapping morning reports can reveal contention requiring workload/schedule changes. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A regional report is filtered but a user can query all gold rows. What is missing?

Underlying data permissions were not scoped as expected. Test serving modes and item/data access separately from semantic-model filters. BI filters do not secure every other data path. Test underlying item/OneLake/SQL access with the relevant identities and effective mode.

A regional consumer must not obtain all countries by bypassing the semantic model and directly querying gold. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. A schema change breaks the semantic model. How would you manage the release?

Version the table/model contract, test dependent measures/relationships and promote compatible changes together or provide a migration version. Product similarity does not prove connector/activity equivalence. A migration needs an inventory of supported behavior and explicit rewrites for gaps.

Validate REST pagination, scheduling and deployed connections when moving an ADF design into Fabric pipelines. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. Gold tables finish at different times and the report combines inconsistent dates. What is the fix?

Define a product publication boundary and consumer accepted-version behavior. Show table/product as-of values when separate releases are intentional. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary.

A report should not mix new transaction facts with an old unmarked balance snapshot. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. An ADF pipeline export cannot run directly in Fabric. Why?

The integration products have different supported features/definitions. Map activities/connections and rebuild unsupported parts with tested equivalence. Product similarity does not prove connector/activity equivalence. A migration needs an inventory of supported behavior and explicit rewrites for gaps.

Validate REST pagination, scheduling and deployed connections when moving an ADF design into Fabric pipelines. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A deployment omits an unsupported item. How do you handle it?

Inventory supported promotion coverage and deploy that item through an approved supported path; verify dependencies and prevent incomplete releases. Deployment coverage differs by item type and platform support. Maintain an inventory and validate connection/model dependencies after promotion.

An omitted pipeline or semantic-model dependency can make a workspace release incomplete despite a successful deployment step. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A financial report sums daily account balances over a month. What must change?

Use snapshot-aware measures and the approved as-of-date definition. Transaction sums and balance snapshots have different aggregation semantics. The semantic model expresses relationships and measure semantics. Correct table rows can still produce incorrect reporting when grains or context are wrong.

Separate daily balance snapshots from transaction activity and create date-aware balance measures. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. The pipeline succeeds but the source data is stale. How do you make that visible?

Monitor last accepted business/source timestamp and freshness target, not only pipeline status; hold or flag the product under its contract. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary.

A report should not mix new transaction facts with an old unmarked balance snapshot. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one Fabric pipeline and analytical publication to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate connection identity, workspace/item/OneLake permissions and semantic-model security. Compare production with the working configuration using Fabric run monitoring, capacity metrics and consumer query behavior; do not resolve the incident by giving every identity broad access. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration. Investigate under the real caller rather than the interactive administrator. The relevant path is connection identity, workspace/item/OneLake permissions and semantic-model security. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Microsoft Fabric is available, but the business result has not advanced. What would you check?

Trace the expected operation through external source connection and Power BI or SQL consumers and compare progress in OneLake table versions, delivery manifests and accepted product boundary. Inspect Fabric run monitoring, capacity metrics and consumer query behavior to distinguish a service being reachable from an accepted business operation actually completing. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration. Walk the dependency chain through external source connection and Power BI or SQL consumers and locate the last accepted evidence in OneLake table versions, delivery manifests and accepted product boundary. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of workspace items, notebook/pipeline definitions and semantic-model contract works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual Lakehouse schema, gold product grain and semantic-model relationships. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Workspace ownership and deployment boundaries should follow the environment and product. Cross-workspace references need tested grants and dependency versions. Treat the release as a change to workspace items, notebook/pipeline definitions and semantic-model contract and its dependencies, not just to one code file. Compare Lakehouse schema, gold product grain and semantic-model relationships and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

Separate development and production artifacts and confirm the production job cannot accidentally use test reference tables. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one Fabric pipeline and analytical publication although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with Fabric run monitoring, capacity metrics and consumer query behavior and inspect capacity contention, Spark processing time and model query latency. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration. Use Fabric run monitoring, capacity metrics and consumer query behavior to compare the same business boundary and concurrency against a known-good baseline. Examine capacity contention, Spark processing time and model query latency and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Microsoft Fabric may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in OneLake table versions, delivery manifests and accepted product boundary before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by OneLake table versions, delivery manifests and accepted product boundary and repeat only through a supported safe operation/status mechanism.

A report should not mix new transaction facts with an old unmarked balance snapshot. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one Fabric pipeline and analytical publication at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in OneLake table versions, delivery manifests and accepted product boundary. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. OneLake organization is tied to Fabric items/workspaces. External ADLS remains a separate resource with its own access, networking and lifecycle controls. Define who owns the shared mutation and which state version each caller expected. Preserve OneLake table versions, delivery manifests and accepted product boundary so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

An external landing shortcut references storage rather than converting the external account into OneLake. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Microsoft Fabric without prior notice. How do you contain the impact?

Validate against Lakehouse schema, gold product grain and semantic-model relationships and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration. Classify the change against Lakehouse schema, gold product grain and semantic-model relationships: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some OneLake table versions, delivery manifests and accepted product boundary evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of OneLake table versions, delivery manifests and accepted product boundary and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary. Recovery can reconstruct only what still exists and is consistent. Inventory OneLake table versions, delivery manifests and accepted product boundary, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

A report should not mix new transaction facts with an old unmarked balance snapshot. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in Fabric run monitoring, capacity metrics and consumer query behavior. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review connection identity, workspace/item/OneLake permissions and semantic-model security for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read Fabric run monitoring, capacity metrics and consumer query behavior and derived exports; minimizing the source log alone does not remove already copied sensitive output.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Microsoft Fabric accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in workspace items, notebook/pipeline definitions and semantic-model contract, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against OneLake table versions, delivery manifests and accepted product boundary before restoring normal processing. Workspace ownership and deployment boundaries should follow the environment and product. Cross-workspace references need tested grants and dependency versions. Environment validation belongs before mutation. Bind workspace items, notebook/pipeline definitions and semantic-model contract to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

Separate development and production artifacts and confirm the production job cannot accidentally use test reference tables. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. External source connection and power bi or sql consumers is temporarily unavailable. What retry and recovery policy fits Microsoft Fabric?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved OneLake table versions, delivery manifests and accepted product boundary; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep OneLake table versions, delivery manifests and accepted product boundary durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Microsoft Fabric rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect capacity contention, Spark processing time and model query latency. Remove demonstrated waste while preserving required OneLake table versions, delivery manifests and accepted product boundary and correctness/access controls. OneLake organization is tied to Fabric items/workspaces. External ADLS remains a separate resource with its own access, networking and lifecycle controls. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to capacity contention, Spark processing time and model query latency and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

An external landing shortcut references storage rather than converting the external account into OneLake. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, workspace items, notebook/pipeline definitions and semantic-model contract is restored but the business path still fails. What else is required?

Restore/validate connection identity, workspace/item/OneLake permissions and semantic-model security, external source connection and Power BI or SQL consumers and the appropriate OneLake table versions, delivery manifests and accepted product boundary. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate connection identity, workspace/item/OneLake permissions and semantic-model security, reconcile OneLake table versions, delivery manifests and accepted product boundary and execute a normal authorized consumer path before calling the recovery successful.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Microsoft Fabric. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with Fabric run monitoring, capacity metrics and consumer query behavior and validate their Lakehouse schema, gold product grain and semantic-model relationships. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration. Find the smallest complete failed business scope using keys/objects and Fabric run monitoring, capacity metrics and consumer query behavior. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow Lakehouse schema, gold product grain and semantic-model relationships and preserve a clear accounting of accepted versus failed scope.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change workspace items, notebook/pipeline definitions and semantic-model contract while dependent workloads remain active. What release sequence would you use?

Inventory consumers and Lakehouse schema, gold product grain and semantic-model relationships compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain OneLake table versions, delivery manifests and accepted product boundary and define a tested rollback/correction route for incompatible behavior. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep OneLake table versions, delivery manifests and accepted product boundary and a tested correction/rollback boundary so a partially applied release remains recoverable.

A report should not mix new transaction facts with an old unmarked balance snapshot. Validate the accepted result and the intended Lakehouse schema, gold product grain and semantic-model relationships. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Draw a Fabric banking analytical platform.

Include supported connections, pipeline, OneLake layers, Spark rules, source reconciliation, accepted publication and semantic-model access. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Design Lakehouse versus Warehouse selection.

State data shape, transformation engine, SQL write needs, BI consumers, operational tradeoffs and tested permissions. Choose from required transformation and serving capabilities. A workload centered on Spark/file engineering can favor a Lakehouse; SQL warehouse write behavior needs its own design.

Do not choose the Lakehouse SQL endpoint for a project that expects it to perform warehouse-style table DML. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Demonstrate a late transaction correction.

Replay a bounded source scope, resolve historical dimensions/FX, reconcile and publish an accepted replacement without duplicating facts. Consumers need a defined accepted-product view when several tables change. Independent commits do not automatically provide one multi-table release boundary.

A report should not mix new transaction facts with an old unmarked balance snapshot. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one Fabric pipeline and analytical publication.

Capture the initial OneLake table versions, delivery manifests and accepted product boundary, introduce one realistic dependency or validation failure and use Fabric run monitoring, capacity metrics and consumer query behavior to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. BI filters do not secure every other data path. Test underlying item/OneLake/SQL access with the relevant identities and effective mode.

A regional consumer must not obtain all countries by bypassing the semantic model and directly querying gold. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Microsoft Fabric.

Document workspace items, notebook/pipeline definitions and semantic-model contract, the Lakehouse schema, gold product grain and semantic-model relationships, required connection identity, workspace/item/OneLake permissions and semantic-model security, owner, normal/failure signals and recovery instructions using OneLake table versions, delivery manifests and accepted product boundary. Include one normal and one failure example plus actual service targets and retention assumptions. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Microsoft Fabric fit in an end-to-end Azure data platform?

Use this specific flow: Source connection -> Fabric pipeline -> OneLake bronze -> Spark silver -> validated gold -> semantic model or SQL serving. Explain what this component owns, how external source connection and Power BI or SQL consumers connects, and what the accepted consumer/result boundary is. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using Microsoft Fabric for Citi EMEA reference Fabric banking analytics design?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one Fabric pipeline and analytical publication meets them, compare a credible alternative and validate using Fabric run monitoring, capacity metrics and consumer query behavior rather than choosing a tool merely because it is on the stack. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround Microsoft Fabric in a financial or telecom project?

Tie Lakehouse schema, gold product grain and semantic-model relationships to accountable business ownership, verify connection identity, workspace/item/OneLake permissions and semantic-model security, preserve OneLake table versions, delivery manifests and accepted product boundary and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your Microsoft Fabric optimization helped?

Record the old/new configuration and comparable workload, measure capacity contention, Spark processing time and model query latency with Fabric run monitoring, capacity metrics and consumer query behavior, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. Direct Lake behavior depends on the actual supported mode/model and data access route. Inspect real query behavior and permissions for the target configuration.

Validate a model against the chosen Lakehouse/Warehouse source rather than assuming all Fabric tables use identical BI access. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a Microsoft Fabric interview project?

Identify which workspace items, notebook/pipeline definitions and semantic-model contract you personally built/reviewed/operated, one specific failure you resolved, the evidence in OneLake table versions, delivery manifests and accepted product boundary and a verified outcome. State team-owned components separately and do not invent scale or savings. Integrated workloads reduce some plumbing but do not eliminate source contracts, identity boundaries or operational ownership. Describe the actual Fabric item and engine involved.

A Fabric pipeline lands data, a Spark notebook transforms it and Power BI consumes the accepted model. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain Microsoft Fabric's specific responsibility in the flow before naming surrounding tools.
- Use the real Lakehouse schema, gold product grain and semantic-model relationships; an accepted request/job does not establish a correct business result.
- Validate connection identity, workspace/item/OneLake permissions and semantic-model security under the actual execution identity, rather than your administrator account.
- Preserve OneLake table versions, delivery manifests and accepted product boundary and inspect it before retrying uncertain side effects.
- Tune capacity contention, Spark processing time and model query latency from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Draw a Fabric banking analytical platform.**

```text
Regional source + customer/account + dated FX + balance feed
-> supported Fabric connection/gateway
-> immutable landed delivery + manifest
-> OneLake bronze
-> Fabric Spark: validate, order changes, resolve historical dimensions
-> gold transaction and balance facts
-> currency/date reconciliation gate
-> accepted publication
-> Power BI semantic model with snapshot-aware measures and tested access
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Microsoft Fabric official documentation](https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview).
- [Enterprise BI architecture](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/analytics/enterprise-bi-microsoft-fabric).

[Back to all 20 interview guides](README.md).
