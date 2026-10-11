# Unity Catalog — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Governed Databricks objects, workload access, storage abstraction and metadata/lineage visibility.

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
Entra workload/user identity -> catalog and schema privileges -> governed table/volume -> approved storage access -> audited consumption
```

For this guide, the primary unit is **one governed object access or grant change**. The engineering artifacts are catalog/schema definitions, reviewed grants and storage-location configuration. Troubleshooting starts with effective privileges, audit events, query identity and supported lineage; durable progress/evidence is represented by approved grant matrix, ownership record and migration acceptance boundary. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is Unity Catalog?

**Answer:** The Databricks governance layer for supported data/AI assets. It manages securable objects, grants and governance capabilities; Azure storage authorization remains relevant.

**Explanation:** Governance describes and controls supported Databricks assets, but direct cloud access can bypass intended paths. Review both catalog and underlying storage grants.

**Practical example:** A masked customer table is insufficient if the same user can download raw ADLS files.

### C02. What is the object hierarchy?

**Answer:** Common table addressing uses catalog.schema.table within a metastore governance context. Different securable object types have their own privileges.

**Explanation:** Parent usage and object privileges participate in an access path. Fully qualify objects to avoid accidental use of similarly named tables in another catalog.

**Practical example:** A job resolves prod.finance.journal and needs the appropriate parent usage plus table access.

### C03. How do managed and external tables differ?

**Answer:** Managed tables let the platform manage relevant data lifecycle; external tables reference externally managed storage. Verify drop/data-retention behavior for the actual table type.

**Explanation:** Lifecycle ownership differs by table type. Dropping metadata and deleting files must follow actual managed/external behavior and retention contracts.

**Practical example:** An external table drop may not justify deleting files still used by another workload.

### C04. What is a storage credential?

**Answer:** An approved credential abstraction used by governed access to external storage. Its backing identity must have appropriate cloud permissions.

**Explanation:** The credential abstraction maps to a real cloud identity. Its permissions, network route and object scope remain operational dependencies.

**Practical example:** A correctly registered credential fails when its backing identity loses ADLS data access.

### C05. What is an external location?

**Answer:** A governed storage path associated with a storage credential. It scopes supported external data access without distributing raw secrets.

**Explanation:** A location couples a governed path with a credential and privileges. Prevent overlapping/broad paths that unintentionally expose unrelated datasets.

**Practical example:** Grant a producer access to its approved domain location rather than all raw storage.

### C06. What are volumes for?

**Answer:** Governed access to supported non-tabular files. Do not confuse file access through a volume with querying a table.

**Explanation:** Non-tabular files need governed file access distinct from relational table grants. Use a supported volume/path pattern for that requirement.

**Practical example:** A notebook reads an approved reference file through a governed volume without handing out a storage secret.

### C07. Why do users need USE privileges?

**Answer:** Object selection/access involves parent catalog/schema usage as well as the object permission. Diagnose the full privilege path.

**Explanation:** Parent/object checks should be diagnosed under the effective caller. Granting SELECT alone may not satisfy all necessary catalog/schema usage conditions.

**Practical example:** Compare an author's successful query with the production service identity's full privilege chain.

### C08. How does ownership differ from reading?

**Answer:** Ownership confers management authority under the governance model; SELECT is a data-read privilege. Assign ownership to accountable groups, not casually to every reader.

**Explanation:** Ownership should belong to accountable groups with controlled membership. Readers usually require narrower permissions than object administrators.

**Practical example:** A consumer receives read access while a data-product owner group controls schema/grant management.

### C09. What is lineage useful for?

**Answer:** Tracing supported upstream/downstream relationships and impact. Validate capture coverage for actual execution paths rather than assuming all external movement is captured.

**Explanation:** Lineage coverage depends on supported execution and movement paths. Missing capture requires documented/custom integration, not an unsupported claim of complete automatic visibility.

**Practical example:** An external exported CSV may need an explicitly registered/documented downstream relationship.

### C10. What does workspace access establish?

**Answer:** It allows platform workspace use subject to controls; it is not automatic permission to every governed data object.

**Explanation:** Workspace/compute access and data access are separate gates. A platform login does not authorize every catalog asset.

**Practical example:** A user can enter the workspace but still cannot read restricted account tables.

## B. Advanced implementation questions

### A01. How do you design least privilege?

**Answer:** Separate producer, engineer, steward and consumer groups; grant required parent/object permissions and control direct cloud access that could bypass governance.

**Explanation:** Least privilege includes controlling group inheritance and cloud bypass routes. Verify both permitted operations and representative denied operations.

**Practical example:** Test regional consumer grants, production writer scope and direct-storage denial separately.

### A02. How do you migrate legacy access?

**Answer:** Inventory tables/paths/identities, map ownership/grants and compatible compute access, test workload identities, then cut over with traceable reconciliation.

**Explanation:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Practical example:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

### A03. How do masking and row filtering help?

**Answer:** Supported policies restrict exposed values/rows for applicable query paths. Verify function/policy compatibility and bypass routes for the actual runtime.

**Explanation:** Policies must be supported by the actual runtime/query path and its identities. Test function behavior and alternate access routes explicitly.

**Practical example:** A row-filter policy is verified on the consumer warehouse while broad raw-file access is removed.

### A04. How do you govern production jobs?

**Answer:** Use approved service/workload identities, narrowly scoped grants and reviewed deployment permissions. Test jobs under their production identity.

**Explanation:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Practical example:** Use an approved service identity with only required catalog objects and storage path access.

### A05. How do you audit access effectively?

**Answer:** Correlate supported audit events with identities, object names and execution context; protect logs and retain them under the approved policy.

**Explanation:** Auditing must identify caller, object and operation while protecting payload values. Retain enough evidence to investigate real access and ownership changes.

**Practical example:** Correlate a restricted query attempt with its job/user identity and object grant state.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. SELECT is granted but the user still cannot query. What do you inspect?

**Answer:** Check catalog/schema USE privileges, workspace/compute eligibility, object name and the effective identity.

**Why this happens and what matters:** Parent/object checks should be diagnosed under the effective caller. Granting SELECT alone may not satisfy all necessary catalog/schema usage conditions.

**Related practical example:** Compare an author's successful query with the production service identity's full privilege chain.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. A storage credential exists but a job gets a storage error. What might be wrong?

**Answer:** Verify backing cloud identity permissions, external-location path, network access and the job's object privileges.

**Why this happens and what matters:** The credential abstraction maps to a real cloud identity. Its permissions, network route and object scope remain operational dependencies.

**Related practical example:** A correctly registered credential fails when its backing identity loses ADLS data access.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. An engineer can bypass filters by opening raw ADLS files. What is the gap?

**Answer:** Direct storage access bypasses the intended catalog path. Review cloud roles/ACLs and permitted external-location access alongside table policies.

**Why this happens and what matters:** Least privilege includes controlling group inheritance and cloud bypass routes. Verify both permitted operations and representative denied operations.

**Related practical example:** Test regional consumer grants, production writer scope and direct-storage denial separately.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A job succeeds for its author but fails as a service identity. What changes?

**Answer:** Grant the service identity the specific parent/object privileges and approved execution/storage path; avoid reusing the author's broad grants.

**Why this happens and what matters:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Related practical example:** Use an approved service identity with only required catalog objects and storage path access.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. A table is dropped and its files remain. Is that always wrong?

**Answer:** External versus managed lifecycle behavior differs. Check table type and retention contracts before cleanup; do not delete data still used elsewhere.

**Why this happens and what matters:** Lifecycle ownership differs by table type. Dropping metadata and deleting files must follow actual managed/external behavior and retention contracts.

**Related practical example:** An external table drop may not justify deleting files still used by another workload.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. Several teams need the same data with separate ownership. How do you organize it?

**Answer:** Define catalogs/schemas and consumer grants around accountable domains, with shared approved products and explicit ownership.

**Why this happens and what matters:** Ownership should belong to accountable groups with controlled membership. Readers usually require narrower permissions than object administrators.

**Related practical example:** A consumer receives read access while a data-product owner group controls schema/grant management.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. Lineage is missing for an external export. What do you do?

**Answer:** Verify supported lineage capture for that path and record/document/custom-register the missing relationship through an approved mechanism.

**Why this happens and what matters:** Lineage coverage depends on supported execution and movement paths. Missing capture requires documented/custom integration, not an unsupported claim of complete automatic visibility.

**Related practical example:** An external exported CSV may need an explicitly registered/documented downstream relationship.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. Granting a catalog-wide privilege exposes unintended objects. How do you prevent recurrence?

**Answer:** Review inherited/broad grants and group membership, narrow scope and test representative restricted objects.

**Why this happens and what matters:** Least privilege includes controlling group inheritance and cloud bypass routes. Verify both permitted operations and representative denied operations.

**Related practical example:** Test regional consumer grants, production writer scope and direct-storage denial separately.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A masking policy fails on one compute/runtime. What do you check?

**Answer:** Validate policy support and execution compatibility for the actual compute/runtime, then use a supported controlled path.

**Why this happens and what matters:** Policies must be supported by the actual runtime/query path and its identities. Test function behavior and alternate access routes explicitly.

**Related practical example:** A row-filter policy is verified on the consumer warehouse while broad raw-file access is removed.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. A legacy notebook uses direct secret-backed storage paths. How would you modernize it?

**Answer:** Migrate to approved storage credentials/external locations or volumes/tables, remove unnecessary direct secrets and validate equivalent output/access.

**Why this happens and what matters:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Related practical example:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one governed object access or grant change to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Answer:** Capture the effective caller and exact error, then validate USE and object privileges, backing storage identity and workspace/compute eligibility. Compare production with the working configuration using effective privileges, audit events, query identity and supported lineage; do not resolve the incident by giving every identity broad access.

**Why this happens and what matters:** Parent/object checks should be diagnosed under the effective caller. Granting SELECT alone may not satisfy all necessary catalog/schema usage conditions.

**Investigation and correction:** Investigate under the real caller rather than the interactive administrator. The relevant path is USE and object privileges, backing storage identity and workspace/compute eligibility. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

**Related practical example:** Compare an author's successful query with the production service identity's full privilege chain.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Unity Catalog is available, but the business result has not advanced. What would you check?

**Answer:** Trace the expected operation through Microsoft Entra identities, Databricks compute and Azure storage and compare progress in approved grant matrix, ownership record and migration acceptance boundary. Inspect effective privileges, audit events, query identity and supported lineage to distinguish a service being reachable from an accepted business operation actually completing.

**Why this happens and what matters:** Parent/object checks should be diagnosed under the effective caller. Granting SELECT alone may not satisfy all necessary catalog/schema usage conditions.

**Investigation and correction:** Walk the dependency chain through Microsoft Entra identities, Databricks compute and Azure storage and locate the last accepted evidence in approved grant matrix, ownership record and migration acceptance boundary. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

**Related practical example:** Compare an author's successful query with the production service identity's full privilege chain.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of catalog/schema definitions, reviewed grants and storage-location configuration works in test but breaks a dependent production consumer. How do you diagnose it?

**Answer:** Compare versions, environment settings and the actual object ownership, data classification and permitted consumer paths. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Why this happens and what matters:** Least privilege includes controlling group inheritance and cloud bypass routes. Verify both permitted operations and representative denied operations.

**Investigation and correction:** Treat the release as a change to catalog/schema definitions, reviewed grants and storage-location configuration and its dependencies, not just to one code file. Compare object ownership, data classification and permitted consumer paths and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

**Related practical example:** Test regional consumer grants, production writer scope and direct-storage denial separately.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one governed object access or grant change although the request or data volume is unchanged. What is your investigation sequence?

**Answer:** Compare a known-good baseline with effective privileges, audit events, query identity and supported lineage and inspect authorization resolution, storage connectivity and unsupported execution paths. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Why this happens and what matters:** A location couples a governed path with a credential and privileges. Prevent overlapping/broad paths that unintentionally expose unrelated datasets.

**Investigation and correction:** Use effective privileges, audit events, query identity and supported lineage to compare the same business boundary and concurrency against a known-good baseline. Examine authorization resolution, storage connectivity and unsupported execution paths and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

**Related practical example:** Grant a producer access to its approved domain location rather than all raw storage.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Unity Catalog may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Answer:** Inspect the durable outcome in approved grant matrix, ownership record and migration acceptance boundary before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Why this happens and what matters:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Investigation and correction:** Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by approved grant matrix, ownership record and migration acceptance boundary and repeat only through a supported safe operation/status mechanism.

**Related practical example:** Use an approved service identity with only required catalog objects and storage path access.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one governed object access or grant change at the same time. How do you prevent lost or inconsistent state?

**Answer:** Identify the shared resource and ownership boundary in approved grant matrix, ownership record and migration acceptance boundary. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Why this happens and what matters:** A location couples a governed path with a credential and privileges. Prevent overlapping/broad paths that unintentionally expose unrelated datasets.

**Investigation and correction:** Define who owns the shared mutation and which state version each caller expected. Preserve approved grant matrix, ownership record and migration acceptance boundary so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

**Related practical example:** Grant a producer access to its approved domain location rather than all raw storage.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Unity Catalog without prior notice. How do you contain the impact?

**Answer:** Validate against object ownership, data classification and permitted consumer paths and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Why this happens and what matters:** Auditing must identify caller, object and operation while protecting payload values. Retain enough evidence to investigate real access and ownership changes.

**Investigation and correction:** Classify the change against object ownership, data classification and permitted consumer paths: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

**Related practical example:** Correlate a restricted query attempt with its job/user identity and object grant state.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some approved grant matrix, ownership record and migration acceptance boundary evidence has expired. What can you recover and what should change?

**Answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of approved grant matrix, ownership record and migration acceptance boundary and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Why this happens and what matters:** Auditing must identify caller, object and operation while protecting payload values. Retain enough evidence to investigate real access and ownership changes.

**Investigation and correction:** Recovery can reconstruct only what still exists and is consistent. Inventory approved grant matrix, ownership record and migration acceptance boundary, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

**Related practical example:** Correlate a restricted query attempt with its job/user identity and object grant state.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in effective privileges, audit events, query identity and supported lineage. How would you fix the logging and access design?

**Answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review USE and object privileges, backing storage identity and workspace/compute eligibility for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Why this happens and what matters:** Auditing must identify caller, object and operation while protecting payload values. Retain enough evidence to investigate real access and ownership changes.

**Investigation and correction:** Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read effective privileges, audit events, query identity and supported lineage and derived exports; minimizing the source log alone does not remove already copied sensitive output.

**Related practical example:** Correlate a restricted query attempt with its job/user identity and object grant state.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Unity Catalog accidentally points to production while rehearsing in development. What controls would you add?

**Answer:** Validate environment/resource identifiers in catalog/schema definitions, reviewed grants and storage-location configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against approved grant matrix, ownership record and migration acceptance boundary before restoring normal processing.

**Why this happens and what matters:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Investigation and correction:** Environment validation belongs before mutation. Bind catalog/schema definitions, reviewed grants and storage-location configuration to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

**Related practical example:** Use an approved service identity with only required catalog objects and storage path access.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Microsoft entra identities, databricks compute and azure storage is temporarily unavailable. What retry and recovery policy fits Unity Catalog?

**Answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved approved grant matrix, ownership record and migration acceptance boundary; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Why this happens and what matters:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Investigation and correction:** Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep approved grant matrix, ownership record and migration acceptance boundary durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

**Related practical example:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Unity Catalog rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect authorization resolution, storage connectivity and unsupported execution paths. Remove demonstrated waste while preserving required approved grant matrix, ownership record and migration acceptance boundary and correctness/access controls.

**Why this happens and what matters:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Investigation and correction:** Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to authorization resolution, storage connectivity and unsupported execution paths and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

**Related practical example:** Use an approved service identity with only required catalog objects and storage path access.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, catalog/schema definitions, reviewed grants and storage-location configuration is restored but the business path still fails. What else is required?

**Answer:** Restore/validate USE and object privileges, backing storage identity and workspace/compute eligibility, Microsoft Entra identities, Databricks compute and Azure storage and the appropriate approved grant matrix, ownership record and migration acceptance boundary. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Why this happens and what matters:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Investigation and correction:** Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate USE and object privileges, backing storage identity and workspace/compute eligibility, reconcile approved grant matrix, ownership record and migration acceptance boundary and execute a normal authorized consumer path before calling the recovery successful.

**Related practical example:** Use an approved service identity with only required catalog objects and storage path access.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Unity Catalog. How do you isolate it without silently accepting incomplete results?

**Answer:** Correlate failing business keys/objects with effective privileges, audit events, query identity and supported lineage and validate their object ownership, data classification and permitted consumer paths. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Why this happens and what matters:** Auditing must identify caller, object and operation while protecting payload values. Retain enough evidence to investigate real access and ownership changes.

**Investigation and correction:** Find the smallest complete failed business scope using keys/objects and effective privileges, audit events, query identity and supported lineage. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow object ownership, data classification and permitted consumer paths and preserve a clear accounting of accepted versus failed scope.

**Related practical example:** Correlate a restricted query attempt with its job/user identity and object grant state.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change catalog/schema definitions, reviewed grants and storage-location configuration while dependent workloads remain active. What release sequence would you use?

**Answer:** Inventory consumers and object ownership, data classification and permitted consumer paths compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain approved grant matrix, ownership record and migration acceptance boundary and define a tested rollback/correction route for incompatible behavior.

**Why this happens and what matters:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Investigation and correction:** Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep approved grant matrix, ownership record and migration acceptance boundary and a tested correction/rollback boundary so a partially applied release remains recoverable.

**Related practical example:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

**How to verify the resolution:** Validate the accepted result and the intended object ownership, data classification and permitted consumer paths. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises include implementation reasoning, solution requirements and selected code or flow examples. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a catalog/schema/grant matrix.

**Answer:** Include owner, production writer, steward and consumer with required parent/object privileges and cloud-bypass review.

**Implementation reasoning:** Parent/object checks should be diagnosed under the effective caller. Granting SELECT alone may not satisfy all necessary catalog/schema usage conditions.

**Example to work through:** Compare an author's successful query with the production service identity's full privilege chain.

**Illustrative implementation:**

```sql
-- Illustrative Unity Catalog grants on pre-existing objects/groups.
GRANT USE CATALOG ON CATALOG prod TO `finance_consumers`;
GRANT USE SCHEMA ON SCHEMA prod.finance TO `finance_consumers`;
GRANT SELECT ON TABLE prod.finance.accepted_journal
TO `finance_consumers`;
-- Separately validate workspace/compute eligibility, ownership,
-- effective inherited grants and unintended direct cloud-storage access.
```

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P02. Trace an access-denied incident.

**Answer:** Show effective identity, workspace/compute context, object grants, external location and cloud/network authorization checks.

**Implementation reasoning:** The credential abstraction maps to a real cloud identity. Its permissions, network route and object scope remain operational dependencies.

**Example to work through:** A correctly registered credential fails when its backing identity loses ADLS data access.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Plan a legacy table migration.

**Answer:** Inventory location/type/history, recreate governance, validate data/grants and cut over consumers with recovery evidence.

**Implementation reasoning:** Governance describes and controls supported Databricks assets, but direct cloud access can bypass intended paths. Review both catalog and underlying storage grants.

**Example to work through:** A masked customer table is insufficient if the same user can download raw ADLS files.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one governed object access or grant change.

**Answer:** Capture the initial approved grant matrix, ownership record and migration acceptance boundary, introduce one realistic dependency or validation failure and use effective privileges, audit events, query identity and supported lineage to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

**Implementation reasoning:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Example to work through:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Unity Catalog.

**Answer:** Document catalog/schema definitions, reviewed grants and storage-location configuration, the object ownership, data classification and permitted consumer paths, required USE and object privileges, backing storage identity and workspace/compute eligibility, owner, normal/failure signals and recovery instructions using approved grant matrix, ownership record and migration acceptance boundary. Include one normal and one failure example plus actual service targets and retention assumptions.

**Implementation reasoning:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Example to work through:** Use an approved service identity with only required catalog objects and storage path access.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Unity Catalog fit in an end-to-end Azure data platform?

**Answer:** Use this specific flow: Entra workload/user identity -> catalog and schema privileges -> governed table/volume -> approved storage access -> audited consumption. Explain what this component owns, how Microsoft Entra identities, Databricks compute and Azure storage connects, and what the accepted consumer/result boundary is.

**Project explanation:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Concrete example:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

### D02. How would you justify using Unity Catalog for governed Databricks domains and production workload access?

**Answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one governed object access or grant change meets them, compare a credible alternative and validate using effective privileges, audit events, query identity and supported lineage rather than choosing a tool merely because it is on the stack.

**Project explanation:** Parent/object checks should be diagnosed under the effective caller. Granting SELECT alone may not satisfy all necessary catalog/schema usage conditions.

**Concrete example:** Compare an author's successful query with the production service identity's full privilege chain.

### D03. What controls must surround Unity Catalog in a financial or telecom project?

**Answer:** Tie object ownership, data classification and permitted consumer paths to accountable business ownership, verify USE and object privileges, backing storage identity and workspace/compute eligibility, preserve approved grant matrix, ownership record and migration acceptance boundary and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

**Project explanation:** Migration changes metadata, ownership, storage access and possibly compute compatibility. Data parity and access validation must precede consumer cutover.

**Concrete example:** A legacy path-based notebook is migrated to a governed table and verified under its job identity.

### D04. Which measures would prove your Unity Catalog optimization helped?

**Answer:** Record the old/new configuration and comparable workload, measure authorization resolution, storage connectivity and unsupported execution paths with effective privileges, audit events, query identity and supported lineage, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

**Project explanation:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Concrete example:** Use an approved service identity with only required catalog objects and storage path access.

### D05. How would you explain your own contribution to a Unity Catalog interview project?

**Answer:** Identify which catalog/schema definitions, reviewed grants and storage-location configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in approved grant matrix, ownership record and migration acceptance boundary and a verified outcome. State team-owned components separately and do not invent scale or savings.

**Project explanation:** Production jobs need stable workload ownership and permission scope. Interactive authors' broad grants should not become the implicit production credential.

**Concrete example:** Use an approved service identity with only required catalog objects and storage path access.

## Revision notes and common mistakes

- Explain Unity Catalog's specific responsibility in the flow before naming surrounding tools.
- Use the real object ownership, data classification and permitted consumer paths; an accepted request/job does not establish a correct business result.
- Validate USE and object privileges, backing storage identity and workspace/compute eligibility under the actual execution identity, rather than your administrator account.
- Preserve approved grant matrix, ownership record and migration acceptance boundary and inspect it before retrying uncertain side effects.
- Tune authorization resolution, storage connectivity and unsupported execution paths from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Unity Catalog official documentation](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/).

[Back to all 20 interview guides](README.md).
