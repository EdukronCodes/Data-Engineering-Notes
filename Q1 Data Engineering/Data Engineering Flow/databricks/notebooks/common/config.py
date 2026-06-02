# Databricks notebook source
# MAGIC %md
# MAGIC # Common lake path utilities for retail medallion pipeline

# COMMAND ----------

DEFAULT_SECRET_SCOPE = "retail-kv"
DEFAULT_LAKE_KEY = "lake-storage-key"


def configure_lake_access(
    storage_account: str,
    secret_scope: str = DEFAULT_SECRET_SCOPE,
    secret_key: str = DEFAULT_LAKE_KEY,
) -> None:
    """Configure abfs access using storage account key from Databricks secrets."""
    account = storage_account.strip()
    if not account:
        return
    storage_key = dbutils.secrets.get(scope=secret_scope, key=secret_key)
    dfs_host = f"{account}.dfs.core.windows.net"
    spark.conf.set(f"fs.azure.account.auth.type.{dfs_host}", "SharedKey")
    spark.conf.set(f"fs.azure.account.key.{dfs_host}", storage_key)


def get_lake_base(storage_account: str, container: str) -> str:
    return f"abfss://{container}@{storage_account}.dfs.core.windows.net"


def landing_path(base: str, source: str) -> str:
    return f"{base}/landing/{source}"


def bronze_path(base: str, source: str) -> str:
    return f"{base}/bronze/{source}"


def silver_path(base: str, source: str) -> str:
    return f"{base}/silver/{source}"


def gold_path(base: str, mart: str) -> str:
    return f"{base}/gold/{mart}"


# COMMAND ----------

try:
    _storage_account = dbutils.widgets.get("storage_account")
    configure_lake_access(_storage_account)
except Exception:
    pass
