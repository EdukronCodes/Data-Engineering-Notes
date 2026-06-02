# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — POS Transactions (cleansed, typed, deduplicated)

# COMMAND ----------

dbutils.widgets.text("environment", "dev")
dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, to_date, trim, upper, current_timestamp
from pyspark.sql.types import DoubleType, IntegerType

base = get_lake_base(storage_account, container)
bronze = spark.read.format("delta").load(bronze_path(base, "pos_transactions"))

silver_df = (
    bronze
    .withColumn("transaction_date", to_date(col("transaction_date")))
    .withColumn("quantity", col("quantity").cast(IntegerType()))
    .withColumn("unit_price", col("unit_price").cast(DoubleType()))
    .withColumn("discount_pct", col("discount_pct").cast(DoubleType()))
    .withColumn("line_total", col("line_total").cast(DoubleType()))
    .withColumn("payment_method", upper(trim(col("payment_method"))))
    .filter(col("transaction_id").isNotNull() & col("store_id").isNotNull())
    .dropDuplicates(["transaction_id", "product_id"])
    .withColumn("_silver_ts", current_timestamp())
)

target = silver_path(base, "pos_transactions")
silver_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
display(spark.read.format("delta").load(target).limit(10))
