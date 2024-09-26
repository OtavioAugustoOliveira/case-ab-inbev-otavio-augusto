#!/bin/bash

# Função responsável por criar um job de execução.                                                                                    
create_job() {
  notebook_name=$1
  cluster_id=$2

  echo "Criando o job para $notebook_name..." >&2
  job_creation_response=$(databricks jobs create --json "{
    \"name\": \"Teste de execução via GitHub Actions - $notebook_name\",
    \"tasks\": [
      {
        \"task_key\": \"task_$(basename "$notebook_name" .py)\",
        \"existing_cluster_id\": \"$cluster_id\",
        \"notebook_task\": {
          \"notebook_path\": \"/Workspace/TEMP/$notebook_name\"
        }
      }
    ]
  }")

  # Validando criação do job.
  job_id=$(echo "$job_creation_response" | jq -r '.job_id')
  if [ -z "$job_id" ] || [ "$job_id" == "null" ]; then
    echo "Falha na criação do job para $notebook_name. Resposta: $job_creation_response" >&2
    exit 1
  else
    echo -e "Criação do job concluída com sucesso." >&2
  fi

  echo "$job_id"
}

# Função responsável por testar a execução do job.
run_job() {
  job_id=$1
  echo "Executando job de ID: $job_id..." >&2
  run_response=$(databricks jobs run-now $job_id)

  # Validando execução do job.
  if [ -z "$run_response" ]; then
    echo -e "Execução do job falhou.\n" >&2
    exit 1
  fi

  # Verificando se o job foi executado com sucesso.
  run_id=$(echo "$run_response" | jq -r '.run_id')
  job_result_state=$(echo "$run_response" | jq -r '.state.result_state')

  if [ "$job_result_state" == "SUCCESS" ]; then
    echo -e "Execução do job concluída com sucesso.\n" >&2
  elif [ "$job_result_state" != "SUCCESS" ]; then
    echo -e "Execução do job falhou.\n" >&2
    exit 1
  fi

  echo "$run_id"
}

# Definição inicial de variáveis
cluster_id="$EXISTING_CLUSTER_ID"

IFS=' ' read -r -a changed_files <<< "$changed_files"

for notebook_path in "${changed_files[@]}"; do
  notebook_name=$(basename "$notebook_path")
  
  echo "Executando notebook: $notebook_name no cluster: $cluster_id" >&2

  job_id=$(create_job $notebook_name $cluster_id)
  run_id=$(run_job $job_id)
done
