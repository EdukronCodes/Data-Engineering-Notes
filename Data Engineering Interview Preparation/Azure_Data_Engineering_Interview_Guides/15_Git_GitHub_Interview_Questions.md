# Git / GitHub — Complete Interview Question Guide

**50 questions with model answers:** 10 core, 5 advanced, 25 scenario-based, 5 practical exercises and 5 architecture/project questions.

**Focus:** Versioned engineering changes, pull requests, collaboration and recoverable source history.

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
Working tree -> staged changes -> commit -> reviewed branch/PR -> integrated history -> versioned deployment artifact
```

For this guide, the primary unit is **one reviewed change and release commit**. The engineering artifacts are commits, branch diff, pull request and versioned release reference. Troubleshooting starts with diff/review history, required-check results and deployment commit identity; durable progress/evidence is represented by commit graph, release artifact mapping and migration version. Distinguish platform availability, technical completion and accepted business correctness.

## A. Core interview questions

### C01. How do Git and GitHub differ?

**Model answer:** Git is distributed version control; GitHub hosts repositories and collaboration/automation services. Local Git operations do not require GitHub.

### C02. What are working tree, index and repository?

**Model answer:** The working tree holds edited files, the index stages the next commit, and the repository stores history/objects/references.

### C03. What is a commit?

**Model answer:** A versioned snapshot with parent history and metadata. Clear scope/messages help review and later recovery.

### C04. What is a branch?

**Model answer:** A reference to a line of commits. Use short-lived reviewed branches for scoped engineering changes where the team workflow supports it.

### C05. How do fetch and pull differ?

**Model answer:** Fetch retrieves remote refs/objects; pull integrates fetched work using configured merge/rebase behavior. Inspect integration mode and local changes first.

### C06. How do merge and rebase differ?

**Model answer:** Merge integrates histories with a merge result; rebase rewrites a commit sequence onto a new base. Avoid rewriting shared history without agreed coordination.

### C07. What is a pull request?

**Model answer:** A review/integration proposal around a branch diff. It should explain the concrete behavior change and relevant validation.

### C08. How do revert and reset differ?

**Model answer:** Revert creates a new inverse commit; reset moves local refs/index/worktree depending on mode. Revert is usually more appropriate for undoing shared committed changes.

### C09. What does .gitignore do?

**Model answer:** It prevents matching untracked files from being included by default. It does not remove already tracked files or purge secrets from history.

### C10. What does a tag provide?

**Model answer:** A named reference useful for releases/version points. Deployment should still identify the actual commit/artifact and validated data compatibility.

## B. Advanced implementation questions

### A01. How do you resolve meaningful merge conflicts?

**Model answer:** Understand both intended changes and dependency effects, resolve the final behavior and rerun affected checks. Accepting one entire file may silently discard valid work.

### A02. How do you review notebook changes?

**Model answer:** Prefer reviewable source/export forms, strip sensitive/generated output and verify parameters/business logic. A notebook binary/JSON diff alone can obscure behavior.

### A03. How do protected branches help?

**Model answer:** They enforce selected review/check/integration rules. Protect production-impacting paths and keep bypass authority narrow.

### A04. How do you handle a committed secret?

**Model answer:** Revoke/rotate it immediately through the approved incident process, then coordinate history cleanup and remove derived copies. A later deletion does not invalidate the secret.

### A05. How do GitHub Actions and Azure Pipelines relate?

**Model answer:** Both can automate CI/CD; execution identity, permissions, runners/agents and artifact handling require explicit configuration. Git versioning alone does not deploy data safely.

## C. Scenario-based interview questions — 25 scenarios

Answer production scenarios in this order: clarify the business impact and processing boundary; inspect the specific evidence; isolate the cause; apply a bounded correction; replay/recover safely; prove the accepted outcome; prevent recurrence. Say which assumptions require checking rather than guessing an API/limit.

### Technology-specific design and troubleshooting

### S01. Two engineers change the same SQL business rule. How do you resolve the conflict?

**Model answer:** Agree the intended final rule with the owner, inspect both diffs and validate fixtures/reconciliation. A textual resolution is not sufficient evidence of semantic correctness.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S02. A notebook commit includes customer data in outputs. What do you do?

**Model answer:** Remove/restrict sensitive output and follow the approved exposure response; sanitize exports and add prevention to the workflow.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S03. A password was removed in the latest commit. Is it safe now?

**Model answer:** No. It can remain in history/copies; rotate/revoke it and coordinate cleanup with affected collaborators.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S04. An engineer force-pushes a shared branch. How do you recover?

**Model answer:** Identify expected commits using available reflogs/refs, coordinate recovery without overwriting others, and restore agreed history under team policy.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S05. A release tag points to code without its schema migration. What is missing?

**Model answer:** A reviewed compatible release unit and migration evidence; tag code and deployable artifacts only with the required schema/configuration scope.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S06. A large generated dataset bloats the repository. What should change?

**Model answer:** Keep data artifacts in approved storage, retain small synthetic fixtures and use suitable artifact pointers where appropriate.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S07. A PR modifies ingestion and unrelated dashboards. How would you improve review?

**Model answer:** Separate independently reviewable changes or clearly justify dependencies; give each scope concrete behavior and validation evidence.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S08. A cherry-pick applies cleanly but breaks a pipeline. Why?

**Model answer:** Text compatibility does not prove dependency compatibility. Check required schema/configuration commits and test the target branch.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S09. A rollback needs to preserve later valid commits. What operation would you consider?

**Model answer:** Use an appropriate inverse/revert change and validate interactions rather than resetting shared history blindly.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### S10. A PR check runs untrusted contributor code with production secrets. What is wrong?

**Model answer:** The trust boundary is unsafe. Use restricted validation contexts and scope secrets/deployment permission to reviewed trusted execution.

**Verification:** Use relevant diff/review history, required-check results and deployment commit identity and confirm the intended review scope, source format and code/schema/configuration compatibility. Reproduce the stated failure with a small synthetic or approved test case before declaring it resolved.

### Production integration, recovery and operational scenarios

### S11. After moving one reviewed change and release commit to production, an authorization error appears. How would you distinguish identity, permission and connectivity failures?

**Model answer:** Capture the effective caller and exact error, then validate repository permissions, protected-branch rules and automation token scope. Compare production with the working configuration using diff/review history, required-check results and deployment commit identity; do not resolve the incident by giving every identity broad access.

**Verification:** Demonstrate the required identity succeeding and an unauthorized identity remaining denied.

### S12. The health page says Git / GitHub is available, but the business result has not advanced. What would you check?

**Model answer:** Trace the expected operation through collaborators, CI runner and deployment artifact consumer and compare progress in commit graph, release artifact mapping and migration version. Inspect diff/review history, required-check results and deployment commit identity to distinguish a service being reachable from an accepted business operation actually completing.

**Verification:** Identify the last accepted business/release boundary and the earliest phase that stopped advancing.

### S13. A new release of commits, branch diff, pull request and versioned release reference works in test but breaks a dependent production consumer. How do you diagnose it?

**Model answer:** Compare versions, environment settings and the actual review scope, source format and code/schema/configuration compatibility. Hold the affected change/consumer path, identify an accepted compatible version, and recover both configuration and any changed durable state.

**Verification:** Run the affected consumer contract test under production-equivalent identity and inputs.

### S14. Latency doubles for one reviewed change and release commit although the request or data volume is unchanged. What is your investigation sequence?

**Model answer:** Compare a known-good baseline with diff/review history, required-check results and deployment commit identity and inspect oversized diffs, generated files, conflicted changes and slow validation. Check dependency/configuration changes before scaling; make one measured correction and validate business results are unchanged.

**Verification:** Compare representative latency distribution, throughput and correctness before and after the change.

### S15. An operation involving Git / GitHub may have completed, but the caller timed out before receiving confirmation. How do you retry safely?

**Model answer:** Inspect the durable outcome in commit graph, release artifact mapping and migration version before repeating the operation. For mutations or external side effects, use a stable operation key and supported idempotent/transactional behavior; read-only retries have a different risk.

**Verification:** Simulate the timeout after completion and prove the retry does not create an extra business side effect.

### S16. Two automated callers perform conflicting changes to one reviewed change and release commit at the same time. How do you prevent lost or inconsistent state?

**Model answer:** Identify the shared resource and ownership boundary in commit graph, release artifact mapping and migration version. Use the platform's supported transaction/lease/lock or a serialized owner, and reconcile the final intended outcome rather than accepting whichever request finishes last.

**Verification:** Execute the conflicting requests and verify one accepted outcome with auditable ownership.

### S17. An upstream contract change reaches Git / GitHub without prior notice. How do you contain the impact?

**Model answer:** Validate against review scope, source format and code/schema/configuration compatibility and distinguish compatible from breaking changes. Retain the original input/change evidence, stop unsafe dependent work and obtain a reviewed migration/version before resuming.

**Verification:** Use a breaking-change fixture and show that the affected consumer is protected rather than silently corrupted.

### S18. You need to investigate last month's incident, but some commit graph, release artifact mapping and migration version evidence has expired. What can you recover and what should change?

**Model answer:** Inventory actual retained records/backups and state honestly which boundaries can still be reconstructed. Align retention of commit graph, release artifact mapping and migration version and operational evidence with recovery/audit requirements; do not promise recovery from expired artifacts.

**Verification:** Reconstruct one retained incident end to end and document the tested retention/recovery boundary.

### S19. Sensitive identifiers appear in diff/review history, required-check results and deployment commit identity. How would you fix the logging and access design?

**Model answer:** Minimize/redact payload values and use restricted references/correlation IDs. Review repository permissions, protected-branch rules and automation token scope for logs and source objects, then follow the approved exposure response and validate logging with synthetic sensitive fields.

**Verification:** Confirm useful troubleshooting context remains while restricted values are absent from general logs/outputs.

### S20. An automation for Git / GitHub accidentally points to production while rehearsing in development. What controls would you add?

**Model answer:** Validate environment/resource identifiers in commits, branch diff, pull request and versioned release reference, use environment-scoped identities and fail closed on a configuration mismatch. Review any completed mutations against commit graph, release artifact mapping and migration version before restoring normal processing.

**Verification:** Demonstrate the development identity/configuration cannot perform the unintended production action.

### S21. Collaborators, ci runner and deployment artifact consumer is temporarily unavailable. What retry and recovery policy fits Git / GitHub?

**Model answer:** Distinguish transient connectivity/rate errors from invalid credentials/contracts. Use bounded platform-supported retry and preserved commit graph, release artifact mapping and migration version; coordinate the owning system and avoid endless retries that duplicate side effects or hide stale results.

**Verification:** Rehearse outage and recovery, checking accepted progress and the absence of duplicate external effects.

### S22. Costs associated with Git / GitHub rise while accepted business volume stays flat. How do you investigate without losing recovery capability?

**Model answer:** Break cost down by relevant compute, storage, requests, retention and dependency use, then inspect oversized diffs, generated files, conflicted changes and slow validation. Remove demonstrated waste while preserving required commit graph, release artifact mapping and migration version and correctness/access controls.

**Verification:** Report comparable cost per accepted operation/workload and confirm service/recovery targets remain met.

### S23. During a recovery exercise, commits, branch diff, pull request and versioned release reference is restored but the business path still fails. What else is required?

**Model answer:** Restore/validate repository permissions, protected-branch rules and automation token scope, collaborators, CI runner and deployment artifact consumer and the appropriate commit graph, release artifact mapping and migration version. Reconcile durable data/external outcomes and consumer routing before declaring the application path recovered.

**Verification:** Complete a normal authorized end-to-end operation and measure recovery against the agreed objective.

### S24. Only a small subset of records, requests or objects fails in Git / GitHub. How do you isolate it without silently accepting incomplete results?

**Model answer:** Correlate failing business keys/objects with diff/review history, required-check results and deployment commit identity and validate their review scope, source format and code/schema/configuration compatibility. Preserve restricted exception evidence and apply the approved hold/quarantine/partial-success policy; do not blanket-ignore errors.

**Verification:** Reconcile successful and failed scope, fix the actual cause and revalidate the affected subset.

### S25. You must change commits, branch diff, pull request and versioned release reference while dependent workloads remain active. What release sequence would you use?

**Model answer:** Inventory consumers and review scope, source format and code/schema/configuration compatibility compatibility, deploy additive/compatible prerequisites first and validate the actual execution path. Control conflicting activation, retain commit graph, release artifact mapping and migration version and define a tested rollback/correction route for incompatible behavior.

**Verification:** Prove old/new consumers work during the intended transition and no operation uses a partially updated configuration.

## D. Practical implementation exercises

These are interview assignments with an answer outline, not provisioned Azure resources. Use development resources and synthetic/approved data. For code questions, name the engine/runtime and supply reproducible input/expected output; for governance/deployment questions, supply configuration and access/recovery evidence.

### P01. Resolve a transformation merge conflict.

**Model answer:** Explain both rules, build the intended final query and validate null/tie/financial fixtures.

### P02. Create a reviewable release change.

**Model answer:** Include scoped commits, PR description, schema/configuration dependencies and relevant acceptance evidence.

### P03. Rehearse source rollback without losing valid work.

**Model answer:** Identify the faulty commit/artifact, create a safe inverse or corrected change and validate downstream compatibility.

### P04. Create a failing-and-recovered test for one reviewed change and release commit.

**Model answer:** Capture the initial commit graph, release artifact mapping and migration version, introduce one realistic dependency or validation failure and use diff/review history, required-check results and deployment commit identity to isolate it. Recover through the supported path and compare accepted outcomes before/after; demonstrate no extra mutation, duplicate side effect or unauthorized access.

### P05. Prepare the operating handoff for Git / GitHub.

**Model answer:** Document commits, branch diff, pull request and versioned release reference, the review scope, source format and code/schema/configuration compatibility, required repository permissions, protected-branch rules and automation token scope, owner, normal/failure signals and recovery instructions using commit graph, release artifact mapping and migration version. Include one normal and one failure example plus actual service targets and retention assumptions.

## E. Architecture and project discussion

### D01. Where does Git / GitHub fit in an end-to-end Azure data platform?

**Model answer:** Use this specific flow: Working tree -> staged changes -> commit -> reviewed branch/PR -> integrated history -> versioned deployment artifact. Explain what this component owns, how collaborators, CI runner and deployment artifact consumer connects, and what the accepted consumer/result boundary is.

### D02. How would you justify using Git / GitHub for review and release history for all six Azure project designs?

**Model answer:** Start with actual volume, freshness, correctness, access and support requirements. Explain how one reviewed change and release commit meets them, compare a credible alternative and validate using diff/review history, required-check results and deployment commit identity rather than choosing a tool merely because it is on the stack.

### D03. What controls must surround Git / GitHub in a financial or telecom project?

**Model answer:** Tie review scope, source format and code/schema/configuration compatibility to accountable business ownership, verify repository permissions, protected-branch rules and automation token scope, preserve commit graph, release artifact mapping and migration version and validate outputs at matching business grain. Separate approved reference designs from evidence of work actually performed.

### D04. Which measures would prove your Git / GitHub optimization helped?

**Model answer:** Record the old/new configuration and comparable workload, measure oversized diffs, generated files, conflicted changes and slow validation with diff/review history, required-check results and deployment commit identity, and report latency/throughput/cost as relevant. Confirm unchanged correctness, access and recovery behavior before claiming improvement.

### D05. How would you explain your own contribution to a Git / GitHub interview project?

**Model answer:** Identify which commits, branch diff, pull request and versioned release reference you personally built/reviewed/operated, one specific failure you resolved, the evidence in commit graph, release artifact mapping and migration version and a verified outcome. State team-owned components separately and do not invent scale or savings.

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

The questions/model answers are original interview preparation guidance. The linked primary documentation describes the platform and selected semantics; use its version-specific pages for exact syntax, limits and capabilities. Overview pages do not independently substantiate every proposed production design.

- [Git / GitHub official documentation](https://git-scm.com/docs).
- [git revert reference](https://git-scm.com/docs/git-revert.html).

[Back to all 20 interview guides](README.md).
