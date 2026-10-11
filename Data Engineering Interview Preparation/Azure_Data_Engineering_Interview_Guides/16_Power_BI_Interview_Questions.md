# Power BI — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Business semantic models, measures, dashboards, refresh behavior and governed reporting.

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
Accepted facts and dimensions -> semantic model -> relationships and DAX measures -> secured report -> consumer decision
```

For this guide, the primary unit is **one semantic-model refresh or report query**. The engineering artifacts are model relationships, DAX measures, report definition and refresh settings. Troubleshooting starts with refresh history, visual/query timings, source queries and accepted-data age; durable progress/evidence is represented by model refresh boundary, accepted fact revision and date partition scope. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is a semantic model?

**Model answer:** A defined analytical model of data, relationships and measures used by reports. Its grain and calculations must reflect the business contract.

### C02. What is a star schema useful for?

**Model answer:** Dimensions filter facts with clear relationships and grains. It simplifies analytical reasoning and avoids accidental many-to-many multiplication.

### C03. How do Import and DirectQuery differ?

**Model answer:** Import stores model data for query use; DirectQuery sends queries to the source under supported behavior. Freshness, latency and source load differ.

### C04. Where does Direct Lake fit?

**Model answer:** A supported lake-oriented model mode for compatible Fabric scenarios. Validate the actual model/endpoint implementation and query path.

### C05. How do measures and calculated columns differ?

**Model answer:** Measures evaluate in query/filter context; calculated columns store/evaluate row-derived values under model processing behavior. Choose based on semantics and resource impact.

### C06. What are filter context and row context?

**Model answer:** Filter context defines selected rows for evaluation; row context iterates/current-row evaluation. DAX behavior depends on context transitions and relationships.

### C07. What is CALCULATE used for?

**Model answer:** Evaluating an expression under modified filter context. The specific filter changes must be intentional and tested.

### C08. What is row-level security?

**Model answer:** Model security rules limiting rows for applicable consumers. Underlying storage/source access and elevated workspace roles require separate review.

### C09. What is incremental refresh for?

**Model answer:** Processing defined date ranges/partitions rather than all historical data, subject to supported configuration. Verify filtering/query folding and late-correction policy.

### C10. Why are dates and relationships important?

**Model answer:** Consistent calendars, active relationships and fact dates determine correct time analysis. Multiple date roles need explicit modeling.

## B. Advanced implementation questions

### A01. How do you model semi-additive balances?

**Model answer:** Aggregate across approved entity dimensions but use selected-date/period-end behavior across time. Do not sum all daily snapshots as current balance.

### A02. How do you diagnose slow reports?

**Model answer:** Measure expensive visuals/measures and source/model queries, then inspect cardinality, relationships and filter paths. Do not start by adding every column to the model.

### A03. How do you handle late fact corrections?

**Model answer:** Refresh/reprocess affected partitions or use a supported current serving mode, then reconcile the revised accepted product and report measures.

### A04. How do you validate RLS?

**Model answer:** Test actual user/group paths and elevated/direct-data access separately; compare allowed/forbidden rows and exports.

### A05. How do you deploy model changes?

**Model answer:** Version model/report dependencies, test relationships/measures/security and promote compatible sources/contracts with environment settings.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. Revenue doubles after adding a customer table. What do you inspect?

**Model answer:** Check relationship cardinality, duplicated dimension keys, filtering and fact grain; fix the model instead of masking totals.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. A monthly chart adds daily closing balances. What is wrong?

**Model answer:** The measure treats snapshot values as fully additive. Implement the approved month-end/selected-date definition.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. RLS works in testing but an admin sees every region. Is that unexpected?

**Model answer:** Elevated roles/access can have different effective security behavior. Validate each real consumer role and underlying data path.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. Refresh succeeds but the report has yesterday's business data. What should be monitored?

**Model answer:** The accepted source/product as-of boundary and freshness target, not just model refresh completion.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. DirectQuery slows an operational database. What options would you evaluate?

**Model answer:** Measure query/concurrency pressure, tune the model/source and consider an appropriate analytical serving/import strategy aligned with freshness needs.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. An incremental-refresh report misses a historical correction. Why?

**Model answer:** The correction falls outside reprocessed scope or filtering policy. Reprocess affected partitions and define a late-correction mechanism.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. A DAX measure returns the same value for every product. What do you inspect?

**Model answer:** Check relationship paths, removed filters and CALCULATE/filter context behavior with small known examples.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. One visual is fast while a page is slow. Why?

**Model answer:** Multiple visuals/queries, expensive measures and interactions can create cumulative load. Measure the full page behavior and simplify the actual bottleneck.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. A schema rename breaks refresh and measures. How do you release safely?

**Model answer:** Use compatibility/versioning, dependency impact checks and coordinated source/model deployment with rollback.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. A user downloads sensitive details from a permitted report. What controls matter?

**Model answer:** Review report/model/export permissions and data minimization alongside row filters; validate the permitted consumer and underlying source paths.

**Verification:** Use relevant refresh history, visual/query timings, source queries and accepted-data age and confirm the intended fact grains, measure definitions, relationship cardinality and date semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one semantic-model refresh or report query to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate workspace/model/report roles, row security and direct source permissions. Compare production with the working configuration using refresh history, visual/query timings, source queries and accepted-data age; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Power BI is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through accepted lakehouse/warehouse tables and report consumers and compare progress in model refresh boundary, accepted fact revision and date partition scope. Inspect refresh history, visual/query timings, source queries and accepted-data age to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of model relationships, DAX measures, report definition and refresh settings works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual fact grains, measure definitions, relationship cardinality and date semantics. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one semantic-model refresh or report query although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with refresh history, visual/query timings, source queries and accepted-data age and inspect high cardinality, expensive DAX, source query latency and visual concurrency. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Power BI may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in model refresh boundary, accepted fact revision and date partition scope before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one semantic-model refresh or report query at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in model refresh boundary, accepted fact revision and date partition scope. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Power BI without prior notice. How do you contain the impact?

**Model answer:** Validate against fact grains, measure definitions, relationship cardinality and date semantics and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some model refresh boundary, accepted fact revision and date partition scope evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of model refresh boundary, accepted fact revision and date partition scope and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in refresh history, visual/query timings, source queries and accepted-data age. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review workspace/model/report roles, row security and direct source permissions for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Power BI accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in model relationships, DAX measures, report definition and refresh settings, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against model refresh boundary, accepted fact revision and date partition scope before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Accepted lakehouse/warehouse tables and report consumers is temporarily unavailable. What retry and recovery policy fits Power BI?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved model refresh boundary, accepted fact revision and date partition scope; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Power BI rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect high cardinality, expensive DAX, source query latency and visual concurrency. Remove demonstrated waste while preserving required model refresh boundary, accepted fact revision and date partition scope and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, model relationships, DAX measures, report definition and refresh settings is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate workspace/model/report roles, row security and direct source permissions, accepted lakehouse/warehouse tables and report consumers and the appropriate model refresh boundary, accepted fact revision and date partition scope. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Power BI. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with refresh history, visual/query timings, source queries and accepted-data age and validate their fact grains, measure definitions, relationship cardinality and date semantics. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change model relationships, DAX measures, report definition and refresh settings while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and fact grains, measure definitions, relationship cardinality and date semantics compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain model refresh boundary, accepted fact revision and date partition scope and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Build a transaction-and-balance model.

**Model answer:** Specify separate fact grains, dimensions and a date-aware balance measure; validate with known daily snapshots.

### P02. Design and test regional RLS.

**Model answer:** Map users/groups to allowed regions, test real role paths and examine elevated/direct data access separately.

### P03. Diagnose one expensive visual.

**Model answer:** Capture query/measure evidence, inspect model relationships and choose a measured optimization without changing totals.

### P04. Create a failing-and-recovered test for one semantic-model refresh or report query.

**Model answer:** Capture the initial model refresh boundary, accepted fact revision and date partition scope, introduce one realistic dependency or validation failure and use refresh history, visual/query timings, source queries and accepted-data age to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Power BI.

**Model answer:** Document model relationships, DAX measures, report definition and refresh settings, the fact grains, measure definitions, relationship cardinality and date semantics, required workspace/model/report roles, row security and direct source permissions, owner, normal/failure signals and recovery instructions using model refresh boundary, accepted fact revision and date partition scope. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Power BI fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Accepted facts and dimensions -> semantic model -> relationships and DAX measures -> secured report -> consumer decision. Explain what this component owns, how accepted lakehouse/warehouse tables and report consumers connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Power BI for banking balances, finance reporting and enterprise quality dashboards?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one semantic-model refresh or report query meets them, compare a credible alternative and validate using refresh history, visual/query timings, source queries and accepted-data age rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Power BI in a financial or telecom project?

**Model answer:** Tie fact grains, measure definitions, relationship cardinality and date semantics to accountable business ownership, verify workspace/model/report roles, row security and direct source permissions, preserve model refresh boundary, accepted fact revision and date partition scope and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Power BI optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure high cardinality, expensive DAX, source query latency and visual concurrency with refresh history, visual/query timings, source queries and accepted-data age, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Power BI interview project?

**Model answer:** Identify which model relationships, DAX measures, report definition and refresh settings you personally built/reviewed/operated, one specific failure you resolved, the evidence in model refresh boundary, accepted fact revision and date partition scope and a verified outcome. State team-owned components separately and do not invent scale or savings.

## Revision notes and common mistakes

- Explain Power BI's specific responsibility in the flow before naming surrounding tools.
- Use the real fact grains, measure definitions, relationship cardinality and date semantics; an accepted request/job does not establish a correct business result.
- Validate workspace/model/report roles, row security and direct source permissions under the actual execution identity, rather than your administrator account.
- Preserve model refresh boundary, accepted fact revision and date partition scope and inspect it before retrying uncertain side effects.
- Tune high cardinality, expensive DAX, source query latency and visual concurrency from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Official references

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Power BI official documentation](https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-overview).

[Back to all 20 interview guides](README.md).
