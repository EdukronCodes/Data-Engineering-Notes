```markdown
# Sales and Content Performance Analytics

## 1. Overview

Analyze sales funnels, campaign performance, content engagement, and attribution across channels to optimize marketing spend and content strategy.

## Key Components

- Data sources: ad platforms, CMS, e-commerce, CRM. Attribution models, revenue reconciliation, ROI dashboards.

## Pipeline Summary (20 activities)

| Step | Activity Name | Activity Type | Purpose | Input | Output |
|---:|---|---|---|---|---|
| 1 | Read_Metadata | Lookup | Campaign and source configs | mtd | metadata |
| 2 | Ingest_Ads | Copy | Pull ad platform data | API | landing |
| 3 | Ingest_CMS | Copy | Export content events | API | landing |
| 4 | Ingest_Sales | Copy | Ingest order data | ecom | landing |
| 5 | PreValidate | DataFlow | Schema checks | landing | pre-bronze |
| 6 | Write_Bronze | Databricks | Store raw events | pre-bronze | bronze |
| 7 | Enrich | Databricks | Join campaigns with content and sales | bronze | enriched |
| 8 | Attribution | Databricks | Compute multi-touch attribution | enriched | attribution |
| 9 | Revenue_Recon | StoredProc | Reconcile revenue across systems | attribution | recon report |
|10 | DQ | DataQuality Job | Validate metrics | attribution | dq_report |
|11 | Aggregations | Databricks | Build CPM/CTR/Conversion metrics | attribution | gold metrics |
|12 | Optimize | Databricks | OPTIMIZE & ZORDER | gold | optimized gold |
|13 | Publish | Synapse | Expose views for BI | gold | views |
|14 | Dashboard_Refresh | REST | Refresh Power BI datasets | views | refreshed |
|15 | Alerts | LogicApp | Alert on campaign anomalies | dq_report | alerts |
|16 | Model_Scoring | Databricks | Predict best-performing content | features | scores |
|17 | PostRun_Audit | StoredProc | Log run metrics | run metrics | audit row |
|18 | Cost_Analysis | Script | Campaign ROI by channel | billing | report |
|19 | Feedback_Loop | API | Feed model outcomes back to ad platforms | scores | updated campaigns |
|20 | Archive | Function | Archive raw campaign snapshots | landing | archive |

```
