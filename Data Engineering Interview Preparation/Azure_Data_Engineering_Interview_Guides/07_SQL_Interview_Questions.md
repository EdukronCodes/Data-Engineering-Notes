# SQL — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Relational querying, data modeling, transformation correctness and query performance.

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
Typed source/staging tables -> joins windows and aggregates -> integrity checks -> accepted facts/views -> consumers
```

For this guide, the primary unit is **one transformation query or stored-procedure batch**. The engineering artifacts are engine-specific SQL scripts, schema migrations and execution parameters. Troubleshooting starts with execution plan, logical reads or scan bytes, waits and row estimates; durable progress/evidence is represented by transaction boundary, staging batch ID and accepted output revision. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. How do INNER and LEFT JOIN differ?

**Model answer:** INNER retains matching pairs; LEFT preserves left rows with nulls for unmatched right rows. Duplicate matches can multiply rows in either join.

### C02. How do WHERE and HAVING differ?

**Model answer:** WHERE filters input rows before grouping; HAVING filters grouped results. Avoid moving predicates if the change alters outer-join or aggregation semantics.

### C03. How do UNION and UNION ALL differ?

**Model answer:** UNION eliminates duplicate result rows; UNION ALL preserves them. Choose from business semantics, not just speed.

### C04. What is a CTE?

**Model answer:** A named query expression used for readability/recursion where supported. It is not inherently a cached result or guaranteed performance improvement.

### C05. How do window functions differ from GROUP BY?

**Model answer:** Windows calculate over related rows while retaining row detail; GROUP BY changes the output grain. Specify partition and ordering carefully.

### C06. How do ROW_NUMBER, RANK and DENSE_RANK differ?

**Model answer:** ROW_NUMBER numbers rows; RANK preserves ties with gaps; DENSE_RANK preserves ties without gaps. Deterministic ordering needs an appropriate tie-breaker.

### C07. How should nulls be tested?

**Model answer:** Use IS NULL/IS NOT NULL and explicit null-aware business logic. Equality to NULL does not behave like ordinary value equality.

### C08. What is a primary versus foreign key?

**Model answer:** A primary key identifies a row; a foreign key describes a reference to another key. Enforcement differs by engine, so verify actual constraint behavior.

### C09. What is normalization versus a star schema?

**Model answer:** Normalization reduces redundant relational facts; star schemas organize dimensional analytical grains. Choose based on transaction versus reporting needs.

### C10. Why use DECIMAL for money?

**Model answer:** It represents specified fixed decimal precision/scale, unlike binary floating point. Rounding and overflow behavior still need explicit policies.

## B. Advanced implementation questions

### A01. What makes a predicate sargable?

**Model answer:** It can support efficient access using the engine's indexing/pruning mechanisms. Avoid unnecessary functions/casts on filtered keys and verify the actual plan.

### A02. How do you diagnose query regression?

**Model answer:** Compare plans, estimates, statistics, parameter behavior, blocking and data changes with a prior baseline. Do not add indexes without evidence.

### A03. How do isolation levels affect ingestion?

**Model answer:** They govern visibility and concurrency behavior; a source-consistent extraction needs a documented snapshot/change boundary. Isolation names and defaults differ by engine.

### A04. How do you design idempotent upserts?

**Model answer:** Define a unique business key and authoritative version/sequence, then use engine-supported transactional logic and concurrency controls. MERGE semantics differ by engine.

### A05. How do you query historical dimensions?

**Model answer:** Join on business key and effective interval, then assert exactly one eligible match per fact. Late changes may require fact re-resolution.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A LEFT JOIN loses unmatched rows after a WHERE filter. Why?

**Model answer:** A predicate on right-side values can reject the null-extended rows. Move the predicate to ON only if that matches the intended business semantics.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. NOT IN returns no rows when its subquery contains NULL. How do you fix it?

**Model answer:** Use a null-aware NOT EXISTS/anti-join design and define desired handling of null keys explicitly.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. A customer join doubles revenue. What do you investigate?

**Model answer:** Check dimension key uniqueness and effective intervals. Establish the correct relationship instead of masking the error with DISTINCT.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A query uses SELECT DISTINCT to hide duplicates. Is that sufficient?

**Model answer:** No. Identify the duplicated grain and join/source cause; DISTINCT may remove legitimate records or conceal incorrect totals.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. Two records share the same latest timestamp. Which should win?

**Model answer:** Use an authoritative source sequence or approved tie-breaker; reject unresolved contradictory ties rather than choosing arbitrarily.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. A daily balance query sums all historical dates. What should change?

**Model answer:** Define selected-date or period-end snapshot semantics. Balances are not additive over time in the same way as transaction amounts.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. A date filter wraps the indexed column in a function. What is your optimization?

**Model answer:** Use an equivalent bounded range where correct, then compare access path and results; confirm timezone and inclusive/exclusive boundaries.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. An update blocks ingestion for minutes. What do you inspect?

**Model answer:** Inspect transaction duration, locks, access paths and isolation behavior; reduce unnecessary scope and keep correctness/concurrency requirements explicit.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. OFFSET pagination skips rows during concurrent inserts. What is better?

**Model answer:** Use a consistent extraction snapshot and deterministic keyset cursor where suitable. Keyset ordering alone does not solve backdated updates.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. The same MERGE script runs differently in Spark and Azure SQL. Why?

**Model answer:** Engines differ in SQL syntax, match semantics and transaction behavior. Implement and test an engine-specific version.

**Verification:** Use relevant execution plan, logical reads or scan bytes, waits and row estimates and confirm the intended table grain, key constraints, types and null semantics. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one transformation query or stored-procedure batch to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate database execution identity, object grants and approved parameter binding. Compare production with the working configuration using execution plan, logical reads or scan bytes, waits and row estimates; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says SQL is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through selected SQL engine and upstream typed staging tables and compare progress in transaction boundary, staging batch ID and accepted output revision. Inspect execution plan, logical reads or scan bytes, waits and row estimates to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of engine-specific SQL scripts, schema migrations and execution parameters works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual table grain, key constraints, types and null semantics. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one transformation query or stored-procedure batch although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with execution plan, logical reads or scan bytes, waits and row estimates and inspect join cardinality, scans, statistics, blocking and distributed data movement. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving SQL may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in transaction boundary, staging batch ID and accepted output revision before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one transformation query or stored-procedure batch at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in transaction boundary, staging batch ID and accepted output revision. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches SQL without prior notice. How do you contain the impact?

**Model answer:** Validate against table grain, key constraints, types and null semantics and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some transaction boundary, staging batch ID and accepted output revision evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of transaction boundary, staging batch ID and accepted output revision and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in execution plan, logical reads or scan bytes, waits and row estimates. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review database execution identity, object grants and approved parameter binding for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for SQL accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in engine-specific SQL scripts, schema migrations and execution parameters, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against transaction boundary, staging batch ID and accepted output revision before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Selected sql engine and upstream typed staging tables is temporarily unavailable. What retry and recovery policy fits SQL?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved transaction boundary, staging batch ID and accepted output revision; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with SQL rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect join cardinality, scans, statistics, blocking and distributed data movement. Remove demonstrated waste while preserving required transaction boundary, staging batch ID and accepted output revision and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, engine-specific SQL scripts, schema migrations and execution parameters is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate database execution identity, object grants and approved parameter binding, selected SQL engine and upstream typed staging tables and the appropriate transaction boundary, staging batch ID and accepted output revision. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in SQL. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with execution plan, logical reads or scan bytes, waits and row estimates and validate their table grain, key constraints, types and null semantics. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change engine-specific SQL scripts, schema migrations and execution parameters while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and table grain, key constraints, types and null semantics compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain transaction boundary, staging batch ID and accepted output revision and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Write latest-record-per-key SQL.

**Model answer:** Use ROW_NUMBER with authoritative ordering, and detect conflicting equal-sequence rows separately.

### P02. Write source-to-target reconciliation SQL.

**Model answer:** Compare key sets, duplicate counts and decimal totals by the same date/entity/currency grain.

### P03. Write an as-of historical join.

**Model answer:** Use valid_from <= event time < valid_to with explicit current-end handling and prove one match per fact.

### P04. Create a failing-and-recovered test for one transformation query or stored-procedure batch.

**Model answer:** Capture the initial transaction boundary, staging batch ID and accepted output revision, introduce one realistic dependency or validation failure and use execution plan, logical reads or scan bytes, waits and row estimates to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for SQL.

**Model answer:** Document engine-specific SQL scripts, schema migrations and execution parameters, the table grain, key constraints, types and null semantics, required database execution identity, object grants and approved parameter binding, owner, normal/failure signals and recovery instructions using transaction boundary, staging batch ID and accepted output revision. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does SQL fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Typed source/staging tables -> joins windows and aggregates -> integrity checks -> accepted facts/views -> consumers. Explain what this component owns, how selected SQL engine and upstream typed staging tables connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using SQL for financial warehouse reconciliation and banking analytical transformations?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one transformation query or stored-procedure batch meets them, compare a credible alternative and validate using execution plan, logical reads or scan bytes, waits and row estimates rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround SQL in a financial or telecom project?

**Model answer:** Tie table grain, key constraints, types and null semantics to accountable business ownership, verify database execution identity, object grants and approved parameter binding, preserve transaction boundary, staging batch ID and accepted output revision and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your SQL optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure join cardinality, scans, statistics, blocking and distributed data movement with execution plan, logical reads or scan bytes, waits and row estimates, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a SQL interview project?

**Model answer:** Identify which engine-specific SQL scripts, schema migrations and execution parameters you personally built/reviewed/operated, one specific failure you resolved, the evidence in transaction boundary, staging batch ID and accepted output revision and a verified outcome. State team-owned components separately and do not invent scale or savings.

## Revision notes and common mistakes

- Explain SQL's specific responsibility in the flow before naming surrounding tools.
- Use the real table grain, key constraints, types and null semantics; an accepted request/job does not establish a correct business result.
- Validate database execution identity, object grants and approved parameter binding under the actual execution identity, rather than your administrator account.
- Preserve transaction boundary, staging batch ID and accepted output revision and inspect it before retrying uncertain side effects.
- Tune join cardinality, scans, statistics, blocking and distributed data movement from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Official references

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [SQL official documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql).

[Back to all 20 interview guides](README.md).
