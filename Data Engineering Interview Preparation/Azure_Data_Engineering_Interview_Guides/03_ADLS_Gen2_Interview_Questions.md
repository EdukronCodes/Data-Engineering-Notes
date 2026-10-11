# Azure Data Lake Storage Gen2 (ADLS) — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Durable lake storage, directory organization, permissions and efficient access for analytical workloads.

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
Approved producer -> immutable ADLS landing -> bronze/silver/gold storage -> governed compute -> accepted SQL/BI consumption
```

For this guide, the primary unit is **one ingestion or curated storage path**. The engineering artifacts are container/path layout, role/ACL assignments and network configuration. Troubleshooting starts with storage request failures, read/list latency, bytes and object counts; durable progress/evidence is represented by delivery manifest, immutable raw path and active table-log references. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is ADLS Gen2?

**Answer:** Azure storage capabilities for analytical lake workloads built on Blob Storage with hierarchical namespace support. It stores files/objects; it does not execute Spark transformations.

**Explanation:** Storage preserves data but does not establish analytical grain or correctness. Those semantics belong to formats, tables, contracts and the processing layer.

**Practical example:** ADLS can hold both raw CSV and gold Delta files, while Spark performs the transformations.

### C02. Why does hierarchical namespace matter?

**Answer:** It provides directory semantics used by data-lake workloads, including directory-oriented operations and ACLs. Evaluate account configuration and feature compatibility before provisioning.

**Explanation:** Directory semantics improve lake organization and path authorization, but account capabilities and migration constraints must be validated before enabling changes.

**Practical example:** Design environment-specific containers and directories under a supported hierarchical-namespace account configuration.

### C03. What is the abfss URI used for?

**Answer:** It identifies secure Azure Blob File System access to a container and path. Authentication still requires the workload's supported identity/credential configuration.

**Explanation:** The URI locates data; it does not grant access. The client's identity, credential configuration, permissions and network route still decide whether reads succeed.

**Practical example:** The same abfss path can work for an engineer and fail for a production job with different grants.

### C04. How do containers and directories differ?

**Answer:** A container is a top-level storage boundary; directories organize paths within it. Choose boundaries based on governance and lifecycle needs, not naming convenience alone.

**Explanation:** Use container boundaries where ownership/access/lifecycle separation requires them. Folders organize datasets but do not automatically isolate identities from broad account grants.

**Practical example:** Restricted raw customer data and generally consumable aggregates can use separately governed storage scopes.

### C05. How do RBAC and ACLs relate?

**Answer:** Azure roles and path ACLs participate in authorization through documented evaluation rules. Broad data-plane role grants can make restrictive ACL assumptions ineffective.

**Explanation:** Authorization evaluation is not simply an intersection of every rule. A broad data-plane role may allow access that a path ACL alone would appear to restrict.

**Practical example:** Test a consumer's actual token instead of assuming a restrictive directory ACL defeats a broad storage role.

### C06. What are access versus default ACLs?

**Answer:** Access ACLs apply to existing objects; default ACLs define inheritance for newly created children. Changing defaults does not automatically rewrite every existing child's ACL.

**Explanation:** Inherited defaults govern new children; existing access entries are separate objects. Permission changes need a deliberate repair/verification plan for older content.

**Practical example:** Fix a writer directory's default ACL, then validate both newly created and previously landed files.

### C07. Which file format would you choose for analytics?

**Answer:** Parquet suits typed columnar analytical scans; JSON/CSV may preserve source interchange; Delta adds a transaction log over data files for table semantics.

**Explanation:** Format affects scan efficiency and types. Preserve source interchange as needed, then convert accepted analytical data under explicit schema and table semantics.

**Practical example:** Retain a raw JSON delivery and produce typed Parquet/Delta columns for repeated selected-column analytics.

### C08. How should lake paths be organized?

**Answer:** Separate source/entity/date/run landing from curated datasets and restricted exceptions. Preserve manifests and avoid high-cardinality directory partitioning without evidence.

**Explanation:** Partitioning changes both write layout and query behavior. High-cardinality paths can increase small files and metadata costs without improving filters.

**Practical example:** Partition a sufficiently large fact by measured date usage rather than by every subscriber ID.

### C09. What do lifecycle policies do?

**Answer:** They automate supported object retention/tiering behavior. Verify compatibility with active table files, recovery needs and the account's enabled features.

**Explanation:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

### C10. What distinguishes storage encryption from authorization?

**Answer:** Encryption protects stored/transmitted data; authorization decides who can access it. Encrypted storage is not proof of appropriate user permissions.

**Explanation:** Encryption and permissions address different threats. Authorized readers still receive plaintext, so data minimization, identity and audit controls remain essential.

**Practical example:** An encrypted customer extract still needs restrictive raw-zone grants and safe exception logging.

## B. Advanced implementation questions

### A01. Why are small files expensive for analytics?

**Answer:** They increase listing/opening/metadata overhead and fragmented reads. Measure actual query and write behavior before choosing compaction or file-size targets.

**Explanation:** File counts can dominate runtime even at modest total bytes. Investigate listing/opening overhead separately from scan and transformation cost.

**Practical example:** A million tiny usage files may benefit from controlled ingestion batching and accepted curated compaction.

### A02. How do you secure network access?

**Answer:** Use supported firewall/private endpoint controls with correct private DNS and permitted workload routes. A valid identity can still fail through network restrictions.

**Explanation:** Private connectivity requires the workload to resolve and route correctly. A private endpoint object is not evidence that every client uses it.

**Practical example:** Resolve the storage hostname from the job's actual execution network and inspect its connection result.

### A03. How do you validate complete delivery?

**Answer:** Use a source manifest, expected file/row counts and checksums where appropriate. Listing currently visible files alone does not establish that the source finished writing.

**Explanation:** Completeness is a producer contract. Validate expected names/counts/checksums or completion markers before treating available objects as a full business delivery.

**Practical example:** Hold a daily ledger batch when one expected regional file is absent from landing.

### A04. How do you design recovery?

**Answer:** Align immutable source retention, table-log/data retention, storage protection and tested restoration with RPO/RTO. Do not equate geo-redundancy with a complete application recovery plan.

**Explanation:** Recovery includes configuration, identities, source retention and consumer state. Storage copies alone may not reproduce an accepted data product.

**Practical example:** Restore raw inputs and relevant table state, rerun controls and validate report as-of boundaries.

### A05. How do you delete sensitive records safely?

**Answer:** Find relevant raw/curated/export copies and apply the approved retention/deletion procedure. Coordinate table-level transactions and physical retention; do not manually delete active Delta files.

**Explanation:** Deletion must account for copies and retention obligations while preserving table consistency. Use supported table/storage procedures rather than arbitrary file removal.

**Practical example:** A sensitive record may exist in raw, silver, exports and retained versions that need coordinated approved handling.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A user can read a file but cannot list its parent. What do you inspect?

**Answer:** Check RBAC and path ACL evaluation, including required traversal permissions on ancestors. Test with the actual user's token and path.

**Why this happens and what matters:** Authorization evaluation is not simply an intersection of every rule. A broad data-plane role may allow access that a path ACL alone would appear to restrict.

**Related practical example:** Test a consumer's actual token instead of assuming a restrictive directory ACL defeats a broad storage role.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. New files inherit the wrong permissions. Why?

**Answer:** Inspect directory default ACLs and the writer's behavior. Correct defaults for future objects and deliberately repair existing ACLs where approved.

**Why this happens and what matters:** Inherited defaults govern new children; existing access entries are separate objects. Permission changes need a deliberate repair/verification plan for older content.

**Related practical example:** Fix a writer directory's default ACL, then validate both newly created and previously landed files.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. A Databricks job gets 403 after an identity change. How do you isolate it?

**Answer:** Check the actual workload identity, storage data-plane roles, ACLs, catalog storage configuration and network routing.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A private endpoint exists but requests still use a public route. What is likely wrong?

**Answer:** Verify DNS resolution and the workload's network path. Endpoint creation alone does not ensure clients resolve/use the private endpoint.

**Why this happens and what matters:** Private connectivity requires the workload to resolve and route correctly. A private endpoint object is not evidence that every client uses it.

**Related practical example:** Resolve the storage hostname from the job's actual execution network and inspect its connection result.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. Millions of tiny JSON files slow ingestion. What would you change?

**Answer:** Measure listing/opening overhead; compact or batch source deliveries and convert accepted data to columnar tables while preserving raw traceability.

**Why this happens and what matters:** File counts can dominate runtime even at modest total bytes. Investigate listing/opening overhead separately from scan and transformation cost.

**Related practical example:** A million tiny usage files may benefit from controlled ingestion batching and accepted curated compaction.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A retention policy removes files still referenced by Delta. What is your response?

**Answer:** Hold consumers, inspect table versions and available backups, restore missing files if possible, and redesign lifecycle rules to respect table retention.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. Someone deletes files directly from a gold table directory. How do you recover?

**Answer:** Inspect transaction-log references and storage recovery options; restore the table consistently. Restrict direct file deletion and use supported table operations.

**Why this happens and what matters:** Completeness is a producer contract. Validate expected names/counts/checksums or completion markers before treating available objects as a full business delivery.

**Related practical example:** Hold a daily ledger batch when one expected regional file is absent from landing.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. An account is being redesigned for hierarchical namespace. What must be checked?

**Answer:** Validate supported enablement/migration paths, workload compatibility, ACL strategy and rollback constraints for the actual account.

**Why this happens and what matters:** Directory semantics improve lake organization and path authorization, but account capabilities and migration constraints must be validated before enabling changes.

**Related practical example:** Design environment-specific containers and directories under a supported hierarchical-namespace account configuration.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A producer overwrites yesterday's source file. How do you retain auditability?

**Answer:** Copy deliveries to immutable run/version paths and record manifest/hash provenance. Corrections create new identified deliveries rather than erasing prior evidence.

**Why this happens and what matters:** Partitioning changes both write layout and query behavior. High-cardinality paths can increase small files and metadata costs without improving filters.

**Related practical example:** Partition a sufficiently large fact by measured date usage rather than by every subscriber ID.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. Storage cost rises while rows remain constant. What do you investigate?

**Answer:** Check retained versions/raw copies, small-file counts, tier/access charges, orphaned exports and transaction-log retention before deleting anything.

**Why this happens and what matters:** Encryption and permissions address different threats. Authorized readers still receive plaintext, so data minimization, identity and audit controls remain essential.

**Related practical example:** An encrypted customer extract still needs restrictive raw-zone grants and safe exception logging.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one ingestion or curated storage path to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Answer:** Capture the effective caller and exact error, then validate data-plane RBAC, directory traversal ACLs, workload identity and storage network route. Compare production with the working configuration using storage request failures, read/list latency, bytes and object counts; do not resolve the incident by giving every identity broad access.

**Why this happens and what matters:** Authorization evaluation is not simply an intersection of every rule. A broad data-plane role may allow access that a path ACL alone would appear to restrict.

**Investigation and correction:** Investigate under the real caller rather than the interactive administrator. The relevant path is data-plane RBAC, directory traversal ACLs, workload identity and storage network route. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

**Related practical example:** Test a consumer's actual token instead of assuming a restrictive directory ACL defeats a broad storage role.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Azure Data Lake Storage Gen2 (ADLS) is available, but the business result has not advanced. What would you check?

**Answer:** Trace the expected operation through source producer and Spark/SQL storage reader and compare progress in delivery manifest, immutable raw path and active table-log references. Inspect storage request failures, read/list latency, bytes and object counts to distinguish a service being reachable from an accepted business operation actually completing.

**Why this happens and what matters:** Completeness is a producer contract. Validate expected names/counts/checksums or completion markers before treating available objects as a full business delivery.

**Investigation and correction:** Walk the dependency chain through source producer and Spark/SQL storage reader and locate the last accepted evidence in delivery manifest, immutable raw path and active table-log references. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

**Related practical example:** Hold a daily ledger batch when one expected regional file is absent from landing.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of container/path layout, role/ACL assignments and network configuration works in test but breaks a dependent production consumer. How do you diagnose it?

**Answer:** Compare versions, environment settings and the actual path conventions, file format, partition keys and retention policy. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Why this happens and what matters:** Recovery includes configuration, identities, source retention and consumer state. Storage copies alone may not reproduce an accepted data product.

**Investigation and correction:** Treat the release as a change to container/path layout, role/ACL assignments and network configuration and its dependencies, not just to one code file. Compare path conventions, file format, partition keys and retention policy and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

**Related practical example:** Restore raw inputs and relevant table state, rerun controls and validate report as-of boundaries.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one ingestion or curated storage path although the request or data volume is unchanged. What is your investigation sequence?

**Answer:** Compare a known-good baseline with storage request failures, read/list latency, bytes and object counts and inspect file listing, tiny-object overhead, read throughput and request rate. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Why this happens and what matters:** File counts can dominate runtime even at modest total bytes. Investigate listing/opening overhead separately from scan and transformation cost.

**Investigation and correction:** Use storage request failures, read/list latency, bytes and object counts to compare the same business boundary and concurrency against a known-good baseline. Examine file listing, tiny-object overhead, read throughput and request rate and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

**Related practical example:** A million tiny usage files may benefit from controlled ingestion batching and accepted curated compaction.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Azure Data Lake Storage Gen2 (ADLS) may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Answer:** Inspect the durable outcome in delivery manifest, immutable raw path and active table-log references before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Investigation and correction:** Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by delivery manifest, immutable raw path and active table-log references and repeat only through a supported safe operation/status mechanism.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one ingestion or curated storage path at the same time. How do you prevent lost or inconsistent state?

**Answer:** Identify the shared resource and ownership boundary in delivery manifest, immutable raw path and active table-log references. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Investigation and correction:** Define who owns the shared mutation and which state version each caller expected. Preserve delivery manifest, immutable raw path and active table-log references so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Azure Data Lake Storage Gen2 (ADLS) without prior notice. How do you contain the impact?

**Answer:** Validate against path conventions, file format, partition keys and retention policy and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Why this happens and what matters:** Directory semantics improve lake organization and path authorization, but account capabilities and migration constraints must be validated before enabling changes.

**Investigation and correction:** Classify the change against path conventions, file format, partition keys and retention policy: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

**Related practical example:** Design environment-specific containers and directories under a supported hierarchical-namespace account configuration.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some delivery manifest, immutable raw path and active table-log references evidence has expired. What can you recover and what should change?

**Answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of delivery manifest, immutable raw path and active table-log references and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Investigation and correction:** Recovery can reconstruct only what still exists and is consistent. Inventory delivery manifest, immutable raw path and active table-log references, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in storage request failures, read/list latency, bytes and object counts. How would you fix the logging and access design?

**Answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review data-plane RBAC, directory traversal ACLs, workload identity and storage network route for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Why this happens and what matters:** Authorization evaluation is not simply an intersection of every rule. A broad data-plane role may allow access that a path ACL alone would appear to restrict.

**Investigation and correction:** Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read storage request failures, read/list latency, bytes and object counts and derived exports; minimizing the source log alone does not remove already copied sensitive output.

**Related practical example:** Test a consumer's actual token instead of assuming a restrictive directory ACL defeats a broad storage role.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Azure Data Lake Storage Gen2 (ADLS) accidentally points to production while rehearsing in development. What controls would you add?

**Answer:** Validate environment/resource identifiers in container/path layout, role/ACL assignments and network configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against delivery manifest, immutable raw path and active table-log references before restoring normal processing.

**Why this happens and what matters:** Recovery includes configuration, identities, source retention and consumer state. Storage copies alone may not reproduce an accepted data product.

**Investigation and correction:** Environment validation belongs before mutation. Bind container/path layout, role/ACL assignments and network configuration to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

**Related practical example:** Restore raw inputs and relevant table state, rerun controls and validate report as-of boundaries.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Source producer and spark/sql storage reader is temporarily unavailable. What retry and recovery policy fits Azure Data Lake Storage Gen2 (ADLS)?

**Answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved delivery manifest, immutable raw path and active table-log references; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Why this happens and what matters:** Storage preserves data but does not establish analytical grain or correctness. Those semantics belong to formats, tables, contracts and the processing layer.

**Investigation and correction:** Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep delivery manifest, immutable raw path and active table-log references durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

**Related practical example:** ADLS can hold both raw CSV and gold Delta files, while Spark performs the transformations.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Azure Data Lake Storage Gen2 (ADLS) rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect file listing, tiny-object overhead, read throughput and request rate. Remove demonstrated waste while preserving required delivery manifest, immutable raw path and active table-log references and correctness/access controls.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Investigation and correction:** Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to file listing, tiny-object overhead, read throughput and request rate and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, container/path layout, role/ACL assignments and network configuration is restored but the business path still fails. What else is required?

**Answer:** Restore/validate data-plane RBAC, directory traversal ACLs, workload identity and storage network route, source producer and Spark/SQL storage reader and the appropriate delivery manifest, immutable raw path and active table-log references. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Why this happens and what matters:** Recovery includes configuration, identities, source retention and consumer state. Storage copies alone may not reproduce an accepted data product.

**Investigation and correction:** Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate data-plane RBAC, directory traversal ACLs, workload identity and storage network route, reconcile delivery manifest, immutable raw path and active table-log references and execute a normal authorized consumer path before calling the recovery successful.

**Related practical example:** Restore raw inputs and relevant table state, rerun controls and validate report as-of boundaries.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Azure Data Lake Storage Gen2 (ADLS). How do you isolate it without silently accepting incomplete results?

**Answer:** Correlate failing business keys/objects with storage request failures, read/list latency, bytes and object counts and validate their path conventions, file format, partition keys and retention policy. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Why this happens and what matters:** Completeness is a producer contract. Validate expected names/counts/checksums or completion markers before treating available objects as a full business delivery.

**Investigation and correction:** Find the smallest complete failed business scope using keys/objects and storage request failures, read/list latency, bytes and object counts. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow path conventions, file format, partition keys and retention policy and preserve a clear accounting of accepted versus failed scope.

**Related practical example:** Hold a daily ledger batch when one expected regional file is absent from landing.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change container/path layout, role/ACL assignments and network configuration while dependent workloads remain active. What release sequence would you use?

**Answer:** Inventory consumers and path conventions, file format, partition keys and retention policy compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain delivery manifest, immutable raw path and active table-log references and define a tested rollback/correction route for incompatible behavior.

**Why this happens and what matters:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Investigation and correction:** Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep delivery manifest, immutable raw path and active table-log references and a tested correction/rollback boundary so a partially applied release remains recoverable.

**Related practical example:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**How to verify the resolution:** Validate the accepted result and the intended path conventions, file format, partition keys and retention policy. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises include implementation reasoning, solution requirements and selected code or flow examples. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a lake directory and permission matrix.

**Answer:** Show source/run landing, curated layers, quarantine, consumer scope and workload identity. Explain traversal and inheritance tests.

**Implementation reasoning:** Directory semantics improve lake organization and path authorization, but account capabilities and migration constraints must be validated before enabling changes.

**Example to work through:** Design environment-specific containers and directories under a supported hierarchical-namespace account configuration.

**Illustrative implementation:**

```text
Scope               Writer            Reader             Recovery evidence
landing/domain      ingestion job     domain engineer    source/run manifest
silver/domain       domain job        approved engineer  input/rule versions
gold/product        publish job       approved consumer  acceptance boundary
quarantine/domain   validation job    assigned steward   restricted reasons
checkpoints/stream  stream identity    stream identity    accepted offsets
# Implement and test actual RBAC/ACL/catalog semantics for these roles.
```

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P02. Build a delivery-manifest validator.

**Answer:** Compare expected objects, size/checksum where meaningful and source control counts; fail a partial delivery before downstream publication.

**Implementation reasoning:** Completeness is a producer contract. Validate expected names/counts/checksums or completion markers before treating available objects as a full business delivery.

**Example to work through:** Hold a daily ledger batch when one expected regional file is absent from landing.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Explain a safe table retention policy.

**Answer:** Map raw recovery, Delta history, stream consumers and deletion obligations; show why deleting arbitrary files is unsafe.

**Implementation reasoning:** Lifecycle automation must not remove files referenced by active transactional tables. Recovery and delayed consumers also need relevant data/log retention.

**Example to work through:** Exclude active Delta storage from arbitrary age-based deletion that ignores the table's retained state.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one ingestion or curated storage path.

**Answer:** Capture the initial delivery manifest, immutable raw path and active table-log references, introduce one realistic dependency or validation failure and use storage request failures, read/list latency, bytes and object counts to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

**Implementation reasoning:** File counts can dominate runtime even at modest total bytes. Investigate listing/opening overhead separately from scan and transformation cost.

**Example to work through:** A million tiny usage files may benefit from controlled ingestion batching and accepted curated compaction.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Azure Data Lake Storage Gen2 (ADLS).

**Answer:** Document container/path layout, role/ACL assignments and network configuration, the path conventions, file format, partition keys and retention policy, required data-plane RBAC, directory traversal ACLs, workload identity and storage network route, owner, normal/failure signals and recovery instructions using delivery manifest, immutable raw path and active table-log references. Include one normal and one failure example plus actual service targets and retention assumptions.

**Implementation reasoning:** The URI locates data; it does not grant access. The client's identity, credential configuration, permissions and network route still decide whether reads succeed.

**Example to work through:** The same abfss path can work for an engineer and fail for a production job with different grants.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Azure Data Lake Storage Gen2 (ADLS) fit in an end-to-end Azure data platform?

**Answer:** Use this specific flow: Approved producer -> immutable ADLS landing -> bronze/silver/gold storage -> governed compute -> accepted SQL/BI consumption. Explain what this component owns, how source producer and Spark/SQL storage reader connects, and what the accepted consumer/result boundary is.

**Project explanation:** Storage preserves data but does not establish analytical grain or correctness. Those semantics belong to formats, tables, contracts and the processing layer.

**Concrete example:** ADLS can hold both raw CSV and gold Delta files, while Spark performs the transformations.

### D02. How would you justify using Azure Data Lake Storage Gen2 (ADLS) for all six project landing and recovery layers?

**Answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one ingestion or curated storage path meets them, compare a credible alternative and validate using storage request failures, read/list latency, bytes and object counts rather than choosing a tool merely because it is on the stack.

**Project explanation:** File counts can dominate runtime even at modest total bytes. Investigate listing/opening overhead separately from scan and transformation cost.

**Concrete example:** A million tiny usage files may benefit from controlled ingestion batching and accepted curated compaction.

### D03. What controls must surround Azure Data Lake Storage Gen2 (ADLS) in a financial or telecom project?

**Answer:** Tie path conventions, file format, partition keys and retention policy to accountable business ownership, verify data-plane RBAC, directory traversal ACLs, workload identity and storage network route, preserve delivery manifest, immutable raw path and active table-log references and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

**Project explanation:** Deletion must account for copies and retention obligations while preserving table consistency. Use supported table/storage procedures rather than arbitrary file removal.

**Concrete example:** A sensitive record may exist in raw, silver, exports and retained versions that need coordinated approved handling.

### D04. Which measures would prove your Azure Data Lake Storage Gen2 (ADLS) optimization helped?

**Answer:** Record the old/new configuration and comparable workload, measure file listing, tiny-object overhead, read throughput and request rate with storage request failures, read/list latency, bytes and object counts, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

**Project explanation:** File counts can dominate runtime even at modest total bytes. Investigate listing/opening overhead separately from scan and transformation cost.

**Concrete example:** A million tiny usage files may benefit from controlled ingestion batching and accepted curated compaction.

### D05. How would you explain your own contribution to a Azure Data Lake Storage Gen2 (ADLS) interview project?

**Answer:** Identify which container/path layout, role/ACL assignments and network configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in delivery manifest, immutable raw path and active table-log references and a verified outcome. State team-owned components separately and do not invent scale or savings.

**Project explanation:** Directory semantics improve lake organization and path authorization, but account capabilities and migration constraints must be validated before enabling changes.

**Concrete example:** Design environment-specific containers and directories under a supported hierarchical-namespace account configuration.

## Revision notes and common mistakes

- Explain Azure Data Lake Storage Gen2 (ADLS)'s specific responsibility in the flow before naming surrounding tools.
- Use the real path conventions, file format, partition keys and retention policy; an accepted request/job does not establish a correct business result.
- Validate data-plane RBAC, directory traversal ACLs, workload identity and storage network route under the actual execution identity, rather than your administrator account.
- Preserve delivery manifest, immutable raw path and active table-log references and inspect it before retrying uncertain side effects.
- Tune file listing, tiny-object overhead, read throughput and request rate from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Data Lake Storage Gen2 (ADLS) official documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction).

[Back to all 20 interview guides](README.md).
