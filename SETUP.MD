# Como Executar a Solução

Este guia fornece um passo a passo para configurar o ambiente e executar o pipeline de dados.

## 1. Pré-requisitos
- **Azure Account**: Tenha uma conta ativa no Azure.
- **Permissões Necessárias**: Acesso para criar recursos como Azure Databricks, Data Factory, e Blob Storage.
- **GitHub Account**: Uma conta GitHub para configurar o CI/CD.

## 2. Configuração de Recursos no Azure

### 2.1 Criar Azure Databricks Workspace
- Acesse o portal do Azure e crie um novo workspace do Databricks.
- [Link para Tutorial](https://docs.microsoft.com/azure/databricks/)

### 2.2 Criar Azure Data Factory
- Crie uma instância do Data Factory para orquestrar os pipelines.
- [Link para Tutorial](https://learn.microsoft.com/azure/data-factory/)

## 3. Configurar Blob Storage e Conectar ao Databricks

### 3.1 Criar Blob Storage
- Configure containers para armazenar dados (camadas Bronze, Silver, Gold).
- [Link para Configuração do Blob Storage](https://learn.microsoft.com/azure/storage/blobs/)

### 3.2 Conectar o Databricks ao Blob Storage
- Obtenha a **chave de acesso** do Blob Storage.
- Configure a conexão no Databricks para permitir leitura/escrita.

## 4. Configuração de Integração do Databricks com o Repositório GitHub

### 4.1 Conectar o Databricks ao Repositório GitHub
Para sincronizar os notebooks do Databricks com seu repositório no GitHub, siga estes passos:

1. **Acesse o Databricks Workspace**: 
   - Navegue até a seção **Repos** no menu à esquerda.
2. **Adicionar Novo Repositório**:
   - Clique em **Add Repo** para conectar ao repositório GitHub.
   - **URL do Repositório**: Insira a URL do repositório GitHub que contém os notebooks.
   - **Autenticação**: Use um **token de acesso pessoal** do GitHub para autorizar o acesso ao repositório. [Como Gerar um Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

3. **Sincronizar o Repositório com o Databricks**:
   - Após conectar o repositório, os notebooks serão sincronizados com o Databricks e você poderá editá-los diretamente no ambiente do Databricks ou no GitHub.
   - **Branches**: Certifique-se de trabalhar na branch correta (`dev`, `main`, etc.) para que o CI/CD funcione corretamente.

## 5. Configuração de CI/CD com GitHub Actions

### 5.1 Configurar Secrets no Repositório GitHub
Para permitir que o GitHub Actions interaja com o Databricks, crie os seguintes **secrets** no repositório do GitHub:

- **`DATABRICKS_HOST`**: A URL do seu workspace no Databricks (por exemplo, `https://<your-workspace>.azuredatabricks.net`).
- **`DATABRICKS_TOKEN`**: Um token de acesso pessoal gerado no Databricks, que permite que o GitHub Actions acesse seu workspace.
- **`EXISTING_CLUSTER_ID`**: O ID do cluster Databricks que será utilizado para executar os notebooks.

### 5.2 Configurar o Workflow no GitHub Actions
- Adicione um arquivo de workflow (`.github/workflows/ci_cd.yml`) no seu repositório para definir as etapas do CI/CD.
  - Certifique-se de incluir etapas para:
    - Formatar notebooks com **Black**.
    - Validar o código com **Flake8**.
    - Executar notebooks no Databricks via API usando os secrets configurados.

## 6. Configurar e Executar Pipelines no Data Factory

### 6.1 Importar Notebooks para Data Factory
- Crie pipelines para cada camada (Bronze, Silver, Gold) e importe os notebooks de transformação.

### 6.2 Criar Pipeline Principal
- Adicione um pipeline mestre que execute todos os pipelines de camada sequencialmente.

### 6.3 Adicionar Trigger e Retry
- Configure triggers para execução diária.
- Configure retries na camada Bronze para lidar com dependências de API.

## 7. Verificação Final
- Verifique se os pipelines estão agendados e rodando corretamente.
- Certifique-se de que os dados estão sendo salvos no Blob Storage e que você pode visualizá-los no Databricks.
