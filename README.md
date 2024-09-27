# Análise de Cervejarias no Azure Databricks

## Índice
1. [Objetivo](#objetivo)
2. [Arquitetura Geral](#arquitetura-geral)
3. [Detalhes da Arquitetura Medalhão](#detalhes-da-arquitetura-medalhão)
   - [Camada Bronze](#camada-bronze)
   - [Camada Silver](#camada-silver)
   - [Camada Gold](#camada-gold)
4. [Processo de Agregação e Transformações](#processo-de-agregação-e-transformações)
   - [Total de Cervejarias por País e Província](#total-de-cervejarias-por-país-e-província)
   - [Cálculo de Cervejarias Fechadas](#cálculo-de-cervejarias-fechadas)
   - [Presença Online das Cervejarias](#presença-online-das-cervejarias)
5. [Criação e Configuração de Tabelas Delta](#criação-e-configuração-de-tabelas-delta)
6. [Visualizações e Dashboards](#visualizações-e-dashboards)

---
## Objetivo do Projeto
O principal objetivo do projeto é construir um pipeline de dados eficiente e escalável para processar, transformar e analisar informações sobre cervejarias, contemplando:

- Integração e transformação de dados para facilitar a análise de cervejarias por país e província.
- Cálculo de métricas relevantes, como o percentual de cervejarias fechadas por região.
- Avaliação da presença online das cervejarias para identificar tendências de mercado digital.
- Construção de visualizações e dashboards interativos para simplificar a exploração dos dados e apoiar decisões baseadas em insights.

## Arquitetura Geral
![Arquitetura](./imagens/Arquitetura.png)

A arquitetura do projeto é composta pelos seguintes componentes:

**Azure Databricks:** Utilizado para realizar as transformações de dados (ETLs) e para criar painéis de visualização interativos. Um cluster Spark é configurado para processar os dados de forma eficiente.

**GitHub Actions:** Gerencia o processo de CI/CD (Integração Contínua e Entrega Contínua) para manter o código atualizado e garantir a implantação automatizada dos notebooks e pipelines.

**Azure Data Lake (Blob Storage):** Armazena os dados em diferentes camadas (Bronze, Silver e Gold), permitindo o versionamento e a separação de dados brutos, processados e prontos para análise.

**Azure Data Factory:** Orquestra a execução dos notebooks no Databricks, garantindo a automação e o agendamento dos processos ETL.

**Azure Monitor:** Ferramenta para coleta de logs e métricas de execução, desempenho e falhas dos componentes da arquitetura, incluindo Data Factory, Databricks, e Blob Storage. Pode ser configurado com alertas e dashboards para monitorar o status do pipeline e qualidade dos dados em tempo real.

# CI/CD com GitHub Actions para Databricks

## Visão Geral
Este projeto utiliza o **GitHub Actions** para gerenciar o processo de CI/CD dos notebooks do **Azure Databricks**. O fluxo de trabalho garante que os notebooks sejam testados, validados e executados automaticamente sempre que houver alterações no repositório.

## Fluxo de CI/CD
![Fluxograma CI_CD](./imagens/Fluxograma_ci_cd.png)


### 1. Integração com o GitHub
O **Azure Databricks** está integrado ao repositório GitHub, permitindo versionamento e controle de código dos notebooks. Isso facilita o rastreamento de mudanças, revisões de código e colaborações entre desenvolvedores.
![Exemplo de Integração com o Databricks](./imagens/commit_databricks.png)

### 2. Detecção de Mudanças via Pull Request (PR) na Branch `dev`
Sempre que um **Pull Request (PR)** é criado ou atualizado na branch `dev`, o GitHub Actions é acionado para iniciar o processo de CI/CD.

- O fluxo detecta quais notebooks foram alterados no PR.

### 3. Formatação Automática com Black
Os notebooks Python são automaticamente formatados com o **Black** para garantir que o código segue um padrão consistente e legível.

- **Black** aplica padrões de estilo (PEP 8) para padronizar o layout do código.

### 4. Validação de Qualidade de Código com Flake8
Após a formatação, os notebooks passam por uma verificação de qualidade de código com o **Flake8**.

- **Flake8** verifica:
  - Estilo e formatação do código (conformidade com PEP 8).
  - Problemas de complexidade.
  - Possíveis bugs ou práticas de codificação incorretas.

### 5. Execução dos Notebooks Alterados no Databricks
Os notebooks que passaram pelas etapas de formatação e validação são executados como **jobs no Databricks**.

- A execução é feita diretamente via API do Databricks, iniciando jobs para cada notebook alterado.
- Isso garante que todas as mudanças de código sejam testadas na prática.

### 6. Acompanhamento de Execução via Workflows no Databricks
Os jobs do Databricks podem ser monitorados pela **interface de workflows**, onde é possível visualizar o status de execução:

- **Status dos Jobs**: Acompanhar se o job foi concluído com sucesso ou falhou.
- **Logs Detalhados**: Visualizar erros, exceções e tempo de execução.
  
Isso permite garantir que todas as alterações foram testadas antes de serem mescladas ou implantadas.

![Workflow](./imagens/workflow_jobs.png)

# Uso do Azure Blob Storage no Pipeline

![Blob Storage](./imagens/blob_storage_container.png)

O **Azure Blob Storage** atua como a principal camada de armazenamento para dados em diferentes etapas do pipeline (Bronze, Silver, Gold):

### Formato Delta
Os dados são armazenados no formato **Delta Lake** para oferecer transações seguras, controle de versão e melhor desempenho de leitura e escrita.

### Partitionamento e Organização
- **Partitionamento**: Dados particionados por `COUNTRY_NAME` e `STATE_PROVINCE` para otimizar consultas.
- **Estrutura de Caminhos**: Dados organizados em `/BRONZE/`, `/SILVER/` e `/GOLD/` para fácil gerenciamento e acesso.

### Integração com Databricks
- O Blob Storage serve como fonte e destino para leitura e escrita dos dados transformados em todas as camadas do pipeline de ETL.

# Detalhes da Arquitetura Medalhão

### Camada Bronze
- **Objetivo**: Armazenar dados brutos coletados de várias fontes.
- **Processo**: Ingestão dos dados de cervejarias e armazenamento como arquivos **Delta** no Azure Blob Storage.


### Camada Silver
- **Objetivo**: Limpar e transformar dados da camada Bronze.
- **Processo**: Remoção de duplicatas, padronização de tipos de dados e enriquecimento dos dados para análises.


### Camada Gold
- **Objetivo**: Agregar e calcular métricas importantes para análise de negócios.
- **Processo**: Transformações finais para criar conjuntos de dados para relatórios.


## Processo de Agregação e Transformações

### Total de Cervejarias por País e Província
- **Descrição**: Agrupar todas as cervejarias por país e província, contando o total para cada combinação.


### Cálculo de Cervejarias Fechadas
- **Descrição**: Filtrar todas as cervejarias fechadas e agrupar por país e província.


### Presença Online das Cervejarias
- **Descrição**: Analisar a presença online das cervejarias (informações de website e telefone).


## Criação e Configuração de Tabelas Delta
- **Objetivo**: Salvar os resultados finais em tabelas Delta para consultas SQL no Hive Metastore.


## Visualizações e Dashboards
Os dashboards interativos foram criados no DataBricks a partir de consultas SQL executadas no Hive Metastore para explorar os dados de forma dinâmica e visual. Abaixo estão as visualizações desenvolvidas:

### Painéis Criados
1. **Painel 1: Quantidade de cervejarias por tipo e localização.**
   ![Porcentagem de Cervejarias Fechadas](./imagens/graph_1_breweries_by_type_location.png)

2. **Painel 2: Porcentagem de cervejarias inativas por país**
   ![Distribuição de Presença Online](./imagens/graph_2_closed_breweries_by_country.png)

3. **Painel 3: Análise de presença online por tipo de cervejaria**
   ![Total vs. Presença Online](./imagens/graph_3_internet_presence.png)


Se tiver dúvidas ou precisar de ajustes, por favor, entre em contato! otavioaugustomachadodeoliveira@gmail.com

