# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Inventory Analytics (turnover, stockout risk)

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

from pyspark.sql.functions import col, when, sum as spark_sum

base = get_lake_base(storage_account, container)
inventory = spark.read.format("delta").load(silver_path(base, "inventory"))
pos = spark.read.format("delta").load(silver_path(base, "pos_transactions"))

sales_by_store_product = (
    pos.groupBy("store_id", "product_id")
    .agg(spark_sum("quantity").alias("units_sold_30d"))
)

inventory_analytics = (
    inventory.alias("i")
    .join(sales_by_store_product.alias("s"), ["store_id", "product_id"], "left")
    .withColumn("units_sold_30d", when(col("units_sold_30d").isNull(), 0).otherwise(col("units_sold_30d")))
    .withColumn(
        "stockout_risk",
        when(col("quantity_on_hand") <= col("reorder_point"), "HIGH")
        .when(col("quantity_on_hand") <= col("reorder_point") * 1.5, "MEDIUM")
        .otherwise("LOW"),
    )
    .withColumn(
        "turnover_ratio",
        when(col("quantity_on_hand") == 0, None).otherwise(col("units_sold_30d") / col("quantity_on_hand")),
    )
    .select(
        "store_id", "product_id", "quantity_on_hand", "reorder_point",
        "snapshot_date", "units_sold_30d", "stockout_risk", "turnover_ratio",
    )
)

target = gold_path(base, "inventory_analytics")
inventory_analytics.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(target)
