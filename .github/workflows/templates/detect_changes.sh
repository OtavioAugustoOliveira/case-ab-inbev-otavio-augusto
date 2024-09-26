#!/bin/bash
# Detect changes in Python files
CHANGED_FILES=($(git diff --name-only --diff-filter=d HEAD~1 HEAD | grep '.py' || true))
if [ ${#CHANGED_FILES[@]} -ne 0 ]; then
  CHANGED_FILES_STR="${CHANGED_FILES[*]}"
  echo "Changed Python files:"
  for file in "${CHANGED_FILES[@]}"; do
    echo "$file"
  done
  # Define output for GitHub Actions
  echo "changed_files=$CHANGED_FILES_STR" >> $GITHUB_ENV
else
  echo "Nenhum arquivo .py alterado."
  exit 1
fi