#!/bin/bash

# Ajuste de formatação e teste de qualidade nos notebooks alterados
IFS=' ' read -r -a changed_files <<< "$changed_files"

# Ajuste de formatação
echo "Iniciando ajuste de formatação nos notebooks alterados..."
for notebook in "${changed_files[@]}"; do
  echo "Realizando ajuste automático no notebook $notebook"
  black "$notebook"
done
echo -e "Ajuste de formatação concluído. \n"

# Teste de qualidade
status=0
echo "Iniciando teste de qualidade nos notebooks alterados..."
for notebook in "${changed_files[@]}"; do
  echo -e "Aplicando teste de qualidade no notebook $notebook"
  
  if flake8 --show-source --format=pylint --color=always "$notebook"; then
    echo -e "\nTeste no notebook $notebook finalizado com sucesso.\n"
  else
    status=$?
    echo -e "\nErro! Teste no notebook $notebook falhou!\n"
  fi
done

# Retorna o código de saída armazenado
exit $status
