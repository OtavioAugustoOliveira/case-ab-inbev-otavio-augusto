# Databricks notebook source
# MAGIC %md
# MAGIC ## Setup de Ambiente

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import col, when, trim, initcap, length, lit, row_number, desc, current_timestamp, count, round
from pyspark.sql.window import Window
import re
import os

# COMMAND ----------

# MAGIC %md
# MAGIC ## Definição de Parâmetros

# COMMAND ----------

dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text('input_path', 'wasbs://case-ab-inbev-container@caseabinbev.blob.core.windows.net/SILVER/')
dbutils.widgets.text('input_filename', 'silver_openbreweries')
dbutils.widgets.text('output_path', 'wasbs://case-ab-inbev-container@caseabinbev.blob.core.windows.net/GOLD/')
dbutils.widgets.text('output_filename', 'closed_breweries_by_country')




# COMMAND ----------

input_path = dbutils.widgets.get('input_path')
input_filename = dbutils.widgets.get('input_filename')
output_path = dbutils.widgets.get('output_path')
output_filename = dbutils.widgets.get('output_filename')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Leitura do dataframe na camada Silver

# COMMAND ----------

# Realiza a leitura dos dados na camada Silver

full_input_path = os.path.join(input_path, input_filename)
silver_df = spark.read.parquet(full_input_path)
   

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análises Agregadas

# COMMAND ----------

# Total de cervejarias por país
total_breweries_by_country_df = (
    silver_df.groupBy("COUNTRY_NAME")
    .agg(count("BREWERY_ID").alias("TOTAL_BREWERIES"))
)

# Cervejarias fechadas por país (onde brewery_type == "Closed")
closed_breweries_by_country_df = (
    silver_df.filter(col("TYPE_OF_BREWERY") == "Closed")
    .groupBy("COUNTRY_NAME")
    .agg(count("BREWERY_ID").alias("CLOSED_BREWERIES"))
)

# Unindo os dois dataframes e calculando a porcentagem de cervejarias fechadas
closed_percentage_by_country_df = (
    closed_breweries_by_country_df.join(
        total_breweries_by_country_df, on="COUNTRY_NAME", how="inner"
    )
    .withColumn(
        "PERCENTAGE_CLOSED",
        round((col("CLOSED_BREWERIES") / col("TOTAL_BREWERIES")) * 100, 2)
    )
    .orderBy("PERCENTAGE_CLOSED", ascending=False)
)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Exportação do Dataframe

# COMMAND ----------

# Adicionando coluna de controle de versão.

current_timestamp = current_timestamp()

adjusted_closed_percentage_by_country_df = closed_percentage_by_country_df.withColumn("DT_CREATED", current_timestamp).withColumn(
    "DT_UPDATED", current_timestamp
)

# COMMAND ----------

adjusted_closed_percentage_by_country_df.display()

# COMMAND ----------

# Definir o caminho e nome do arquivo usando a data

full_output_path = os.path.join(output_path, output_filename)

# Salvar o DataFrame em formato Parquet no Azure Blob Storage
closed_percentage_by_country_df.write.mode("overwrite").parquet(full_output_path) 

# COMMAND ----------

#teste
