# Apache Kafka — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Partitioned event logs, producers, consumer groups, offsets and streaming reliability.

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
Producer -> topic partition and replicated log -> consumer group -> accepted processing -> transactional or idempotent sink
```

For this guide, the primary unit is **one topic partition consumption batch**. The engineering artifacts are producer/consumer configuration, schema contract and processing code. Troubleshooting starts with consumer-group lag, rebalance events, broker/client errors and sink latency; durable progress/evidence is represented by committed offsets, producer sequence, transaction boundary and target idempotency keys. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. What is a Kafka topic?

A named logical stream divided into partitions. Retention/replay and consumer progress are separate concerns. A topic's retention determines available history, while each application controls its own progress. Reading an event does not remove it for other groups.

Two independent reporting applications consume the same payment topic with separate group offsets. Keep each application's accepted progress separate from topic retention, and do not confuse reading an event with deleting it for other consumers.

### C02. What ordering does Kafka provide?

Record order within a partition. Global ordering across partitions requires a separate design and can constrain scale. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate key routing and application processing order as well as broker partition order, especially when reference and usage events arrive out of business time.

### C03. What does a consumer group do?

Distributes partition ownership across group members for an application. Separate groups read independently. Group members share partition ownership under coordinated consumption. Too many members can be idle when partition parallelism is exhausted.

Adding consumers beyond available assigned partitions does not necessarily improve throughput. Measure assigned partitions and hot-key workload before scaling, because extra group members may have no useful parallel work to perform.

### C04. What are committed offsets?

Recorded next-progress positions for group consumption. Commit timing relative to processing determines replay or loss risks. Commit positions and accepted business writes must have a failure policy. Advancing early risks loss; advancing afterward permits replay unless the sink is safe.

A database write followed by a crash before offset commit requires a replay-safe unique event key. Test crashes before and after sink acceptance/commit, and use stable keys or a supported coordinated design for records that replay.

### C05. What do producer acknowledgments affect?

They influence durability/latency tradeoffs with broker replication settings. Explain the full failure model rather than treating one setting as a universal guarantee. Acknowledgment configuration works with replication and failure assumptions. Define the durability target and test the relevant outage cases.

A low-latency producer configuration may have a different accepted loss risk from a finance event pipeline. Describe replication and failure assumptions with acknowledgment settings, rather than claiming one producer option alone guarantees no loss under every outage.

### C06. What is the ISR concept?

In-sync replicas describe replicas sufficiently caught up under broker rules. Replication and minimum ISR settings participate in write availability/durability tradeoffs. Replica health affects durability and availability choices. Broker-side replication policy must be considered alongside producer acknowledgments.

A replication failure can change whether new writes are accepted under the configured policy. Assess write availability and accepted durability together when replicas fall behind, and validate the configured broker/producer behavior under that failure.

### C07. What does producer idempotence address?

Supported producer retry duplication within Kafka's documented semantics. It does not automatically deduplicate every business event or external sink side effect. Retry protection at the producer boundary does not identify every duplicated business event. Independent producers can still send equivalent operations with different transport identities.

Keep a business event ID that the database/lake can use even if producer sessions change. Keep a stable domain event identifier at the sink, because producer retry protection does not deduplicate equivalent business events sent by different producers/sessions.

### C08. What is log compaction?

Retention of latest values by key under compaction semantics, with tombstone behavior. It is not instant uniqueness enforcement or complete event history. Compaction maintains keyed-state retention semantics asynchronously. It should not replace immutable audit history when all transitions are required.

Use a compacted account-state topic plus a separately retained transaction/audit history where justified. Use retained raw/audit history when every transition matters, and do not treat asynchronous compaction as an immediate uniqueness constraint.

### C09. What is a rebalance?

A reassignment of partition ownership in a consumer group. Consumers must manage in-flight work and offset handling safely. Partition reassignment creates uncertainty for in-flight work. Stop/coordinate work and commit only accepted boundaries under the client's supported lifecycle.

A revoked partition must not continue uncontrolled external writes after another worker starts processing it. Handle in-flight operations when ownership changes, and prevent revoked workers from continuing conflicting side effects after another worker takes the partition.

### C10. How do schemas affect event compatibility?

Define versioned producer/consumer contracts and compatibility rules. Broker byte transport does not establish that a field change is safe. Contract compatibility belongs to producers and consumers, not merely the broker. Required fields, key semantics and correction versions need explicit rules.

A new optional payload field differs from changing the payment ID format used for deduplication. Version key/meaning changes explicitly and validate dependent consumers, rather than approving every new payload that the broker can transport.

## B. Advanced implementation questions

### A01. What does exactly-once mean in Kafka processing?

Supported transactions can coordinate Kafka records/offsets under specified conditions. Arbitrary external databases/APIs still require an explicit transactional/idempotent integration design. Kafka transactions cover their documented participating operations. External APIs/databases require a separate coordination/idempotency design.

An HTTP charge request does not become transactional simply because the input Kafka offset is transactional. For external effects, require the target's idempotency/status contract or an explicit durable coordination pattern beyond Kafka's participating transaction scope.

### A02. How do you avoid offset loss?

Process safely, then commit an appropriate accepted boundary; preserve replay-safe targets and handle partial-batch/rebalance cases. Commit the accepted progress boundary, not whatever was most recently fetched. Partial batches and rebalance can make those positions differ.

If only five of ten fetched records are accepted, do not record progress as though all ten completed. Commit only the accepted processed boundary, including partial-batch cases, and retain enough outcome state to resolve uncertain completion.

### A03. How do you troubleshoot lag?

Compare per-partition input rate, consumer work, rebalance frequency and sink latency; distinguish hot keys from general undercapacity. Lag is a symptom with several causes. Distinguish producer spikes, hot keys, slow transformations, external delays and frequent rebalances.

Low consumer CPU alongside high lag often directs attention to a slow API or sink. Inspect sink latency, rebalances and source/key distribution in addition to CPU, since a waiting consumer can be behind while appearing underutilized.

### A04. How do you plan partition increases?

Evaluate routing/key ordering impacts, producer mapping and downstream assumptions. Existing and future records may not map identically under a changed partition count. Partition changes can alter key routing and complicate state/order assumptions. Plan producer rollout and downstream processing around the new mapping.

A customer's old and new records may need reconciliation if they span routing generations. Plan old/new routing and state reconciliation during partition-count changes, especially when per-key history or ordering spans the transition.

### A05. How does Event Hubs compare?

It provides a managed Kafka-compatible endpoint with documented service support. Native broker operations/features and limits cannot be assumed identical. Managed Kafka-compatible endpoints and administered Kafka clusters have different supported control surfaces. Explain actual deployment rather than assuming the label determines capabilities.

Event Hubs does not let the application administer a native Kafka broker fleet merely through its protocol endpoint. Name the actual deployment and supported control surface, and validate the managed endpoint's behavior instead of assuming native broker administration or feature parity.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. You commit offsets before writing the database and then crash. What happens?

The consumer may resume after unpersisted records, causing loss. Coordinate the accepted write boundary and offset or use durable replay-safe processing. Commit positions and accepted business writes must have a failure policy. Advancing early risks loss; advancing afterward permits replay unless the sink is safe.

A database write followed by a crash before offset commit requires a replay-safe unique event key. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. You commit after database writes and then crash before commit. What happens?

Records can replay. Make database writes idempotent with stable keys or use an explicit supported coordinated design. Commit positions and accepted business writes must have a failure policy. Advancing early risks loss; advancing afterward permits replay unless the sink is safe.

A database write followed by a crash before offset commit requires a replay-safe unique event key. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. A rebalance duplicates external API calls. What prevents that?

Handle partition revocation/in-flight work and use external request idempotency keys; broker offset coordination alone cannot undo an API call. Partition reassignment creates uncertainty for in-flight work. Stop/coordinate work and commit only accepted boundaries under the client's supported lifecycle.

A revoked partition must not continue uncontrolled external writes after another worker starts processing it. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. One customer key dominates a partition. How would you redesign?

Measure key skew and ordering needs; consider a revised routing/business aggregation design while preserving required per-entity sequencing. Group members share partition ownership under coordinated consumption. Too many members can be idle when partition parallelism is exhausted.

Adding consumers beyond available assigned partitions does not necessarily improve throughput. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. A partition increase changes key routing. What risk follows?

Per-key history may span old/new partitions, complicating ordering and state. Plan the migration and downstream state handling explicitly. Partition changes can alter key routing and complicate state/order assumptions. Plan producer rollout and downstream processing around the new mapping.

A customer's old and new records may need reconciliation if they span routing generations. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. Compaction removes data needed for audits. What should change?

Separate compacted current-state topics from retained audit/raw history and align retention with approved evidence needs. Compaction maintains keyed-state retention semantics asynchronously. It should not replace immutable audit history when all transitions are required.

Use a compacted account-state topic plus a separately retained transaction/audit history where justified. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. A poison payload stops a consumer group. What is your approach?

Capture restricted error evidence, route to an approved exception path and advance only under a defined completeness policy. Contract compatibility belongs to producers and consumers, not merely the broker. Required fields, key semantics and correction versions need explicit rules.

A new optional payload field differs from changing the payment ID format used for deduplication. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A producer times out despite broker acceptance. How do you handle duplicates?

Use supported idempotent producer configuration and stable business event IDs; validate downstream replay handling. Retry protection at the producer boundary does not identify every duplicated business event. Independent producers can still send equivalent operations with different transport identities.

Keep a business event ID that the database/lake can use even if producer sessions change. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. Consumer lag grows while CPU is low. What do you inspect?

Inspect slow sink/API calls, throttling, fetch behavior and partition ownership before adding CPU. Lag is a symptom with several causes. Distinguish producer spikes, hot keys, slow transformations, external delays and frequent rebalances.

Low consumer CPU alongside high lag often directs attention to a slow API or sink. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. A team claims Kafka transactions make a REST side effect exactly once. How do you respond?

Kafka transactions do not automatically include an external REST operation. Require the API's idempotency/status contract or a durable outbox/workflow design. Kafka transactions cover their documented participating operations. External APIs/databases require a separate coordination/idempotency design.

An HTTP charge request does not become transactional simply because the input Kafka offset is transactional. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one topic partition consumption batch to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

Capture the effective caller and exact error, then validate client authentication, topic/group authorization and broker network route. Compare production with the working configuration using consumer-group lag, rebalance events, broker/client errors and sink latency; do not resolve the incident by giving every identity broad access. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order. Investigate under the real caller rather than the interactive administrator. The relevant path is client authentication, topic/group authorization and broker network route. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Apache Kafka is available, but the business result has not advanced. What would you check?

Trace the expected operation through Kafka producer/broker/consumer and downstream database or lake and compare progress in committed offsets, producer sequence, transaction boundary and target idempotency keys. Inspect consumer-group lag, rebalance events, broker/client errors and sink latency to distinguish a service being reachable from an accepted business operation actually completing. Retry protection at the producer boundary does not identify every duplicated business event. Independent producers can still send equivalent operations with different transport identities. Walk the dependency chain through Kafka producer/broker/consumer and downstream database or lake and locate the last accepted evidence in committed offsets, producer sequence, transaction boundary and target idempotency keys. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

Keep a business event ID that the database/lake can use even if producer sessions change. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of producer/consumer configuration, schema contract and processing code works in test but breaks a dependent production consumer. How do you diagnose it?

Compare versions, environment settings and the actual topic schema, partition routing, retention and business ordering. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order. Treat the release as a change to producer/consumer configuration, schema contract and processing code and its dependencies, not just to one code file. Compare topic schema, partition routing, retention and business ordering and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one topic partition consumption batch although the request or data volume is unchanged. What is your investigation sequence?

Compare a known-good baseline with consumer-group lag, rebalance events, broker/client errors and sink latency and inspect hot partitions, consumer processing rate, rebalance churn and external sink delays. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order. Use consumer-group lag, rebalance events, broker/client errors and sink latency to compare the same business boundary and concurrency against a known-good baseline. Examine hot partitions, consumer processing rate, rebalance churn and external sink delays and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Apache Kafka may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

Inspect the durable outcome in committed offsets, producer sequence, transaction boundary and target idempotency keys before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk. Acknowledgment configuration works with replication and failure assumptions. Define the durability target and test the relevant outage cases. Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by committed offsets, producer sequence, transaction boundary and target idempotency keys and repeat only through a supported safe operation/status mechanism.

A low-latency producer configuration may have a different accepted loss risk from a finance event pipeline. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one topic partition consumption batch at the same time. How do you prevent lost or inconsistent state?

Identify the shared resource and ownership boundary in committed offsets, producer sequence, transaction boundary and target idempotency keys. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last. Partition changes can alter key routing and complicate state/order assumptions. Plan producer rollout and downstream processing around the new mapping. Define who owns the shared mutation and which state version each caller expected. Preserve committed offsets, producer sequence, transaction boundary and target idempotency keys so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

A customer's old and new records may need reconciliation if they span routing generations. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Apache Kafka without prior notice. How do you contain the impact?

Validate against topic schema, partition routing, retention and business ordering and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order. Classify the change against topic schema, partition routing, retention and business ordering: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some committed offsets, producer sequence, transaction boundary and target idempotency keys evidence has expired. What can you recover and what should change?

Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of committed offsets, producer sequence, transaction boundary and target idempotency keys and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts. Compaction maintains keyed-state retention semantics asynchronously. It should not replace immutable audit history when all transitions are required. Recovery can reconstruct only what still exists and is consistent. Inventory committed offsets, producer sequence, transaction boundary and target idempotency keys, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

Use a compacted account-state topic plus a separately retained transaction/audit history where justified. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in consumer-group lag, rebalance events, broker/client errors and sink latency. How would you fix the logging and access design?

Minimize/redact payload values and use restricted references/correlation IDs. Review client authentication, topic/group authorization and broker network route for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields. Contract compatibility belongs to producers and consumers, not merely the broker. Required fields, key semantics and correction versions need explicit rules. Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read consumer-group lag, rebalance events, broker/client errors and sink latency and derived exports; minimizing the source log alone does not remove already copied sensitive output.

A new optional payload field differs from changing the payment ID format used for deduplication. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Apache Kafka accidentally points to production while rehearsing in development. What controls would you add?

Validate environment/resource identifiers in producer/consumer configuration, schema contract and processing code, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against committed offsets, producer sequence, transaction boundary and target idempotency keys before restoring normal processing. A topic's retention determines available history, while each application controls its own progress. Reading an event does not remove it for other groups. Environment validation belongs before mutation. Bind producer/consumer configuration, schema contract and processing code to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

Two independent reporting applications consume the same payment topic with separate group offsets. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Kafka producer/broker/consumer and downstream database or lake is temporarily unavailable. What retry and recovery policy fits Apache Kafka?

Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved committed offsets, producer sequence, transaction boundary and target idempotency keys; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results. Retry protection at the producer boundary does not identify every duplicated business event. Independent producers can still send equivalent operations with different transport identities. Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep committed offsets, producer sequence, transaction boundary and target idempotency keys durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

Keep a business event ID that the database/lake can use even if producer sessions change. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Apache Kafka rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect hot partitions, consumer processing rate, rebalance churn and external sink delays. Remove demonstrated waste while preserving required committed offsets, producer sequence, transaction boundary and target idempotency keys and correctness/access controls. Lag is a symptom with several causes. Distinguish producer spikes, hot keys, slow transformations, external delays and frequent rebalances. Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to hot partitions, consumer processing rate, rebalance churn and external sink delays and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

Low consumer CPU alongside high lag often directs attention to a slow API or sink. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, producer/consumer configuration, schema contract and processing code is restored but the business path still fails. What else is required?

Restore/validate client authentication, topic/group authorization and broker network route, Kafka producer/broker/consumer and downstream database or lake and the appropriate committed offsets, producer sequence, transaction boundary and target idempotency keys. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered. Retry protection at the producer boundary does not identify every duplicated business event. Independent producers can still send equivalent operations with different transport identities. Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate client authentication, topic/group authorization and broker network route, reconcile committed offsets, producer sequence, transaction boundary and target idempotency keys and execute a normal authorized consumer path before calling the recovery successful.

Keep a business event ID that the database/lake can use even if producer sessions change. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Apache Kafka. How do you isolate it without silently accepting incomplete results?

Correlate failing business keys/objects with consumer-group lag, rebalance events, broker/client errors and sink latency and validate their topic schema, partition routing, retention and business ordering. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order. Find the smallest complete failed business scope using keys/objects and consumer-group lag, rebalance events, broker/client errors and sink latency. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow topic schema, partition routing, retention and business ordering and preserve a clear accounting of accepted versus failed scope.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change producer/consumer configuration, schema contract and processing code while dependent workloads remain active. What release sequence would you use?

Inventory consumers and topic schema, partition routing, retention and business ordering compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain committed offsets, producer sequence, transaction boundary and target idempotency keys and define a tested rollback/correction route for incompatible behavior. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order. Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep committed offsets, producer sequence, transaction boundary and target idempotency keys and a tested correction/rollback boundary so a partially applied release remains recoverable.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Validate the accepted result and the intended topic schema, partition routing, retention and business ordering. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises have two-paragraph answers describing the implementation and expected evidence. Selected code or flow references are collected later in this same file. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Draw an offset commit failure timeline.

Show crashes before write, after write and after commit; explain lost/replayed records and target idempotency. Commit positions and accepted business writes must have a failure policy. Advancing early risks loss; advancing afterward permits replay unless the sink is safe.

A database write followed by a crash before offset commit requires a replay-safe unique event key. The corresponding code or flow reference is included in the implementation-reference section of this same file.

### P02. Design a keyed event contract.

Specify stable event ID, partition/business key, source sequence, schema version, correction rules and retention. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Create a consumer recovery rehearsal.

Simulate rebalance and replay, then verify accepted database/output keys and compare consumer offset boundaries. Commit positions and accepted business writes must have a failure policy. Advancing early risks loss; advancing afterward permits replay unless the sink is safe.

A database write followed by a crash before offset commit requires a replay-safe unique event key. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one topic partition consumption batch.

Capture the initial committed offsets, producer sequence, transaction boundary and target idempotency keys, introduce one realistic dependency or validation failure and use consumer-group lag, rebalance events, broker/client errors and sink latency to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access. Acknowledgment configuration works with replication and failure assumptions. Define the durability target and test the relevant outage cases.

A low-latency producer configuration may have a different accepted loss risk from a finance event pipeline. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Apache Kafka.

Document producer/consumer configuration, schema contract and processing code, the topic schema, partition routing, retention and business ordering, required client authentication, topic/group authorization and broker network route, owner, normal/failure signals and recovery instructions using committed offsets, producer sequence, transaction boundary and target idempotency keys. Include one normal and one failure example plus actual service targets and retention assumptions. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Apache Kafka fit in an end-to-end Azure data platform?

Use this specific flow: Producer -> topic partition and replicated log -> consumer group -> accepted processing -> transactional or idempotent sink. Explain what this component owns, how Kafka producer/broker/consumer and downstream database or lake connects, and what the accepted consumer/result boundary is. Retry protection at the producer boundary does not identify every duplicated business event. Independent producers can still send equivalent operations with different transport identities.

Keep a business event ID that the database/lake can use even if producer sessions change. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D02. How would you justify using Apache Kafka for streaming concepts for telecom and enterprise datahub integrations?

Start with actual volume, freshness, correctness, access and support requirements. Explain how one topic partition consumption batch meets them, compare a credible alternative and validate using consumer-group lag, rebalance events, broker/client errors and sink latency rather than choosing a tool merely because it is on the stack. Managed Kafka-compatible endpoints and administered Kafka clusters have different supported control surfaces. Explain actual deployment rather than assuming the label determines capabilities.

Event Hubs does not let the application administer a native Kafka broker fleet merely through its protocol endpoint. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D03. What controls must surround Apache Kafka in a financial or telecom project?

Tie topic schema, partition routing, retention and business ordering to accountable business ownership, verify client authentication, topic/group authorization and broker network route, preserve committed offsets, producer sequence, transaction boundary and target idempotency keys and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed. A topic's retention determines available history, while each application controls its own progress. Reading an event does not remove it for other groups.

Two independent reporting applications consume the same payment topic with separate group offsets. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D04. Which measures would prove your Apache Kafka optimization helped?

Record the old/new configuration and comparable workload, measure hot partitions, consumer processing rate, rebalance churn and external sink delays with consumer-group lag, rebalance events, broker/client errors and sink latency, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement. Within-partition ordering is only useful when routing and consumer processing preserve the required business relationship. Parallel partitions do not yield global order.

A keyed subscriber stream needs a plan for plan/usage events whose business times differ from arrival. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

### D05. How would you explain your own contribution to a Apache Kafka interview project?

Identify which producer/consumer configuration, schema contract and processing code you personally built/reviewed/operated, one specific failure you resolved, the evidence in committed offsets, producer sequence, transaction boundary and target idempotency keys and a verified outcome. State team-owned components separately and do not invent scale or savings. Acknowledgment configuration works with replication and failure assumptions. Define the durability target and test the relevant outage cases.

A low-latency producer configuration may have a different accepted loss risk from a finance event pipeline. Relate this example to the actual source boundary, required access and accepted consumer result. Explain which component you personally implemented, why the design suited the workload, and what measurable evidence establishes its correctness or improvement. Distinguish confirmed experience from a proposed reference architecture when discussing a named client.

## Revision notes and common mistakes

- Explain Apache Kafka's specific responsibility in the flow before naming surrounding tools.
- Use the real topic schema, partition routing, retention and business ordering; an accepted request/job does not establish a correct business result.
- Validate client authentication, topic/group authorization and broker network route under the actual execution identity, rather than your administrator account.
- Preserve committed offsets, producer sequence, transaction boundary and target idempotency keys and inspect it before retrying uncertain side effects.
- Tune hot partitions, consumer processing rate, rebalance churn and external sink delays from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Implementation references for the practical questions

These code and flow examples support the two-paragraph answers above. They are illustrative, require the stated engine/configuration and have not provisioned or executed cloud resources.

**Reference for P01 — Draw an offset commit failure timeline.**

```text
Fetch records -> process -> durable sink write -> commit accepted offsets
Crash before sink write: replay; no accepted output yet.
Crash after sink write but before commit: replay; sink must be idempotent.
Commit before sink write, then crash: unpersisted data can be skipped.
Kafka transaction: covers only documented participating operations.
External API/database: requires its own explicit safe integration contract.
```

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Apache Kafka official documentation](https://kafka.apache.org/documentation/).
- [Kafka 4.1 delivery and transaction design](https://kafka.apache.org/41/design/design/).

[Back to all 20 interview guides](README.md).
