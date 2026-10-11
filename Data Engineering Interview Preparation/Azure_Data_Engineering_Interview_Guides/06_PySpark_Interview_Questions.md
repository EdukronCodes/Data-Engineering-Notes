# PySpark — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Distributed DataFrame transformations, join/window logic, aggregation and streaming correctness.

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
Explicit-schema input -> DataFrame transformations -> validation and ordered deduplication -> Delta/Parquet output -> reconciliation
```

For this guide, the primary unit is **one distributed DataFrame transformation**. The engineering artifacts are PySpark module/notebook, explicit input schema and transformation tests. Troubleshooting starts with explain plan, Spark UI exchanges, task skew and spill metrics; durable progress/evidence is represented by source sequence, input snapshot, output table version and checkpoint if streaming. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. How do DataFrames differ from RDDs?

DataFrames provide schema-aware operations and optimizer visibility. RDDs expose lower-level transformations and may be appropriate for specialized requirements. DataFrames expose schema and relational operations to Spark's optimizer. Lower-level RDD logic gives more manual control but can obscure query optimization opportunities.

Express a keyed decimal aggregation through native DataFrame operations before considering custom partition code. Choose the highest-level operation that expresses the required logic clearly, then inspect the resulting plan and keep low-level custom processing justified by a specific need.

### C02. What is lazy evaluation?

Transformations define a plan; actions execute it. Repeated actions can repeat computation unless reuse is deliberately materialized or persisted. An action materializes a computation plan. Plan construction is cheap relative to execution, and repeated actions may repeat scans/shuffles.

Calling count and then write can execute overlapping work twice unless an appropriate reuse strategy exists. Measure when expensive execution actually happens, especially when validation counts and writes both trigger actions over the same transformation lineage.

### C03. What is a shuffle?

Redistribution of records across partitions for joins, grouping or sorting. It can add network, memory and disk cost. Shuffles redistribute records to satisfy grouping/join/order requirements. Network transfer and per-key skew can dominate even when input reading is fast.

A subscriber aggregation sends related records to common partitions and must handle hot subscribers explicitly. Filter and select columns before wide work where correct, and inspect shuffle/spill metrics to distinguish network redistribution from source-read delays.

### C04. What is the difference between repartition and coalesce?

Repartition generally redistributes data with shuffle. Coalesce can reduce partitions with less movement but may create imbalance; choose based on the workload. Partition-count changes are not performance guarantees. Too few partitions create large tasks; too many create overhead and potentially tiny output files.

Choose writer/task layout from representative volume and measured durations, not an arbitrary fixed repartition count. Compare task balance and output file counts after changes, because fewer tasks or fewer files alone does not prove better end-to-end performance.

### C05. How do narrow and wide transformations differ?

Narrow operations can operate within a partition lineage; wide operations require cross-partition dependencies such as shuffle. Dependency structure determines whether an operation needs data exchange. Recognizing exchanges helps prioritize the expensive portions of a plan.

Filtering rows before a wide join can reduce transferred data without changing the intended result. The same logical query can contain several exchanges; focus on the expensive boundaries rather than attempting to eliminate every distributed operation.

### C06. Why prefer built-in expressions over Python UDFs?

Built-ins usually preserve optimizer visibility and avoid Python serialization overhead. Use a UDF only when suitable native expressions are unavailable. Native expressions preserve engine optimization and avoid much Python cross-language work. A UDF must have defined types/null behavior and measured justification.

Use built-in conditional/string/date functions for common validation rather than row-by-row Python parsing. Define expected nulls and output types explicitly, and benchmark the native expression against a representative input before replacing a custom UDF.

### C07. How do window functions help deduplication?

Partition by business key and order by an authoritative source sequence, then select the latest row. Reject conflicting ties instead of choosing an arbitrary record. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate null keys and conflicting equal-sequence payloads before the window, then confirm the selected record survives stale and duplicate replay.

### C08. What is cache/persist for?

Reusing computed data across actions when the cost and memory/storage footprint justify it. Remove persistence when no longer needed. Persistence trades compute reuse against memory/storage pressure. Materialization and cleanup must be intentional; caching once-used data often wastes resources.

Persist a reused bounded intermediate only after measuring the benefit and unpersist it when its consumers finish. Do not cache merely because the dataset is large; expensive once-only results can waste memory and force other useful data to spill.

### C09. How do nulls behave in filters/joins?

SQL-like three-valued logic means null comparisons are not ordinary equality. Define null semantics explicitly, including null-safe equality where appropriate. Null is not an ordinary comparable value in SQL logic. Three-valued predicates can unintentionally leave records unclassified without explicit null handling.

A missing currency requires isNull validation in addition to checking whether a code is an allowed value. Test null, missing and malformed values separately, and distinguish an ineligible record from one that genuinely violates a required business rule.

### C10. Why are explicit schemas useful?

They avoid repeated inference and ambiguous types, especially decimal/time fields. Malformed and unexpected input still needs a deliberate rejection/evolution policy. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Keep approved parsing and corrupt-record handling visible, because accepting an inferred type can silently weaken financial or historical-time correctness.

## B. Advanced implementation questions

### A01. How do you handle skew?

Measure hot keys and task imbalance; consider filtering, aggregation, supported adaptive handling or carefully designed salting that preserves semantics. Skew handling must preserve logical multiplicity. Salting only one join side or changing group keys without a correct recombination can alter results.

Split a known hot key only with a tested strategy that restores the original aggregation grain. Any salted or adaptive strategy must preserve original join multiplicity and aggregation grain; compare independent key/totals evidence after tuning.

### A02. How do you implement SCD Type 2 correctly?

Define tracked attributes, effective timestamps and half-open intervals. Validate one current version and nonoverlap; rebuild timelines for late changes. Temporal correctness comes from ordered effective intervals, not merely a hash difference. Late changes require recomputing the impacted key timeline.

A backdated subscriber plan change can affect usage facts already enriched with the wrong historical version. Assert nonoverlapping intervals and at most one current version, then reprocess the facts whose business times fall in a corrected interval.

### A03. What is watermarking?

An event-time policy used by supported stateful streaming operations to manage late data/state. It is not a universal promise that all late events are retained or rejected identically. Watermarks manage supported state based on event time and operation semantics. Retention of raw events and durable key-based replay rules remain necessary.

An old CDR replay outside the state horizon still needs protection against being counted twice. Separate event-time completeness from processing activity, retain raw recovery data and define how out-of-horizon arrivals rebuild accepted outputs.

### A04. How do you test distributed logic?

Use small explicit fixtures for nulls, ties, duplicates, decimal boundaries and late history; compare expected business outputs and test representative integration behavior. Test business edge cases rather than copying implementation logic into expectations. Use independent expected rows/counts/totals and a representative execution check.

A fixture with two equal-sequence conflicting rows should fail before gold publication. Expected results should be independent of the implementation, including decimal boundaries, tie conflicts, late history and replay scenarios.

### A05. How do you interpret an execution plan?

Identify scans, filters, exchanges, joins and aggregates, then compare estimates/task metrics with the data. An optimized plan still requires output validation. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Use plans and measured tasks together, and confirm that optimization changes neither business keys, decimal totals nor historical reference resolution.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A latest-row window returns different results on reruns. Why?

The ordering has ties or lacks an authoritative sequence. Add deterministic source semantics and reject contradictory equal-sequence payloads. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. dropDuplicates removes a corrected transaction. What is wrong?

It does not select the correct latest business version automatically. Use key plus source ordering and explicit correction semantics. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. An aggregation changes decimal cents. What do you inspect?

Check input casts, decimal precision/scale, rounding policy and accidental floating-point conversions. Reconcile with approved decimal totals. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A join increases row count unexpectedly. How do you diagnose it?

Check right-side key uniqueness and effective interval overlaps. Count matches per fact and fix the intended relationship before publishing. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. A UDF is much slower than SQL expressions. What should change?

Translate logic to native functions where possible and benchmark the plan. Check Python serialization and row-at-a-time overhead. Native expressions preserve engine optimization and avoid much Python cross-language work. A UDF must have defined types/null behavior and measured justification.

Use built-in conditional/string/date functions for common validation rather than row-by-row Python parsing. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A global sort slows the whole job. Is it necessary?

Determine whether ordering is required globally or only within business groups. Use the minimal supported ordering required for correctness. Dependency structure determines whether an operation needs data exchange. Recognizing exchanges helps prioritize the expensive portions of a plan.

Filtering rows before a wide join can reduce transferred data without changing the intended result. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. Caching a large table causes spills and recomputation. What do you do?

Measure reuse and storage pressure, choose a suitable persistence level or remove caching, and materialize only genuinely reused scoped data. Persistence trades compute reuse against memory/storage pressure. Materialization and cleanup must be intentional; caching once-used data often wastes resources.

Persist a reused bounded intermediate only after measuring the benefit and unpersist it when its consumers finish. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A null currency slips through a not-equal filter. Why?

Null comparison yields unknown, not true. Include explicit isNull handling and test the predicate's business semantics. Null is not an ordinary comparable value in SQL logic. Three-valued predicates can unintentionally leave records unclassified without explicit null handling.

A missing currency requires isNull validation in addition to checking whether a code is an allowed value. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A stream accepts a very old replay. Does a watermark prevent all duplicates?

No. Bounded state expires; use durable key-based idempotency and retained raw reconciliation for out-of-horizon replay. Watermarks manage supported state based on event time and operation semantics. Retention of raw events and durable key-based replay rules remain necessary.

An old CDR replay outside the state horizon still needs protection against being counted twice. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. An event-time join finds two subscriber versions. What should happen?

Treat overlapping dimension intervals as a critical integrity failure; repair the timeline rather than multiplying usage facts. Temporal correctness comes from ordered effective intervals, not merely a hash difference. Late changes require recomputing the impacted key timeline.

A backdated subscriber plan change can affect usage facts already enriched with the wrong historical version. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one distributed DataFrame transformation to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate execution identity and governed source/target table permissions. Compare production with the working configuration using explain plan, Spark UI exchanges, task skew and spill metrics; do not resolve the incident by giving every identity broad access. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic. Investigate under the real caller rather than the interactive administrator. The relevant path is execution identity and governed source/target table permissions. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says PySpark is available, but the business result has not advanced. What would you check?

Trace the expected operation through Spark runtime, source format and Delta/Parquet sink and compare progress in source sequence, input snapshot, output table version and checkpoint if streaming. Inspect explain plan, Spark UI exchanges, task skew and spill metrics to distinguish a service being reachable from an accepted business operation actually completing. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic. Walk the dependency chain through Spark runtime, source format and Delta/Parquet sink and locate the last accepted evidence in source sequence, input snapshot, output table version and checkpoint if streaming. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of PySpark module/notebook, explicit input schema and transformation tests works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual DataFrame types, business-key uniqueness and event-time semantics. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience. Treat the release as a change to PySpark module/notebook, explicit input schema and transformation tests and its dependencies, not just to one code file. Compare DataFrame types, business-key uniqueness and event-time semantics and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one distributed DataFrame transformation although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with explain plan, Spark UI exchanges, task skew and spill metrics and inspect shuffle, serialization, skewed partitions and driver materialization. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic. Use explain plan, Spark UI exchanges, task skew and spill metrics to compare the same business boundary and concurrency against a known-good baseline. Examine shuffle, serialization, skewed partitions and driver materialization and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving PySpark may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in source sequence, input snapshot, output table version and checkpoint if streaming before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by source sequence, input snapshot, output table version and checkpoint if streaming and repeat only through a supported safe operation/status mechanism.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one distributed DataFrame transformation at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in source sequence, input snapshot, output table version and checkpoint if streaming. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection. Define who owns the shared mutation and which state version each caller expected. Preserve source sequence, input snapshot, output table version and checkpoint if streaming so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches PySpark without prior notice. How do you contain the impact?

Validate against DataFrame types, business-key uniqueness and event-time semantics and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience. Classify the change against DataFrame types, business-key uniqueness and event-time semantics: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some source sequence, input snapshot, output table version and checkpoint if streaming evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of source sequence, input snapshot, output table version and checkpoint if streaming and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. Shuffles redistribute records to satisfy grouping/join/order requirements. Network transfer and per-key skew can dominate even when input reading is fast. Recovery can reconstruct only what still exists and is consistent. Inventory source sequence, input snapshot, output table version and checkpoint if streaming, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

A subscriber aggregation sends related records to common partitions and must handle hot subscribers explicitly. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in explain plan, Spark UI exchanges, task skew and spill metrics. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review execution identity and governed source/target table permissions for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read explain plan, Spark UI exchanges, task skew and spill metrics and derived exports; minimizing the source log alone does not remove already copied sensitive output.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for PySpark accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in PySpark module/notebook, explicit input schema and transformation tests, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against source sequence, input snapshot, output table version and checkpoint if streaming before restoring normal processing. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience. Environment validation belongs before mutation. Bind PySpark module/notebook, explicit input schema and transformation tests to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Spark runtime, source format and delta/parquet sink is temporarily unavailable. What retry and recovery policy fits PySpark?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved source sequence, input snapshot, output table version and checkpoint if streaming; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep source sequence, input snapshot, output table version and checkpoint if streaming durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with PySpark rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect shuffle, serialization, skewed partitions and driver materialization. Remove demonstrated waste while preserving required source sequence, input snapshot, output table version and checkpoint if streaming and correctness/access controls. Partition-count changes are not performance guarantees. Too few partitions create large tasks; too many create overhead and potentially tiny output files. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to shuffle, serialization, skewed partitions and driver materialization and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

Choose writer/task layout from representative volume and measured durations, not an arbitrary fixed repartition count. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, PySpark module/notebook, explicit input schema and transformation tests is restored but the business path still fails. What else is required?

Restore/validate execution identity and governed source/target table permissions, Spark runtime, source format and Delta/Parquet sink and the appropriate source sequence, input snapshot, output table version and checkpoint if streaming. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate execution identity and governed source/target table permissions, reconcile source sequence, input snapshot, output table version and checkpoint if streaming and execute a normal authorized consumer path before calling the recovery successful.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in PySpark. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with explain plan, Spark UI exchanges, task skew and spill metrics and validate their DataFrame types, business-key uniqueness and event-time semantics. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic. Find the smallest complete failed business scope using keys/objects and explain plan, Spark UI exchanges, task skew and spill metrics. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow DataFrame types, business-key uniqueness and event-time semantics and preserve a clear accounting of accepted versus failed scope.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change PySpark module/notebook, explicit input schema and transformation tests while dependent workloads remain active. What release sequence would you use?

Inventory consumers and DataFrame types, business-key uniqueness and event-time semantics compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain source sequence, input snapshot, output table version and checkpoint if streaming and define a tested rollback/correction route for incompatible behavior. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep source sequence, input snapshot, output table version and checkpoint if streaming and a tested correction/rollback boundary so a partially applied release remains recoverable.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Validate the accepted result and the intended DataFrame types, business-key uniqueness and event-time semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Write deterministic latest-per-key logic.

Use Window partitioning and authoritative source sequence, assert equal-sequence payload consistency and verify rerun stability. Latest-per-key means latest under a business ordering contract. A timestamp tie or duplicate key is not resolved correctly by arbitrary row selection.

Reject two conflicting transaction amounts at the same source sequence instead of trusting an unstable row order. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Build a financial reconciliation aggregation.

Cast to explicit decimals, group by matching entity/date/currency grain and compare expected signed totals. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Implement a historical dimension join.

Use half-open intervals and test zero/one/multiple matches plus a late-arriving dimension update. Temporal correctness comes from ordered effective intervals, not merely a hash difference. Late changes require recomputing the impacted key timeline.

A backdated subscriber plan change can affect usage facts already enriched with the wrong historical version. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one distributed DataFrame transformation.

Capture the initial source sequence, input snapshot, output table version and checkpoint if streaming, introduce one realistic dependency or validation failure and use explain plan, Spark UI exchanges, task skew and spill metrics to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for PySpark.

Document PySpark module/notebook, explicit input schema and transformation tests, the DataFrame types, business-key uniqueness and event-time semantics, required execution identity and governed source/target table permissions, owner, normal/failure signals and recovery instructions using source sequence, input snapshot, output table version and checkpoint if streaming. Include one normal and one failure example plus actual service targets and retention assumptions. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does PySpark fit in an end-to-end Azure data platform?

Use this specific flow: Explicit-schema input -> DataFrame transformations -> validation and ordered deduplication -> Delta/Parquet output -> reconciliation. Explain what this component owns, how Spark runtime, source format and Delta/Parquet sink connects, and what the accepted consumer/result boundary is. DataFrames expose schema and relational operations to Spark's optimizer. Lower-level RDD logic gives more manual control but can obscure query optimization opportunities.

Express a keyed decimal aggregation through native DataFrame operations before considering custom partition code. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using PySpark for all six domain transformations and telecom streaming enrichment?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one distributed DataFrame transformation meets them, compare a credible alternative and validate using explain plan, Spark UI exchanges, task skew and spill metrics rather than choosing a tool merely because it is on the stack. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround PySpark in a financial or telecom project?

Tie DataFrame types, business-key uniqueness and event-time semantics to accountable business ownership, verify execution identity and governed source/target table permissions, preserve source sequence, input snapshot, output table version and checkpoint if streaming and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your PySpark optimization helped?

Record the old/new configuration and comparable workload, measure shuffle, serialization, skewed partitions and driver materialization with explain plan, Spark UI exchanges, task skew and spill metrics, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. Plans explain engine choices; task metrics explain actual workload. Validate results after changing join strategy, partitioning or expression logic.

Compare output keys/totals and task skew after replacing a Python UDF with a native expression. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a PySpark interview project?

Identify which PySpark module/notebook, explicit input schema and transformation tests you personally built/reviewed/operated, one specific failure you resolved, the evidence in source sequence, input snapshot, output table version and checkpoint if streaming and a verified outcome. State team-owned components separately and do not invent scale or savings. Explicit types make malformed input visible and protect financial/time semantics. Define corrupt-record and schema-evolution behavior separately from parsing convenience.

Read amounts as decimals and timestamps under a documented timezone instead of accepting inferred strings/floats. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain PySpark's specific responsibility in the flow before naming surrounding tools.
- Use the real DataFrame types, business-key uniqueness and event-time semantics; an accepted request/job does not establish a correct business result.
- Validate execution identity and governed source/target table permissions under the actual execution identity, rather than your administrator account.
- Preserve source sequence, input snapshot, output table version and checkpoint if streaming and inspect it before retrying uncertain side effects.
- Tune shuffle, serialization, skewed partitions and driver materialization from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Write deterministic latest-per-key logic.**

```python
from pyspark.sql import functions as F, Window
keys = ["source_system", "transaction_id", "line_id"]
payload = F.struct("amount", "currency_code", "modified_at")
conflicts = (df.groupBy(*(keys + ["source_sequence"]))
             .agg(F.countDistinct(payload).alias("versions"))
             .where("versions > 1"))
if conflicts.limit(1).count():
    raise ValueError("Conflicting payloads at the same source sequence")
# Validate null keys/sequence and the full relevant payload before this step.
w = Window.partitionBy(*keys).orderBy(F.col("source_sequence").desc())
latest = (df.dropDuplicates(keys + ["source_sequence"])
          .withColumn("rn", F.row_number().over(w))
          .where("rn = 1").drop("rn"))
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [PySpark official documentation](https://spark.apache.org/docs/latest/api/python/index.html).

[Back to all 20 interview guides](README.md).
