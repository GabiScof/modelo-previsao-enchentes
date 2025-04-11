import requests
from env import Env

class ApiAnaGov:
    def __init__(self):
        self.url = 'https://www.ana.gov.br/hidrowebservice'

    def main(self):
        print("\nMODELO-PREVISAO-ENCHENTES : Iniciando resgaste dos dados!\n")

        # Resgatando token de autenticação
        token = self.get_token()

        # Definindo municipios que serão estudados
        lista_municipios = ['AM', 'AP', 'AC', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']

        # Buscando código das estações por município
        estacoes_por_municipio = dict()
        estacoes_por_municipio[lista_municipios[0]] = self.busca_estacoes_integerers(municipio=lista_municipios[0],token=token)
        for municipio in lista_municipios[1:]:
            estacoes_por_municipio[municipio] = self.busca_estacoes_integerers(municipio=municipio,token=token)
        print(estacoes_por_municipio)

        # Formatação dos códigos de estação por município
        codigos_das_estacoes = self.filtra_estacoes_pluviometricas(estacoes_por_municipio,lista_municipios)
        print(codigos_das_estacoes)

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

    def busca_estacoes_integerers(self, municipio: str, token : str):
        path = '/EstacoesTelemetricas/HidroInventarioEstacoes/v1'
        print(f"Inicializando busca de Estacoes")
        response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Unidade Federativa': municipio})
        response=response.json()
        print(response)
        print(f"Busca de Estacoes finalizada!\n")
        return response

    def filtra_estacoes_pluviometricas(self,dict_estacoes,lista_municipios):
        print(f"Inicializando formatação de código de Estacoes por município")

        estacoes_pluviometricas = dict()
        for municipio in lista_municipios:
            estacoes_pluviometricas[municipio] = []
            for el in dict_estacoes[municipio]['items']:
                if el['Tipo_Estacao_Pluviometro'] == '1':
                    estacoes_pluviometricas[municipio].append(el['codigoestacao'])
        print(estacoes_pluviometricas)

        print(f"Formatação de códigos de Estacoes concluída!\n")
        return estacoes_pluviometricas


if __name__ == "__main__":
    classe = ApiAnaGov()
    classe.main()
