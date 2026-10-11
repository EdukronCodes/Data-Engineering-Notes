# Azure Databricks — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Distributed lakehouse transformations, orchestration of Spark workloads and governed analytical serving.

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
ADF or event source -> ADLS/Delta bronze -> Databricks job -> silver transformations -> gold Delta -> Databricks SQL or reporting
```

For this guide, the primary unit is **one Databricks job or notebook task**. The engineering artifacts are job definition, notebook/package version and compute configuration. Troubleshooting starts with Spark UI stages, task skew, job logs and Delta operation history; durable progress/evidence is represented by Delta table version, job run ID and streaming checkpoint where relevant. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is Azure Databricks?

**Model answer:** An Azure-integrated data/AI platform used for distributed processing and lakehouse workloads. Distinguish the platform from Apache Spark, which is one processing engine it uses.

### C02. What is the driver versus an executor?

**Model answer:** The driver coordinates application execution and planning; executors process distributed tasks. Collecting large data to the driver defeats distributed memory scaling.

### C03. How do jobs differ from exploratory notebooks?

**Model answer:** Jobs provide scheduled/triggered production tasks, parameters and execution controls. Notebooks support development; production requires versioning, ownership and reproducible deployment.

### C04. What is a Delta table?

**Model answer:** A table with transaction-log metadata over data files, providing supported transactional and schema behavior. It is not merely a folder of Parquet files.

### C05. What are bronze, silver and gold layers?

**Model answer:** Bronze preserves raw/source context, silver conforms business records, and gold serves defined analytical products. They are design conventions, not required platform names.

### C06. How do SQL warehouses differ from Spark job compute?

**Model answer:** SQL warehouses serve SQL workloads; Spark compute executes distributed jobs/notebooks. Match compute to workload, isolation and measured concurrency.

### C07. What does lazy execution mean?

**Model answer:** Spark transformations build a plan and actions trigger computation. Several actions can recompute the same lineage unless reuse is deliberately materialized or persisted.

### C08. What should a production notebook accept?

**Model answer:** Validated input/output identifiers, run ID, bounded processing scope and rule/configuration version. Return meaningful status without embedding credentials.

### C09. How do you govern access?

**Model answer:** Use Unity Catalog object grants and approved storage credentials/external locations where appropriate, plus platform identity/workspace policies.

### C10. What does the Spark UI reveal?

**Model answer:** Stages, task duration, shuffle volume, skew, spills and execution plans help identify bottlenecks. Correlate them with job input and output evidence.

## B. Advanced implementation questions

### A01. When should you broadcast a dimension?

**Model answer:** When the actual serialized relation is small enough for executor memory and the join plan benefits. Verify size, skew and runtime behavior instead of forcing broadcasts universally.

### A02. How do you handle late dimension changes?

**Model answer:** Maintain effective intervals, reconstruct affected key timelines and re-resolve impacted facts. Closing only the current row may mishandle out-of-order history.

### A03. How do you make foreachBatch safe?

**Model answer:** Design the handler to be idempotent using batch/business keys and transactional target operations where supported. The function can execute more than once.

### A04. How do you tune cost and performance together?

**Model answer:** Measure cost per accepted workload, startup/runtime, utilization, shuffle and query latency. Select compute and scaling from these measures, not only job duration.

### A05. How do you upgrade runtimes safely?

**Model answer:** Pin dependencies, validate API/connector compatibility and run correctness/performance/replay fixtures in test. Promote with a rollback and data compatibility plan.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A Spark job spends most time in one task. What do you investigate?

**Model answer:** Check skewed keys and partition sizes in task metrics. Filter early, redesign keys or use supported skew handling, then compare the new plan.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. Executors fail after a forced broadcast. What do you do?

**Model answer:** Confirm relation size and memory pressure, remove the forced hint if unsuitable, and evaluate a shuffle join with appropriate partitioning.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. The driver crashes during collect(). What is the fix?

**Model answer:** Remove large driver materialization. Write distributed output or use bounded samples; increasing driver size alone preserves the faulty scaling design.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A job creates thousands of tiny Delta files. How do you improve it?

**Model answer:** Measure batch sizes and writer partitions, use suitable compaction/layout maintenance and verify retention. Avoid arbitrary repartitioning without workload evidence.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. Two tasks MERGE the same target partition. How do you respond to conflicts?

**Model answer:** Partition ownership or serialize conflicting writes, handle supported optimistic conflicts with bounded retry and verify idempotent results.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. A reference change arrives after gold facts were published. What must change?

**Model answer:** Rebuild the affected dimension timeline and identify dependent fact dates. Publish a reconciled revision rather than only changing the current dimension.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. A notebook works interactively but not in a job. What do you compare?

**Model answer:** Compare execution identity, runtime, dependencies, parameters, catalog/context and network permissions. Reproduce under the job identity.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. A stream checkpoint is deleted. Is restart from latest safe?

**Model answer:** Not automatically. Identify recoverable offsets/raw input and target idempotency; plan controlled replay instead of silently skipping data.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. SQL warehouse queries slow during a batch workload. What would you isolate?

**Model answer:** Measure concurrency and resource contention; separate serving and transformation compute where justified and tune the expensive query plan.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. A runtime upgrade changes output decimal rounding. How do you detect and prevent it?

**Model answer:** Run explicit decimal/null/timezone fixtures and financial reconciliation before promotion. Record the runtime/rule version and roll back incompatible outputs.

**Verification:** Use relevant Spark UI stages, task skew, job logs and Delta operation history and confirm the intended input schema, source keys and silver/gold table contract. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one Databricks job or notebook task to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate job identity, Unity Catalog grants, storage credential and network connectivity. Compare production with the working configuration using Spark UI stages, task skew, job logs and Delta operation history; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Azure Databricks is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through ADLS source, Unity Catalog metadata and upstream orchestration and compare progress in Delta table version, job run ID and streaming checkpoint where relevant. Inspect Spark UI stages, task skew, job logs and Delta operation history to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of job definition, notebook/package version and compute configuration works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual input schema, source keys and silver/gold table contract. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one Databricks job or notebook task although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with Spark UI stages, task skew, job logs and Delta operation history and inspect shuffle spill, skewed tasks, scan volume and compute utilization. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Azure Databricks may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in Delta table version, job run ID and streaming checkpoint where relevant before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one Databricks job or notebook task at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in Delta table version, job run ID and streaming checkpoint where relevant. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Azure Databricks without prior notice. How do you contain the impact?

**Model answer:** Validate against input schema, source keys and silver/gold table contract and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some Delta table version, job run ID and streaming checkpoint where relevant evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of Delta table version, job run ID and streaming checkpoint where relevant and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in Spark UI stages, task skew, job logs and Delta operation history. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review job identity, Unity Catalog grants, storage credential and network connectivity for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Azure Databricks accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in job definition, notebook/package version and compute configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against Delta table version, job run ID and streaming checkpoint where relevant before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Adls source, unity catalog metadata and upstream orchestration is temporarily unavailable. What retry and recovery policy fits Azure Databricks?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved Delta table version, job run ID and streaming checkpoint where relevant; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Azure Databricks rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect shuffle spill, skewed tasks, scan volume and compute utilization. Remove demonstrated waste while preserving required Delta table version, job run ID and streaming checkpoint where relevant and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, job definition, notebook/package version and compute configuration is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate job identity, Unity Catalog grants, storage credential and network connectivity, ADLS source, Unity Catalog metadata and upstream orchestration and the appropriate Delta table version, job run ID and streaming checkpoint where relevant. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Azure Databricks. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with Spark UI stages, task skew, job logs and Delta operation history and validate their input schema, source keys and silver/gold table contract. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change job definition, notebook/package version and compute configuration while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and input schema, source keys and silver/gold table contract compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain Delta table version, job run ID and streaming checkpoint where relevant and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Create a parameterized bronze-to-silver notebook.

**Model answer:** Use explicit schemas, bad-record handling, ordered deduplication and target controls. Prove replay produces the same business output.

### P02. Diagnose a slow Spark join from a plan.

**Model answer:** Identify join type, shuffle boundaries, estimates and task skew; propose a measured change and explain its tradeoff.

### P03. Build a multi-task job dependency graph.

**Model answer:** Separate independent tasks, reference dependencies and critical publication gates. Include durable run IDs and failure recovery.

### P04. Create a failing-and-recovered test for one Databricks job or notebook task.

**Model answer:** Capture the initial Delta table version, job run ID and streaming checkpoint where relevant, introduce one realistic dependency or validation failure and use Spark UI stages, task skew, job logs and Delta operation history to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Azure Databricks.

**Model answer:** Document job definition, notebook/package version and compute configuration, the input schema, source keys and silver/gold table contract, required job identity, Unity Catalog grants, storage credential and network connectivity, owner, normal/failure signals and recovery instructions using Delta table version, job run ID and streaming checkpoint where relevant. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Azure Databricks fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: ADF or event source -> ADLS/Delta bronze -> Databricks job -> silver transformations -> gold Delta -> Databricks SQL or reporting. Explain what this component owns, how ADLS source, Unity Catalog metadata and upstream orchestration connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Azure Databricks for lake modernization, banking transformations and telecom usage processing?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one Databricks job or notebook task meets them, compare a credible alternative and validate using Spark UI stages, task skew, job logs and Delta operation history rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Azure Databricks in a financial or telecom project?

**Model answer:** Tie input schema, source keys and silver/gold table contract to accountable business ownership, verify job identity, Unity Catalog grants, storage credential and network connectivity, preserve Delta table version, job run ID and streaming checkpoint where relevant and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Azure Databricks optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure shuffle spill, skewed tasks, scan volume and compute utilization with Spark UI stages, task skew, job logs and Delta operation history, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Azure Databricks interview project?

**Model answer:** Identify which job definition, notebook/package version and compute configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in Delta table version, job run ID and streaming checkpoint where relevant and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

## Official references

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Azure Databricks official documentation](https://learn.microsoft.com/en-us/azure/databricks/introduction/).
- [Structured Streaming with Unity Catalog](https://learn.microsoft.com/en-us/azure/databricks/structured-streaming/unity-catalog).

[Back to all 20 interview guides](README.md).
