import requests
from env import Env

class ApiAnaGov:
    def __init__(self):
        self.url = 'https://www.ana.gov.br/hidrowebservice'

    def main(self):
        lista_estacoes = self.busca_estacoes()
        estacoes_amazonia = self.filtra_estacoes(lista_estacoes)
        print(estacoes_amazonia)
        return

    def get_token(self):
        """
        É necessário preencher o Identificador e Senha no arquivo env.py
        """
        print(f"Inicializando resgate do token de autenticacao")
        path = '/EstacoesTelemetricas/OAUth/v1'
        response = requests.get(url = self.url + path, headers={'Identificador': Env.ID, 'Senha': Env.SENHA})
        response = response.json()
        print(f"Token de autenticacao gerado!\n")
        return response['items']['tokenautenticacao']

    def busca_estacoes(self):
        path = '/EstacoesTelemetricas/HidrosatInventarioEstacoes/v1'
        token = self.get_token()
        print(f"Inicializando busca de Estacoes")
        response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token})
        response=response.json()
        print(f"Busca de Estacoes finalizada!\n")
        return response['items']

    def filtra_estacoes(self, lista_estacoes):
        print(f"Inicializando filtragem de Estacoes")
        lista_municipios = ['AC', 'AP', 'AM', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']
        estacoes_amazonia = []
        for el in lista_estacoes:
            if el['UF'] in lista_municipios:
                estacoes_amazonia.append(el)
        print(f"Filtragem de Estacoes concluída!\n")
        return estacoes_amazonia

    def busca_estacoes_integerers(self):
        path = '/EstacoesTelemetricas/HidroInventarioEstacoes/v1'
        token = self.get_token()
        print(f"Inicializando busca de Estacoes")
        response = requests.get(url = self.url + path, headers={'Unidade Federativa': 'AM', 'Authorization': 'Bearer '+token})
        response=response.json()
        print(response)
        print(f"Busca de Estacoes finalizada!\n")
        return response['items']

    def get_vazoes(self,estacoes_amazonia):
        print(f"Inicializando busca de vazões por Estacoes")

        for estacao in estacoes_amazonia:
            if estacao['codigoestacao'] in estacoes_amazonia:
                estacoes_amazonia.append(estacao)
        print(f"Filtragem de Estacoes concluída!\n")
        return estacoes_amazonia

    def df_estacoes_codigo(self):
        path = '/EstacoesTelemetricas/HidroInventarioEstacoes/v1'
        token = self.get_token()
        print(f"Inicializando busca de Estacoes")
        response = requests.get(url = self.url + path, headers={'Código da Bacia': '1', 'Authorization': 'Bearer '+token})
        response=response.json()
        print(response)
        print(f"Busca de Estacoes finalizada!\n")
        return response['items']


if __name__ == "__main__":
    classe = ApiAnaGov()
    classe.main()
    classe.busca_estacoes_integerers()