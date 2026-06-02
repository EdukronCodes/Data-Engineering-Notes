# Retail Data Pipeline — Azure provisioning (ADF + Databricks medallion)

**Full implementation guide:** [docs/END-TO-END-IMPLEMENTATION-NOTES.md](docs/END-TO-END-IMPLEMENTATION-NOTES.md)

## Five diverse retail sources (SALES-aligned)

All five sources share coherent retail **sales** data: matching store IDs (`S001`–`S005`), product SKUs (`P1001`–`P1008`), and customer IDs (`C0001`–`C0008`).

| Entity | Azure source | Sample data | ADF pipeline |
|--------|--------------|-------------|--------------|
| POS sales lines | Azure SQL Database | 352 transactions May 2025 | `pl_ingest_pos_transactions` |
| Product catalog | ADLS Gen2 CSV | 8 SKUs with unit prices | `pl_ingest_products` |
| Customer purchase profiles | REST JSON on blob | 8 loyalty-tier customers | `pl_ingest_customers` |
| Inventory (sales-driven) | PostgreSQL Flexible | 40 store×SKU snapshots | `pl_ingest_inventory` |
| Store sales locations | Cosmos DB | 5 stores + annual sales USD | `pl_ingest_stores` |

Master orchestrator: **`pl_master_retail_pipeline`** (parallel ingest → bronze → silver → gold).

## Prerequisites

- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) (`az`)
- PowerShell 5.1+
- Optional: `sqlcmd`, `psql` (or Python `pyodbc` / `psycopg2-binary` for seed fallback)
- Optional: `DATABRICKS_TOKEN` for automated cluster creation

```powershell
az login
az account set --subscription "c4682434-f940-4f2f-a64f-c69a6054bb10"
```

## Quick start (deployed environment)

```powershell
cd "c:\Users\Admin\Downloads\Healthcare-APP-main\Data Engineering Flow"

# 1. Seed coherent sales data to all 5 sources
.\scripts\seed-sample-data.ps1

# 2. Deploy ADF artifacts (linked services, pipelines)
.\scripts\deploy-adf-artifacts.ps1

# 3. Deploy monitoring (Log Analytics, diagnostics, alerts, workbook)
.\scripts\deploy-monitoring.ps1

# 4. Run master pipeline (creates Databricks cluster if DATABRICKS_TOKEN set)
$env:DATABRICKS_TOKEN = "<your-pat>"   # optional
.\scripts\run-adf-master.ps1 -Wait
```

## Deployed resources (subscription `c4682434-f940-4f2f-a64f-c69a6054bb10`)

| Resource | Name | Region |
|----------|------|--------|
| Resource group | `rg-retailde-dev` | eastus |
| Lake storage | `stretaildelake3546` | eastus |
| Sources storage | `stretaildesrc3546` | eastus |
| Key Vault | `kvretailde3546` | eastus |
| Data Factory | `adf-retailde-dev3546` | eastus |
| SQL (POS) | `sql-retailde-ci3546` / `sqldb-pos` | centralindia |
| PostgreSQL | `psql-retailde-ci3546` / `inventory` | centralindia |
| Cosmos DB | `cosmos-retailde-ci3546` | centralindia |
| Databricks | `dbw-retailde-ci3546` | centralindia |
| Log Analytics | `log-retailde-3546` | eastus |

Names and URLs are in `infra/provisioned.dev.json`.

## Sample data

Generate locally:

```powershell
python .\scripts\generate-sample-data.py
python .\scripts\seed\build-seed-from-csv.py
```

Output:

- `data/sample/*.csv` — POS, products, customers, inventory, stores
- `data/sample/customers.json` — REST payload for ADF
- `scripts/seed/pos_transactions.sql` — full SQL seed (352 rows)
- `scripts/seed/inventory.sql` — full Postgres seed (40 rows)

### Seed to Azure

```powershell
.\scripts\seed-sample-data.ps1 -ProvisionedPath .\infra\provisioned.dev.json
```

Uploads product CSV and customer JSON to blob, runs SQL/Postgres/Cosmos seeds. Generates a read SAS for the REST linked service and saves `restCustomersBaseUrl` to `provisioned.dev.json`.

## ADF artifacts

Deploy from `adf/`:

```powershell
.\scripts\deploy-adf-artifacts.ps1
```

If `pl_ingest_inventory` fails with PostgreSQL password errors, refresh the linked service:

```powershell
.\scripts\fix-postgres-linked-service.ps1
```

Then test **Manage → Linked services → ls_postgresql_inventory → Test connection** in ADF Studio. If CLI updates do not refresh the encrypted password, set it manually using Key Vault secret `postgres-admin-password`.

Linked services: SQL POS, PostgreSQL inventory, REST customers (blob JSON + SAS), Cosmos stores, ADLS lake/sources, Databricks, Key Vault.

## Run master pipeline

```powershell
.\scripts\run-adf-master.ps1 -Wait
```

Without `DATABRICKS_TOKEN`, create a cluster manually:

1. Open https://adb-7405606963187307.7.azuredatabricks.net
2. **Compute** → Create cluster (Single Node, Runtime 13.3 LTS)
3. Copy cluster ID → `infra/provisioned.dev.json` → `databricksClusterId`
4. Upload `databricks/notebooks` to workspace (Repos or Workspace import)
5. Re-run `.\scripts\deploy-adf-artifacts.ps1` then `.\scripts\run-adf-master.ps1 -Wait`

Monitor runs in Azure Portal → Data Factory → `adf-retailde-dev3546` → Monitor.

## Monitoring & dashboard

Deploy Log Analytics, diagnostic settings, alerts, and workbook:

```powershell
.\scripts\deploy-monitoring.ps1
```

Or Bicep:

```powershell
az deployment group create -g rg-retailde-dev `
  -f infra/monitoring/main.bicep `
  -p infra/monitoring/parameters.dev.json
```

### What gets monitored

| Resource | Diagnostics | Log categories |
|----------|-------------|----------------|
| ADF | `diag-adf-retail` | PipelineRuns, ActivityRuns, TriggerRuns |
| Lake + sources storage | `diag-stretailde*` | StorageRead/Write, Transactions |
| SQL Server + DB | `diag-sql-retail` | SQLInsights, Errors |
| PostgreSQL | `diag-postgres-retail` | PostgreSQLLogs |
| Cosmos DB | `diag-cosmos-retail` | DataPlaneRequests |
| Databricks | `diag-databricks-retail` | clusters, jobs, notebook |
| Key Vault | `diag-kv-retail` | AuditEvent |

### Alerts

- `alert-adf-pipeline-failure-3546` — ADF pipeline run failures (15 min window)
- `alert-storage-ingestion-errors-3546` — storage activity anomalies

### Dashboard (workbook)

1. Azure Portal → **Monitor** → **Workbooks** → **Retail Data Pipeline Dashboard**
2. Or: Resource group `rg-retailde-dev` → `workbook-retail-pipeline-3546`

Workbook JSON: `monitoring/workbook-retail-pipeline.json`

Panels: pipeline success rate, run timeline, ingestion volumes by source, sales KPIs (sample/gold), storage health, recent failures.

## Provision from scratch

```powershell
$env:SQL_ADMIN_PASSWORD = "<strong-password>"
$env:POSTGRES_ADMIN_PASSWORD = "<strong-password>"
.\scripts\provision-all-resources.ps1 -FixedSuffix 3546 -DataServicesLocation centralindia
.\scripts\seed-sample-data.ps1
.\scripts\deploy-adf-artifacts.ps1
.\scripts\deploy-monitoring.ps1
```

## Gold layer sales KPIs

After a successful master run, Databricks notebooks produce:

- `gold/fact_sales` — net sales, units, transaction count by store/product/customer/day
- `gold/inventory_analytics` — stock vs sales velocity
- `gold/customer_segments` — loyalty tier analytics

Query in Databricks or export to Log Analytics for the workbook sales panel.
