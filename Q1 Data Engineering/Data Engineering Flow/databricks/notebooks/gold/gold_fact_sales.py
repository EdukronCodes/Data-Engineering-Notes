# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Fact Sales (daily sales by store, product, customer)

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, sum as spark_sum, countDistinct

base = get_lake_base(storage_account, container)
pos = spark.read.format("delta").load(silver_path(base, "pos_transactions"))

fact_sales = (
    pos.groupBy("transaction_date", "store_id", "product_id", "customer_id", "payment_method")
    .agg(
        spark_sum("line_total").alias("net_sales"),
        spark_sum("quantity").alias("units_sold"),
        countDistinct("transaction_id").alias("transaction_count"),
    )
)

target = gold_path(base, "fact_sales")
fact_sales.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
display(spark.read.format("delta").load(target).orderBy(col("net_sales").desc()).limit(20))
