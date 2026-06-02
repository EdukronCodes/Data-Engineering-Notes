# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Customer Segments (RFM-style loyalty segments)

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, sum as spark_sum, max as spark_max, countDistinct, when

base = get_lake_base(storage_account, container)
customers = spark.read.format("delta").load(silver_path(base, "customers"))
pos = spark.read.format("delta").load(silver_path(base, "pos_transactions"))

customer_metrics = (
    pos.groupBy("customer_id")
    .agg(
        spark_sum("line_total").alias("total_spend"),
        countDistinct("transaction_id").alias("order_count"),
        spark_max("transaction_date").alias("last_purchase_date"),
    )
)

segments = (
    customers.alias("c")
    .join(customer_metrics.alias("m"), "customer_id", "left")
    .withColumn("total_spend", when(col("total_spend").isNull(), 0).otherwise(col("total_spend")))
    .withColumn("order_count", when(col("order_count").isNull(), 0).otherwise(col("order_count")))
    .withColumn(
        "segment",
        when((col("total_spend") >= 500) & (col("order_count") >= 5), "VIP")
        .when(col("total_spend") >= 200, "Loyal")
        .when(col("order_count") >= 1, "Active")
        .otherwise("Dormant"),
    )
    .select(
        "customer_id", "first_name", "last_name", "email", "loyalty_tier",
        "total_spend", "order_count", "last_purchase_date", "segment",
    )
)

target = gold_path(base, "customer_segments")
segments.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
