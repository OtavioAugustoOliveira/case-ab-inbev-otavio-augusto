# Databricks notebook source
# MAGIC %md
# MAGIC ## Setup de Ambiente

# COMMAND ----------

import requests
import os
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import current_timestamp

# COMMAND ----------

# MAGIC %md
# MAGIC ## Definição de Parâmetros

# COMMAND ----------

dbutils.widgets.removeAll()

# COMMAND ----------

dbutils.widgets.text('output_path', 'wasbs://case-ab-inbev-container@caseabinbev.blob.core.windows.net/BRONZE/')
dbutils.widgets.text('output_filename', 'bronze_openbreweries')

# COMMAND ----------

output_path = dbutils.widgets.get('output_path')
output_filename = dbutils.widgets.get('output_filename')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Extração via API

# COMMAND ----------

# Definir a URL base
base_url = "https://api.openbrewerydb.org/v1/breweries"
all_breweries = []

# Parâmetros iniciais
page = 1
per_page = 200  # Manter 200 por página para maximizar a eficiência

while True:
    # Requisição GET para a API com paginação
    response = requests.get(base_url, params={"page": page, "per_page": per_page})

    # Verificar se a requisição foi bem-sucedida
    if response.status_code != 200:
        print(f"Erro na página {page}: {response.status_code}")
        break

    # Extrair os dados da resposta
    data = response.json()

    # Se não houver mais dados, parar a iteração
    if not data:
        print("Todos os dados foram buscados.")
        break

    # Adicionar os dados da página atual à lista total
    all_breweries.extend(data)

    # Imprimir status
    print(f"Dados da página {page} buscados com sucesso.")

    # Incrementar o número da página
    page += 1



# COMMAND ----------

# Definir o esquema do DataFrame para corresponder aos campos de dados
schema = StructType(
    [
        StructField("id", StringType(), True),
        StructField("name", StringType(), True),
        StructField("brewery_type", StringType(), True),
        StructField("address_1", StringType(), True),
        StructField("address_2", StringType(), True),
        StructField("address_3", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state_province", StringType(), True),
        StructField("postal_code", StringType(), True),
        StructField("country", StringType(), True),
        StructField("longitude", StringType(), True),
        StructField("latitude", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("website_url", StringType(), True),
        StructField("state", StringType(), True),
        StructField("street", StringType(), True),
    ]
)

# Converter a lista de dicionários em um DataFrame do PySpark
df_breweries = spark.createDataFrame(all_breweries, schema)



# COMMAND ----------

# Exibir a quantidade total de registros
print(f"Total de cervejarias encontradas: {df_breweries.count()}")

# COMMAND ----------

# Adicionando coluna de controle de versão.

current_timestamp = current_timestamp()

bronze_df = df_breweries.withColumn("DT_CREATED", current_timestamp).withColumn(
    "DT_UPDATED", current_timestamp
)

                                                   

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exportação do Dataframe

# COMMAND ----------

# Definir o caminho e nome do arquivo usando a data

full_output_path = os.path.join(output_path, output_filename)


# Salvar o DataFrame em formato Delta no Azure Blob Storage
bronze_df.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("path", full_output_path) \
    .saveAsTable("BRONZE_BREWERY")


# COMMAND ----------

#teste
