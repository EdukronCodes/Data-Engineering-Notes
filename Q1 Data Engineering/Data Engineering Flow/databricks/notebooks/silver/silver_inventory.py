# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — Inventory

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, to_date, current_timestamp
from pyspark.sql.types import IntegerType

base = get_lake_base(storage_account, container)
bronze = spark.read.format("delta").load(bronze_path(base, "inventory"))

silver_df = (
    bronze
    .withColumn("quantity_on_hand", col("quantity_on_hand").cast(IntegerType()))
    .withColumn("reorder_point", col("reorder_point").cast(IntegerType()))
    .withColumn("snapshot_date", to_date(col("snapshot_date")))
    .filter(col("quantity_on_hand") >= 0)
    .dropDuplicates(["store_id", "product_id", "snapshot_date"])
    .withColumn("_silver_ts", current_timestamp())
)

target = silver_path(base, "inventory")
silver_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
