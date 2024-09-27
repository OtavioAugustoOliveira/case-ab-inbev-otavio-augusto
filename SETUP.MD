# Como Executar a Solução

Este guia fornece um passo a passo para configurar o ambiente e executar o pipeline de dados.

## 1. Pré-requisitos
- **Azure Account**: Tenha uma conta ativa no Azure.
- **Permissões Necessárias**: Acesso para criar recursos como Azure Databricks, Data Factory, e Blob Storage.

## 2. Configuração de Recursos no Azure
1. **Criar Azure Databricks Workspace**
   - Acesse o portal do Azure e crie um novo workspace do Databricks.
   - [Link para Tutorial](https://docs.microsoft.com/azure/databricks/)

2. **Criar Azure Data Factory**
   - Crie uma instância do Data Factory para orquestrar os pipelines.
   - [Link para Tutorial](https://learn.microsoft.com/azure/data-factory/)

## 3. Configurar Blob Storage e Conectar ao Databricks
1. **Criar Blob Storage**
   - Configure containers para armazenar dados (camadas Bronze, Silver, Gold).
   - [Link para Configuração do Blob Storage](https://learn.microsoft.com/azure/storage/blobs/)

2. **Conectar o Databricks ao Blob Storage**
   - Obtenha a **chave de acesso** do Blob Storage.
   - Configure a conexão no Databricks para permitir leitura/escrita.

## 4. Configurar e Executar Pipelines no Data Factory
1. **Importar Notebooks para Data Factory**
   - Crie pipelines para cada camada e importe os notebooks de transformação.

2. **Criar Pipeline Principal**
   - Adicione um pipeline mestre que execute todos os pipelines de camada sequencialmente.

3. **Adicionar Trigger e Retry**
   - Configure triggers para execução diária.
   - Configure retries na camada Bronze para lidar com dependências de API.

## 5. Verificação Final
- Verifique se os pipelines estão agendados e rodando corretamente.
- Certifique-se de que os dados estão sendo salvos no Blob Storage e que você pode visualizá-los no Databricks.
