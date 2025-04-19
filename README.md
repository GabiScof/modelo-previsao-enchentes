# HidroWebService Utils

Funções em Python para facilitar o acesso à **API Hidro WebService da ANA** (Agência Nacional de Águas e Saneamento Básico).  
Este projeto visa permitir que outras pessoas reutilizem essas funções para obter dados hidrológicos, como níveis de rios, vazão, precipitação, entre outros.

---

 
## 🔧 Funcionalidades

- Busca de códigos de estação por município
- Filtragem de estação por aquelas que possuem dados pluviométricos
- Consulta de dados pluviométricos por estação e mês e ano
- Conversão dos dados para DataFrame do Pandas
- Tratamento e formatação de datas e valores
- Suporte para múltiplas variáveis hidrológicas


## 🔐 Configuração
Antes de usar as funções, você precisa configurar suas credenciais da API HidroWebService.
1. Abra o arquivo `env.py` localizado na raiz do projeto.
2. Preencha os campos `ID` e `SENHA` com os seus dados de login do site da ANA.


## 📚 Documentação
A documentação da API original está disponível em:
🔗 [Swagger Hidro Webservice](https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html#/WSEstacoesTelemetricasController/oAUth)

   
## Pré-requisitos
- Ter uma conta ativa no site do Hidro WebService da ANA.
- Python 3.8 ou superior
- Instalar os pacotes listados em requirements.txt

## Exemplo de uso

Buscando códigos de estação apenas em 'AM'

```bash
from src.common.api import ApiAnaGov

def main():
    api = ApiAnaGov()
    token = api.get_token() # Sempre inicializar essa função
    lista_codigos_estacoes = api.busca_estacoes_integerers(municipio = 'AM',token=token)
```
