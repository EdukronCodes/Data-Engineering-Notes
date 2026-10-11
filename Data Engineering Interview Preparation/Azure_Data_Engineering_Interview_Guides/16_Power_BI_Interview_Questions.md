# Power BI — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Business semantic models, measures, dashboards, refresh behavior and governed reporting.

**Audience:** Azure data engineering interviews, from fundamentals through production troubleshooting and design. Each answer explains the concept, its practical use and implementation context. Scenario answers cover the cause, investigation, correction and verification. Check source semantics, engine/runtime, workload identity and acceptance evidence for your actual configuration. Practice scenarios are hypothetical and are not claims about the named client projects.

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

**Answer:** A defined analytical model of data, relationships and measures used by reports. Its grain and calculations must reflect the business contract.

**Explanation:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Practical example:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

### C02. What is a star schema useful for?

**Answer:** Dimensions filter facts with clear relationships and grains. It simplifies analytical reasoning and avoids accidental many-to-many multiplication.

**Explanation:** Dimensions should filter facts under clear cardinality and key integrity. Unexpected many-to-many paths can multiply or alter totals.

**Practical example:** One account version relationship should resolve the intended snapshot/fact rows rather than duplicate journal amounts.

### C03. How do Import and DirectQuery differ?

**Answer:** Import stores model data for query use; DirectQuery sends queries to the source under supported behavior. Freshness, latency and source load differ.

**Explanation:** Storage mode affects source load and latency/freshness. Choose from actual consumers and supported model behavior, not only a preference for live data.

**Practical example:** A frequently filtered finance dashboard can need a different serving plan from an occasional source drill-through.

### C04. Where does Direct Lake fit?

**Answer:** A supported lake-oriented model mode for compatible Fabric scenarios. Validate the actual model/endpoint implementation and query path.

**Explanation:** Lake-oriented access still depends on supported configuration, permissions and query behavior. Check the effective path for the actual endpoint/model.

**Practical example:** A Fabric semantic model is tested against its selected source mode rather than assumed identical to every other model.

### C05. How do measures and calculated columns differ?

**Answer:** Measures evaluate in query/filter context; calculated columns store/evaluate row-derived values under model processing behavior. Choose based on semantics and resource impact.

**Explanation:** Stored row-derived values and query-context measures serve different purposes. Consider semantics, memory and refresh behavior when choosing.

**Practical example:** A current filtered transaction sum is a measure; a stable approved classification may be a source/model attribute.

### C06. What are filter context and row context?

**Answer:** Filter context defines selected rows for evaluation; row context iterates/current-row evaluation. DAX behavior depends on context transitions and relationships.

**Explanation:** Contexts determine which rows contribute to a calculation. Relationships and iteration can change evaluation even when the formula text looks simple.

**Practical example:** A product filter should reach the relevant fact before its revenue measure is summed.

### C07. What is CALCULATE used for?

**Answer:** Evaluating an expression under modified filter context. The specific filter changes must be intentional and tested.

**Explanation:** Filter modification must be intentional. Removing the wrong context can make every product display the same total or bypass a desired analytical selection.

**Practical example:** Compare CALCULATE variants against a tiny known product/date fixture.

### C08. What is row-level security?

**Answer:** Model security rules limiting rows for applicable consumers. Underlying storage/source access and elevated workspace roles require separate review.

**Explanation:** Security behavior depends on actual consumer role/mode and underlying access. Test permitted and denied paths, including exports and direct queries.

**Practical example:** A regional analyst sees permitted rows while a separate data-path test confirms no broad raw access.

### C09. What is incremental refresh for?

**Answer:** Processing defined date ranges/partitions rather than all historical data, subject to supported configuration. Verify filtering/query folding and late-correction policy.

**Explanation:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Practical example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

### C10. Why are dates and relationships important?

**Answer:** Consistent calendars, active relationships and fact dates determine correct time analysis. Multiple date roles need explicit modeling.

**Explanation:** Date roles and calendars affect period filtering. Use explicit business calendars, active/inactive relationships and timezone-derived dates where appropriate.

**Practical example:** Posting date and settlement date can drive different legitimate measures and need clear model choices.

## B. Advanced implementation questions

### A01. How do you model semi-additive balances?

**Answer:** Aggregate across approved entity dimensions but use selected-date/period-end behavior across time. Do not sum all daily snapshots as current balance.

**Explanation:** Snapshots are semi-additive across time. Define latest/period-end behavior under the business calendar rather than adding every daily balance.

**Practical example:** Closing balances 100 and 120 on two days yield 120 for the second date, not 220.

### A02. How do you diagnose slow reports?

**Answer:** Measure expensive visuals/measures and source/model queries, then inspect cardinality, relationships and filter paths. Do not start by adding every column to the model.

**Explanation:** Performance work begins with expensive queries/visuals and model structure. Reducing load must not alter measure definitions or access semantics.

**Practical example:** Optimize a slow page after identifying a costly measure or source query rather than dropping essential controls.

### A03. How do you handle late fact corrections?

**Answer:** Refresh/reprocess affected partitions or use a supported current serving mode, then reconcile the revised accepted product and report measures.

**Explanation:** Source acceptance and model freshness must both be visible. A model refresh can succeed over stale or uncorrected source partitions.

**Practical example:** Display accepted business as-of time and reprocess the actual correction scope.

### A04. How do you validate RLS?

**Answer:** Test actual user/group paths and elevated/direct-data access separately; compare allowed/forbidden rows and exports.

**Explanation:** Testing as a role alone does not cover every real access path. Elevated workspace roles, source access and exports need separate review.

**Practical example:** Validate an actual regional user's permitted/report and denied/direct-data behavior.

### A05. How do you deploy model changes?

**Answer:** Version model/report dependencies, test relationships/measures/security and promote compatible sources/contracts with environment settings.

**Explanation:** Source/model changes form a dependency release. Relationships and DAX can break even if the new source table remains queryable.

**Practical example:** Promote a reviewed compatible schema/model update and verify financial measures with known fixtures.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. Revenue doubles after adding a customer table. What do you inspect?

**Answer:** Check relationship cardinality, duplicated dimension keys, filtering and fact grain; fix the model instead of masking totals.

**Why this happens and what matters:** Dimensions should filter facts under clear cardinality and key integrity. Unexpected many-to-many paths can multiply or alter totals.

**Related practical example:** One account version relationship should resolve the intended snapshot/fact rows rather than duplicate journal amounts.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. A monthly chart adds daily closing balances. What is wrong?

**Answer:** The measure treats snapshot values as fully additive. Implement the approved month-end/selected-date definition.

**Why this happens and what matters:** Snapshots are semi-additive across time. Define latest/period-end behavior under the business calendar rather than adding every daily balance.

**Related practical example:** Closing balances 100 and 120 on two days yield 120 for the second date, not 220.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. RLS works in testing but an admin sees every region. Is that unexpected?

**Answer:** Elevated roles/access can have different effective security behavior. Validate each real consumer role and underlying data path.

**Why this happens and what matters:** Testing as a role alone does not cover every real access path. Elevated workspace roles, source access and exports need separate review.

**Related practical example:** Validate an actual regional user's permitted/report and denied/direct-data behavior.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. Refresh succeeds but the report has yesterday's business data. What should be monitored?

**Answer:** The accepted source/product as-of boundary and freshness target, not just model refresh completion.

**Why this happens and what matters:** Source acceptance and model freshness must both be visible. A model refresh can succeed over stale or uncorrected source partitions.

**Related practical example:** Display accepted business as-of time and reprocess the actual correction scope.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. DirectQuery slows an operational database. What options would you evaluate?

**Answer:** Measure query/concurrency pressure, tune the model/source and consider an appropriate analytical serving/import strategy aligned with freshness needs.

**Why this happens and what matters:** Storage mode affects source load and latency/freshness. Choose from actual consumers and supported model behavior, not only a preference for live data.

**Related practical example:** A frequently filtered finance dashboard can need a different serving plan from an occasional source drill-through.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. An incremental-refresh report misses a historical correction. Why?

**Answer:** The correction falls outside reprocessed scope or filtering policy. Reprocess affected partitions and define a late-correction mechanism.

**Why this happens and what matters:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Related practical example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. A DAX measure returns the same value for every product. What do you inspect?

**Answer:** Check relationship paths, removed filters and CALCULATE/filter context behavior with small known examples.

**Why this happens and what matters:** Filter modification must be intentional. Removing the wrong context can make every product display the same total or bypass a desired analytical selection.

**Related practical example:** Compare CALCULATE variants against a tiny known product/date fixture.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. One visual is fast while a page is slow. Why?

**Answer:** Multiple visuals/queries, expensive measures and interactions can create cumulative load. Measure the full page behavior and simplify the actual bottleneck.

**Why this happens and what matters:** Performance work begins with expensive queries/visuals and model structure. Reducing load must not alter measure definitions or access semantics.

**Related practical example:** Optimize a slow page after identifying a costly measure or source query rather than dropping essential controls.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A schema rename breaks refresh and measures. How do you release safely?

**Answer:** Use compatibility/versioning, dependency impact checks and coordinated source/model deployment with rollback.

**Why this happens and what matters:** Source/model changes form a dependency release. Relationships and DAX can break even if the new source table remains queryable.

**Related practical example:** Promote a reviewed compatible schema/model update and verify financial measures with known fixtures.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. A user downloads sensitive details from a permitted report. What controls matter?

**Answer:** Review report/model/export permissions and data minimization alongside row filters; validate the permitted consumer and underlying source paths.

**Why this happens and what matters:** Security behavior depends on actual consumer role/mode and underlying access. Test permitted and denied paths, including exports and direct queries.

**Related practical example:** A regional analyst sees permitted rows while a separate data-path test confirms no broad raw access.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one semantic-model refresh or report query to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Answer:** Capture the effective caller and exact error, then validate workspace/model/report roles, row security and direct source permissions. Compare production with the working configuration using refresh history, visual/query timings, source queries and accepted-data age; do not resolve the incident by giving every identity broad access.

**Why this happens and what matters:** Lake-oriented access still depends on supported configuration, permissions and query behavior. Check the effective path for the actual endpoint/model.

**Investigation and correction:** Investigate under the real caller rather than the interactive administrator. The relevant path is workspace/model/report roles, row security and direct source permissions. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

**Related practical example:** A Fabric semantic model is tested against its selected source mode rather than assumed identical to every other model.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Power BI is available, but the business result has not advanced. What would you check?

**Answer:** Trace the expected operation through accepted lakehouse/warehouse tables and report consumers and compare progress in model refresh boundary, accepted fact revision and date partition scope. Inspect refresh history, visual/query timings, source queries and accepted-data age to distinguish a service being reachable from an accepted business operation actually completing.

**Why this happens and what matters:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Investigation and correction:** Walk the dependency chain through accepted lakehouse/warehouse tables and report consumers and locate the last accepted evidence in model refresh boundary, accepted fact revision and date partition scope. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

**Related practical example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of model relationships, DAX measures, report definition and refresh settings works in test but breaks a dependent production consumer. How do you diagnose it?

**Answer:** Compare versions, environment settings and the actual fact grains, measure definitions, relationship cardinality and date semantics. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Why this happens and what matters:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Investigation and correction:** Treat the release as a change to model relationships, DAX measures, report definition and refresh settings and its dependencies, not just to one code file. Compare fact grains, measure definitions, relationship cardinality and date semantics and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

**Related practical example:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one semantic-model refresh or report query although the request or data volume is unchanged. What is your investigation sequence?

**Answer:** Compare a known-good baseline with refresh history, visual/query timings, source queries and accepted-data age and inspect high cardinality, expensive DAX, source query latency and visual concurrency. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Why this happens and what matters:** Lake-oriented access still depends on supported configuration, permissions and query behavior. Check the effective path for the actual endpoint/model.

**Investigation and correction:** Use refresh history, visual/query timings, source queries and accepted-data age to compare the same business boundary and concurrency against a known-good baseline. Examine high cardinality, expensive DAX, source query latency and visual concurrency and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

**Related practical example:** A Fabric semantic model is tested against its selected source mode rather than assumed identical to every other model.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Power BI may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Answer:** Inspect the durable outcome in model refresh boundary, accepted fact revision and date partition scope before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Why this happens and what matters:** Stored row-derived values and query-context measures serve different purposes. Consider semantics, memory and refresh behavior when choosing.

**Investigation and correction:** Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by model refresh boundary, accepted fact revision and date partition scope and repeat only through a supported safe operation/status mechanism.

**Related practical example:** A current filtered transaction sum is a measure; a stable approved classification may be a source/model attribute.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one semantic-model refresh or report query at the same time. How do you prevent lost or inconsistent state?

**Answer:** Identify the shared resource and ownership boundary in model refresh boundary, accepted fact revision and date partition scope. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Why this happens and what matters:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Investigation and correction:** Define who owns the shared mutation and which state version each caller expected. Preserve model refresh boundary, accepted fact revision and date partition scope so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

**Related practical example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Power BI without prior notice. How do you contain the impact?

**Answer:** Validate against fact grains, measure definitions, relationship cardinality and date semantics and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Why this happens and what matters:** Dimensions should filter facts under clear cardinality and key integrity. Unexpected many-to-many paths can multiply or alter totals.

**Investigation and correction:** Classify the change against fact grains, measure definitions, relationship cardinality and date semantics: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

**Related practical example:** One account version relationship should resolve the intended snapshot/fact rows rather than duplicate journal amounts.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some model refresh boundary, accepted fact revision and date partition scope evidence has expired. What can you recover and what should change?

**Answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of model refresh boundary, accepted fact revision and date partition scope and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Why this happens and what matters:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Investigation and correction:** Recovery can reconstruct only what still exists and is consistent. Inventory model refresh boundary, accepted fact revision and date partition scope, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

**Related practical example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in refresh history, visual/query timings, source queries and accepted-data age. How would you fix the logging and access design?

**Answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review workspace/model/report roles, row security and direct source permissions for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Why this happens and what matters:** Testing as a role alone does not cover every real access path. Elevated workspace roles, source access and exports need separate review.

**Investigation and correction:** Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read refresh history, visual/query timings, source queries and accepted-data age and derived exports; minimizing the source log alone does not remove already copied sensitive output.

**Related practical example:** Validate an actual regional user's permitted/report and denied/direct-data behavior.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Power BI accidentally points to production while rehearsing in development. What controls would you add?

**Answer:** Validate environment/resource identifiers in model relationships, DAX measures, report definition and refresh settings, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against model refresh boundary, accepted fact revision and date partition scope before restoring normal processing.

**Why this happens and what matters:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Investigation and correction:** Environment validation belongs before mutation. Bind model relationships, DAX measures, report definition and refresh settings to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

**Related practical example:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Accepted lakehouse/warehouse tables and report consumers is temporarily unavailable. What retry and recovery policy fits Power BI?

**Answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved model refresh boundary, accepted fact revision and date partition scope; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Why this happens and what matters:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Investigation and correction:** Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep model refresh boundary, accepted fact revision and date partition scope durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

**Related practical example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Power BI rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect high cardinality, expensive DAX, source query latency and visual concurrency. Remove demonstrated waste while preserving required model refresh boundary, accepted fact revision and date partition scope and correctness/access controls.

**Why this happens and what matters:** Performance work begins with expensive queries/visuals and model structure. Reducing load must not alter measure definitions or access semantics.

**Investigation and correction:** Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to high cardinality, expensive DAX, source query latency and visual concurrency and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

**Related practical example:** Optimize a slow page after identifying a costly measure or source query rather than dropping essential controls.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, model relationships, DAX measures, report definition and refresh settings is restored but the business path still fails. What else is required?

**Answer:** Restore/validate workspace/model/report roles, row security and direct source permissions, accepted lakehouse/warehouse tables and report consumers and the appropriate model refresh boundary, accepted fact revision and date partition scope. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Why this happens and what matters:** Date roles and calendars affect period filtering. Use explicit business calendars, active/inactive relationships and timezone-derived dates where appropriate.

**Investigation and correction:** Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate workspace/model/report roles, row security and direct source permissions, reconcile model refresh boundary, accepted fact revision and date partition scope and execute a normal authorized consumer path before calling the recovery successful.

**Related practical example:** Posting date and settlement date can drive different legitimate measures and need clear model choices.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Power BI. How do you isolate it without silently accepting incomplete results?

**Answer:** Correlate failing business keys/objects with refresh history, visual/query timings, source queries and accepted-data age and validate their fact grains, measure definitions, relationship cardinality and date semantics. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Why this happens and what matters:** Stored row-derived values and query-context measures serve different purposes. Consider semantics, memory and refresh behavior when choosing.

**Investigation and correction:** Find the smallest complete failed business scope using keys/objects and refresh history, visual/query timings, source queries and accepted-data age. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow fact grains, measure definitions, relationship cardinality and date semantics and preserve a clear accounting of accepted versus failed scope.

**Related practical example:** A current filtered transaction sum is a measure; a stable approved classification may be a source/model attribute.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change model relationships, DAX measures, report definition and refresh settings while dependent workloads remain active. What release sequence would you use?

**Answer:** Inventory consumers and fact grains, measure definitions, relationship cardinality and date semantics compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain model refresh boundary, accepted fact revision and date partition scope and define a tested rollback/correction route for incompatible behavior.

**Why this happens and what matters:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Investigation and correction:** Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep model refresh boundary, accepted fact revision and date partition scope and a tested correction/rollback boundary so a partially applied release remains recoverable.

**Related practical example:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

**How to verify the resolution:** Validate the accepted result and the intended fact grains, measure definitions, relationship cardinality and date semantics. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises include implementation reasoning, solution requirements and selected code or flow examples. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Build a transaction-and-balance model.

**Answer:** Specify separate fact grains, dimensions and a date-aware balance measure; validate with known daily snapshots.

**Implementation reasoning:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Example to work through:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

**Illustrative implementation:**

```text
Transactions: one posted source transaction line; sum accepted activity.
Daily balances: one account/date/currency snapshot; selected-date behavior.
Dimensions: approved account/customer/product/date relationships.
Known fixture: balance day 1 = 100, balance day 2 = 120.
Expected day-2 balance = 120; adding both snapshots as 220 is incorrect.
Actual DAX follows the approved calendar, keys, relationships and date policy.
```

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P02. Design and test regional RLS.

**Answer:** Map users/groups to allowed regions, test real role paths and examine elevated/direct data access separately.

**Implementation reasoning:** Security behavior depends on actual consumer role/mode and underlying access. Test permitted and denied paths, including exports and direct queries.

**Example to work through:** A regional analyst sees permitted rows while a separate data-path test confirms no broad raw access.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Diagnose one expensive visual.

**Answer:** Capture query/measure evidence, inspect model relationships and choose a measured optimization without changing totals.

**Implementation reasoning:** Performance work begins with expensive queries/visuals and model structure. Reducing load must not alter measure definitions or access semantics.

**Example to work through:** Optimize a slow page after identifying a costly measure or source query rather than dropping essential controls.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one semantic-model refresh or report query.

**Answer:** Capture the initial model refresh boundary, accepted fact revision and date partition scope, introduce one realistic dependency or validation failure and use refresh history, visual/query timings, source queries and accepted-data age to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

**Implementation reasoning:** Lake-oriented access still depends on supported configuration, permissions and query behavior. Check the effective path for the actual endpoint/model.

**Example to work through:** A Fabric semantic model is tested against its selected source mode rather than assumed identical to every other model.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Power BI.

**Answer:** Document model relationships, DAX measures, report definition and refresh settings, the fact grains, measure definitions, relationship cardinality and date semantics, required workspace/model/report roles, row security and direct source permissions, owner, normal/failure signals and recovery instructions using model refresh boundary, accepted fact revision and date partition scope. Include one normal and one failure example plus actual service targets and retention assumptions.

**Implementation reasoning:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Example to work through:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Power BI fit in an end-to-end Azure data platform?

**Answer:** Use this specific flow: Accepted facts and dimensions -> semantic model -> relationships and DAX measures -> secured report -> consumer decision. Explain what this component owns, how accepted lakehouse/warehouse tables and report consumers connects, and what the accepted consumer/result boundary is.

**Project explanation:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Concrete example:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

### D02. How would you justify using Power BI for banking balances, finance reporting and enterprise quality dashboards?

**Answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one semantic-model refresh or report query meets them, compare a credible alternative and validate using refresh history, visual/query timings, source queries and accepted-data age rather than choosing a tool merely because it is on the stack.

**Project explanation:** Lake-oriented access still depends on supported configuration, permissions and query behavior. Check the effective path for the actual endpoint/model.

**Concrete example:** A Fabric semantic model is tested against its selected source mode rather than assumed identical to every other model.

### D03. What controls must surround Power BI in a financial or telecom project?

**Answer:** Tie fact grains, measure definitions, relationship cardinality and date semantics to accountable business ownership, verify workspace/model/report roles, row security and direct source permissions, preserve model refresh boundary, accepted fact revision and date partition scope and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

**Project explanation:** The model is a business interpretation layer with relationships and measures, not just a collection of report visuals. Validate its grain before styling dashboards.

**Concrete example:** Separate transaction activity and daily balances so each measure follows its intended time semantics.

### D04. Which measures would prove your Power BI optimization helped?

**Answer:** Record the old/new configuration and comparable workload, measure high cardinality, expensive DAX, source query latency and visual concurrency with refresh history, visual/query timings, source queries and accepted-data age, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

**Project explanation:** Stored row-derived values and query-context measures serve different purposes. Consider semantics, memory and refresh behavior when choosing.

**Concrete example:** A current filtered transaction sum is a measure; a stable approved classification may be a source/model attribute.

### D05. How would you explain your own contribution to a Power BI interview project?

**Answer:** Identify which model relationships, DAX measures, report definition and refresh settings you personally built/reviewed/operated, one specific failure you resolved, the evidence in model refresh boundary, accepted fact revision and date partition scope and a verified outcome. State team-owned components separately and do not invent scale or savings.

**Project explanation:** Refresh partition scope must cover expected changes. Historical corrections outside the usual window require explicit reprocessing/revision handling.

**Concrete example:** A backdated journal correction needs its impacted partition refreshed and its report total reconciled.

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

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Power BI official documentation](https://learn.microsoft.com/en-us/power-bi/fundamentals/power-bi-overview).

[Back to all 20 interview guides](README.md).
