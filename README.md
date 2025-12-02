# PRF Accident Clustering
**Análise Comportamental e Geoespacial de Acidentes Rodoviários Federais (2007-2024)**

Este repositório contém um projeto de Ciência de Dados *end-to-end* que aplica técnicas de aprendizado não-supervisionado para identificar padrões de acidentalidade nas rodovias federais brasileiras. O projeto utiliza um pipeline automatizado de Engenharia de Dados para processar 18 anos de dados públicos da Polícia Rodoviária Federal (PRF), superando desafios de inconsistência de *schema* e dados legados.

## Tópicos
- [Visão Geral e Objetivos](#visão-geral-e-objetivos)
- [Arquitetura da Solução](#arquitetura-da-solução)
- [Engenharia de Dados (ETL)](#engenharia-de-dados-etl)
- [Metodologia de Clusterização](#metodologia-de-clusterização)
- [Resultados: Perfis e Hotspots](#resultados-perfis-e-hotspots)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Autor](#autor)

## Visão Geral e Objetivos
A segurança viária é um desafio crítico no Brasil. O objetivo deste trabalho é ir além das estatísticas descritivas básicas e responder a duas perguntas fundamentais:
1.  **O QUE acontece?** (Quais são os perfis típicos de acidentes?)
2.  **ONDE acontece?** (Onde estão os pontos de alta letalidade?)

Para isso, utilizamos algoritmos de *Machine Learning* para segmentar os acidentes em grupos comportamentais e identificar *hotspots* geográficos de risco.

## Arquitetura da Solução
A solução foi construída sobre três pilares:
1.  **Ingestão Automatizada:** Uso de *n8n* e *Docker* para orquestrar o download e extração de dados brutos.
2.  **Harmonização de Dados:** Scripts Python para unificar *schemas* divergentes (2007-2016 vs. 2017-2024) e tratar dados nulos.
3.  **Modelagem Híbrida:** Uso de *K-Prototypes* para dados tabulares mistos e *DBSCAN* para dados geoespaciais.

## Engenharia de Dados (ETL)
O processo de ETL foi desenhado para ser resiliente e escalável. A ferramenta *n8n* foi utilizada para criar um fluxo visual que realiza o *scraping* do portal de dados abertos, baixa os arquivos ZIP anuais, extrai os CSVs e os organiza em um *Data Lake* local.

![Fluxo de Automação ETL no n8n](img/n8n_workflow.png)
*Figura 1: Pipeline de orquestração no n8n.*

**Desafios Superados:**
* **Schema Drift:** Os dados anteriores a 2017 não possuíam coordenadas geográficas padronizadas e utilizavam separadores decimais diferentes.
* **Qualidade dos Dados:** Tratamento extensivo de campos de texto livre (ex: "Falta de Atenção" vs "falta de atencao") e remoção de coordenadas inválidas (pontos fora do Brasil).

## Metodologia de Clusterização
A análise foi dividida em duas frentes complementares:

### Cluster A: Análise Comportamental
Utilizou-se o algoritmo **K-Prototypes** para agrupar acidentes com base em características mistas (numéricas e categóricas), como tipo de pista, clima, horário e severidade. O número ideal de clusters (K=6) foi determinado pelo Método do Cotovelo (*Elbow Method*).

![Método do Cotovelo](img/elbow_method.png)
*Figura 2: Definição do número ideal de clusters.*

### Cluster B: Análise Geoespacial
Utilizou-se o algoritmo **DBSCAN** com distância de Haversine para identificar aglomerados de alta densidade (*hotspots*) ao longo das rodovias. Diferentes cenários foram testados:
* **Micro (0.2km):** Para detectar curvas ou pontos específicos de alta letalidade.
* **Macro (5.0km):** Para identificar regiões metropolitanas ou trechos longos de saturação.

## Resultados: Perfis e Hotspots

### Taxonomia dos Acidentes (Cluster A)
Foram identificados 6 perfis distintos de acidentes:
1.  **O Acidente Padrão (63.9%):** Colisões traseiras leves em retas e tempo bom.
2.  **A Tangente da Curva (19.3%):** Saídas de pista em curvas, com média letalidade.
3.  **Conflito Urbano (7.1%):** Colisões transversais em cruzamentos.
4.  **Tragédia de Massa (5.4%):** Múltiplos veículos e vítimas, com **letalidade 4x superior à média**.
5.  **Risco do Relevo (3.4%):** Acidentes em serras e declives.
6.  **Gargalo de Obra (0.9%):** Ocorrências em desvios ou estreitamento de pista.

### Mapeamento de Hotspots (Cluster B)
A análise geoespacial permitiu localizar com precisão os pontos críticos. O mapa abaixo destaca os clusters, onde a cor vermelha indica a presença de vítimas fatais.

![Mapa de Hotspots](img/mapa_hotspots.png)
*Figura 3: Distribuição dos clusters de acidentes na malha viária brasileira.*

## Como Executar o Projeto

### Pré-requisitos
* Docker e Docker Compose
* Python 3.10+
* Jupyter Notebook

### Passo 1: Iniciar o Pipeline de Dados (n8n)
O ambiente de orquestração (n8n + Postgres) é containerizado. Na raiz do projeto, execute o comando para construir e subir os serviços:

```bash
docker compose up --build -d
```

Após a inicialização, acesse a interface do n8n em:

http://localhost:5678

#### Configuração do Workflow:

No n8n, vá em "Workflows" > "Import from File".

Selecione o arquivo localizado em workflows/prf_downloader.json.

Ative e execute o workflow para iniciar o download dos dados para a pasta data/raw.

### Passo 2: Executar as Análises (Jupyter)
Com os dados baixados, execute os notebooks na seguinte ordem:

analytics.ipynb: Realiza a limpeza, harmonização e gera o arquivo df_final_processed.pkl.

cluster_A.ipynb: Executa o K-Prototypes e gera os perfis comportamentais.

cluster_B.ipynb: Executa o DBSCAN, gera os mapas HTML e realiza a análise cruzada (DNA do Hotspot).

## Estrutura de Arquivos

```
	PRF-Accident-Clustering/
	│
	├── arquivos_prf/
	│   ├── raw/					# Arquivos ZIP originais (Baixados pelo n8n)
	│   ├── csv/					# Arquivos CSV (Extraídos pelo n8n)
	│   └── dict/					# Dicionário dos dados (Baixados pelo n8n)
	│
	├── data/
	│   ├── .pkl/					# Arquivos Pickle ou ZIPs se disponível (Processados pelo analytics.ipynb e Cluster A)
	│   └── maps/					# Mapas HTML (Gerados pelo Cluster B)
	│
	├── img/						# Imagens para documentação
	│
	├── scripts/
	│   ├── analytics.ipynb			# ETL e Engenharia de Features
	│   ├── cluster_A.ipynb			# Modelagem Comportamental
	│   └── cluster_B.ipynb			# Modelagem Geoespacial
	│   └── decompress.py			# Script usado pelo n8n (Para descompressão correta dos arquivos)
	│
	├── view/
	│   ├── .html					# Recorte da página da PRF para visualização para extração dos links
	│
	├── workflows/
	│   └── prf_downloader.json		# Workflow do n8n exportado
	│
	├── docker-compose.yml			# Configuração do ambiente n8n
	│
	└── README.md					# Esse arquivo
```

## Autor

Vinícius Santos Monteiro
* [GitHub - Projeto PRF - Accident Clustering](https://github.com/vini-mon/PRF-Accident-Clustering)

* [LinkedIn](https://www.linkedin.com/in/vinicius-santos-monteiro-a3a88a1aa/)


---
