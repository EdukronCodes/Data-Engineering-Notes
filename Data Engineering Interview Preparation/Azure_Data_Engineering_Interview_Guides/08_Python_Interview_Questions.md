# Python — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Reliable ingestion scripts, API/file processing, validation and engineering automation.

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
Configuration -> authenticated source reader -> bounded processing -> validated durable output -> logs and status
```

For this guide, the primary unit is **one ingestion or automation script execution**. The engineering artifacts are Python package, dependency lock and validated configuration. Troubleshooting starts with structured logs, traceback, request timing, memory and accepted record counts; durable progress/evidence is represented by API cursor, run manifest, stable idempotency key and durable output path. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. When is Python appropriate versus PySpark?

**Model answer:** Use local Python for bounded scripting, API integration and automation; use distributed processing when data volume/work requires it. Python code does not become distributed merely by running in a notebook.

### C02. How do lists, tuples, sets and dictionaries differ?

**Model answer:** Lists are ordered mutable sequences, tuples ordered immutable sequences, sets unique-value collections and dictionaries key-value mappings. Choose based on required semantics.

### C03. What are generators?

**Model answer:** Lazy iterators that produce values on demand. They help bounded-memory processing when downstream code does not materialize everything.

### C04. What is a context manager?

**Model answer:** A structured resource lifecycle, commonly with with, that ensures cleanup for files/connections even on exceptions.

### C05. How should exceptions be handled?

**Model answer:** Catch specific expected failures, preserve useful context, clean up resources and surface unrecoverable errors. Broad silent catches can publish incomplete data.

### C06. Why use Decimal for financial scripting?

**Model answer:** Decimal supports decimal arithmetic with explicit context/rounding. Construct from decimal text rather than an already-rounded binary float.

### C07. How do modules and packages help?

**Model answer:** They organize reusable code and dependency boundaries. Avoid production scripts that rely on undocumented interactive notebook state.

### C08. What does type hinting provide?

**Model answer:** Readable contracts and support for static tooling. It does not automatically validate every runtime value or source payload.

### C09. What makes a script idempotent?

**Model answer:** Repeating the same business input produces the same intended state without extra side effects. Use stable keys/manifests and atomic supported target operations.

### C10. How should configuration and secrets be handled?

**Model answer:** Separate validated configuration from code, use approved identity/secret providers and redact logs. Never check secret values into source control.

## B. Advanced implementation questions

### A01. How do you process large files safely?

**Model answer:** Stream records/chunks, bound memory and preserve schema/error policy. Do not read an entire lake-scale dataset into local memory.

### A02. How do you implement HTTP retries?

**Model answer:** Retry appropriate transient errors with bounded exponential backoff/jitter, timeouts and rate-limit handling. Make repeated requests safe or use idempotency keys.

### A03. Threads, processes or asyncio?

**Model answer:** Choose from I/O versus CPU work, library behavior, runtime characteristics and serialization cost. Do not assume a fixed GIL behavior across all Python builds.

### A04. How do you test an ingestion script?

**Model answer:** Use fixtures for pagination, nulls, malformed records, decimal/time boundaries and partial failures. Mock external boundaries while testing actual parsing/business logic.

### A05. How do you make deployments reproducible?

**Model answer:** Pin supported dependencies, use an isolated environment, build the same package artifact and validate runtime/OS compatibility.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. A script runs out of memory reading a CSV. What changes?

**Model answer:** Use chunked/streaming parsing and bounded output or move to a distributed engine when needed. Measure peak memory and test malformed records.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. An API returns 429. How do you respond?

**Model answer:** Honor supported rate-limit/retry guidance, bound concurrency and retry with backoff; record the cursor so progress is resumable.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. An HTTP timeout occurs after a POST may have succeeded. Is retry safe?

**Model answer:** Check the API's idempotency contract and use a stable request key/status lookup. Blind retries can duplicate side effects.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. A decimal total differs from the ledger by cents. What do you inspect?

**Model answer:** Check float conversion, Decimal construction, precision and rounding order; use approved decimal fixtures and reconciliation.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. A timezone-naive datetime shifts a business date. How do you prevent it?

**Model answer:** Parse the source timezone explicitly, use timezone-aware values and define business-date conversion, including daylight-saving cases.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. A broad except logs success after rejecting half the rows. What is wrong?

**Model answer:** Failure status and rejection thresholds are missing. Catch expected errors, retain exception evidence and block publication when the contract fails.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. A package works locally but fails on the job host. What do you compare?

**Model answer:** Compare Python build, dependency lock, compiled libraries, OS, environment variables and workload permissions.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. Concurrent workers write the same output file. How do you fix it?

**Model answer:** Use isolated temporary/run paths and a controlled publication step; serialize conflicting writes and verify durable output manifests.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. Logs include bearer tokens from request headers. What should change?

**Model answer:** Redact sensitive headers/payload fields centrally, restrict logs and rotate exposed credentials through the approved incident process.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. An API cursor changes during the extraction. How do you keep a consistent result?

**Model answer:** Use source snapshot/version support if available, stable keys and defined overlap/reconciliation; document limits when the API cannot offer consistency.

**Verification:** Use relevant structured logs, traceback, request timing, memory and accepted record counts and confirm the intended payload schema, parsing types, decimal/time rules and API behavior. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one ingestion or automation script execution to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate SDK credential chain, workload identity and source/target permissions. Compare production with the working configuration using structured logs, traceback, request timing, memory and accepted record counts; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Python is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through source API/file library and target SDK/database driver and compare progress in API cursor, run manifest, stable idempotency key and durable output path. Inspect structured logs, traceback, request timing, memory and accepted record counts to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of Python package, dependency lock and validated configuration works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual payload schema, parsing types, decimal/time rules and API behavior. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one ingestion or automation script execution although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with structured logs, traceback, request timing, memory and accepted record counts and inspect I/O latency, local memory, concurrency limits and CPU parsing. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Python may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in API cursor, run manifest, stable idempotency key and durable output path before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one ingestion or automation script execution at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in API cursor, run manifest, stable idempotency key and durable output path. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Python without prior notice. How do you contain the impact?

**Model answer:** Validate against payload schema, parsing types, decimal/time rules and API behavior and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some API cursor, run manifest, stable idempotency key and durable output path evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of API cursor, run manifest, stable idempotency key and durable output path and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in structured logs, traceback, request timing, memory and accepted record counts. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review SDK credential chain, workload identity and source/target permissions for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Python accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in Python package, dependency lock and validated configuration, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against API cursor, run manifest, stable idempotency key and durable output path before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Source api/file library and target sdk/database driver is temporarily unavailable. What retry and recovery policy fits Python?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved API cursor, run manifest, stable idempotency key and durable output path; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Python rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect I/O latency, local memory, concurrency limits and CPU parsing. Remove demonstrated waste while preserving required API cursor, run manifest, stable idempotency key and durable output path and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, Python package, dependency lock and validated configuration is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate SDK credential chain, workload identity and source/target permissions, source API/file library and target SDK/database driver and the appropriate API cursor, run manifest, stable idempotency key and durable output path. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Python. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with structured logs, traceback, request timing, memory and accepted record counts and validate their payload schema, parsing types, decimal/time rules and API behavior. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change Python package, dependency lock and validated configuration while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and payload schema, parsing types, decimal/time rules and API behavior compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain API cursor, run manifest, stable idempotency key and durable output path and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Build a paginated REST extraction function.

**Model answer:** Include timeouts, bounded retries, rate-limit handling, stable output keys, cursor persistence and redacted logs.

### P02. Write a streaming CSV validator.

**Model answer:** Parse explicit types, use Decimal/timezone-aware values and retain bad-record counts/reasons without excessive memory.

### P03. Implement a run manifest and replay test.

**Model answer:** Record input boundaries and output hashes/counts, simulate partial failure, and prove a second attempt creates no duplicate result.

### P04. Create a failing-and-recovered test for one ingestion or automation script execution.

**Model answer:** Capture the initial API cursor, run manifest, stable idempotency key and durable output path, introduce one realistic dependency or validation failure and use structured logs, traceback, request timing, memory and accepted record counts to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Python.

**Model answer:** Document Python package, dependency lock and validated configuration, the payload schema, parsing types, decimal/time rules and API behavior, required SDK credential chain, workload identity and source/target permissions, owner, normal/failure signals and recovery instructions using API cursor, run manifest, stable idempotency key and durable output path. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Python fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Configuration -> authenticated source reader -> bounded processing -> validated durable output -> logs and status. Explain what this component owns, how source API/file library and target SDK/database driver connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Python for API integration, validation and deployment automation for the six designs?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one ingestion or automation script execution meets them, compare a credible alternative and validate using structured logs, traceback, request timing, memory and accepted record counts rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Python in a financial or telecom project?

**Model answer:** Tie payload schema, parsing types, decimal/time rules and API behavior to accountable business ownership, verify SDK credential chain, workload identity and source/target permissions, preserve API cursor, run manifest, stable idempotency key and durable output path and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Python optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure I/O latency, local memory, concurrency limits and CPU parsing with structured logs, traceback, request timing, memory and accepted record counts, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Python interview project?

**Model answer:** Identify which Python package, dependency lock and validated configuration you personally built/reviewed/operated, one specific failure you resolved, the evidence in API cursor, run manifest, stable idempotency key and durable output path and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

## Official references

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Python official documentation](https://docs.python.org/3/library/index.html).

[Back to all 20 interview guides](README.md).
