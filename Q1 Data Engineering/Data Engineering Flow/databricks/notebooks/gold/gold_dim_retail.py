# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Retail Dimensions (conformed dim_store, dim_product, dim_customer)

# COMMAND ----------

dbutils.widgets.text("storage_account", "stretaildatalakedev")
dbutils.widgets.text("container", "retaildatalake")

storage_account = dbutils.widgets.get("storage_account")
container = dbutils.widgets.get("container")

# COMMAND ----------

# MAGIC %run ./../common/config

# COMMAND ----------

base = get_lake_base(storage_account, container)

dim_store = spark.read.format("delta").load(silver_path(base, "stores"))
dim_product = spark.read.format("delta").load(silver_path(base, "products"))
dim_customer = spark.read.format("delta").load(silver_path(base, "customers"))

dim_store.write.format("delta").mode("overwrite").save(gold_path(base, "dim_store"))
dim_product.write.format("delta").mode("overwrite").save(gold_path(base, "dim_product"))
dim_customer.write.format("delta").mode("overwrite").save(gold_path(base, "dim_customer"))

display(dim_store)
display(dim_product.limit(5))
