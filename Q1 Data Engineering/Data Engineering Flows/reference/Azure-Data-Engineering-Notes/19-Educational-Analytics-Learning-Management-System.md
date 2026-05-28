```markdown
# Educational Analytics and Learning Management System

## 1. Overview

Integrated analytics for LMS and learning content management to deliver insights on course effectiveness, student outcomes, and resource allocation.

## Key Features

- Ingestion of LMS logs, grades, content usage; learning outcome modeling; instructor dashboards; data subject rights handling.

## 20-Activity Pipeline (LMS Analytics)

| Step | Activity Name | Activity Type | Purpose | Input | Output |
|---:|---|---|---|---|---|
| 1 | Read_Metadata | Lookup | Course and source config | mtd_courses | metadata |
| 2 | Ingest_Logs | Copy/Stream | Ingest activity logs | LMS | landing |
| 3 | Validate | DataFlow | Schema & integrity checks | landing | pre-bronze |
| 4 | Pseudonymize | Databricks | PII handling and pseudonymization | pre-bronze | sanitized |
| 5 | Write_Bronze | Databricks | Persist raw sanitized events | sanitized | bronze |
| 6 | Feature_Engineering | Databricks | Build engagement & mastery features | bronze | features |
| 7 | Score_Models | Databricks | Predict dropout and mastery likelihood | features | scores |
| 8 | Merge_Profiles | MERGE | Update student profiles with SCD2 | scores | dim_students |
| 9 | Build_Report | Databricks | Course effectiveness metrics | dim + scores | gold |
|10 | Publish_Dash | PowerBI | Instructor dashboards | gold | dashboards |
|11 | Alerts | LogicApp | Notify instructors of at-risk learners | scores | alerts |
|12 | PostRun_Audit | StoredProc | Log run & DQ results | run metrics | audit |
|13 | Retrain | Databricks | Retrain models periodically | labeled | new models |
|14 | A_B_Test | Experiment | Evaluate pedagogical variations | experiments | results |
|15 | Access_Control | Script | Enforce role-based data access | policies | enforced |
|16 | Data_Retention | Function | Enforce retention and GDPR requests | requests | logs |
|17 | Catalog | Purview | Register datasets & lineage | gold | cataloged assets |
|18 | CI_CD | Pipeline | Deploy notebook and model changes | repo | deployed |
|19 | Cost_Monitor | Script | Monitor compute and storage costs | billing | report |
|20 | Archive | Function | Archive course snapshots and logs | gold | archive |

```
