```markdown
# Retail Development Project (Cloud Data Platform)

## 1. Project Overview

Create a cloud data platform supporting retail development teams for analytics, experimentation, and feature development with sandbox environments, CI/CD, and shared data models.

## 2. Requirements

- Multi-tenant workspaces, cost controls, reproducible environments, dataset catalogs.

## 3. Architecture

- Use resource groups per environment, Azure DevTest labs or separate workspaces, Databricks Repos, IaC templates.

## 4. Data Layout

- Shared gold datasets, dev sandboxes under `/dev/{team}/` with quotas and TTL.

## 5. Connectivity

- Securely expose production read-only datasets via Databricks Delta Sharing and snapshot exports.

## 6. Governance

- Quotas, Purview catalog, cost monitoring, and access policies.

## Detailed Project Flow & 20-Activity Pipeline (Development Platform)

| Step | Activity Name | Activity Type | Purpose | Input | Output |
|---:|---|---|---|---|---|
| 1 | Read_Metadata | Lookup | Team quotas and sandbox configs | mtd_dev_env | metadata |
| 2 | Provision_Sandbox | IaC | Create dev workspace resources | metadata | sandbox resources |
| 3 | Seed_Data | Copy | Provision sample or snapshot data | gold tables | dev datasets |
| 4 | Validate_Provision | Script | Validate resource health | sandbox | status |
| 5 | Notify_Team | LogicApp | Notify team on readiness | status | notification |
| 6 | Run_Unit_Tests | CI | Execute tests for code in repo | repo | test results |
| 7 | Run_Data_Tests | Notebook | Validate seeded data quality | dev datasets | dq_report |
| 8 | Deploy_Notebooks | Databricks | Deploy notebooks from CI | repo | workspace artifacts |
| 9 | Integration_Test | CI | Run integration jobs against dev data | notebooks | results |
|10 | Merge_Changes | PR | Code review and merge | PR | merged code |
|11 | Run_Stage_Deploy | IaC | Deploy to staging resources | merged code | stage resources |
|12 | Smoke_Test | Script | Basic validation in staging | stage resources | smoke results |
|13 | Approval | Manual | Approve promotion to prod | smoke results | approval |
|14 | Prod_Deploy | IaC | Deploy to prod resources | approval | prod artifacts |
|15 | PostDeploy_Check | Script | Validate prod deployments | prod | results |
|16 | Cost_Report | Script | Generate cost usage per team | billing | report |
|17 | Teardown_Expired | Function | Clean up stale sandboxes | metadata | teardown logs |
|18 | Audit | StoredProc | Log deployment activities | run metrics | audit row |
|19 | Document | Script | Update docs and catalog | artifacts | docs updated |
|20 | Feedback | Survey | Collect developer feedback | users | feedback report |

```
