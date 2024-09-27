# Análise de Cervejarias no Azure Databricks

## Índice
1. [Introdução](#introdução)
2. [Arquitetura Geral](#arquitetura-geral)
3. [Detalhes do Pipeline de Dados](#detalhes-do-pipeline-de-dados)
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

## Introdução
Este projeto tem como objetivo analisar dados de cervejarias a partir de diversas perspectivas, tais como a quantidade total de cervejarias ativas, a porcentagem de cervejarias fechadas e a presença online delas. O processo busca responder a perguntas como: Quais países e regiões têm o maior número de cervejarias fechadas? Ou ainda, Quais tipos de cervejarias estão mais presentes online com informações como site e telefone?.

## Objetivo do Projeto
O objetivo principal é analisar as cervejarias por diferentes dimensões:
- Quantificar o total de cervejarias por **país** e **província**.
- Analisar a porcentagem de cervejarias fechadas.
- Estudar a presença online das cervejarias (com base em informações de URL e telefone).
- Criar visualizações e dashboards para insights sobre a distribuição das cervejarias.

## Arquitetura Geral
A solução está estruturada em uma arquitetura de **3 camadas de dados** no **Azure Databricks**, usando **Delta Lake**:
1. **Bronze**: Dados brutos coletados.
2. **Silver**: Dados limpos e transformados para análise.
3. **Gold**: Dados finalizados para relatórios e visualizações.

## Detalhes do Pipeline de Dados

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

