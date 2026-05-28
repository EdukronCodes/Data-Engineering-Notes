```markdown
# Smart City IoT Data Analytics Platform

## 1. Project Overview

Platform to ingest and analyze high-volume IoT telemetry from sensors (traffic, environment, utilities) to improve city operations, safety, and resource optimization.

## 2. Requirements

- High-throughput event ingestion, low-latency processing for alarms, long-term archival for planning analytics, spatial enrichment.

## 3. Architecture

- IoT Hub/Event Hub for ingestion, Databricks for stream processing, Synapse for spatial analytics, ADLS for storage.

## 4. Data Layout

- Separate containers for telemetry, events, alerts, and aggregated planning datasets.

## Detailed Project Flow & 20-Activity Pipeline (Smart City)

| Step | Activity Name | Activity Type | Purpose | Input | Output |
|---:|---|---|---|---|---|
| 1 | Read_Metadata | Lookup | Sensor configs and ingestion SLAs | mtd_sensors | metadata |
| 2 | Validate_Ingest | WebActivity | Test IoT hub endpoints | metadata | status |
| 3 | Capture_Events | Stream | Ingest sensor streams | IoT Hub | landing events |
| 4 | Format_Check | Spark Streaming | Validate telemetry format & timestamps | stream | valid events |
| 5 | Enrich_Geo | Databricks | Enrich events with geolocation & zones | valid events | enriched |
| 6 | Anomaly_Detect | Databricks | Real-time anomaly detection | enriched | alerts |
| 7 | Persist_Bronze | Databricks | Append to bronze telemetry deltas | enriched | bronze |
| 8 | Bronze_Audit | StoredProc | Log ingestion metrics | metrics | audit |
| 9 | Feature_Gen | Databricks | Build features for planning models | bronze | features |
|10 | Bulk_Aggregate | Databricks | Hourly/day aggregates for dashboards | features | aggregates |
|11 | Optimize | Databricks | OPTIMIZE time-series tables | aggregates | optimized |
|12 | Publish_Alerts | LogicApp | Route critical alerts to ops | alerts | notifications |
|13 | Build_Maps | Synapse | Spatial joins and heatmaps for planning | aggregates | map layers |
|14 | Dashboard_Publish | PowerBI | Publish city operations dashboards | map layers | dashboards |
|15 | PostRun_Audit | StoredProc | Log job metrics and latencies | run metrics | audit updated |
|16 | Archive | Function | Archive old telemetry partitions | bronze | archive |
|17 | Model_Retrain | Databricks | Retrain anomaly models with labeled data | historical | new models |
|18 | SLA_Monitor | Script | Monitor ingestion SLA compliance | metrics | SLA report |
|19 | Cost_Optimize | Script | Adjust provisioned throughput and retention | billing | cost changes |
|20 | Compliance | Script | Apply data retention & privacy rules | requests | action logs |

```
