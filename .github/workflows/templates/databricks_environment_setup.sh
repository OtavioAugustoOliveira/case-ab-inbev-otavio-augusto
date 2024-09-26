#!/bin/bash

# Instalar Databricks CLI
echo "Instalando Databricks CLI..."
curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh
echo "Instalação do Databricks CLI concluída."

# Exportar variáveis de ambiente explicitamente
export DATABRICKS_HOST=$DATABRICKS_HOST
export DATABRICKS_TOKEN=$DATABRICKS_TOKEN

# Configurar o Databricks CLI para usar o método de token em modo não interativo
echo "Configurando o Databricks CLI para usar o método de token..."
echo "$DATABRICKS_TOKEN" | databricks configure --host "$DATABRICKS_HOST"


# Testar a autenticação e listar os clusters
echo "Clusters list: $(databricks clusters list)"


# Deletar a pasta /TEMP no Workspace caso ela exista.
echo "Verificando existência da pasta /TEMP no Workspace..."
FOLDERS=$(databricks workspace list //)
if [[ $FOLDERS == *"/TEMP"* ]]; then
  echo "Pasta /TEMP encontrada. Removendo..."
  databricks workspace delete --recursive /TEMP
  echo "Pasta /TEMP removida com sucesso."
else
  echo "Pasta /TEMP não encontrada. Nenhuma ação necessária."
fi

# Criar pasta /TEMP no Workspace
echo "Criando pasta /TEMP no Workspace..."
databricks workspace mkdirs /TEMP

# Fazer upload de cada notebook alterado para a pasta TEMP
IFS=' ' read -r -a changed_files <<< "$changed_files"
for notebook in "${changed_files[@]}"; do
  echo "Fazendo upload de $notebook para Workspace/TEMP"
  databricks workspace import --format SOURCE --language PYTHON --file "$notebook" /TEMP/$(basename "$notebook")
done

echo "Upload de notebooks concluído."

