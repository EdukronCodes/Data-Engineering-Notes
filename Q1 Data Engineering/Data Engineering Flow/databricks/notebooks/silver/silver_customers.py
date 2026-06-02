# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — Customers (SCD Type 1 overwrite)

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, trim, lower, to_date, current_timestamp

base = get_lake_base(storage_account, container)
bronze = spark.read.format("delta").load(bronze_path(base, "customers"))

silver_df = (
    bronze
    .withColumn("email", lower(trim(col("email"))))
    .withColumn("loyalty_tier", trim(col("loyalty_tier")))
    .withColumn("signup_date", to_date(col("signup_date")))
    .filter(col("customer_id").isNotNull() & col("email").contains("@"))
    .dropDuplicates(["customer_id"])
    .withColumn("_silver_ts", current_timestamp())
)

target = silver_path(base, "customers")
silver_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
