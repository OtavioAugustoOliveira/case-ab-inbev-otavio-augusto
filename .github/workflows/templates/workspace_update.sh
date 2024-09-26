#!/bin/bash

# Atualizar repositório após o Merge
echo "Atualizando o repositório após o merge na branch DEV..."
databricks repos update "$REPO_ID" --branch DEV

echo "Atualização concluída."
