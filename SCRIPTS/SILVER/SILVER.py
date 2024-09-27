# Databricks notebook source
from pyspark.sql.functions import col, when, trim, initcap, length, lit, row_number, current_timestamp
from pyspark.sql.window import Window
import re
import os

# COMMAND ----------

# MAGIC %md
# MAGIC ## Definição de Parâmetros

# COMMAND ----------

dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text('input_path', 'wasbs://case-ab-inbev-container@caseabinbev.blob.core.windows.net/BRONZE/')
dbutils.widgets.text('input_filename', 'bronze_openbreweries')
dbutils.widgets.text('output_path', 'wasbs://case-ab-inbev-container@caseabinbev.blob.core.windows.net/SILVER/')
dbutils.widgets.text('output_filename', 'silver_openbreweries')

dbutils.widgets.text('output_keys', 'id')




# COMMAND ----------

input_path = dbutils.widgets.get('input_path')
input_filename = dbutils.widgets.get('input_filename')
output_path = dbutils.widgets.get('output_path')
output_filename = dbutils.widgets.get('output_filename')

output_keys = dbutils.widgets.get('output_keys')


# COMMAND ----------

# MAGIC %md
# MAGIC ## Leitura dos dados

# COMMAND ----------

# Realiza a leitura dos dados na camada Bronze

full_input_path = os.path.join(input_path, input_filename)
bronze_df = spark.read.format("delta").load(full_input_path)
   

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sanitização Inicial

# COMMAND ----------

def sanitize_input(df, output_keys):
    input_columns = df.columns
    separator_regex = r',\s*|\s*,\s*'
    keys_list = re.split(separator_regex, output_keys)
    
    window = Window.partitionBy(*keys_list).orderBy(col("DT_CREATED").desc())

    select_cols = []
    for column in input_columns:
        if "_file_" not in column:
            if "." in column:
                column_1 = f'`{column}`'
                select_instance = (
                    when((length(col(column_1)) == 0), lit(None))
                    .otherwise(col(column_1))
                ).alias(column)
            else:
                select_instance = (
                    when((length(col(column)) == 0), lit(None))
                    .otherwise(col(column))
                ).alias(column)
            select_cols.append(select_instance)

    # Aqui usamos o row_number sem orderBy (sem considerar modificação)
    sanitized_df = df.withColumn("__rn__", row_number().over(window)).filter(col("__rn__") == 1).select(*select_cols)
    return sanitized_df

# COMMAND ----------

sanitized_df = sanitize_input(bronze_df, output_keys)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tratamento e normalização dos dados

# COMMAND ----------

#Limpeza e Normalização Inicial

silver_df = sanitized_df.fillna({
    "name": "Unknown Brewery",  
    "city": "Unknown City",      
    "state": "Unknown State",    
    "country": "Unknown Country",
    "address_1":  "Unknown Address",
    "address_2":  "Unknown Address",
    "address_3":  "Unknown Address"
}) 


# COMMAND ----------

#Normalização e Padronização de Strings

silver_df = silver_df.withColumn("name", initcap(trim(col("name")))) \
                     .withColumn("city", initcap(trim(col("city")))) \
                     .withColumn("state", initcap(trim(col("state")))) \
                     .withColumn("country", initcap(trim(col("country")))) \
                     .withColumn("brewery_type", initcap(trim(col("brewery_type"))))

# 4. Remoção de Espaços em Branco nas outras colunas
silver_df = silver_df.withColumn("address_1", trim(col("address_1"))) \
                     .withColumn("address_2", trim(col("address_2"))) \
                     .withColumn("address_3", trim(col("address_3"))) \
                     .withColumn("postal_code", trim(col("postal_code")))

# COMMAND ----------

new_base_columns = [
    col("id").alias("BREWERY_ID"),
    col("name").alias("BREWERY_NAME"),
    col("brewery_type").alias("TYPE_OF_BREWERY"),
    col("address_1").alias("ADDRESS_LINE_1"),
    col("address_2").alias("ADDRESS_LINE_2"),
    col("address_3").alias("ADDRESS_LINE_3"),
    col("city").alias("CITY_NAME"),
    col("state_province").alias("STATE_PROVINCE"),
    col("postal_code").alias("POSTAL_CODE"),
    col("country").alias("COUNTRY_NAME"),
    col("longitude").alias("GEO_LONGITUDE"),
    col("latitude").alias("GEO_LATITUDE"),
    col("phone").alias("CONTACT_PHONE"),
    col("website_url").alias("WEBSITE"),
    col("state").alias("STATE_NAME"),
    col("street").alias("STREET_NAME"),
]

adjusted_silver_df = silver_df.select(new_base_columns)

# COMMAND ----------

# Adicionando coluna de controle de versão.

current_timestamp = current_timestamp()

adjusted_silver_df = adjusted_silver_df.withColumn("DT_CREATED", current_timestamp).withColumn(
    "DT_UPDATED", current_timestamp
)

                                                   

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exportação do Dataframe

# COMMAND ----------

# Definir o caminho e nome do arquivo usando a data

full_output_path = os.path.join(output_path, output_filename)

# Salvar o DataFrame em formato Delta no Azure Blob Storage
adjusted_silver_df.write.format("delta") \
    .mode("overwrite") \
    .partitionBy("COUNTRY_NAME", "STATE_PROVINCE") \
    .option("path", full_output_path) \
    .saveAsTable("SILVER_BREWERY")
