#!/bin/bash

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

echo "Deleção de pasta TEMP concluída."
