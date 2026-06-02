# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze â€” Inventory Snapshots

# COMMAND ----------

dbutils.widgets.text("environment", "dev")
dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

environment = dbutils.widgets.get("environment")
storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit, input_file_name

base = get_lake_base(storage_account, container)
source_path = f"{landing_path(base, 'inventory')}"
target_path = bronze_path(base, "inventory")

df = (
    spark.read.option("header", True).option("inferSchema", True).option("recursiveFileLookup", "true").csv(source_path)
    .withColumn("_ingest_ts", current_timestamp())
    .withColumn("_source_file", input_file_name())
    .withColumn("_environment", lit(environment))
)

df.write.format("delta").mode("append").option("mergeSchema", "true").save(target_path)
display(spark.read.format("delta").load(target_path).limit(10))


