from src.common.api import ApiAnaGov

def main():
    print("\nMODELO-PREVISAO-ENCHENTES : Iniciando resgaste dos dados!\n")
    # Chamando classe com funções da API
    api = ApiAnaGov()

    # Resgatando token de autenticação
    token = api.get_token()

    # Definindo municipios que serão estudados
    lista_municipios = ['AM', 'AP', 'AC', 'MA', 'MT', 'PA', 'RO', 'RR', 'TO']

    # Buscando código das estações por município
    print(f"Inicializando busca de Estacoes!\n")
    estacoes_por_municipio = dict()

    estacoes_por_municipio[lista_municipios[0]] = api.busca_estacoes_integerers(municipio=lista_municipios[0],token=token)
    for municipio in lista_municipios[1:]:
        estacoes_por_municipio[municipio] = api.busca_estacoes_integerers(municipio=municipio,token=token)
    print(f"\nBusca de Estacoes finalizada!\n")

    # Formatação dos códigos de estação pluviométrica por município
    codigos_estacoes_pluviometricas, df_estacoes_pluviometricas = api.filtra_estacoes_pluviometricas(estacoes_por_municipio,lista_municipios)

    # Gera df associando a estação pluviométrica ao municipio
    df_estacoes_pluviometricas.to_csv('estacao-pluviometrica-municipio.csv', index=False)

    # Busca dados de pluviometria por estação
    df_pluviometria = api.busca_chuva_por_estacao(dict_estacoes=codigos_estacoes_pluviometricas,token=token, lista_municipios=lista_municipios)
    df_pluviometria.to_csv('dados-pluviometricos.csv', index=False)

    # Formatação dos códigos de estação de vazão por município
    codigos_estacoes_de_vazao, df_estacoes_vazao = api.filtra_estacoes_de_vazao(estacoes_por_municipio,lista_municipios)

    # Gera df associando a estação de vazão ao municipio
    df_estacoes_vazao.to_csv('estacao-vazao-municipio.csv', index=False)

    # Busca dados de vazão por estação
    df_vazao = api.busca_vazao_por_estacao(dict_estacoes=codigos_estacoes_de_vazao,token=token, lista_municipios=lista_municipios)
    df_vazao.to_csv('dados-vazao.csv', index=False)

    return


if __name__ == "__main__":
    main()