# Databricks notebook source
df_raw = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("/Volumes/workspace/default/healthlake/diabetic_data.csv")
)

print(f"Linhas: {df_raw.count()}")
print(f"Colunas: {len(df_raw.columns)}")
df_raw.printSchema()


# COMMAND ----------

(
    df_raw.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.default.bronze_diabetic")
)

print("Bronze salvo com sucesso!")

# COMMAND ----------

spark.sql("SELECT * FROM workspace.default.bronze_diabetic LIMIT 5").display()