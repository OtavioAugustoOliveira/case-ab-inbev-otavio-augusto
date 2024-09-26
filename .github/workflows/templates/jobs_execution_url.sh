#!/bin/bash

# Gerar link de execução de jobs no Databricks
echo "Gerando link de execução de jobs no Databricks..."

# Extrair a instância do Databricks a partir do host
DATABRICKS_INSTANCE=$(echo $DATABRICKS_HOST | grep -oP '(?<=adb-)\d+(?=\.)')
DATABRICKS_JOBS_EXECUTION_URL="${DATABRICKS_HOST}/#joblist/runs?o=${DATABRICKS_INSTANCE}"

# Definir como saída do script para uso no workflow
echo "databricks_jobs_execution_url=$DATABRICKS_JOBS_EXECUTION_URL" >> $GITHUB_OUTPUT

echo "Link de execução de jobs no Databricks gerado."
