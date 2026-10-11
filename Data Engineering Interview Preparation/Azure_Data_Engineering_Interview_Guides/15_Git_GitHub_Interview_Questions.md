# Git / GitHub — Complete Interview Question Guide

**50 questions with detailed answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Versioned engineering changes, pull requests, collaboration and recoverable source history.

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
Working tree -> staged changes -> commit -> reviewed branch/PR -> integrated history -> versioned deployment artifact
```

For this guide, the primary unit is **one reviewed change and release commit**. The engineering artifacts are commits, branch diff, pull request and versioned release reference. Troubleshooting starts with diff/review history, required-check results and deployment commit identity; durable progress/evidence is represented by commit graph, release artifact mapping and migration version. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. How do Git and GitHub differ?

**Answer:** Git is distributed version control; GitHub hosts repositories and collaboration/automation services. Local Git operations do not require GitHub.

**Explanation:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Practical example:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

### C02. What are working tree, index and repository?

**Answer:** The working tree holds edited files, the index stages the next commit, and the repository stores history/objects/references.

**Explanation:** Staging selects the precise content of the next snapshot. Reviewing the staged diff prevents unrelated/sensitive edits from becoming part of a change.

**Practical example:** A notebook author excludes generated output and stages only the intended source and fixture changes.

### C03. What is a commit?

**Answer:** A versioned snapshot with parent history and metadata. Clear scope/messages help review and later recovery.

**Explanation:** Commits are auditable source units, not evidence of deployed behavior. Link them to reviewed artifacts and relevant acceptance checks.

**Practical example:** A transaction-rule commit records expected fixture results and later maps to a release artifact.

### C04. What is a branch?

**Answer:** A reference to a line of commits. Use short-lived reviewed branches for scoped engineering changes where the team workflow supports it.

**Explanation:** Branching isolates work until integration, but it does not isolate external production effects from scripts. Keep execution permissions separate.

**Practical example:** A feature branch cannot freely mutate production just because its code is not yet merged.

### C05. How do fetch and pull differ?

**Answer:** Fetch retrieves remote refs/objects; pull integrates fetched work using configured merge/rebase behavior. Inspect integration mode and local changes first.

**Explanation:** Integration may alter local history or create conflicts. Inspect local changes and the configured merge/rebase strategy before pulling.

**Practical example:** Fetch and review a teammate's schema change before integrating it with your notebook work.

### C06. How do merge and rebase differ?

**Answer:** Merge integrates histories with a merge result; rebase rewrites a commit sequence onto a new base. Avoid rewriting shared history without agreed coordination.

**Explanation:** History rewriting changes commit identities and can disrupt collaborators. Use the team's agreed shared-history policy and review the resulting final diff.

**Practical example:** Rebase a private feature branch where appropriate, but avoid force-rewriting other engineers' shared commits.

### C07. What is a pull request?

**Answer:** A review/integration proposal around a branch diff. It should explain the concrete behavior change and relevant validation.

**Explanation:** Review explains the concrete before/after behavior and test evidence. Generated noise makes semantic changes harder to see.

**Practical example:** A journal mapping PR states which postings now resolve differently and how reconciliation was checked.

### C08. How do revert and reset differ?

**Answer:** Revert creates a new inverse commit; reset moves local refs/index/worktree depending on mode. Revert is usually more appropriate for undoing shared committed changes.

**Explanation:** Undo strategies have different effects on shared history and local files. Protect valuable uncommitted work and later valid commits.

**Practical example:** Use an appropriate inverse change to undo a deployed rule without erasing a teammate's later fix.

### C09. What does .gitignore do?

**Answer:** It prevents matching untracked files from being included by default. It does not remove already tracked files or purge secrets from history.

**Explanation:** Ignore rules apply to untracked paths, not all repository copies or historical content. Secrets require immediate credential response, not just file deletion.

**Practical example:** Adding a tracked password file to .gitignore does not remove the exposed password from prior commits.

### C10. What does a tag provide?

**Answer:** A named reference useful for releases/version points. Deployment should still identify the actual commit/artifact and validated data compatibility.

**Explanation:** Release references identify a source point, while deployable dependencies still need controlled versions. Tags do not package a complete database migration automatically.

**Practical example:** Associate a release tag with its artifact, schema/configuration version and validation record.

## B. Advanced implementation questions

### A01. How do you resolve meaningful merge conflicts?

**Answer:** Understand both intended changes and dependency effects, resolve the final behavior and rerun affected checks. Accepting one entire file may silently discard valid work.

**Explanation:** Conflict resolution combines intended behavior, not merely text. Test both dependent logic and the final business outcome.

**Practical example:** Resolve two effective-date changes and verify nonoverlapping dimension intervals.

### A02. How do you review notebook changes?

**Answer:** Prefer reviewable source/export forms, strip sensitive/generated output and verify parameters/business logic. A notebook binary/JSON diff alone can obscure behavior.

**Explanation:** Notebooks can contain execution output, metadata and sensitive payloads. Reviewable source forms and output sanitation improve both governance and code review.

**Practical example:** Export/sanitize a notebook so a reviewer can see the PySpark rule without customer rows.

### A03. How do protected branches help?

**Answer:** They enforce selected review/check/integration rules. Protect production-impacting paths and keep bypass authority narrow.

**Explanation:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Practical example:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

### A04. How do you handle a committed secret?

**Answer:** Revoke/rotate it immediately through the approved incident process, then coordinate history cleanup and remove derived copies. A later deletion does not invalidate the secret.

**Explanation:** The secret remains valid until revoked/rotated regardless of history cleanup. Coordinate copied logs/clones/artifacts under the approved response.

**Practical example:** Rotate a leaked service credential first, then clean relevant history and prevention paths.

### A05. How do GitHub Actions and Azure Pipelines relate?

**Answer:** Both can automate CI/CD; execution identity, permissions, runners/agents and artifact handling require explicit configuration. Git versioning alone does not deploy data safely.

**Explanation:** CI hosts execute code with particular trust and credential scope. Source review and artifact promotion remain necessary even when automation is convenient.

**Practical example:** Restrict production tokens to the reviewed deployment context rather than arbitrary PR scripts.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. Two engineers change the same SQL business rule. How do you resolve the conflict?

**Answer:** Agree the intended final rule with the owner, inspect both diffs and validate fixtures/reconciliation. A textual resolution is not sufficient evidence of semantic correctness.

**Why this happens and what matters:** Conflict resolution combines intended behavior, not merely text. Test both dependent logic and the final business outcome.

**Related practical example:** Resolve two effective-date changes and verify nonoverlapping dimension intervals.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S02. A notebook commit includes customer data in outputs. What do you do?

**Answer:** Remove/restrict sensitive output and follow the approved exposure response; sanitize exports and add prevention to the workflow.

**Why this happens and what matters:** Notebooks can contain execution output, metadata and sensitive payloads. Reviewable source forms and output sanitation improve both governance and code review.

**Related practical example:** Export/sanitize a notebook so a reviewer can see the PySpark rule without customer rows.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S03. A password was removed in the latest commit. Is it safe now?

**Answer:** No. It can remain in history/copies; rotate/revoke it and coordinate cleanup with affected collaborators.

**Why this happens and what matters:** The secret remains valid until revoked/rotated regardless of history cleanup. Coordinate copied logs/clones/artifacts under the approved response.

**Related practical example:** Rotate a leaked service credential first, then clean relevant history and prevention paths.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S04. An engineer force-pushes a shared branch. How do you recover?

**Answer:** Identify expected commits using available reflogs/refs, coordinate recovery without overwriting others, and restore agreed history under team policy.

**Why this happens and what matters:** History rewriting changes commit identities and can disrupt collaborators. Use the team's agreed shared-history policy and review the resulting final diff.

**Related practical example:** Rebase a private feature branch where appropriate, but avoid force-rewriting other engineers' shared commits.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S05. A release tag points to code without its schema migration. What is missing?

**Answer:** A reviewed compatible release unit and migration evidence; tag code and deployable artifacts only with the required schema/configuration scope.

**Why this happens and what matters:** Release references identify a source point, while deployable dependencies still need controlled versions. Tags do not package a complete database migration automatically.

**Related practical example:** Associate a release tag with its artifact, schema/configuration version and validation record.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S06. A large generated dataset bloats the repository. What should change?

**Answer:** Keep data artifacts in approved storage, retain small synthetic fixtures and use suitable artifact pointers where appropriate.

**Why this happens and what matters:** Ignore rules apply to untracked paths, not all repository copies or historical content. Secrets require immediate credential response, not just file deletion.

**Related practical example:** Adding a tracked password file to .gitignore does not remove the exposed password from prior commits.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S07. A PR modifies ingestion and unrelated dashboards. How would you improve review?

**Answer:** Separate independently reviewable changes or clearly justify dependencies; give each scope concrete behavior and validation evidence.

**Why this happens and what matters:** Review explains the concrete before/after behavior and test evidence. Generated noise makes semantic changes harder to see.

**Related practical example:** A journal mapping PR states which postings now resolve differently and how reconciliation was checked.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S08. A cherry-pick applies cleanly but breaks a pipeline. Why?

**Answer:** Text compatibility does not prove dependency compatibility. Check required schema/configuration commits and test the target branch.

**Why this happens and what matters:** Conflict resolution combines intended behavior, not merely text. Test both dependent logic and the final business outcome.

**Related practical example:** Resolve two effective-date changes and verify nonoverlapping dimension intervals.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S09. A rollback needs to preserve later valid commits. What operation would you consider?

**Answer:** Use an appropriate inverse/revert change and validate interactions rather than resetting shared history blindly.

**Why this happens and what matters:** Undo strategies have different effects on shared history and local files. Protect valuable uncommitted work and later valid commits.

**Related practical example:** Use an appropriate inverse change to undo a deployed rule without erasing a teammate's later fix.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S10. A PR check runs untrusted contributor code with production secrets. What is wrong?

**Answer:** The trust boundary is unsafe. Use restricted validation contexts and scope secrets/deployment permission to reviewed trusted execution.

**Why this happens and what matters:** CI hosts execute code with particular trust and credential scope. Source review and artifact promotion remain necessary even when automation is convenient.

**Related practical example:** Restrict production tokens to the reviewed deployment context rather than arbitrary PR scripts.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### Production integration, recovery and operational scenarios

### S11. After moving one reviewed change and release commit to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Answer:** Capture the effective caller and exact error, then validate repository permissions, protected-branch rules and automation token scope. Compare production with the working configuration using diff/review history, required-check results and deployment commit identity; do not resolve the incident by giving every identity broad access.

**Why this happens and what matters:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Investigation and correction:** Investigate under the real caller rather than the interactive administrator. The relevant path is repository permissions, protected-branch rules and automation token scope. Capture the exact failure and compare one allowed operation with one deliberately denied operation, so fixing connectivity does not accidentally broaden authorization.

**Related practical example:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S12. The health page says Git / GitHub is available, but the business result has not advanced. What would you check?

**Answer:** Trace the expected operation through collaborators, CI runner and deployment artifact consumer and compare progress in commit graph, release artifact mapping and migration version. Inspect diff/review history, required-check results and deployment commit identity to distinguish a service being reachable from an accepted business operation actually completing.

**Why this happens and what matters:** Commits are auditable source units, not evidence of deployed behavior. Link them to reviewed artifacts and relevant acceptance checks.

**Investigation and correction:** Walk the dependency chain through collaborators, CI runner and deployment artifact consumer and locate the last accepted evidence in commit graph, release artifact mapping and migration version. Distinguish a source that delivered nothing, an execution that never started, a held result and a consumer that still reads an old version; those require different fixes.

**Related practical example:** A transaction-rule commit records expected fixture results and later maps to a release artifact.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S13. A new release of commits, branch diff, pull request and versioned release reference works in test but breaks a dependent production consumer. How do you diagnose it?

**Answer:** Compare versions, environment settings and the actual review scope, source format and code/schema/configuration compatibility. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Why this happens and what matters:** Release references identify a source point, while deployable dependencies still need controlled versions. Tags do not package a complete database migration automatically.

**Investigation and correction:** Treat the release as a change to commits, branch diff, pull request and versioned release reference and its dependencies, not just to one code file. Compare review scope, source format and code/schema/configuration compatibility and the execution identity between test and production. Restore a compatible state before allowing unsafe consumers to continue.

**Related practical example:** Associate a release tag with its artifact, schema/configuration version and validation record.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S14. Latency doubles for one reviewed change and release commit although the request or data volume is unchanged. What is your investigation sequence?

**Answer:** Compare a known-good baseline with diff/review history, required-check results and deployment commit identity and inspect oversized diffs, generated files, conflicted changes and slow validation. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Why this happens and what matters:** Integration may alter local history or create conflicts. Inspect local changes and the configured merge/rebase strategy before pulling.

**Investigation and correction:** Use diff/review history, required-check results and deployment commit identity to compare the same business boundary and concurrency against a known-good baseline. Examine oversized diffs, generated files, conflicted changes and slow validation and changed dependencies/configuration. A faster run is not acceptable if it changes values, permitted access or recovery behavior.

**Related practical example:** Fetch and review a teammate's schema change before integrating it with your notebook work.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S15. An operation involving Git / GitHub may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Answer:** Inspect the durable outcome in commit graph, release artifact mapping and migration version before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Why this happens and what matters:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Investigation and correction:** Separate an uncertain response from an uncertain operation. The caller's timeout does not undo a completed write, grant, deployment or external request. Read the outcome represented by commit graph, release artifact mapping and migration version and repeat only through a supported safe operation/status mechanism.

**Related practical example:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S16. Two automated callers perform conflicting changes to one reviewed change and release commit at the same time. How do you prevent lost or inconsistent state?

**Answer:** Identify the shared resource and ownership boundary in commit graph, release artifact mapping and migration version. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Why this happens and what matters:** Commits are auditable source units, not evidence of deployed behavior. Link them to reviewed artifacts and relevant acceptance checks.

**Investigation and correction:** Define who owns the shared mutation and which state version each caller expected. Preserve commit graph, release artifact mapping and migration version so a rejected or losing caller can reconcile rather than overwrite blindly. The exact transaction, lease or lock must be supported by the target service.

**Related practical example:** A transaction-rule commit records expected fixture results and later maps to a release artifact.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S17. An upstream contract change reaches Git / GitHub without prior notice. How do you contain the impact?

**Answer:** Validate against review scope, source format and code/schema/configuration compatibility and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Why this happens and what matters:** Integration may alter local history or create conflicts. Inspect local changes and the configured merge/rebase strategy before pulling.

**Investigation and correction:** Classify the change against review scope, source format and code/schema/configuration compatibility: additional optional information may be compatible, while key/type/meaning changes can be breaking. Preserve evidence and identify all affected consumers before approving a migration or versioned release.

**Related practical example:** Fetch and review a teammate's schema change before integrating it with your notebook work.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S18. You need to investigate last month's incident, but some commit graph, release artifact mapping and migration version evidence has expired. What can you recover and what should change?

**Answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of commit graph, release artifact mapping and migration version and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Why this happens and what matters:** Commits are auditable source units, not evidence of deployed behavior. Link them to reviewed artifacts and relevant acceptance checks.

**Investigation and correction:** Recovery can reconstruct only what still exists and is consistent. Inventory commit graph, release artifact mapping and migration version, relevant backups and dependency records, then state any gap explicitly. Retention must be set from agreed audit, replay and recovery use cases rather than an arbitrary cleanup interval.

**Related practical example:** A transaction-rule commit records expected fixture results and later maps to a release artifact.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S19. Sensitive identifiers appear in diff/review history, required-check results and deployment commit identity. How would you fix the logging and access design?

**Answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review repository permissions, protected-branch rules and automation token scope for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Why this happens and what matters:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Investigation and correction:** Keep identity, run/object references and reason codes needed for troubleshooting while excluding restricted payload values. Review who can read diff/review history, required-check results and deployment commit identity and derived exports; minimizing the source log alone does not remove already copied sensitive output.

**Related practical example:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S20. An automation for Git / GitHub accidentally points to production while rehearsing in development. What controls would you add?

**Answer:** Validate environment/resource identifiers in commits, branch diff, pull request and versioned release reference, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against commit graph, release artifact mapping and migration version before restoring normal processing.

**Why this happens and what matters:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Investigation and correction:** Environment validation belongs before mutation. Bind commits, branch diff, pull request and versioned release reference to approved resource names and scoped identities so the development execution cannot reach unintended production targets. If the mistake already happened, reconcile the exact affected state before rerunning.

**Related practical example:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S21. Collaborators, ci runner and deployment artifact consumer is temporarily unavailable. What retry and recovery policy fits Git / GitHub?

**Answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved commit graph, release artifact mapping and migration version; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Why this happens and what matters:** Commits are auditable source units, not evidence of deployed behavior. Link them to reviewed artifacts and relevant acceptance checks.

**Investigation and correction:** Use the dependency's documented error and retry contract. Invalid permissions/schema are not transient outages; retries do not repair them. During an outage, keep commit graph, release artifact mapping and migration version durable and make accepted-data/service staleness visible instead of reporting a healthy end-to-end operation.

**Related practical example:** A transaction-rule commit records expected fixture results and later maps to a release artifact.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S22. Costs associated with Git / GitHub rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect oversized diffs, generated files, conflicted changes and slow validation. Remove demonstrated waste while preserving required commit graph, release artifact mapping and migration version and correctness/access controls.

**Why this happens and what matters:** Release references identify a source point, while deployable dependencies still need controlled versions. Tags do not package a complete database migration automatically.

**Investigation and correction:** Measure cost at an accepted business workload boundary, including repeated attempts and retained artifacts. Link changes to oversized diffs, generated files, conflicted changes and slow validation and test the same service targets afterward. Deleting recovery evidence to lower cost changes capabilities and requires an explicit approved retention decision.

**Related practical example:** Associate a release tag with its artifact, schema/configuration version and validation record.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S23. During a recovery exercise, commits, branch diff, pull request and versioned release reference is restored but the business path still fails. What else is required?

**Answer:** Restore/validate repository permissions, protected-branch rules and automation token scope, collaborators, CI runner and deployment artifact consumer and the appropriate commit graph, release artifact mapping and migration version. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Why this happens and what matters:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Investigation and correction:** Configuration restoration alone is incomplete when identities, network routing, dependencies or durable business state remain unavailable. Revalidate repository permissions, protected-branch rules and automation token scope, reconcile commit graph, release artifact mapping and migration version and execute a normal authorized consumer path before calling the recovery successful.

**Related practical example:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S24. Only a small subset of records, requests or objects fails in Git / GitHub. How do you isolate it without silently accepting incomplete results?

**Answer:** Correlate failing business keys/objects with diff/review history, required-check results and deployment commit identity and validate their review scope, source format and code/schema/configuration compatibility. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Why this happens and what matters:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Investigation and correction:** Find the smallest complete failed business scope using keys/objects and diff/review history, required-check results and deployment commit identity. Distinguish invalid input from missing reference, permission or ordering conflicts. Any quarantine or partial success must follow review scope, source format and code/schema/configuration compatibility and preserve a clear accounting of accepted versus failed scope.

**Related practical example:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

### S25. You must change commits, branch diff, pull request and versioned release reference while dependent workloads remain active. What release sequence would you use?

**Answer:** Inventory consumers and review scope, source format and code/schema/configuration compatibility compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain commit graph, release artifact mapping and migration version and define a tested rollback/correction route for incompatible behavior.

**Why this happens and what matters:** Release references identify a source point, while deployable dependencies still need controlled versions. Tags do not package a complete database migration automatically.

**Investigation and correction:** Order changes by dependency and compatibility. Introduce safe prerequisites, verify both existing and transitioning consumers, then activate the intended route. Keep commit graph, release artifact mapping and migration version and a tested correction/rollback boundary so a partially applied release remains recoverable.

**Related practical example:** Associate a release tag with its artifact, schema/configuration version and validation record.

**How to verify the resolution:** Validate the accepted result and the intended review scope, source format and code/schema/configuration compatibility. Retain the original failure and recovered result with their operation/run references. Where the operation mutates data or an external outcome, test a repeated attempt; for an access incident, also confirm the unrelated forbidden operation remains denied.

## D. Practical implementation exercises

These exercises include implementation reasoning, solution requirements and selected code or flow examples. They do not provision Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Resolve a transformation merge conflict.

**Answer:** Explain both rules, build the intended final query and validate null/tie/financial fixtures.

**Implementation reasoning:** Conflict resolution combines intended behavior, not merely text. Test both dependent logic and the final business outcome.

**Example to work through:** Resolve two effective-date changes and verify nonoverlapping dimension intervals.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P02. Create a reviewable release change.

**Answer:** Include scoped commits, PR description, schema/configuration dependencies and relevant acceptance evidence.

**Implementation reasoning:** Commits are auditable source units, not evidence of deployed behavior. Link them to reviewed artifacts and relevant acceptance checks.

**Example to work through:** A transaction-rule commit records expected fixture results and later maps to a release artifact.

**Illustrative implementation:**

```bash
# Read-only review commands; create/change operations follow team policy.
git status
git diff
git diff --staged
git log --oneline -10
# Inspect intended source/fixture/migration scope before committing.
# PR description: concrete behavior change, dependencies and validation.
# Never commit secret values or customer-bearing notebook output.
```

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P03. Rehearse source rollback without losing valid work.

**Answer:** Identify the faulty commit/artifact, create a safe inverse or corrected change and validate downstream compatibility.

**Implementation reasoning:** Undo strategies have different effects on shared history and local files. Protect valuable uncommitted work and later valid commits.

**Example to work through:** Use an appropriate inverse change to undo a deployed rule without erasing a teammate's later fix.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P04. Create a failing-and-recovered test for one reviewed change and release commit.

**Answer:** Capture the initial commit graph, release artifact mapping and migration version, introduce one realistic dependency or validation failure and use diff/review history, required-check results and deployment commit identity to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

**Implementation reasoning:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Example to work through:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

### P05. Prepare the operating handoff for Git / GitHub.

**Answer:** Document commits, branch diff, pull request and versioned release reference, the review scope, source format and code/schema/configuration compatibility, required repository permissions, protected-branch rules and automation token scope, owner, normal/failure signals and recovery instructions using commit graph, release artifact mapping and migration version. Include one normal and one failure example plus actual service targets and retention assumptions.

**Implementation reasoning:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Example to work through:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

**Expected deliverable:** Provide the implementation described above, its explicit inputs and expected results, and evidence for a normal case plus the failure/recovery case relevant to this question. Use the actual engine/runtime and approved identity; the example is a design/code starting point, not an executed cloud solution.

## E. Architecture and project discussion

### D01. Where does Git / GitHub fit in an end-to-end Azure data platform?

**Answer:** Use this specific flow: Working tree -> staged changes -> commit -> reviewed branch/PR -> integrated history -> versioned deployment artifact. Explain what this component owns, how collaborators, CI runner and deployment artifact consumer connects, and what the accepted consumer/result boundary is.

**Project explanation:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Concrete example:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

### D02. How would you justify using Git / GitHub for review and release history for all six Azure project designs?

**Answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one reviewed change and release commit meets them, compare a credible alternative and validate using diff/review history, required-check results and deployment commit identity rather than choosing a tool merely because it is on the stack.

**Project explanation:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Concrete example:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

### D03. What controls must surround Git / GitHub in a financial or telecom project?

**Answer:** Tie review scope, source format and code/schema/configuration compatibility to accountable business ownership, verify repository permissions, protected-branch rules and automation token scope, preserve commit graph, release artifact mapping and migration version and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

**Project explanation:** Release references identify a source point, while deployable dependencies still need controlled versions. Tags do not package a complete database migration automatically.

**Concrete example:** Associate a release tag with its artifact, schema/configuration version and validation record.

### D04. Which measures would prove your Git / GitHub optimization helped?

**Answer:** Record the old/new configuration and comparable workload, measure oversized diffs, generated files, conflicted changes and slow validation with diff/review history, required-check results and deployment commit identity, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

**Project explanation:** Protected rules control selected integration actions; bypass access and automation identity still need governance. Required checks should be relevant and trustworthy.

**Concrete example:** A protected main branch requires review and transformation fixtures before a deployment-relevant change merges.

### D05. How would you explain your own contribution to a Git / GitHub interview project?

**Answer:** Identify which commits, branch diff, pull request and versioned release reference you personally built/reviewed/operated, one specific failure you resolved, the evidence in commit graph, release artifact mapping and migration version and a verified outcome. State team-owned components separately and do not invent scale or savings.

**Project explanation:** Version control records source history; collaboration hosting adds reviews/checks/automation. These are related but different responsibilities.

**Concrete example:** A local SQL commit is versioned before its GitHub pull request is reviewed or deployed.

## Revision notes and common mistakes

- Explain Git / GitHub's specific responsibility in the flow before naming surrounding tools.
- Use the real review scope, source format and code/schema/configuration compatibility; an accepted request/job does not establish a correct business result.
- Validate repository permissions, protected-branch rules and automation token scope under the actual execution identity, rather than your administrator account.
- Preserve commit graph, release artifact mapping and migration version and inspect it before retrying uncertain side effects.
- Tune oversized diffs, generated files, conflicted changes and slow validation from measured evidence and confirm business correctness remains unchanged.
- Keep secret/personal data out of answers, fixtures and general logs; use synthetic examples.
- Runtime, connector, tier, licensing, limits and deployment support can change. Check the official documentation for the target configuration before quoting exact values.

## Self-assessment

Score each answer 0–3: **0** cannot explain; **1** can define the concept; **2** can propose a correct implementation; **3** can explain tradeoffs, failure handling and verification evidence. Revisit weak answers and complete at least one practical exercise before describing it as hands-on experience.

For a mock round, choose 3 core, 2 advanced, 5 scenario and 1 practical question. Answer aloud, draw the relevant flow and distinguish what you know from what you would inspect. Follow up with: “Which evidence proves this?”, “What happens after a retry?”, and “How would the consumer know the result is accepted?”

## Official references

The questions and detailed answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Git / GitHub official documentation](https://git-scm.com/docs).
- [git revert reference](https://git-scm.com/docs/git-revert.html).

[Back to all 20 interview guides](README.md).
