# Azure Data Factory (ADF) — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Source ingestion, orchestration, scheduling and controlled ETL/ELT execution.

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
Source -> linked service and integration runtime -> Copy activity -> ADLS landing -> transformation activity -> validation -> accepted serving dataset
```

For this guide, the primary unit is **one scheduled entity pipeline**. The engineering artifacts are pipeline JSON, linked services, trigger definitions and parameterized datasets. Troubleshooting starts with activity output, integration-runtime diagnostics and source/sink throughput; durable progress/evidence is represented by source watermark, immutable delivery manifest and accepted run record. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is an ADF pipeline?

**Model answer:** A pipeline groups activities into an orchestrated workflow. A pipeline run is one execution with a specific parameter set and run identity.

### C02. What are linked services and datasets?

**Model answer:** A linked service defines connectivity/authentication to a data store or compute service; a dataset identifies the data structure or location used by an activity.

### C03. What is an integration runtime?

**Model answer:** It provides the execution/connectivity bridge for integration work. Choose Azure, self-hosted or Azure-SSIS runtime based on the workload and network requirements.

### C04. When do you use Copy activity versus Mapping Data Flow?

**Model answer:** Copy moves supported data between sources and sinks. Mapping Data Flow performs visual Spark-based transformations; external activities can invoke custom compute such as Databricks.

### C05. How do ETL and ELT differ?

**Model answer:** ETL transforms before the analytical destination; ELT lands data and transforms within the destination platform. Select based on data volume, engine capabilities and control needs.

### C06. How do parameters differ from variables?

**Model answer:** Parameters supply read-only run configuration. Variables hold mutable pipeline state; avoid shared mutable variables in parallel iterations.

### C07. What trigger patterns should you know?

**Model answer:** Schedule triggers start time-based runs, tumbling windows represent bounded recurring windows, and supported event triggers respond to events. Choose based on replay, dependency and timing requirements.

### C08. How do Lookup and Get Metadata differ?

**Model answer:** Lookup reads configuration or query results; Get Metadata reads supported object/file metadata. Their output size and connector constraints matter for large workloads.

### C09. How do you process multiple entities?

**Model answer:** Read reviewed metadata and iterate with parameterized datasets/pipelines. Bound concurrency to protect the source and avoid conflicting target publications.

### C10. What proves a pipeline succeeded?

**Model answer:** Execution status proves activities completed. Business success also requires manifest completeness, quality/reconciliation controls and accepted consumer publication.

## B. Advanced implementation questions

### A01. How do you make incremental ingestion safe?

**Model answer:** Use a source-consistent bounded change boundary, retain raw input and advance accepted state after publication. Timestamp-only extraction requires explicit assumptions and cannot detect hard deletes by itself.

### A02. How do you build restartable pipelines?

**Model answer:** Persist phase state, source boundaries and manifests. Make target operations idempotent and reconcile cases where publication succeeds but state recording fails.

### A03. How do you parameterize dynamic SQL safely?

**Model answer:** Bind values using supported parameters and allow-list object identifiers. Metadata-driven ingestion must not execute unrestricted configuration as SQL.

### A04. How do you deploy ADF across environments?

**Model answer:** Version source definitions, produce deployable artifacts, use environment parameters and separate identities, and validate trigger behavior during promotion.

### A05. How do you tune Copy performance?

**Model answer:** Inspect source, network, runtime and sink throughput; adjust partitioning/concurrency only at a measured bottleneck. Higher parallelism can overload the source.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. An on-premises SQL connection fails while cloud copies work. What do you check?

**Model answer:** Inspect self-hosted runtime availability, service credentials, outbound connectivity, DNS and source permissions. Reproduce with the runtime identity rather than your interactive account.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. A file event starts before all delivery files arrive. How do you prevent incomplete processing?

**Model answer:** Treat the event as a signal, then validate an expected manifest or completion marker. Publish only after the complete delivery is present.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. Two runs update the same watermark. How do you fix it?

**Model answer:** Serialize the entity or acquire a durable lease; use compare-and-set state updates. Preserve distinct run IDs and prevent competing publication.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A source hard-deletes rows. Will your timestamp query capture this?

**Model answer:** No. Use source-supported CDC, a tombstone feed or an authoritative full-snapshot comparison with explicit deletion rules.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. Copy succeeds but the notebook fails. What do you rerun?

**Model answer:** Reuse the durable landed input and same boundary for transformation. Do not re-extract a changing source without recording a new input version.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. Parallel ForEach produces incorrect shared totals. Why?

**Model answer:** Pipeline variables are shared mutable state. Return per-iteration outputs or persist isolated results and aggregate after the parallel work.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. REST pagination repeats a page after a timeout. What is your strategy?

**Model answer:** Persist cursor/page identity, bound retries and deduplicate stable source keys. Verify whether the API supports a consistent snapshot while pages are fetched.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. A tumbling-window backfill overloads the database. What changes?

**Model answer:** Lower approved concurrency, chunk the ranges and measure database pressure. Keep backfill separate from the live freshness workload where necessary.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. A Databricks activity times out after the job finished. Should you submit a new job immediately?

**Model answer:** Inspect the external job/run status and target publication before retrying. Use correlation IDs and idempotency to avoid duplicated side effects.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. Triggers run during deployment and read half-updated configuration. How do you prevent that?

**Model answer:** Use a controlled deployment sequence for affected triggers and dependencies, validate the release, then resume scheduling and reconcile missed windows.

**Verification:** Use relevant activity output, integration-runtime diagnostics and source/sink throughput and confirm the intended source schema, extraction boundary and sink dataset schema. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one scheduled entity pipeline to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants. Compare production with the working configuration using activity output, integration-runtime diagnostics and source/sink throughput; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Azure Data Factory (ADF) is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through source system and invoked Databricks/SQL transformation and compare progress in source watermark, immutable delivery manifest and accepted run record. Inspect activity output, integration-runtime diagnostics and source/sink throughput to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of pipeline JSON, linked services, trigger definitions and parameterized datasets works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual source schema, extraction boundary and sink dataset schema. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one scheduled entity pipeline although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with activity output, integration-runtime diagnostics and source/sink throughput and inspect source query duration, Copy throughput and transformation activity duration. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Azure Data Factory (ADF) may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in source watermark, immutable delivery manifest and accepted run record before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one scheduled entity pipeline at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in source watermark, immutable delivery manifest and accepted run record. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Azure Data Factory (ADF) without prior notice. How do you contain the impact?

**Model answer:** Validate against source schema, extraction boundary and sink dataset schema and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some source watermark, immutable delivery manifest and accepted run record evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of source watermark, immutable delivery manifest and accepted run record and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in activity output, integration-runtime diagnostics and source/sink throughput. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Azure Data Factory (ADF) accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in pipeline JSON, linked services, trigger definitions and parameterized datasets, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against source watermark, immutable delivery manifest and accepted run record before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Source system and invoked databricks/sql transformation is temporarily unavailable. What retry and recovery policy fits Azure Data Factory (ADF)?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved source watermark, immutable delivery manifest and accepted run record; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Azure Data Factory (ADF) rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect source query duration, Copy throughput and transformation activity duration. Remove demonstrated waste while preserving required source watermark, immutable delivery manifest and accepted run record and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, pipeline JSON, linked services, trigger definitions and parameterized datasets is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, source system and invoked Databricks/SQL transformation and the appropriate source watermark, immutable delivery manifest and accepted run record. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Azure Data Factory (ADF). How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with activity output, integration-runtime diagnostics and source/sink throughput and validate their source schema, extraction boundary and sink dataset schema. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change pipeline JSON, linked services, trigger definitions and parameterized datasets while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and source schema, extraction boundary and sink dataset schema compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain source watermark, immutable delivery manifest and accepted run record and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Design a metadata-driven ingestion pipeline.

**Model answer:** Show entity configuration, validated identifiers, extraction boundary, Copy, notebook dispatch, controls, publication and state update. Demonstrate one failed-run replay.

### P02. Write a bounded incremental extraction query.

**Model answer:** Use old < boundary <= new under a documented source contract. Include a deletion strategy and explain why backdated updates need more than a timestamp.

### P03. Implement a file completeness gate.

**Model answer:** Compare expected manifest paths/counts/checksums against landed objects and preserve run evidence. Test a missing and a duplicate delivery.

### P04. Create a failing-and-recovered test for one scheduled entity pipeline.

**Model answer:** Capture the initial source watermark, immutable delivery manifest and accepted run record, introduce one realistic dependency or validation failure and use activity output, integration-runtime diagnostics and source/sink throughput to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Azure Data Factory (ADF).

**Model answer:** Document pipeline JSON, linked services, trigger definitions and parameterized datasets, the source schema, extraction boundary and sink dataset schema, required linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, owner, normal/failure signals and recovery instructions using source watermark, immutable delivery manifest and accepted run record. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Azure Data Factory (ADF) fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Source -> linked service and integration runtime -> Copy activity -> ADLS landing -> transformation activity -> validation -> accepted serving dataset. Explain what this component owns, how source system and invoked Databricks/SQL transformation connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Azure Data Factory (ADF) for banking transaction ingestion and restartable lake modernization?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one scheduled entity pipeline meets them, compare a credible alternative and validate using activity output, integration-runtime diagnostics and source/sink throughput rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Azure Data Factory (ADF) in a financial or telecom project?

**Model answer:** Tie source schema, extraction boundary and sink dataset schema to accountable business ownership, verify linked-service identity, source permissions, integration-runtime connectivity and ADLS target grants, preserve source watermark, immutable delivery manifest and accepted run record and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Azure Data Factory (ADF) optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure source query duration, Copy throughput and transformation activity duration with activity output, integration-runtime diagnostics and source/sink throughput, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Azure Data Factory (ADF) interview project?

**Model answer:** Identify which pipeline JSON, linked services, trigger definitions and parameterized datasets you personally built/reviewed/operated, one specific failure you resolved, the evidence in source watermark, immutable delivery manifest and accepted run record and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Data Factory (ADF) official documentation](https://learn.microsoft.com/en-us/azure/data-factory/introduction).
- [Integration runtime concepts](https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime).

[Back to all 20 interview guides](README.md).
