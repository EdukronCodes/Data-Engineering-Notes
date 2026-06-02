# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — Stores

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, trim, upper, to_date, current_timestamp

base = get_lake_base(storage_account, container)
bronze = spark.read.format("delta").load(bronze_path(base, "stores"))

silver_df = (
    bronze
    .withColumn("store_name", trim(col("store_name")))
    .withColumn("state", upper(trim(col("state"))))
    .withColumn("region", trim(col("region")))
    .withColumn("opened_date", to_date(col("opened_date")))
    .dropDuplicates(["store_id"])
    .withColumn("_silver_ts", current_timestamp())
)

target = silver_path(base, "stores")
silver_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
