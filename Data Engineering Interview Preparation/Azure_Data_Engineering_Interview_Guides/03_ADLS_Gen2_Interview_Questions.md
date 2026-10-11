# Azure Data Lake Storage Gen2 (ADLS) — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Durable lake storage, directory organization, permissions and efficient access for analytical workloads.

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
Approved producer -> immutable ADLS landing -> bronze/silver/gold storage -> governed compute -> accepted SQL/BI consumption
```

For this guide, the primary unit is **one ingestion or curated storage path**. The engineering artifacts are container/path layout, role/ACL assignments and network configuration. Troubleshooting starts with storage request failures, read/list latency, bytes and object counts; durable progress/evidence is represented by delivery manifest, immutable raw path and active table-log references. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is ADLS Gen2?

**Model answer:** Azure storage capabilities for analytical lake workloads built on Blob Storage with hierarchical namespace support. It stores files/objects; it does not execute Spark transformations.

### C02. Why does hierarchical namespace matter?

**Model answer:** It provides directory semantics used by data-lake workloads, including directory-oriented operations and ACLs. Evaluate account configuration and feature compatibility before provisioning.

### C03. What is the abfss URI used for?

**Model answer:** It identifies secure Azure Blob File System access to a container and path. Authentication still requires the workload's supported identity/credential configuration.

### C04. How do containers and directories differ?

**Model answer:** A container is a top-level storage boundary; directories organize paths within it. Choose boundaries based on governance and lifecycle needs, not naming convenience alone.

### C05. How do RBAC and ACLs relate?

**Model answer:** Azure roles and path ACLs participate in authorization through documented evaluation rules. Broad data-plane role grants can make restrictive ACL assumptions ineffective.

### C06. What are access versus default ACLs?

**Model answer:** Access ACLs apply to existing objects; default ACLs define inheritance for newly created children. Changing defaults does not automatically rewrite every existing child's ACL.

### C07. Which file format would you choose for analytics?

**Model answer:** Parquet suits typed columnar analytical scans; JSON/CSV may preserve source interchange; Delta adds a transaction log over data files for table semantics.

### C08. How should lake paths be organized?

**Model answer:** Separate source/entity/date/run landing from curated datasets and restricted exceptions. Preserve manifests and avoid high-cardinality directory partitioning without evidence.

### C09. What do lifecycle policies do?

**Model answer:** They automate supported object retention/tiering behavior. Verify compatibility with active table files, recovery needs and the account's enabled features.

### C10. What distinguishes storage encryption from authorization?

**Model answer:** Encryption protects stored/transmitted data; authorization decides who can access it. Encrypted storage is not proof of appropriate user permissions.

## B. Advanced implementation questions

### A01. Why are small files expensive for analytics?

**Model answer:** They increase listing/opening/metadata overhead and fragmented reads. Measure actual query and write behavior before choosing compaction or file-size targets.

### A02. How do you secure network access?

**Model answer:** Use supported firewall/private endpoint controls with correct private DNS and permitted workload routes. A valid identity can still fail through network restrictions.

### A03. How do you validate complete delivery?

**Model answer:** Use a source manifest, expected file/row counts and checksums where appropriate. Listing currently visible files alone does not establish that the source finished writing.

### A04. How do you design recovery?

**Model answer:** Align immutable source retention, table-log/data retention, storage protection and tested restoration with RPO/RTO. Do not equate geo-redundancy with a complete application recovery plan.

### A05. How do you delete sensitive records safely?

**Model answer:** Find relevant raw/curated/export copies and apply the approved retention/deletion procedure. Coordinate table-level transactions and physical retention; do not manually delete active Delta files.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A user can read a file but cannot list its parent. What do you inspect?

**Model answer:** Check RBAC and path ACL evaluation, including required traversal permissions on ancestors. Test with the actual user's token and path.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. New files inherit the wrong permissions. Why?

**Model answer:** Inspect directory default ACLs and the writer's behavior. Correct defaults for future objects and deliberately repair existing ACLs where approved.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. A Databricks job gets 403 after an identity change. How do you isolate it?

**Model answer:** Check the actual workload identity, storage data-plane roles, ACLs, catalog storage configuration and network routing.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A private endpoint exists but requests still use a public route. What is likely wrong?

**Model answer:** Verify DNS resolution and the workload's network path. Endpoint creation alone does not ensure clients resolve/use the private endpoint.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. Millions of tiny JSON files slow ingestion. What would you change?

**Model answer:** Measure listing/opening overhead; compact or batch source deliveries and convert accepted data to columnar tables while preserving raw traceability.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. A retention policy removes files still referenced by Delta. What is your response?

**Model answer:** Hold consumers, inspect table versions and available backups, restore missing files if possible, and redesign lifecycle rules to respect table retention.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. Someone deletes files directly from a gold table directory. How do you recover?

**Model answer:** Inspect transaction-log references and storage recovery options; restore the table consistently. Restrict direct file deletion and use supported table operations.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. An account is being redesigned for hierarchical namespace. What must be checked?

**Model answer:** Validate supported enablement/migration paths, workload compatibility, ACL strategy and rollback constraints for the actual account.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. A producer overwrites yesterday's source file. How do you retain auditability?

**Model answer:** Copy deliveries to immutable run/version paths and record manifest/hash provenance. Corrections create new identified deliveries rather than erasing prior evidence.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. Storage cost rises while rows remain constant. What do you investigate?

**Model answer:** Check retained versions/raw copies, small-file counts, tier/access charges, orphaned exports and transaction-log retention before deleting anything.

**Verification:** Use relevant storage request failures, read/list latency, bytes and object counts and confirm the intended path conventions, file format, partition keys and retention policy. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one ingestion or curated storage path to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate data-plane RBAC, directory traversal ACLs, workload identity and storage network route. Compare production with the working configuration using storage request failures, read/list latency, bytes and object counts; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Azure Data Lake Storage Gen2 (ADLS) is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through source producer and Spark/SQL storage reader and compare progress in delivery manifest, immutable raw path and active table-log references. Inspect storage request failures, read/list latency, bytes and object counts to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of container/path layout, role/ACL assignments and network configuration works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual path conventions, file format, partition keys and retention policy. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one ingestion or curated storage path although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with storage request failures, read/list latency, bytes and object counts and inspect file listing, tiny-object overhead, read throughput and request rate. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Azure Data Lake Storage Gen2 (ADLS) may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in delivery manifest, immutable raw path and active table-log references before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one ingestion or curated storage path at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in delivery manifest, immutable raw path and active table-log references. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Azure Data Lake Storage Gen2 (ADLS) without prior notice. How do you contain the impact?

**Model answer:** Validate against path conventions, file format, partition keys and retention policy and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some delivery manifest, immutable raw path and active table-log references evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of delivery manifest, immutable raw path and active table-log references and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in storage request failures, read/list latency, bytes and object counts. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review data-plane RBAC, directory traversal ACLs, workload identity and storage network route for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Azure Data Lake Storage Gen2 (ADLS) accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in container/path layout, role/ACL assignments and network configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against delivery manifest, immutable raw path and active table-log references before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Source producer and spark/sql storage reader is temporarily unavailable. What retry and recovery policy fits Azure Data Lake Storage Gen2 (ADLS)?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved delivery manifest, immutable raw path and active table-log references; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Azure Data Lake Storage Gen2 (ADLS) rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect file listing, tiny-object overhead, read throughput and request rate. Remove demonstrated waste while preserving required delivery manifest, immutable raw path and active table-log references and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, container/path layout, role/ACL assignments and network configuration is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate data-plane RBAC, directory traversal ACLs, workload identity and storage network route, source producer and Spark/SQL storage reader and the appropriate delivery manifest, immutable raw path and active table-log references. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Azure Data Lake Storage Gen2 (ADLS). How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with storage request failures, read/list latency, bytes and object counts and validate their path conventions, file format, partition keys and retention policy. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change container/path layout, role/ACL assignments and network configuration while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and path conventions, file format, partition keys and retention policy compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain delivery manifest, immutable raw path and active table-log references and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a lake directory and permission matrix.

**Model answer:** Show source/run landing, curated layers, quarantine, consumer scope and workload identity. Explain traversal and inheritance tests.

### P02. Build a delivery-manifest validator.

**Model answer:** Compare expected objects, size/checksum where meaningful and source control counts; fail a partial delivery before downstream publication.

### P03. Explain a safe table retention policy.

**Model answer:** Map raw recovery, Delta history, stream consumers and deletion obligations; show why deleting arbitrary files is unsafe.

### P04. Create a failing-and-recovered test for one ingestion or curated storage path.

**Model answer:** Capture the initial delivery manifest, immutable raw path and active table-log references, introduce one realistic dependency or validation failure and use storage request failures, read/list latency, bytes and object counts to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Azure Data Lake Storage Gen2 (ADLS).

**Model answer:** Document container/path layout, role/ACL assignments and network configuration, the path conventions, file format, partition keys and retention policy, required data-plane RBAC, directory traversal ACLs, workload identity and storage network route, owner, normal/failure signals and recovery instructions using delivery manifest, immutable raw path and active table-log references. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Azure Data Lake Storage Gen2 (ADLS) fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Approved producer -> immutable ADLS landing -> bronze/silver/gold storage -> governed compute -> accepted SQL/BI consumption. Explain what this component owns, how source producer and Spark/SQL storage reader connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Azure Data Lake Storage Gen2 (ADLS) for all six project landing and recovery layers?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one ingestion or curated storage path meets them, compare a credible alternative and validate using storage request failures, read/list latency, bytes and object counts rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Azure Data Lake Storage Gen2 (ADLS) in a financial or telecom project?

**Model answer:** Tie path conventions, file format, partition keys and retention policy to accountable business ownership, verify data-plane RBAC, directory traversal ACLs, workload identity and storage network route, preserve delivery manifest, immutable raw path and active table-log references and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Azure Data Lake Storage Gen2 (ADLS) optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure file listing, tiny-object overhead, read throughput and request rate with storage request failures, read/list latency, bytes and object counts, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Azure Data Lake Storage Gen2 (ADLS) interview project?

**Model answer:** Identify which container/path layout, role/ACL assignments and network configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in delivery manifest, immutable raw path and active table-log references and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Data Lake Storage Gen2 (ADLS) official documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction).

[Back to all 20 interview guides](README.md).
