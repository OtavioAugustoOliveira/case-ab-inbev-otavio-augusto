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
A solução está estruturada em uma arquitetura de **3 camadas de dados** no **Azure Databricks**, usando **Delta Lake**:
1. **Bronze**: Dados brutos coletados.
2. **Silver**: Dados limpos e transformados para análise.
3. **Gold**: Dados finalizados para relatórios e visualizações.

## Detalhes da Arquitetura Medalhão

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
Os dashboards interativos foram criados a partir de consultas SQL executadas no Hive Metastore para explorar os dados de forma dinâmica e visual. Abaixo estão as visualizações desenvolvidas:

### Painéis Criados



Se tiver dúvidas ou precisar de ajustes, por favor, entre em contato! otavioaugustomachadodeoliveira@gmail.com

