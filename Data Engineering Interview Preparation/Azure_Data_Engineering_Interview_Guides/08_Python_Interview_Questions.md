# Python — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Reliable ingestion scripts, API/file processing, validation and engineering automation.

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
Configuration -> authenticated source reader -> bounded processing -> validated durable output -> logs and status
```

For this guide, the primary unit is **one ingestion or automation script execution**. The engineering artifacts are Python package, dependency lock and validated configuration. Troubleshooting starts with structured logs, traceback, request timing, memory and accepted record counts; durable progress/evidence is represented by API cursor, run manifest, stable idempotency key and durable output path. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. When is Python appropriate versus PySpark?

Use local Python for bounded scripting, API integration and automation; use distributed processing when data volume/work requires it. Python code does not become distributed merely by running in a notebook. A bounded scripting process has local resources even in a cloud notebook. Use distributed compute when the input/algorithm exceeds those limits.

Python can paginate reference APIs while Spark handles the large usage join. Measure input size, memory use and the algorithm's intermediate state, since a small-looking script can still materialize an unbounded history or response.

### C02. How do lists, tuples, sets and dictionaries differ?

Lists are ordered mutable sequences, tuples ordered immutable sequences, sets unique-value collections and dictionaries key-value mappings. Choose based on required semantics. Choose data structures from access patterns and semantics. Mutation, membership tests and ordering requirements affect correctness as well as complexity.

Use a dictionary for reviewed entity configuration and a set for allowed reference values. Select structures deliberately for membership, key lookup, iteration and mutation, and validate that changing structures does not alter duplicate/order semantics.

### C03. What are generators?

Lazy iterators that produce values on demand. They help bounded-memory processing when downstream code does not materialize everything. Lazy iteration reduces peak memory only when downstream operations stay bounded. Converting a generator to a list materializes everything again.

Stream parsed CSV rows into bounded output batches rather than accumulating the entire file. Keep downstream batches bounded as well as the generator itself, and persist enough progress to resume after a partial file or API failure.

### C04. What is a context manager?

A structured resource lifecycle, commonly with with, that ensures cleanup for files/connections even on exceptions. Resource cleanup must occur on both success and failure. Context managers simplify this but do not automatically commit a correct business result.

Close the source file and database cursor even when a validation error holds the run. Combine cleanup with explicit commit/failure behavior; closing a resource does not justify publishing a result whose validation failed.

### C05. How should exceptions be handled?

Catch specific expected failures, preserve useful context, clean up resources and surface unrecoverable errors. Broad silent catches can publish incomplete data. Error handling should preserve the failed scope and distinguish retryable transport errors from invalid payloads. A catch-all success response conceals incomplete processing.

Report rejected counts and fail a critical contract instead of silently skipping malformed journal lines. Keep the source key/run context while redacting sensitive payloads, and propagate critical failures so orchestration can hold the affected publication.

### C06. Why use Decimal for financial scripting?

Decimal supports decimal arithmetic with explicit context/rounding. Construct from decimal text rather than an already-rounded binary float. Decimal arithmetic requires an explicit precision/rounding policy and correctly typed inputs. Converting an existing float can preserve its binary approximation.

Parse the string 100.10 directly into Decimal before financial calculations. Set the applicable precision and rounding policy, and test finite values, scale and boundary amounts before comparing source and output financial totals.

### C07. How do modules and packages help?

They organize reusable code and dependency boundaries. Avoid production scripts that rely on undocumented interactive notebook state. Reusable modules separate configuration, parsing, business logic and external I/O. This improves testability and deployment reproducibility.

A parsing function can be tested with a local fixture while the source API client is mocked at its boundary. Keep external I/O behind narrow interfaces, which allows business parsing/transformation tests without pretending a mocked API proves production connectivity.

### C08. What does type hinting provide?

Readable contracts and support for static tooling. It does not automatically validate every runtime value or source payload. Type annotations help developers/tools understand expectations, but runtime payload validation still belongs at external boundaries.

A function annotated with a datetime parameter must still reject an invalid API timestamp. Validate actual types and allowed values at file/API boundaries; annotations document expectations but do not enforce a complete source contract.

### C09. What makes a script idempotent?

Repeating the same business input produces the same intended state without extra side effects. Use stable keys/manifests and atomic supported target operations. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Distinguish a delivery ID from an attempt ID, and inspect the existing accepted outcome when a timeout leaves completion uncertain.

### C10. How should configuration and secrets be handled?

Separate validated configuration from code, use approved identity/secret providers and redact logs. Never check secret values into source control. Secrets are dependencies with rotation/access behavior, not ordinary configuration strings. Avoid logging request headers or serializing credentials into exceptions.

Use an approved workload credential provider and retain only the secret reference, not its value. Validate credentials under the deployed identity and test rotation/refresh, because a locally authenticated developer script can hide production permission gaps.

## B. Advanced implementation questions

### A01. How do you process large files safely?

Stream records/chunks, bound memory and preserve schema/error policy. Do not read an entire lake-scale dataset into local memory. Chunking preserves memory bounds only if intermediate joins/aggregates also remain controlled. Move unsuitable algorithms to a distributed engine.

A large-file parser writes bounded staged output instead of keeping every customer's history in memory. Local chunking does not make a global many-to-many join inexpensive; use a suitable distributed/serving engine where the actual state exceeds local resources.

### A02. How do you implement HTTP retries?

Retry appropriate transient errors with bounded exponential backoff/jitter, timeouts and rate-limit handling. Make repeated requests safe or use idempotency keys. Retry policies should consider method semantics and uncertain outcomes. Timeout after server acceptance can make repeating a mutation unsafe.

Use an API idempotency key for a request whose result may not have reached the client. Bound attempts and elapsed time, distinguish invalid input from transient failures, and preserve a cursor or operation key for safe recovery.

### A03. Threads, processes or asyncio?

Choose from I/O versus CPU work, library behavior, runtime characteristics and serialization cost. Do not assume a fixed GIL behavior across all Python builds. Concurrency helps different workloads differently. Measure dependency limits, CPU work and runtime/library behavior before selecting threads/processes/async I/O.

Parallel API requests can improve I/O throughput but still require a source rate-limit cap. Respect source/target limits even when more concurrency helps the script, and test resource cleanup and partial-result handling under cancellation/failure.

### A04. How do you test an ingestion script?

Use fixtures for pagination, nulls, malformed records, decimal/time boundaries and partial failures. Mock external boundaries while testing actual parsing/business logic. Expected outputs should be independently derived from small fixtures. Include malformed pagination, duplicate keys and precise time/decimal boundaries.

Test an API timeout after page acceptance and prove recovery does not create duplicate rows. Include timezone, decimal, malformed-record and duplicate-page fixtures with independent expected outcomes, then add actual dependency checks in an approved test environment.

### A05. How do you make deployments reproducible?

Pin supported dependencies, use an isolated environment, build the same package artifact and validate runtime/OS compatibility. Reproducibility includes interpreter, packages, compiled dependencies and environment configuration. Pinning source code alone leaves behavior uncontrolled.

Deploy the same tested package/dependency set on the job host and record its runtime identity. Record interpreter and package versions with the deployed artifact and test compiled/runtime dependencies on the target host, not only the developer machine.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A script runs out of memory reading a CSV. What changes?

Use chunked/streaming parsing and bounded output or move to a distributed engine when needed. Measure peak memory and test malformed records. Chunking preserves memory bounds only if intermediate joins/aggregates also remain controlled. Move unsuitable algorithms to a distributed engine.

A large-file parser writes bounded staged output instead of keeping every customer's history in memory. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. An API returns 429. How do you respond?

Honor supported rate-limit/retry guidance, bound concurrency and retry with backoff; record the cursor so progress is resumable. Retry policies should consider method semantics and uncertain outcomes. Timeout after server acceptance can make repeating a mutation unsafe.

Use an API idempotency key for a request whose result may not have reached the client. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. An HTTP timeout occurs after a POST may have succeeded. Is retry safe?

Check the API's idempotency contract and use a stable request key/status lookup. Blind retries can duplicate side effects. Retry policies should consider method semantics and uncertain outcomes. Timeout after server acceptance can make repeating a mutation unsafe.

Use an API idempotency key for a request whose result may not have reached the client. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. A decimal total differs from the ledger by cents. What do you inspect?

Check float conversion, Decimal construction, precision and rounding order; use approved decimal fixtures and reconciliation. Decimal arithmetic requires an explicit precision/rounding policy and correctly typed inputs. Converting an existing float can preserve its binary approximation.

Parse the string 100.10 directly into Decimal before financial calculations. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. A timezone-naive datetime shifts a business date. How do you prevent it?

Parse the source timezone explicitly, use timezone-aware values and define business-date conversion, including daylight-saving cases. Secrets are dependencies with rotation/access behavior, not ordinary configuration strings. Avoid logging request headers or serializing credentials into exceptions.

Use an approved workload credential provider and retain only the secret reference, not its value. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A broad except logs success after rejecting half the rows. What is wrong?

Failure status and rejection thresholds are missing. Catch expected errors, retain exception evidence and block publication when the contract fails. Error handling should preserve the failed scope and distinguish retryable transport errors from invalid payloads. A catch-all success response conceals incomplete processing.

Report rejected counts and fail a critical contract instead of silently skipping malformed journal lines. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. A package works locally but fails on the job host. What do you compare?

Compare Python build, dependency lock, compiled libraries, OS, environment variables and workload permissions. Reproducibility includes interpreter, packages, compiled dependencies and environment configuration. Pinning source code alone leaves behavior uncontrolled.

Deploy the same tested package/dependency set on the job host and record its runtime identity. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. Concurrent workers write the same output file. How do you fix it?

Use isolated temporary/run paths and a controlled publication step; serialize conflicting writes and verify durable output manifests. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. Logs include bearer tokens from request headers. What should change?

Redact sensitive headers/payload fields centrally, restrict logs and rotate exposed credentials through the approved incident process. Secrets are dependencies with rotation/access behavior, not ordinary configuration strings. Avoid logging request headers or serializing credentials into exceptions.

Use an approved workload credential provider and retain only the secret reference, not its value. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. An API cursor changes during the extraction. How do you keep a consistent result?

Use source snapshot/version support if available, stable keys and defined overlap/reconciliation; document limits when the API cannot offer consistency. Retry policies should consider method semantics and uncertain outcomes. Timeout after server acceptance can make repeating a mutation unsafe.

Use an API idempotency key for a request whose result may not have reached the client. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one ingestion or automation script execution to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate SDK credential chain, workload identity and source/target permissions. Compare production with the working configuration using structured logs, traceback, request timing, memory and accepted record counts; do not resolve the incident by giving every identity broad access. Secrets are dependencies with rotation/access behavior, not ordinary configuration strings. Avoid logging request headers or serializing credentials into exceptions. Investigate under the real caller rather than the interactive administrator. The relevant path is SDK credential chain, workload identity and source/target permissions. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

Use an approved workload credential provider and retain only the secret reference, not its value. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Python is available, but the business result has not advanced. What would you check?

Trace the expected operation through source API/file library and target SDK/database driver and compare progress in API cursor, run manifest, stable idempotency key and durable output path. Inspect structured logs, traceback, request timing, memory and accepted record counts to distinguish a service being reachable from an accepted business operation actually completing. Resource cleanup must occur on both success and failure. Context managers simplify this but do not automatically commit a correct business result. Walk the dependency chain through source API/file library and target SDK/database driver and locate the last accepted evidence in API cursor, run manifest, stable idempotency key and durable output path. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

Close the source file and database cursor even when a validation error holds the run. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of Python package, dependency lock and validated configuration works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual payload schema, parsing types, decimal/time rules and API behavior. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Reproducibility includes interpreter, packages, compiled dependencies and environment configuration. Pinning source code alone leaves behavior uncontrolled. Treat the release as a change to Python package, dependency lock and validated configuration and its dependencies, not just to one code file. Compare payload schema, parsing types, decimal/time rules and API behavior and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

Deploy the same tested package/dependency set on the job host and record its runtime identity. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one ingestion or automation script execution although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with structured logs, traceback, request timing, memory and accepted record counts and inspect I/O latency, local memory, concurrency limits and CPU parsing. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Reusable modules separate configuration, parsing, business logic and external I/O. This improves testability and deployment reproducibility. Use structured logs, traceback, request timing, memory and accepted record counts to compare the same business boundary and concurrency against a known-good baseline. Examine I/O latency, local memory, concurrency limits and CPU parsing and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

A parsing function can be tested with a local fixture while the source API client is mocked at its boundary. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Python may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in API cursor, run manifest, stable idempotency key and durable output path before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by API cursor, run manifest, stable idempotency key and durable output path and repeat only through a supported safe operation/status mechanism.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one ingestion or automation script execution at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in API cursor, run manifest, stable idempotency key and durable output path. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable. Define who owns the shared mutation and which state version each caller expected. Preserve API cursor, run manifest, stable idempotency key and durable output path so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Python without prior notice. How do you contain the impact?

Validate against payload schema, parsing types, decimal/time rules and API behavior and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. A bounded scripting process has local resources even in a cloud notebook. Use distributed compute when the input/algorithm exceeds those limits. Classify the change against payload schema, parsing types, decimal/time rules and API behavior: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

Python can paginate reference APIs while Spark handles the large usage join. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some API cursor, run manifest, stable idempotency key and durable output path evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of API cursor, run manifest, stable idempotency key and durable output path and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable. Recovery can reconstruct only what still exists and is consistent. Inventory API cursor, run manifest, stable idempotency key and durable output path, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in structured logs, traceback, request timing, memory and accepted record counts. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review SDK credential chain, workload identity and source/target permissions for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Secrets are dependencies with rotation/access behavior, not ordinary configuration strings. Avoid logging request headers or serializing credentials into exceptions. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read structured logs, traceback, request timing, memory and accepted record counts and derived exports; minimizing the source log alone does not remove already copied sensitive output.

Use an approved workload credential provider and retain only the secret reference, not its value. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Python accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in Python package, dependency lock and validated configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against API cursor, run manifest, stable idempotency key and durable output path before restoring normal processing. Reproducibility includes interpreter, packages, compiled dependencies and environment configuration. Pinning source code alone leaves behavior uncontrolled. Environment validation belongs before mutation. Bind Python package, dependency lock and validated configuration to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

Deploy the same tested package/dependency set on the job host and record its runtime identity. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Source api/file library and target sdk/database driver is temporarily unavailable. What retry and recovery policy fits Python?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved API cursor, run manifest, stable idempotency key and durable output path; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. Resource cleanup must occur on both success and failure. Context managers simplify this but do not automatically commit a correct business result. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep API cursor, run manifest, stable idempotency key and durable output path durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

Close the source file and database cursor even when a validation error holds the run. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Python rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect I/O latency, local memory, concurrency limits and CPU parsing. Remove demonstrated waste while preserving required API cursor, run manifest, stable idempotency key and durable output path and correctness/access controls. A bounded scripting process has local resources even in a cloud notebook. Use distributed compute when the input/algorithm exceeds those limits. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to I/O latency, local memory, concurrency limits and CPU parsing and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

Python can paginate reference APIs while Spark handles the large usage join. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, Python package, dependency lock and validated configuration is restored but the business path still fails. What else is required?

Restore/validate SDK credential chain, workload identity and source/target permissions, source API/file library and target SDK/database driver and the appropriate API cursor, run manifest, stable idempotency key and durable output path. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Resource cleanup must occur on both success and failure. Context managers simplify this but do not automatically commit a correct business result. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate SDK credential chain, workload identity and source/target permissions, reconcile API cursor, run manifest, stable idempotency key and durable output path and execute a normal authorized consumer path before calling the recovery successful.

Close the source file and database cursor even when a validation error holds the run. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Python. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with structured logs, traceback, request timing, memory and accepted record counts and validate their payload schema, parsing types, decimal/time rules and API behavior. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. Error handling should preserve the failed scope and distinguish retryable transport errors from invalid payloads. A catch-all success response conceals incomplete processing. Find the smallest complete failed business scope using keys/objects and structured logs, traceback, request timing, memory and accepted record counts. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow payload schema, parsing types, decimal/time rules and API behavior and preserve a clear accounting of accepted versus failed scope.

Report rejected counts and fail a critical contract instead of silently skipping malformed journal lines. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change Python package, dependency lock and validated configuration while dependent workloads remain active. What release sequence would you use?

Inventory consumers and payload schema, parsing types, decimal/time rules and API behavior compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain API cursor, run manifest, stable idempotency key and durable output path and define a tested rollback/correction route for incompatible behavior. Reproducibility includes interpreter, packages, compiled dependencies and environment configuration. Pinning source code alone leaves behavior uncontrolled. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep API cursor, run manifest, stable idempotency key and durable output path and a tested correction/rollback boundary so a partially applied release remains recoverable.

Deploy the same tested package/dependency set on the job host and record its runtime identity. Validate the accepted result and the intended payload schema, parsing types, decimal/time rules and API behavior. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Build a paginated REST extraction function.

Include timeouts, bounded retries, rate-limit handling, stable output keys, cursor persistence and redacted logs. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P02. Write a streaming CSV validator.

Parse explicit types, use Decimal/timezone-aware values and retain bad-record counts/reasons without excessive memory. Decimal arithmetic requires an explicit precision/rounding policy and correctly typed inputs. Converting an existing float can preserve its binary approximation.

Parse the string 100.10 directly into Decimal before financial calculations. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P03. Implement a run manifest and replay test.

Record input boundaries and output hashes/counts, simulate partial failure, and prove a second attempt creates no duplicate result. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one ingestion or automation script execution.

Capture the initial API cursor, run manifest, stable idempotency key and durable output path, introduce one realistic dependency or validation failure and use structured logs, traceback, request timing, memory and accepted record counts to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Python.

Document Python package, dependency lock and validated configuration, the payload schema, parsing types, decimal/time rules and API behavior, required SDK credential chain, workload identity and source/target permissions, owner, normal/failure signals and recovery instructions using API cursor, run manifest, stable idempotency key and durable output path. Include one normal and one failure example plus actual service targets and retention assumptions. Reproducibility includes interpreter, packages, compiled dependencies and environment configuration. Pinning source code alone leaves behavior uncontrolled.

Deploy the same tested package/dependency set on the job host and record its runtime identity. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Python fit in an end-to-end Azure data platform?

Use this specific flow: Configuration -> authenticated source reader -> bounded processing -> validated durable output -> logs and status. Explain what this component owns, how source API/file library and target SDK/database driver connects, and what the accepted consumer/result boundary is. Resource cleanup must occur on both success and failure. Context managers simplify this but do not automatically commit a correct business result.

Close the source file and database cursor even when a validation error holds the run. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using Python for API integration, validation and deployment automation for the six designs?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one ingestion or automation script execution meets them, compare a credible alternative and validate using structured logs, traceback, request timing, memory and accepted record counts rather than choosing a tool merely because it is on the stack. Choose data structures from access patterns and semantics. Mutation, membership tests and ordering requirements affect correctness as well as complexity.

Use a dictionary for reviewed entity configuration and a set for allowed reference values. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround Python in a financial or telecom project?

Tie payload schema, parsing types, decimal/time rules and API behavior to accountable business ownership, verify SDK credential chain, workload identity and source/target permissions, preserve API cursor, run manifest, stable idempotency key and durable output path and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your Python optimization helped?

Record the old/new configuration and comparable workload, measure I/O latency, local memory, concurrency limits and CPU parsing with structured logs, traceback, request timing, memory and accepted record counts, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. Secrets are dependencies with rotation/access behavior, not ordinary configuration strings. Avoid logging request headers or serializing credentials into exceptions.

Use an approved workload credential provider and retain only the secret reference, not its value. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a Python interview project?

Identify which Python package, dependency lock and validated configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in API cursor, run manifest, stable idempotency key and durable output path and a verified outcome. State team-owned components separately and do not invent scale or savings. Idempotence must be defined at the business operation boundary. Temporary files, stable keys and durable manifests make partial failure recoverable.

A second attempt replaces the same identified output batch instead of appending a duplicate export. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain Python's specific responsibility in the flow before naming surrounding tools.
- Use the real payload schema, parsing types, decimal/time rules and API behavior; an accepted request/job does not establish a correct business result.
- Validate SDK credential chain, workload identity and source/target permissions under the actual execution identity, rather than your administrator account.
- Preserve API cursor, run manifest, stable idempotency key and durable output path and inspect it before retrying uncertain side effects.
- Tune I/O latency, local memory, concurrency limits and CPU parsing from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P02 — Write a streaming CSV validator.**

```python
import csv
from decimal import Decimal, InvalidOperation

def validated_rows(path):
    with open(path, newline="", encoding="utf-8") as stream:
        for line_no, row in enumerate(csv.DictReader(stream), start=2):
            try:
                if not row.get("transaction_id"):
                    raise ValueError("missing transaction key")
                amount = Decimal(row["amount"])
                if not amount.is_finite():
                    raise ValueError("non-finite amount")
                yield {"transaction_id": row["transaction_id"],
                       "amount": amount, "line_no": line_no}
            except (KeyError, ValueError, InvalidOperation) as error:
                # Actual jobs persist restricted exception/count evidence
                # and apply the approved critical-rule publication gate.
                raise ValueError(f"Invalid row at line {line_no}") from error
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Python official documentation](https://docs.python.org/3/library/index.html).

[Back to all 20 interview guides](README.md).
