import requests
from pandas.core.interchange.dataframe_protocol import DataFrame

from env import Env
import pandas as pd


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
        print(f"Inicializando busca de Estacoes!\n")
        estacoes_por_municipio = dict()

        estacoes_por_municipio[lista_municipios[0]] = self.busca_estacoes_integerers(municipio=lista_municipios[0],token=token)
        for municipio in lista_municipios[1:]:
            estacoes_por_municipio[municipio] = self.busca_estacoes_integerers(municipio=municipio,token=token)
        print(f"\nBusca de Estacoes finalizada!\n")

        # Formatação dos códigos de estação por município
        codigos_das_estacoes = self.filtra_estacoes_pluviometricas(estacoes_por_municipio,lista_municipios)

        # Busca dados de pluviometria por estação
        df_pluviometria = self.busca_chuva_por_estacao(dict_estacoes=codigos_das_estacoes,token=token, lista_municipios=lista_municipios)
        print(df_pluviometria)

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
        print(f"Buscando codigos de estação do municipio : {municipio}")
        path = '/EstacoesTelemetricas/HidroInventarioEstacoes/v1'
        response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Unidade Federativa': municipio})
        response=response.json()
        return response

    def filtra_estacoes_pluviometricas(self,dict_estacoes,lista_municipios):
        print(f"Inicializando formatação de código de Estacoes por município")

        estacoes_pluviometricas = dict()
        for municipio in lista_municipios:
            estacoes_pluviometricas[municipio] = []
            for el in dict_estacoes[municipio]['items']:
                if el['Tipo_Estacao_Pluviometro'] == '1':
                    estacoes_pluviometricas[municipio].append(el['codigoestacao'])

        print(f"Formatação de códigos de Estacoes concluída!\n")
        return estacoes_pluviometricas


    def busca_chuva_por_estacao(self,dict_estacoes : dict ,token : str, lista_municipios: list):
        """
        A busca de pluviometria é feita por cada metade do ano, pois a requisião só aceita buscas de um intervalo de no máximo de 6 meses.
        """
        print(f"Inicializando busca pluviometria por Estacoes")

        path = '/EstacoesTelemetricas/HidroSerieChuva/v1'

        df_pluviometria = pd.DataFrame()

        for municipio in lista_municipios:
            print(f"Buscando dados de pluviometria do municipio {municipio}")
            codigos = dict_estacoes[municipio]
            for codigo in codigos:
                print(f"Buscando dados para a estação {codigo}")
                for ano in range(2024, 2023, -1): #TODO Alterar para 1990
                    print(f"Buscando para o ano {ano}")

                    # Primeira metade do ano
                    response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-01-01", 'Data Final (yyyy-MM-dd)': f"{ano}-06-01", 'Código da Estação':int(codigo)})
                    response = response.json()
                    if response['message'] == "Não houve retorno de registros. Verifique!":
                        print("\nNão houve registros a partir desse ano.\nPassando para o próximo código de estação.\n")
                        break

                    df_primeira_metade = pd.DataFrame(response["items"])
                    df_pluviometria = pd.concat([df_pluviometria, df_primeira_metade], ignore_index=True)

                    # Segunda metade do ano
                    response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-07-01", 'Data Final (yyyy-MM-dd)': f"{ano}-12-01", 'Código da Estação':int(codigo)})
                    response = response.json()
                    df_segunda_metade = pd.DataFrame(response["items"])
                    df_pluviometria = pd.concat([df_pluviometria, df_segunda_metade], ignore_index=True)
                    print(df_pluviometria)
                    df_pluviometria = self.transformar_chuva(df_pluviometria)
                    print(df_pluviometria)

        print(df_pluviometria)

        print(f"Formatação de códigos de Estacoes concluída!\n")
        return df_pluviometria

    def transformar_chuva(self, df: pd.DataFrame):
        # Lista para armazenar as novas linhas
        novas_linhas = []

        # Iterando sobre as linhas do DataFrame
        for i, row in df.iterrows():
            # Pega o ano da data_hora_dado
            data_base = pd.to_datetime(row['Data_Hora_Dado'])
            ano = data_base.year
            mes = data_base.month

            # Iterando sobre as colunas de chuva (chuva_01, chuva_02, ..., chuva_31)
            for dia in range(1, 32):
                # Nome da coluna de chuva
                chuva_coluna = f'Chuva_{str(dia).zfill(2)}'  # Ex: 'chuva_01', 'chuva_02', etc.
                if chuva_coluna in row:
                    try:
                        nova_data = data_base.replace(year=ano, month=mes, day=dia)
                        nova_linha = {
                            'data': nova_data,  # Data com o dia e mês ajustados
                            'chuva': row[chuva_coluna]  # Valor de chuva correspondente
                        }
                        novas_linhas.append(nova_linha)
                    except ValueError:
                        pass

        # Cria o novo DataFrame
        df_novo = pd.DataFrame(novas_linhas)

        return df_novo


if __name__ == "__main__":
    classe = ApiAnaGov()
    classe.main()
