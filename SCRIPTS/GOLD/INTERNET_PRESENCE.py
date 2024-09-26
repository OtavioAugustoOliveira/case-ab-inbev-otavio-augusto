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
dbutils.widgets.text('output_filename', 'internet_presence')




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

#Análise de presença na internet: Qual perfil de cervejaria costuma ter maior indice de preenchimento de url e telefone para contato?


# Total de cervejarias por tipo
total_breweries_df = (
    silver_df.groupBy("TYPE_OF_BREWERY")
    .agg(count("BREWERY_ID").alias("TOTAL_BREWERIES"))
)

# Análise de presença na internet
internet_presence_df = (
    silver_df.filter((~col("WEBSITE").isNull()) & ~col("CONTACT_PHONE").isNull())
    .groupBy("TYPE_OF_BREWERY")
    .agg(count("BREWERY_ID").alias("QUANTITY_OF_BREWERIES_PRESENT_IN_INTERNET"))
)

# Unindo os dois dataframes
internet_presence_with_percentage_df = (
    internet_presence_df.join(
        total_breweries_df, on="TYPE_OF_BREWERY", how="inner"
    )
    .withColumn(
        "PERCENTAGE_PRESENT_IN_INTERNET",
        round(
            (col("QUANTITY_OF_BREWERIES_PRESENT_IN_INTERNET") / col("TOTAL_BREWERIES")) * 100, 2
        )
    )
    .orderBy("PERCENTAGE_PRESENT_IN_INTERNET", ascending=False)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exportação do Dataframe

# COMMAND ----------

# Adicionando coluna de controle de versão.

current_timestamp = current_timestamp()

adjusted_internet_presence_with_percentage_df = internet_presence_with_percentage_df.withColumn("DT_CREATED", current_timestamp).withColumn(
    "DT_UPDATED", current_timestamp
)

# COMMAND ----------

adjusted_internet_presence_with_percentage_df.display()

# COMMAND ----------

# Definir o caminho e nome do arquivo usando a data

full_output_path = os.path.join(output_path, output_filename)

# Salvar o DataFrame em formato Parquet no Azure Blob Storage
internet_presence_with_percentage_df.write.mode("overwrite").parquet(full_output_path) 
