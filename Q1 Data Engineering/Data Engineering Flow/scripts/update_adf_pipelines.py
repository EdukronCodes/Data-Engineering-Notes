import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "adf"

def write(rel, obj):
    p = ROOT / rel
    p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    print("wrote", rel)

write("pipeline/pl_ingest_pos_transactions.json", {
  "name": "pl_ingest_pos_transactions",
  "properties": {
    "description": "Ingest POS line items from Azure SQL to landing CSV",
    "activities": [{
      "name": "Copy POS SQL to Landing", "type": "Copy", "dependsOn": [],
      "policy": {"timeout": "0.12:00:00", "retry": 2, "retryIntervalInSeconds": 30},
      "typeProperties": {
        "source": {"type": "AzureSqlSource", "sqlReaderQuery": "SELECT transaction_id, transaction_date, transaction_time, store_id, customer_id, product_id, quantity, unit_price, discount_pct, line_total, payment_method FROM dbo.pos_transactions"},
        "sink": {"type": "DelimitedTextSink", "storeSettings": {"type": "AzureBlobFSWriteSettings"}, "formatSettings": {"type": "DelimitedTextWriteSettings", "quoteAllText": True, "fileExtension": ".csv"}},
        "enableStaging": False
      },
      "inputs": [{"referenceName": "ds_azure_sql_pos", "type": "DatasetReference"}],
      "outputs": [{"referenceName": "ds_landing_retail_csv", "type": "DatasetReference", "parameters": {
        "lakeStorageAccountUrl": "@pipeline().parameters.lakeStorageAccountUrl",
        "lakeContainer": "@pipeline().parameters.lakeContainer",
        "landingFolder": "@concat(pipeline().parameters.landingPathPrefix, '/pos_transactions')",
        "landingFileName": "pos_transactions.csv"}}]
    }],
    "parameters": {
      "environment": {"type": "String", "defaultValue": "dev"},
      "lakeStorageAccountUrl": {"type": "String"},
      "lakeContainer": {"type": "String", "defaultValue": "retaildatalake"},
      "landingPathPrefix": {"type": "String", "defaultValue": "landing"}
    },
    "annotations": ["retail", "ingest", "pos", "sql"]
  },
  "type": "Microsoft.DataFactory/factories/pipelines"
})

write("pipeline/pl_ingest_inventory.json", {
  "name": "pl_ingest_inventory",
  "properties": {
    "description": "Ingest inventory from Azure PostgreSQL to landing CSV",
    "activities": [{
      "name": "Copy Inventory PG to Landing", "type": "Copy", "dependsOn": [],
      "policy": {"timeout": "0.12:00:00", "retry": 2, "retryIntervalInSeconds": 30},
      "typeProperties": {
        "source": {"type": "AzurePostgreSqlSource", "query": "SELECT store_id, product_id, quantity_on_hand, reorder_point, snapshot_date::text AS snapshot_date FROM inventory_snapshot"},
        "sink": {"type": "DelimitedTextSink", "storeSettings": {"type": "AzureBlobFSWriteSettings"}, "formatSettings": {"type": "DelimitedTextWriteSettings", "quoteAllText": True, "fileExtension": ".csv"}}
      },
      "inputs": [{"referenceName": "ds_postgresql_inventory", "type": "DatasetReference"}],
      "outputs": [{"referenceName": "ds_landing_retail_csv", "type": "DatasetReference", "parameters": {
        "lakeStorageAccountUrl": "@pipeline().parameters.lakeStorageAccountUrl",
        "lakeContainer": "@pipeline().parameters.lakeContainer",
        "landingFolder": "@concat(pipeline().parameters.landingPathPrefix, '/inventory')",
        "landingFileName": "inventory.csv"}}]
    }],
    "parameters": {
      "environment": {"type": "String", "defaultValue": "dev"},
      "lakeStorageAccountUrl": {"type": "String"},
      "lakeContainer": {"type": "String", "defaultValue": "retaildatalake"},
      "landingPathPrefix": {"type": "String", "defaultValue": "landing"}
    },
    "annotations": ["retail", "ingest", "inventory", "postgresql"]
  },
  "type": "Microsoft.DataFactory/factories/pipelines"
})

write("pipeline/pl_ingest_customers.json", {
  "name": "pl_ingest_customers",
  "properties": {
    "description": "Ingest customers from REST API to landing CSV",
    "activities": [{
      "name": "Copy REST Customers to Landing", "type": "Copy", "dependsOn": [],
      "policy": {"timeout": "0.12:00:00", "retry": 2, "retryIntervalInSeconds": 30},
      "typeProperties": {
        "source": {"type": "RestSource", "httpRequestTimeout": "00:05:00", "requestMethod": "GET"},
        "sink": {"type": "DelimitedTextSink", "storeSettings": {"type": "AzureBlobFSWriteSettings"}, "formatSettings": {"type": "DelimitedTextWriteSettings", "quoteAllText": True, "fileExtension": ".csv"}},
        "translator": {"type": "TabularTranslator", "mappings": [
          {"source": {"path": "$['id']"}, "sink": {"name": "customer_id"}},
          {"source": {"path": "$['name']"}, "sink": {"name": "full_name"}},
          {"source": {"path": "$['email']"}, "sink": {"name": "email"}},
          {"source": {"path": "$['address']['city']"}, "sink": {"name": "city"}}
        ]}
      },
      "inputs": [{"referenceName": "ds_rest_customers", "type": "DatasetReference", "parameters": {"relativeUrl": "/users"}}],
      "outputs": [{"referenceName": "ds_landing_retail_csv", "type": "DatasetReference", "parameters": {
        "lakeStorageAccountUrl": "@pipeline().parameters.lakeStorageAccountUrl",
        "lakeContainer": "@pipeline().parameters.lakeContainer",
        "landingFolder": "@concat(pipeline().parameters.landingPathPrefix, '/customers')",
        "landingFileName": "customers.csv"}}]
    }],
    "parameters": {
      "environment": {"type": "String", "defaultValue": "dev"},
      "lakeStorageAccountUrl": {"type": "String"},
      "lakeContainer": {"type": "String", "defaultValue": "retaildatalake"},
      "landingPathPrefix": {"type": "String", "defaultValue": "landing"},
      "restBaseUrl": {"type": "String"}
    },
    "annotations": ["retail", "ingest", "customers", "rest"]
  },
  "type": "Microsoft.DataFactory/factories/pipelines"
})

write("pipeline/pl_ingest_stores.json", {
  "name": "pl_ingest_stores",
  "properties": {
    "description": "Ingest store metadata from Cosmos DB to landing CSV",
    "activities": [{
      "name": "Copy Cosmos Stores to Landing", "type": "Copy", "dependsOn": [],
      "policy": {"timeout": "0.12:00:00", "retry": 2, "retryIntervalInSeconds": 30},
      "typeProperties": {
        "source": {"type": "CosmosDbSqlApiSource", "query": "SELECT c.store_id, c.store_name, c.city, c.state, c.postal_code, c.region, c.opened_date FROM c"},
        "sink": {"type": "DelimitedTextSink", "storeSettings": {"type": "AzureBlobFSWriteSettings"}, "formatSettings": {"type": "DelimitedTextWriteSettings", "quoteAllText": True, "fileExtension": ".csv"}}
      },
      "inputs": [{"referenceName": "ds_cosmos_stores", "type": "DatasetReference"}],
      "outputs": [{"referenceName": "ds_landing_retail_csv", "type": "DatasetReference", "parameters": {
        "lakeStorageAccountUrl": "@pipeline().parameters.lakeStorageAccountUrl",
        "lakeContainer": "@pipeline().parameters.lakeContainer",
        "landingFolder": "@concat(pipeline().parameters.landingPathPrefix, '/stores')",
        "landingFileName": "stores.csv"}}]
    }],
    "parameters": {
      "environment": {"type": "String", "defaultValue": "dev"},
      "lakeStorageAccountUrl": {"type": "String"},
      "lakeContainer": {"type": "String", "defaultValue": "retaildatalake"},
      "landingPathPrefix": {"type": "String", "defaultValue": "landing"}
    },
    "annotations": ["retail", "ingest", "stores", "cosmosdb"]
  },
  "type": "Microsoft.DataFactory/factories/pipelines"
})

# products stays blob - update description only
prod_path = ROOT / "pipeline/pl_ingest_products.json"
prod = json.loads(prod_path.read_text(encoding="utf-8"))
prod["properties"]["description"] = "Ingest product catalog CSV from ADLS Gen2 sources container to landing"
prod["properties"].setdefault("annotations", [])
if "blob" not in prod["properties"]["annotations"]:
    prod["properties"]["annotations"].append("blob")
write("pipeline/pl_ingest_products.json", prod)
