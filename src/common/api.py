import requests
from env import Env
import pandas as pd


class ApiAnaGov:
    def __init__(self):
        self.url = 'https://www.ana.gov.br/hidrowebservice'

    def get_token(self):
        """
        Resgata token de Autenticação.
        --> É necessário preencher o Identificador e Senha no arquivo env.py
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
        print(f"Inicializando formatação de código de Estacoes Pluviométricas por município")

        novas_linhas = []
        estacoes_pluviometricas = dict()
        for municipio in lista_municipios:
            estacoes_pluviometricas[municipio] = []
            for el in dict_estacoes[municipio]['items']:
                if el['Tipo_Estacao_Pluviometro'] == '1':
                    estacoes_pluviometricas[municipio].append(el['codigoestacao'])
                    nova_linha = {
                    'codigo_estacao': el['codigoestacao'],
                    'municipio': el['Municipio_Nome'],
                    'uf': municipio
                    }
                    novas_linhas.append(nova_linha)

        df_estacoes_pluviometricas = pd.DataFrame(novas_linhas)

        print(f"Formatação de códigos de Estacoes Pluviométricas concluída!\n")
        return estacoes_pluviometricas, df_estacoes_pluviometricas

    def filtra_estacoes_de_vazao(self,dict_estacoes,lista_municipios):
        print(f"Inicializando formatação de código de Estacoes de Vazão por município")

        novas_linhas = []
        estacoes_pluviometricas = dict()
        for municipio in lista_municipios:
            estacoes_pluviometricas[municipio] = []
            for el in dict_estacoes[municipio]['items']:
                if el['Tipo_Estacao_Desc_Liquida'] == '1':
                    estacoes_pluviometricas[municipio].append(el['codigoestacao'])
                    nova_linha = {
                        'codigo_estacao': el['codigoestacao'],
                        'municipio': el['Municipio_Nome'],
                        'uf': municipio
                    }
                    novas_linhas.append(nova_linha)

        df_estacoes_vazao = pd.DataFrame(novas_linhas)

        print(f"Formatação de códigos de Estacoes de Vazão concluída!\n")
        return estacoes_pluviometricas, df_estacoes_vazao


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
                for ano in range(2024, 1990, -1):
                    print(f"Buscando para o ano {ano}")

                    # Primeira metade do ano
                    response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-01-01", 'Data Final (yyyy-MM-dd)': f"{ano}-06-01", 'Código da Estação':int(codigo)})
                    if response.status_code == 401:
                        token = self.get_token()
                        response = requests.get(url=self.url + path, headers={'Authorization': 'Bearer ' + token},params={'Tipo Filtro Data': 'DATA_LEITURA','Data Inicial (yyyy-MM-dd)': f"{ano}-01-01",'Data Final (yyyy-MM-dd)': f"{ano}-06-01",'Código da Estação': int(codigo)})
                    response = response.json()
                    if response['message'] == "Não houve retorno de registros. Verifique!":
                        print("\nNão houve registros a partir desse ano.\nPassando para o próximo código de estação.\n")
                        break

                    df_primeira_metade = pd.DataFrame(response["items"])
                    df_primeira_metade = self.transformar_chuva(df_primeira_metade)
                    df_pluviometria = pd.concat([df_pluviometria, df_primeira_metade], ignore_index=True)

                    # Segunda metade do ano
                    response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-07-01", 'Data Final (yyyy-MM-dd)': f"{ano}-12-01", 'Código da Estação':int(codigo)})
                    if response.status_code == 401:
                        token = self.get_token()
                        response = requests.get(url=self.url + path, headers={'Authorization': 'Bearer ' + token},params={'Tipo Filtro Data': 'DATA_LEITURA','Data Inicial (yyyy-MM-dd)': f"{ano}-01-01",'Data Final (yyyy-MM-dd)': f"{ano}-06-01",'Código da Estação': int(codigo)})
                    response = response.json()

                    df_segunda_metade = pd.DataFrame(response["items"])
                    df_segunda_metade = self.transformar_chuva(df_segunda_metade)
                    df_pluviometria = pd.concat([df_pluviometria, df_segunda_metade], ignore_index=True)

        print(f"Formatação de códigos de Estacoes concluída!\n")
        return df_pluviometria

    def busca_chuva_por_estacao_e_uf(self,dict_estacoes : dict ,token : str, uf: str):
        """
        A busca de pluviometria é feita por cada metade do ano, pois a requisião só aceita buscas de um intervalo de no máximo de 6 meses.
        """
        print(f"Inicializando busca pluviometria por Estacoes para o estado: {uf}")

        path = '/EstacoesTelemetricas/HidroSerieChuva/v1'

        df_pluviometria = pd.DataFrame()
        codigos = dict_estacoes[uf]
        tam = len(codigos)
        i = 1
        for codigo in codigos:
            print(f"({i}/{tam})")
            i+=1
            print(f"Buscando dados para a estação {codigo}")
            for ano in range(2024, 1990, -1):
                print(f"Buscando para o ano {ano}")

                # Primeira metade do ano
                response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-01-01", 'Data Final (yyyy-MM-dd)': f"{ano}-06-01", 'Código da Estação':int(codigo)})
                if response.status_code == 401:
                    token = self.get_token()
                    response = requests.get(url=self.url + path, headers={'Authorization': 'Bearer ' + token},params={'Tipo Filtro Data': 'DATA_LEITURA','Data Inicial (yyyy-MM-dd)': f"{ano}-01-01",'Data Final (yyyy-MM-dd)': f"{ano}-06-01",'Código da Estação': int(codigo)})
                response = response.json()
                if response['message'] == "Não houve retorno de registros. Verifique!":
                    print("\nNão houve registros a partir desse ano.\nPassando para o próximo código de estação.\n")
                    break

                df_primeira_metade = pd.DataFrame(response["items"])
                df_primeira_metade = self.transformar_chuva(df_primeira_metade)
                df_pluviometria = pd.concat([df_pluviometria, df_primeira_metade], ignore_index=True)

                # Segunda metade do ano
                response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-07-01", 'Data Final (yyyy-MM-dd)': f"{ano}-12-01", 'Código da Estação':int(codigo)})
                if response.status_code == 401:
                    token = self.get_token()
                    response = requests.get(url=self.url + path, headers={'Authorization': 'Bearer ' + token},params={'Tipo Filtro Data': 'DATA_LEITURA','Data Inicial (yyyy-MM-dd)': f"{ano}-01-01",'Data Final (yyyy-MM-dd)': f"{ano}-06-01",'Código da Estação': int(codigo)})
                response = response.json()

                df_segunda_metade = pd.DataFrame(response["items"])
                df_segunda_metade = self.transformar_chuva(df_segunda_metade)
                df_pluviometria = pd.concat([df_pluviometria, df_segunda_metade], ignore_index=True)

        print(f"Busca de dados pluviométricos para {uf} concluída!\n")
        return df_pluviometria

    def busca_vazao_por_estacao(self,dict_estacoes : dict ,token : str, lista_municipios: list):
        """
        A busca de pluviometria é feita por cada metade do ano, pois a requisião só aceita buscas de um intervalo de no máximo de 6 meses.
        """
        print(f"Inicializando busca pluviometria por Estacoes")

        path = '/EstacoesTelemetricas/HidroSerieVazao/v1'

        df_vazoes = pd.DataFrame()

        for municipio in lista_municipios:
            print(f"Buscando dados de pluviometria do municipio {municipio}")
            codigos = dict_estacoes[municipio]
            for codigo in codigos:
                print(f"Buscando dados para a estação {codigo}")
                for ano in range(2024, 1990, -1):
                    print(f"Buscando para o ano {ano}")

                    # Primeira metade do ano
                    response = requests.get(url = self.url + path, headers={'Authorization': 'Bearer '+token}, params={'Tipo Filtro Data': 'DATA_LEITURA', 'Data Inicial (yyyy-MM-dd)': f"{ano}-01-01", 'Data Final (yyyy-MM-dd)': f"{ano}-12-01", 'Código da Estação':int(codigo)})
                    response = response.json()
                    if response['message'] == "Não houve retorno de registros. Verifique!":
                        print("\nNão houve registros a partir desse ano.\nPassando para o próximo código de estação.\n")
                        break

                    df_vazoes_por_ano = pd.DataFrame(response["items"])
                    df_vazoes = pd.concat([df_vazoes, df_vazoes_por_ano], ignore_index=True)

                    df_vazoes = self.transformar_vazao(df_vazoes)

        print(df_vazoes)

        print(f"Formatação de códigos de Estacoes concluída!\n")
        return df_vazoes

    def transformar_chuva(self, df: pd.DataFrame):
        """
        Formatação do dataframe de pluviometria dado uma estação e uma data.
        Queremos transformar cada coluna de chuva por dia, em uma linha definida por sua data.
        """
        novas_linhas = []
        for i, row in df.iterrows():
            data_base = pd.to_datetime(row['Data_Hora_Dado'])
            ano = data_base.year
            mes = data_base.month

            for dia in range(1, 32):
                chuva_coluna = f'Chuva_{str(dia).zfill(2)}'
                try:
                    nova_data = data_base.replace(year=ano, month=mes, day=dia)
                    nova_linha = {
                        'data': nova_data,
                        'chuva': row[chuva_coluna],
                        'estacao': row['codigoestacao']
                    }
                    novas_linhas.append(nova_linha)
                except ValueError:
                    pass

        df_novo = pd.DataFrame(novas_linhas)

        return df_novo

    def transformar_vazao(self, df: pd.DataFrame):
        """
        Formatação do dataframe de vazão dado uma estação e uma data.
        Queremos transformar cada coluna de vazão por dia, em uma linha definida por sua data.
        """

        novas_linhas = []
        for i, row in df.iterrows():
            data_base = pd.to_datetime(row['Data_Hora_Dado'])
            ano = data_base.year
            mes = data_base.month

            for dia in range(1, 32):
                chuva_coluna = f'Vazao_{str(dia).zfill(2)}'
                try:
                    nova_data = data_base.replace(year=ano, month=mes, day=dia)
                    nova_linha = {
                        'data': nova_data,
                        'vazao': row[chuva_coluna],
                        'estacao': row['codigoestacao']
                    }
                    novas_linhas.append(nova_linha)
                except ValueError:
                    pass

        df_novo = pd.DataFrame(novas_linhas)

        return df_novo