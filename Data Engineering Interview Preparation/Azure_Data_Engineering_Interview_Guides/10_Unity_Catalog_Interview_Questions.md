# Unity Catalog — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Governed Databricks objects, workload access, storage abstraction and metadata/lineage visibility.

**Audience:** Azure data engineering interviews, from fundamentals through production troubleshooting and design. The model answers are concise starting points; expand them with the actual source semantics, engine/runtime, workload identity and acceptance evidence. Practice scenarios are hypothetical and are not claims about the named client projects.

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

**Model answer:** The Databricks governance layer for supported data/AI assets. It manages securable objects, grants and governance capabilities; Azure storage authorization remains relevant.

### C02. What is the object hierarchy?

**Model answer:** Common table addressing uses catalog.schema.table within a metastore governance context. Different securable object types have their own privileges.

### C03. How do managed and external tables differ?

**Model answer:** Managed tables let the platform manage relevant data lifecycle; external tables reference externally managed storage. Verify drop/data-retention behavior for the actual table type.

### C04. What is a storage credential?

**Model answer:** An approved credential abstraction used by governed access to external storage. Its backing identity must have appropriate cloud permissions.

### C05. What is an external location?

**Model answer:** A governed storage path associated with a storage credential. It scopes supported external data access without distributing raw secrets.

### C06. What are volumes for?

**Model answer:** Governed access to supported non-tabular files. Do not confuse file access through a volume with querying a table.

### C07. Why do users need USE privileges?

**Model answer:** Object selection/access involves parent catalog/schema usage as well as the object permission. Diagnose the full privilege path.

### C08. How does ownership differ from reading?

**Model answer:** Ownership confers management authority under the governance model; SELECT is a data-read privilege. Assign ownership to accountable groups, not casually to every reader.

### C09. What is lineage useful for?

**Model answer:** Tracing supported upstream/downstream relationships and impact. Validate capture coverage for actual execution paths rather than assuming all external movement is captured.

### C10. What does workspace access establish?

**Model answer:** It allows platform workspace use subject to controls; it is not automatic permission to every governed data object.

## B. Advanced implementation questions

### A01. How do you design least privilege?

**Model answer:** Separate producer, engineer, steward and consumer groups; grant required parent/object permissions and control direct cloud access that could bypass governance.

### A02. How do you migrate legacy access?

**Model answer:** Inventory tables/paths/identities, map ownership/grants and compatible compute access, test workload identities, then cut over with traceable reconciliation.

### A03. How do masking and row filtering help?

**Model answer:** Supported policies restrict exposed values/rows for applicable query paths. Verify function/policy compatibility and bypass routes for the actual runtime.

### A04. How do you govern production jobs?

**Model answer:** Use approved service/workload identities, narrowly scoped grants and reviewed deployment permissions. Test jobs under their production identity.

### A05. How do you audit access effectively?

**Model answer:** Correlate supported audit events with identities, object names and execution context; protect logs and retain them under the approved policy.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. SELECT is granted but the user still cannot query. What do you inspect?

**Model answer:** Check catalog/schema USE privileges, workspace/compute eligibility, object name and the effective identity.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. A storage credential exists but a job gets a storage error. What might be wrong?

**Model answer:** Verify backing cloud identity permissions, external-location path, network access and the job's object privileges.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. An engineer can bypass filters by opening raw ADLS files. What is the gap?

**Model answer:** Direct storage access bypasses the intended catalog path. Review cloud roles/ACLs and permitted external-location access alongside table policies.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A job succeeds for its author but fails as a service identity. What changes?

**Model answer:** Grant the service identity the specific parent/object privileges and approved execution/storage path; avoid reusing the author's broad grants.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. A table is dropped and its files remain. Is that always wrong?

**Model answer:** External versus managed lifecycle behavior differs. Check table type and retention contracts before cleanup; do not delete data still used elsewhere.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. Several teams need the same data with separate ownership. How do you organize it?

**Model answer:** Define catalogs/schemas and consumer grants around accountable domains, with shared approved products and explicit ownership.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. Lineage is missing for an external export. What do you do?

**Model answer:** Verify supported lineage capture for that path and record/document/custom-register the missing relationship through an approved mechanism.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. Granting a catalog-wide privilege exposes unintended objects. How do you prevent recurrence?

**Model answer:** Review inherited/broad grants and group membership, narrow scope and test representative restricted objects.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. A masking policy fails on one compute/runtime. What do you check?

**Model answer:** Validate policy support and execution compatibility for the actual compute/runtime, then use a supported controlled path.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. A legacy notebook uses direct secret-backed storage paths. How would you modernize it?

**Model answer:** Migrate to approved storage credentials/external locations or volumes/tables, remove unnecessary direct secrets and validate equivalent output/access.

**Verification:** Use relevant effective privileges, audit events, query identity and supported lineage and confirm the intended object ownership, data classification and permitted consumer paths. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one governed object access or grant change to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate USE and object privileges, backing storage identity and workspace/compute eligibility. Compare production with the working configuration using effective privileges, audit events, query identity and supported lineage; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Unity Catalog is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through Microsoft Entra identities, Databricks compute and Azure storage and compare progress in approved grant matrix, ownership record and migration acceptance boundary. Inspect effective privileges, audit events, query identity and supported lineage to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of catalog/schema definitions, reviewed grants and storage-location configuration works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual object ownership, data classification and permitted consumer paths. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one governed object access or grant change although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with effective privileges, audit events, query identity and supported lineage and inspect authorization resolution, storage connectivity and unsupported execution paths. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Unity Catalog may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in approved grant matrix, ownership record and migration acceptance boundary before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one governed object access or grant change at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in approved grant matrix, ownership record and migration acceptance boundary. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Unity Catalog without prior notice. How do you contain the impact?

**Model answer:** Validate against object ownership, data classification and permitted consumer paths and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some approved grant matrix, ownership record and migration acceptance boundary evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of approved grant matrix, ownership record and migration acceptance boundary and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in effective privileges, audit events, query identity and supported lineage. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review USE and object privileges, backing storage identity and workspace/compute eligibility for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Unity Catalog accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in catalog/schema definitions, reviewed grants and storage-location configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against approved grant matrix, ownership record and migration acceptance boundary before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Microsoft entra identities, databricks compute and azure storage is temporarily unavailable. What retry and recovery policy fits Unity Catalog?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved approved grant matrix, ownership record and migration acceptance boundary; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Unity Catalog rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect authorization resolution, storage connectivity and unsupported execution paths. Remove demonstrated waste while preserving required approved grant matrix, ownership record and migration acceptance boundary and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, catalog/schema definitions, reviewed grants and storage-location configuration is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate USE and object privileges, backing storage identity and workspace/compute eligibility, Microsoft Entra identities, Databricks compute and Azure storage and the appropriate approved grant matrix, ownership record and migration acceptance boundary. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Unity Catalog. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with effective privileges, audit events, query identity and supported lineage and validate their object ownership, data classification and permitted consumer paths. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change catalog/schema definitions, reviewed grants and storage-location configuration while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and object ownership, data classification and permitted consumer paths compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain approved grant matrix, ownership record and migration acceptance boundary and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a catalog/schema/grant matrix.

**Model answer:** Include owner, production writer, steward and consumer with required parent/object privileges and cloud-bypass review.

### P02. Trace an access-denied incident.

**Model answer:** Show effective identity, workspace/compute context, object grants, external location and cloud/network authorization checks.

### P03. Plan a legacy table migration.

**Model answer:** Inventory location/type/history, recreate governance, validate data/grants and cut over consumers with recovery evidence.

### P04. Create a failing-and-recovered test for one governed object access or grant change.

**Model answer:** Capture the initial approved grant matrix, ownership record and migration acceptance boundary, introduce one realistic dependency or validation failure and use effective privileges, audit events, query identity and supported lineage to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Unity Catalog.

**Model answer:** Document catalog/schema definitions, reviewed grants and storage-location configuration, the object ownership, data classification and permitted consumer paths, required USE and object privileges, backing storage identity and workspace/compute eligibility, owner, normal/failure signals and recovery instructions using approved grant matrix, ownership record and migration acceptance boundary. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Unity Catalog fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Entra workload/user identity -> catalog and schema privileges -> governed table/volume -> approved storage access -> audited consumption. Explain what this component owns, how Microsoft Entra identities, Databricks compute and Azure storage connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Unity Catalog for governed Databricks domains and production workload access?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one governed object access or grant change meets them, compare a credible alternative and validate using effective privileges, audit events, query identity and supported lineage rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Unity Catalog in a financial or telecom project?

**Model answer:** Tie object ownership, data classification and permitted consumer paths to accountable business ownership, verify USE and object privileges, backing storage identity and workspace/compute eligibility, preserve approved grant matrix, ownership record and migration acceptance boundary and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Unity Catalog optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure authorization resolution, storage connectivity and unsupported execution paths with effective privileges, audit events, query identity and supported lineage, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Unity Catalog interview project?

**Model answer:** Identify which catalog/schema definitions, reviewed grants and storage-location configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in approved grant matrix, ownership record and migration acceptance boundary and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Unity Catalog official documentation](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/).

[Back to all 20 interview guides](README.md).
