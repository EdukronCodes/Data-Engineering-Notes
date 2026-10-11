# SQL — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Relational querying, data modeling, transformation correctness and query performance.

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
Typed source/staging tables -> joins windows and aggregates -> integrity checks -> accepted facts/views -> consumers
```

For this guide, the primary unit is **one transformation query or stored-procedure batch**. The engineering artifacts are engine-specific SQL scripts, schema migrations and execution parameters. Troubleshooting starts with execution plan, logical reads or scan bytes, waits and row estimates; durable progress/evidence is represented by transaction boundary, staging batch ID and accepted output revision. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. How do INNER and LEFT JOIN differ?

INNER retains matching pairs; LEFT preserves left rows with nulls for unmatched right rows. Duplicate matches can multiply rows in either join. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first.

Two matching customer versions can duplicate one journal line and inflate revenue. Prove the intended key uniqueness on both sides before joining, and use a match-count control when a fact is expected to resolve exactly one dimension.

### C02. How do WHERE and HAVING differ?

WHERE filters input rows before grouping; HAVING filters grouped results. Avoid moving predicates if the change alters outer-join or aggregation semantics. Filtering before or after aggregation changes the population. Outer joins also react differently to predicates placed in ON versus WHERE.

A right-table WHERE condition can remove null-extended rows that a LEFT JOIN was intended to preserve. Validate the query using unmatched rows and boundary cases, since moving a predicate can change outer-join meaning even if the resulting plan looks faster.

### C03. How do UNION and UNION ALL differ?

UNION eliminates duplicate result rows; UNION ALL preserves them. Choose from business semantics, not just speed. Duplicate elimination is a semantic operation with computational cost. Prefer preserving records unless the contract explicitly requires set uniqueness.

UNION ALL is appropriate for distinct source deliveries only if duplicate business keys are handled elsewhere. Define whether repeated rows are errors, legitimate events or overlapping deliveries; choosing UNION should not substitute for a business-key strategy.

### C04. What is a CTE?

A named query expression used for readability/recursion where supported. It is not inherently a cached result or guaranteed performance improvement. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Use materialization only when the engine/workload benefits and the desired scope is explicit; readability and caching are different decisions.

### C05. How do window functions differ from GROUP BY?

Windows calculate over related rows while retaining row detail; GROUP BY changes the output grain. Specify partition and ordering carefully. Window calculations retain rows while grouped aggregation changes grain. Specify key partitioning, authoritative order and frame where applicable.

Use a window to choose latest events, then group accepted events to daily subscriber totals. The window's ordering and frame affect which records contribute; test ties and nulls before relying on a latest or running-total calculation.

### C06. How do ROW_NUMBER, RANK and DENSE_RANK differ?

ROW_NUMBER numbers rows; RANK preserves ties with gaps; DENSE_RANK preserves ties without gaps. Deterministic ordering needs an appropriate tie-breaker. Tie behavior is part of business meaning. A rank function cannot choose an authoritative latest correction when the source provides conflicting equal-order rows.

Keep both tied winners for ranking requirements, or reject conflicting ties for latest-state ingestion. Use a business-authoritative tie-breaker where a single current row is required, or retain legitimate ties when the analytical question calls for ranking.

### C07. How should nulls be tested?

Use IS NULL/IS NOT NULL and explicit null-aware business logic. Equality to NULL does not behave like ordinary value equality. Unknown values require deliberate classification. NOT IN with a nullable set and ordinary equality to NULL can defeat intended exclusion checks.

Use a tested null-aware anti-join for missing reference keys and separately report null source keys. Include explicit null cases in fixtures, especially for exclusion lists and joins, so an unknown comparison cannot silently remove the intended population.

### C08. What is a primary versus foreign key?

A primary key identifies a row; a foreign key describes a reference to another key. Enforcement differs by engine, so verify actual constraint behavior. Constraints encode/enforce selected relationships only where the engine supports enforcement. Analytical engines may require explicit integrity checks.

Do not assume a declared warehouse key prevented duplicates without testing the selected engine's behavior. Run duplicate and missing-reference checks where the engine does not enforce the assumed relationship, and reconcile the fact grain independently.

### C09. What is normalization versus a star schema?

Normalization reduces redundant relational facts; star schemas organize dimensional analytical grains. Choose based on transaction versus reporting needs. Model shape follows workload semantics. Normalized operational entities and dimensional analytical facts solve different access and history problems.

A journal reporting model can use dimensions around a line-level fact while operational account updates use relational entities. Define each fact's grain, additive dimensions and history rules before selecting its shape, rather than calling every curated table a warehouse fact.

### C10. Why use DECIMAL for money?

It represents specified fixed decimal precision/scale, unlike binary floating point. Rounding and overflow behavior still need explicit policies. Precision, scale and rounding are part of the contract. Fixed decimal input still needs overflow and aggregation policy checks.

Reconcile signed debit/credit totals in the agreed decimal scale and transaction currency. Avoid intermediate floating-point conversion and decide whether rounding occurs per line or after aggregation, because the two policies can produce different totals.

## B. Advanced implementation questions

### A01. What makes a predicate sargable?

It can support efficient access using the engine's indexing/pruning mechanisms. Avoid unnecessary functions/casts on filtered keys and verify the actual plan. An efficient access predicate must still match timezone and boundary semantics. Rewriting a date expression incorrectly can change which records qualify.

Use a tested half-open timestamp range for a day when that matches the source/business timezone contract. Compare the actual access plan and result set after rewriting predicates, including inclusive/exclusive endpoints and daylight-saving business-date cases.

### A02. How do you diagnose query regression?

Compare plans, estimates, statistics, parameter behavior, blocking and data changes with a prior baseline. Do not add indexes without evidence. Plan changes can come from data distribution, statistics, parameters, indexes or engine behavior. Compare evidence rather than assuming every regression needs an index.

A once-selective customer predicate may become expensive after one customer dominates the data. Inspect waits and locking as well as logical reads, so an efficient-looking access path does not conceal a concurrency-related delay.

### A03. How do isolation levels affect ingestion?

They govern visibility and concurrency behavior; a source-consistent extraction needs a documented snapshot/change boundary. Isolation names and defaults differ by engine. Isolation affects what a query can observe under concurrent writes. A bounded extraction also needs a source-supported change/commit contract.

A stable paginated snapshot and CDC boundary is stronger than repeatedly querying a mutable table with OFFSET. Coordinate snapshot and change boundaries with the source owner; stable ordering does not by itself detect hard deletes or backdated modifications.

### A04. How do you design idempotent upserts?

Define a unique business key and authoritative version/sequence, then use engine-supported transactional logic and concurrency controls. MERGE semantics differ by engine. Upsert correctness requires unique source matches and authoritative change order. Concurrency and deletion ordering must be addressed independently of syntax.

A stale replay must not overwrite a newer accepted amount or resurrect a deleted account. Use engine-supported concurrency protection and retained deletion ordering where needed, and test insert, correction, stale update and replay cases.

### A05. How do you query historical dimensions?

Join on business key and effective interval, then assert exactly one eligible match per fact. Late changes may require fact re-resolution. Effective-time joins require nonoverlapping intervals and an explicit zero-match policy. Current dimension joins can silently restate old facts.

Use the account mapping effective at posting time and fail if two versions qualify. Resolve an unknown key through an approved suspense/default policy and reject ambiguous multiple matches instead of inflating downstream aggregates.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A LEFT JOIN loses unmatched rows after a WHERE filter. Why?

A predicate on right-side values can reject the null-extended rows. Move the predicate to ON only if that matches the intended business semantics. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first.

Two matching customer versions can duplicate one journal line and inflate revenue. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. NOT IN returns no rows when its subquery contains NULL. How do you fix it?

Use a null-aware NOT EXISTS/anti-join design and define desired handling of null keys explicitly. Unknown values require deliberate classification. NOT IN with a nullable set and ordinary equality to NULL can defeat intended exclusion checks.

Use a tested null-aware anti-join for missing reference keys and separately report null source keys. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. A customer join doubles revenue. What do you investigate?

Check dimension key uniqueness and effective intervals. Establish the correct relationship instead of masking the error with DISTINCT. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first.

Two matching customer versions can duplicate one journal line and inflate revenue. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A query uses SELECT DISTINCT to hide duplicates. Is that sufficient?

No. Identify the duplicated grain and join/source cause; DISTINCT may remove legitimate records or conceal incorrect totals. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. Two records share the same latest timestamp. Which should win?

Use an authoritative source sequence or approved tie-breaker; reject unresolved contradictory ties rather than choosing arbitrarily. Tie behavior is part of business meaning. A rank function cannot choose an authoritative latest correction when the source provides conflicting equal-order rows.

Keep both tied winners for ranking requirements, or reject conflicting ties for latest-state ingestion. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A daily balance query sums all historical dates. What should change?

Define selected-date or period-end snapshot semantics. Balances are not additive over time in the same way as transaction amounts. Window calculations retain rows while grouped aggregation changes grain. Specify key partitioning, authoritative order and frame where applicable.

Use a window to choose latest events, then group accepted events to daily subscriber totals. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. A date filter wraps the indexed column in a function. What is your optimization?

Use an equivalent bounded range where correct, then compare access path and results; confirm timezone and inclusive/exclusive boundaries. An efficient access predicate must still match timezone and boundary semantics. Rewriting a date expression incorrectly can change which records qualify.

Use a tested half-open timestamp range for a day when that matches the source/business timezone contract. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. An update blocks ingestion for minutes. What do you inspect?

Inspect transaction duration, locks, access paths and isolation behavior; reduce unnecessary scope and keep correctness/concurrency requirements explicit. Isolation affects what a query can observe under concurrent writes. A bounded extraction also needs a source-supported change/commit contract.

A stable paginated snapshot and CDC boundary is stronger than repeatedly querying a mutable table with OFFSET. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. OFFSET pagination skips rows during concurrent inserts. What is better?

Use a consistent extraction snapshot and deterministic keyset cursor where suitable. Keyset ordering alone does not solve backdated updates. Isolation affects what a query can observe under concurrent writes. A bounded extraction also needs a source-supported change/commit contract.

A stable paginated snapshot and CDC boundary is stronger than repeatedly querying a mutable table with OFFSET. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. The same MERGE script runs differently in Spark and Azure SQL. Why?

Engines differ in SQL syntax, match semantics and transaction behavior. Implement and test an engine-specific version. Upsert correctness requires unique source matches and authoritative change order. Concurrency and deletion ordering must be addressed independently of syntax.

A stale replay must not overwrite a newer accepted amount or resurrect a deleted account. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one transformation query or stored-procedure batch to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate database execution identity, object grants and approved parameter binding. Compare production with the working configuration using execution plan, logical reads or scan bytes, waits and row estimates; do not resolve the incident by giving every identity broad access. Plan changes can come from data distribution, statistics, parameters, indexes or engine behavior. Compare evidence rather than assuming every regression needs an index. Investigate under the real caller rather than the interactive administrator. The relevant path is database execution identity, object grants and approved parameter binding. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

A once-selective customer predicate may become expensive after one customer dominates the data. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says SQL is available, but the business result has not advanced. What would you check?

Trace the expected operation through selected SQL engine and upstream typed staging tables and compare progress in transaction boundary, staging batch ID and accepted output revision. Inspect execution plan, logical reads or scan bytes, waits and row estimates to distinguish a service being reachable from an accepted business operation actually completing. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan. Walk the dependency chain through selected SQL engine and upstream typed staging tables and locate the last accepted evidence in transaction boundary, staging batch ID and accepted output revision. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of engine-specific SQL scripts, schema migrations and execution parameters works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual table grain, key constraints, types and null semantics. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Plan changes can come from data distribution, statistics, parameters, indexes or engine behavior. Compare evidence rather than assuming every regression needs an index. Treat the release as a change to engine-specific SQL scripts, schema migrations and execution parameters and its dependencies, not just to one code file. Compare table grain, key constraints, types and null semantics and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

A once-selective customer predicate may become expensive after one customer dominates the data. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one transformation query or stored-procedure batch although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with execution plan, logical reads or scan bytes, waits and row estimates and inspect join cardinality, scans, statistics, blocking and distributed data movement. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Plan changes can come from data distribution, statistics, parameters, indexes or engine behavior. Compare evidence rather than assuming every regression needs an index. Use execution plan, logical reads or scan bytes, waits and row estimates to compare the same business boundary and concurrency against a known-good baseline. Examine join cardinality, scans, statistics, blocking and distributed data movement and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

A once-selective customer predicate may become expensive after one customer dominates the data. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving SQL may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in transaction boundary, staging batch ID and accepted output revision before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by transaction boundary, staging batch ID and accepted output revision and repeat only through a supported safe operation/status mechanism.

Two matching customer versions can duplicate one journal line and inflate revenue. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one transformation query or stored-procedure batch at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in transaction boundary, staging batch ID and accepted output revision. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. Plan changes can come from data distribution, statistics, parameters, indexes or engine behavior. Compare evidence rather than assuming every regression needs an index. Define who owns the shared mutation and which state version each caller expected. Preserve transaction boundary, staging batch ID and accepted output revision so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

A once-selective customer predicate may become expensive after one customer dominates the data. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches SQL without prior notice. How do you contain the impact?

Validate against table grain, key constraints, types and null semantics and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Filtering before or after aggregation changes the population. Outer joins also react differently to predicates placed in ON versus WHERE. Classify the change against table grain, key constraints, types and null semantics: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

A right-table WHERE condition can remove null-extended rows that a LEFT JOIN was intended to preserve. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some transaction boundary, staging batch ID and accepted output revision evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of transaction boundary, staging batch ID and accepted output revision and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. An efficient access predicate must still match timezone and boundary semantics. Rewriting a date expression incorrectly can change which records qualify. Recovery can reconstruct only what still exists and is consistent. Inventory transaction boundary, staging batch ID and accepted output revision, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

Use a tested half-open timestamp range for a day when that matches the source/business timezone contract. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in execution plan, logical reads or scan bytes, waits and row estimates. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review database execution identity, object grants and approved parameter binding for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read execution plan, logical reads or scan bytes, waits and row estimates and derived exports; minimizing the source log alone does not remove already copied sensitive output.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for SQL accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in engine-specific SQL scripts, schema migrations and execution parameters, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against transaction boundary, staging batch ID and accepted output revision before restoring normal processing. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan. Environment validation belongs before mutation. Bind engine-specific SQL scripts, schema migrations and execution parameters to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Selected sql engine and upstream typed staging tables is temporarily unavailable. What retry and recovery policy fits SQL?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved transaction boundary, staging batch ID and accepted output revision; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep transaction boundary, staging batch ID and accepted output revision durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

Two matching customer versions can duplicate one journal line and inflate revenue. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with SQL rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect join cardinality, scans, statistics, blocking and distributed data movement. Remove demonstrated waste while preserving required transaction boundary, staging batch ID and accepted output revision and correctness/access controls. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to join cardinality, scans, statistics, blocking and distributed data movement and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

Two matching customer versions can duplicate one journal line and inflate revenue. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, engine-specific SQL scripts, schema migrations and execution parameters is restored but the business path still fails. What else is required?

Restore/validate database execution identity, object grants and approved parameter binding, selected SQL engine and upstream typed staging tables and the appropriate transaction boundary, staging batch ID and accepted output revision. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate database execution identity, object grants and approved parameter binding, reconcile transaction boundary, staging batch ID and accepted output revision and execute a normal authorized consumer path before calling the recovery successful.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in SQL. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with execution plan, logical reads or scan bytes, waits and row estimates and validate their table grain, key constraints, types and null semantics. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. Duplicate elimination is a semantic operation with computational cost. Prefer preserving records unless the contract explicitly requires set uniqueness. Find the smallest complete failed business scope using keys/objects and execution plan, logical reads or scan bytes, waits and row estimates. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow table grain, key constraints, types and null semantics and preserve a clear accounting of accepted versus failed scope.

UNION ALL is appropriate for distinct source deliveries only if duplicate business keys are handled elsewhere. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change engine-specific SQL scripts, schema migrations and execution parameters while dependent workloads remain active. What release sequence would you use?

Inventory consumers and table grain, key constraints, types and null semantics compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain transaction boundary, staging batch ID and accepted output revision and define a tested rollback/correction route for incompatible behavior. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep transaction boundary, staging batch ID and accepted output revision and a tested correction/rollback boundary so a partially applied release remains recoverable.

Two matching customer versions can duplicate one journal line and inflate revenue. Validate the accepted result and the intended table grain, key constraints, types and null semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Write latest-record-per-key SQL.

Use ROW_NUMBER with authoritative ordering, and detect conflicting equal-sequence rows separately. Tie behavior is part of business meaning. A rank function cannot choose an authoritative latest correction when the source provides conflicting equal-order rows.

Keep both tied winners for ranking requirements, or reject conflicting ties for latest-state ingestion. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Write source-to-target reconciliation SQL.

Compare key sets, duplicate counts and decimal totals by the same date/entity/currency grain. Precision, scale and rounding are part of the contract. Fixed decimal input still needs overflow and aggregation policy checks.

Reconcile signed debit/credit totals in the agreed decimal scale and transaction currency. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Write an as-of historical join.

Use valid_from <= event time < valid_to with explicit current-end handling and prove one match per fact. Effective-time joins require nonoverlapping intervals and an explicit zero-match policy. Current dimension joins can silently restate old facts.

Use the account mapping effective at posting time and fail if two versions qualify. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one transformation query or stored-procedure batch.

Capture the initial transaction boundary, staging batch ID and accepted output revision, introduce one realistic dependency or validation failure and use execution plan, logical reads or scan bytes, waits and row estimates to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first.

Two matching customer versions can duplicate one journal line and inflate revenue. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for SQL.

Document engine-specific SQL scripts, schema migrations and execution parameters, the table grain, key constraints, types and null semantics, required database execution identity, object grants and approved parameter binding, owner, normal/failure signals and recovery instructions using transaction boundary, staging batch ID and accepted output revision. Include one normal and one failure example plus actual service targets and retention assumptions. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first.

Two matching customer versions can duplicate one journal line and inflate revenue. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does SQL fit in an end-to-end Azure data platform?

Use this specific flow: Typed source/staging tables -> joins windows and aggregates -> integrity checks -> accepted facts/views -> consumers. Explain what this component owns, how selected SQL engine and upstream typed staging tables connects, and what the accepted consumer/result boundary is. Constraints encode/enforce selected relationships only where the engine supports enforcement. Analytical engines may require explicit integrity checks.

Do not assume a declared warehouse key prevented duplicates without testing the selected engine's behavior. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using SQL for financial warehouse reconciliation and banking analytical transformations?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one transformation query or stored-procedure batch meets them, compare a credible alternative and validate using execution plan, logical reads or scan bytes, waits and row estimates rather than choosing a tool merely because it is on the stack. A named expression improves readability but does not necessarily persist results. Reuse and execution behavior depend on the engine/plan.

A CTE referenced twice may still need plan inspection rather than an assumption that it was materialized once. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround SQL in a financial or telecom project?

Tie table grain, key constraints, types and null semantics to accountable business ownership, verify database execution identity, object grants and approved parameter binding, preserve transaction boundary, staging batch ID and accepted output revision and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. An efficient access predicate must still match timezone and boundary semantics. Rewriting a date expression incorrectly can change which records qualify.

Use a tested half-open timestamp range for a day when that matches the source/business timezone contract. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your SQL optimization helped?

Record the old/new configuration and comparable workload, measure join cardinality, scans, statistics, blocking and distributed data movement with execution plan, logical reads or scan bytes, waits and row estimates, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. A join's output grain follows all eligible pairs, not the left input's intended uniqueness. Define relationship cardinality and unmatched-row behavior first.

Two matching customer versions can duplicate one journal line and inflate revenue. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a SQL interview project?

Identify which engine-specific SQL scripts, schema migrations and execution parameters you personally built/reviewed/operated, one specific failure you resolved, the evidence in transaction boundary, staging batch ID and accepted output revision and a verified outcome. State team-owned components separately and do not invent scale or savings. Plan changes can come from data distribution, statistics, parameters, indexes or engine behavior. Compare evidence rather than assuming every regression needs an index.

A once-selective customer predicate may become expensive after one customer dominates the data. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

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

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Write latest-record-per-key SQL.**

```sql
-- T-SQL example: validate null keys and conflicting equal-sequence
-- payloads separately before using this latest-per-key result.
WITH ordered AS (
  SELECT source_system, transaction_id, line_id, source_sequence,
         amount, currency_code,
         ROW_NUMBER() OVER (
           PARTITION BY source_system, transaction_id, line_id
           ORDER BY source_sequence DESC
         ) AS rn
  FROM dbo.validated_staging
)
SELECT source_system, transaction_id, line_id, source_sequence,
       amount, currency_code
FROM ordered WHERE rn = 1;
-- Equal sequence rows must have an identical full relevant payload
-- or fail validation; otherwise ordering remains ambiguous.
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [SQL official documentation](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql).

[Back to all 20 interview guides](README.md).
