# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — Products

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, trim, upper, current_timestamp
from pyspark.sql.types import DoubleType

base = get_lake_base(storage_account, container)
bronze = spark.read.format("delta").load(bronze_path(base, "products"))

silver_df = (
    bronze
    .withColumn("product_name", trim(col("product_name")))
    .withColumn("category", trim(col("category")))
    .withColumn("unit_price", col("unit_price").cast(DoubleType()))
    .withColumn("is_active", upper(trim(col("is_active"))))
    .filter(col("product_id").isNotNull() & (col("unit_price") > 0))
    .dropDuplicates(["product_id"])
    .withColumn("_silver_ts", current_timestamp())
)

target = silver_path(base, "products")
silver_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
