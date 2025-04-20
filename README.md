# Hidro WebService Utils

Funções em Python para facilitar o acesso à **API Hidro WebService da ANA** (Agência Nacional de Águas e Saneamento Básico).  
Este projeto visa permitir que outras pessoas reutilizem essas funções para obter dados hidrológicos, como níveis de rios, vazão, precipitação, entre outros.

---
<br>

 
## 🔧 Funcionalidades

- Busca de códigos de estação por município
- Filtragem de estação por aquelas que possuem dados pluviométricos
- Consulta de dados pluviométricos por estação e mês e ano
- Conversão dos dados para DataFrame do Pandas
- Tratamento e formatação de datas e valores
- Suporte para múltiplas variáveis hidrológicas
<br><br>


## 🔐 Configuração
Antes de usar as funções, você precisa configurar suas credenciais da API HidroWebService.
1. Abra o arquivo `env.py` localizado na raiz do projeto.
2. Preencha os campos `ID` e `SENHA` com os seus dados de login do site da ANA.
<br><br>


## 📚 Documentação
A documentação da API original está disponível em:
🔗 [Swagger Hidro Webservice](https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html#/WSEstacoesTelemetricasController/oAUth)
<br><br>

   
## Pré-requisitos
- Ter uma conta ativa no site do Hidro WebService da ANA.
- Python 3.8 ou superior
- Instalar os pacotes listados em requirements.txt
<br><br>

## 🚀 Modos de Execução
Este projeto oferece dois modos principais de execução para facilitar a coleta de dados conforme sua necessidade de processamento:
<br><br>

🟢 **1. `main.py`: Processa todos os estados de uma vez.**

Este script executa o fluxo completo de coleta e salvamento dos dados pluviométricos para todos os estados da região coberta pela floresta amazônica, de forma automática.

Uso:

```bash
python src/main_all.py
```
Busca os códigos das estações para todos os estados definidos na lista de municípios:
```bash
lista_municipios = ['AM', 'AP', 'AC', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']
```
Salva apenas um arquivo `.csv` final com todos os dados pluviométricos, por dia e mês, de cada estação de cada estado na pasta `data/`.

Gera um arquivo final consolidado: `dados-pluviometricos-final.csv`.

⚠️ Recomendado apenas se sua máquina tiver boa capacidade de processamento e memória.

 <br> <br>
🔵  **2. `main_uf.py`: Processa apenas um estado por vez.**

Ideal para executar o script de forma incremental, estado por estado. Evita sobrecarregar o sistema e facilita a depuração em caso de falha da API.

Uso:

```bash
python src/main_uf.py
```

Gera um arquivo .csv separado para cada estado, salvo na pasta `data/` com o nome do estado. Exemplo: `dados-pluviometricos-AM.csv`

No final, assim como a `main.py`, ele também gera um arquivo final com todos os dados pluviométricos, por dia e mês, de cada estação de cada estado na pasta `data/`: `dados-pluviometricos-final.csv`.
 <br> <br>

## Diferença entre funções de coleta de chuva
Este projeto possui duas funções principais para coletar dados pluviométricos:
<br><br>
📌 **`busca_chuva_por_estacao_e_uf`**

Coleta os dados de todas as estações de uma UF automaticamente.

✅ Utilizado na main_uf.py.

```python
df_am = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos, token=token, uf='AM')
```
<br>

📌 **`busca_chuva_por_estacao`**

Coleta os dados de todas as estações de todas as UFs listadas.

✅ Utilizado na main.py.
```python
lista_municipios = ['AM', 'AP', 'AC', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']
df_pluviometria = api.busca_chuva_por_estacao(dict_estacoes=codigos_estacoes_pluviometricas,token=token, lista_municipios=lista_municipios)
```
 <br> <br>

## Intervalo de Coleta de Dados

Este projeto está configurado para buscar dados de **1990 até 2024** por padrão.

Caso deseje alterar esse intervalo para reduzir o tempo de execução ou focar em anos específicos, você pode editar os parâmetros de data nas funções de coleta localizadas no arquivo `api.py`:
```python
for ano in range(2024, 1990, -1):
```
Esse intervalo pode ser alterado para as funções de coleta: `busca_chuva_por_estacao_e_uf`, `busca_chuva_por_estacao`, `busca_vazao_por_estacao`, `busca_vazao_por_estacao_e_uf`
 <br> <br>


## Exemplo de uso

Buscando códigos de estação apenas em 'AM'

```bash
from src.common.api import ApiAnaGov

def main():
    api = ApiAnaGov()
    token = api.get_token() # Sempre inicializar essa função
    lista_codigos_estacoes = api.busca_estacoes_integerers(municipio = 'AM',token=token)
```
