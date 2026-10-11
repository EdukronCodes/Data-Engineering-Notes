# Microsoft Fabric — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Integrated ingestion, engineering, OneLake lakehouses, warehouse analytics and Power BI serving.

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
Source connection -> Fabric pipeline -> OneLake bronze -> Spark silver -> validated gold -> semantic model or SQL serving
```

For this guide, the primary unit is **one Fabric pipeline and analytical publication**. The engineering artifacts are workspace items, notebook/pipeline definitions and semantic-model contract. Troubleshooting starts with Fabric run monitoring, capacity metrics and consumer query behavior; durable progress/evidence is represented by OneLake table versions, delivery manifests and accepted product boundary. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is Microsoft Fabric?

**Model answer:** A Microsoft SaaS analytics platform with integrated workloads and OneLake. Distinguish its services from separately provisioned Azure ADF, ADLS and Synapse resources.

### C02. What is OneLake?

**Model answer:** The logical data lake for Fabric tenant data. It is not a user-created ADLS account, even though supported integration can connect to external storage.

### C03. What is a Fabric Lakehouse?

**Model answer:** An analytical item that organizes files and tables for engineering/analytics workloads. Delta tables support Spark transformations and supported SQL/BI access.

### C04. How do Lakehouse and Warehouse choices differ?

**Model answer:** A Lakehouse emphasizes Spark/data-file engineering; a Warehouse emphasizes relational SQL warehouse work. Choose from transformation and serving requirements.

### C05. What does the Lakehouse SQL analytics endpoint do?

**Model answer:** It provides SQL querying over supported Lakehouse tables. Do not use its read-oriented table access as a substitute for Spark Delta mutations.

### C06. What are shortcuts?

**Model answer:** References to supported data locations that can reduce copying. Availability, identity, freshness and source permissions still depend on the target connection.

### C07. How does Fabric Data Factory relate to ADF?

**Model answer:** Both support integration/orchestration, but connectors, activities, execution and deployment capabilities are not guaranteed identical.

### C08. What is a semantic model?

**Model answer:** A governed analytical model of tables, relationships and measures for BI consumption. Its security and aggregation behavior must match the business contract.

### C09. What is Direct Lake conceptually?

**Model answer:** A Power BI storage mode designed to use lake-backed data under supported conditions. Validate the model/endpoint type and actual query behavior rather than assuming every model stays on the same path.

### C10. What should separate workspaces achieve?

**Model answer:** Environment isolation, ownership and access boundaries. Workspace structure should follow deployment and governance needs, with tested cross-workspace dependencies.

## B. Advanced implementation questions

### A01. How do you control capacity contention?

**Model answer:** Measure capacity/workload utilization, execution patterns and consumer latency. Isolate or reschedule heavy workloads and size capacity from evidence.

### A02. How do you prevent mixed publication versions?

**Model answer:** Use accepted boundaries/manifests and a consumer contract that selects the intended release. Independent table writes are not automatically an atomic product release.

### A03. How do you verify underlying data security?

**Model answer:** Test OneLake/item/workload permissions and direct SQL/file access independently of Power BI row filters. The effective identity varies by access mode.

### A04. How do you deploy Fabric items?

**Model answer:** Use supported Git/deployment/API mechanisms for the actual item types and validate dependencies/parameters. Do not assume every item supports the same promotion workflow.

### A05. How do you integrate external Azure storage?

**Model answer:** Use supported connections/shortcuts or controlled copying according to security and freshness requirements. Verify external target permissions and network support.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. The SQL endpoint will not accept your Delta MERGE. What do you do?

**Model answer:** Run compatible Delta mutations through Spark notebooks for Lakehouse tables, or choose a SQL Warehouse implementation where the workload requires warehouse DML.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. A shortcut suddenly becomes unreadable. What do you inspect?

**Model answer:** Check external target availability, connection identity/permissions, network support and changes to the referenced location.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. Power BI is slow during notebook runs. How do you diagnose it?

**Model answer:** Correlate capacity contention, notebook timing, query workload and model behavior; isolate or schedule based on measured resource pressure.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A regional report is filtered but a user can query all gold rows. What is missing?

**Model answer:** Underlying data permissions were not scoped as expected. Test serving modes and item/data access separately from semantic-model filters.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. A schema change breaks the semantic model. How would you manage the release?

**Model answer:** Version the table/model contract, test dependent measures/relationships and promote compatible changes together or provide a migration version.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. Gold tables finish at different times and the report combines inconsistent dates. What is the fix?

**Model answer:** Define a product publication boundary and consumer accepted-version behavior. Show table/product as-of values when separate releases are intentional.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. An ADF pipeline export cannot run directly in Fabric. Why?

**Model answer:** The integration products have different supported features/definitions. Map activities/connections and rebuild unsupported parts with tested equivalence.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. A deployment omits an unsupported item. How do you handle it?

**Model answer:** Inventory supported promotion coverage and deploy that item through an approved supported path; verify dependencies and prevent incomplete releases.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. A financial report sums daily account balances over a month. What must change?

**Model answer:** Use snapshot-aware measures and the approved as-of-date definition. Transaction sums and balance snapshots have different aggregation semantics.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. The pipeline succeeds but the source data is stale. How do you make that visible?

**Model answer:** Monitor last accepted business/source timestamp and freshness target, not only pipeline status; hold or flag the product under its contract.

**Verification:** Use relevant Fabric run monitoring, capacity metrics and consumer query behavior and confirm the intended Lakehouse schema, gold product grain and semantic-model relationships. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one Fabric pipeline and analytical publication to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate connection identity, workspace/item/OneLake permissions and semantic-model security. Compare production with the working configuration using Fabric run monitoring, capacity metrics and consumer query behavior; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Microsoft Fabric is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through external source connection and Power BI or SQL consumers and compare progress in OneLake table versions, delivery manifests and accepted product boundary. Inspect Fabric run monitoring, capacity metrics and consumer query behavior to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of workspace items, notebook/pipeline definitions and semantic-model contract works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual Lakehouse schema, gold product grain and semantic-model relationships. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one Fabric pipeline and analytical publication although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with Fabric run monitoring, capacity metrics and consumer query behavior and inspect capacity contention, Spark processing time and model query latency. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Microsoft Fabric may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in OneLake table versions, delivery manifests and accepted product boundary before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one Fabric pipeline and analytical publication at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in OneLake table versions, delivery manifests and accepted product boundary. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Microsoft Fabric without prior notice. How do you contain the impact?

**Model answer:** Validate against Lakehouse schema, gold product grain and semantic-model relationships and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some OneLake table versions, delivery manifests and accepted product boundary evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of OneLake table versions, delivery manifests and accepted product boundary and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in Fabric run monitoring, capacity metrics and consumer query behavior. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review connection identity, workspace/item/OneLake permissions and semantic-model security for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Microsoft Fabric accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in workspace items, notebook/pipeline definitions and semantic-model contract, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against OneLake table versions, delivery manifests and accepted product boundary before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. External source connection and power bi or sql consumers is temporarily unavailable. What retry and recovery policy fits Microsoft Fabric?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved OneLake table versions, delivery manifests and accepted product boundary; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Microsoft Fabric rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect capacity contention, Spark processing time and model query latency. Remove demonstrated waste while preserving required OneLake table versions, delivery manifests and accepted product boundary and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, workspace items, notebook/pipeline definitions and semantic-model contract is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate connection identity, workspace/item/OneLake permissions and semantic-model security, external source connection and Power BI or SQL consumers and the appropriate OneLake table versions, delivery manifests and accepted product boundary. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Microsoft Fabric. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with Fabric run monitoring, capacity metrics and consumer query behavior and validate their Lakehouse schema, gold product grain and semantic-model relationships. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change workspace items, notebook/pipeline definitions and semantic-model contract while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and Lakehouse schema, gold product grain and semantic-model relationships compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain OneLake table versions, delivery manifests and accepted product boundary and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Draw a Fabric banking analytical platform.

**Model answer:** Include supported connections, pipeline, OneLake layers, Spark rules, source reconciliation, accepted publication and semantic-model access.

### P02. Design Lakehouse versus Warehouse selection.

**Model answer:** State data shape, transformation engine, SQL write needs, BI consumers, operational tradeoffs and tested permissions.

### P03. Demonstrate a late transaction correction.

**Model answer:** Replay a bounded source scope, resolve historical dimensions/FX, reconcile and publish an accepted replacement without duplicating facts.

### P04. Create a failing-and-recovered test for one Fabric pipeline and analytical publication.

**Model answer:** Capture the initial OneLake table versions, delivery manifests and accepted product boundary, introduce one realistic dependency or validation failure and use Fabric run monitoring, capacity metrics and consumer query behavior to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Microsoft Fabric.

**Model answer:** Document workspace items, notebook/pipeline definitions and semantic-model contract, the Lakehouse schema, gold product grain and semantic-model relationships, required connection identity, workspace/item/OneLake permissions and semantic-model security, owner, normal/failure signals and recovery instructions using OneLake table versions, delivery manifests and accepted product boundary. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Microsoft Fabric fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Source connection -> Fabric pipeline -> OneLake bronze -> Spark silver -> validated gold -> semantic model or SQL serving. Explain what this component owns, how external source connection and Power BI or SQL consumers connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Microsoft Fabric for Citi EMEA reference Fabric banking analytics design?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one Fabric pipeline and analytical publication meets them, compare a credible alternative and validate using Fabric run monitoring, capacity metrics and consumer query behavior rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Microsoft Fabric in a financial or telecom project?

**Model answer:** Tie Lakehouse schema, gold product grain and semantic-model relationships to accountable business ownership, verify connection identity, workspace/item/OneLake permissions and semantic-model security, preserve OneLake table versions, delivery manifests and accepted product boundary and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Microsoft Fabric optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure capacity contention, Spark processing time and model query latency with Fabric run monitoring, capacity metrics and consumer query behavior, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Microsoft Fabric interview project?

**Model answer:** Identify which workspace items, notebook/pipeline definitions and semantic-model contract you personally built/reviewed/operated, one specific failure you resolved, the evidence in OneLake table versions, delivery manifests and accepted product boundary and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

## Official references

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Microsoft Fabric official documentation](https://learn.microsoft.com/en-us/fabric/fundamentals/microsoft-fabric-overview).
- [Enterprise BI architecture](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/analytics/enterprise-bi-microsoft-fabric).

[Back to all 20 interview guides](README.md).
