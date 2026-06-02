"""Seed Cosmos DB stores container from stores.csv using Azure CLI + REST or azure-cosmos if installed."""
import argparse, csv, json, subprocess, uuid
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--account"); p.add_argument("--database"); p.add_argument("--container")
    p.add_argument("--rg"); p.add_argument("--csv")
    args = p.parse_args()
    rows = list(csv.DictReader(Path(args.csv).open(encoding="utf-8")))
    try:
        from azure.cosmos import CosmosClient
    except ImportError:
        print("Install: pip install azure-cosmos")
        print("Or insert documents via Azure Portal Data Explorer")
        for r in rows:
            doc = {**r, "id": r.get("store_id", str(uuid.uuid4()))}
            print(json.dumps(doc))
        return
    key = subprocess.check_output(
        "az cosmosdb keys list -g {} -n {} --type keys -o tsv --query primaryMasterKey".format(args.rg, args.account),
        shell=True,
        text=True,
    ).strip()
    endpoint = f"https://{args.account}.documents.azure.com:443/"
    client = CosmosClient(endpoint, key)
    container = client.get_database_client(args.database).get_container_client(args.container)
    for r in rows:
        doc = dict(r)
        doc["id"] = r["store_id"]
        container.upsert_item(doc)
    print(f"Upserted {len(rows)} store documents")

if __name__ == "__main__":
    main()
