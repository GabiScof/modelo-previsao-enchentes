import pandas as pd
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
    df_estacoes_pluviometricas.to_csv('data/estacao-pluviometrica-municipio.csv', index=False)

    # Busca dados de pluviometria por estado individualmente
    df_pluviometria_ap = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='AP')
    df_pluviometria_ap.to_csv('data/dados-pluviometricos-AP.csv', index=False)

    df_pluviometria_ac = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='AC')
    df_pluviometria_ac.to_csv('data/dados-pluviometricos-AC.csv', index=False)

    df_pluviometria_rr = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas, token=token,uf='RR')
    df_pluviometria_rr.to_csv('data/dados-pluviometricos-RR.csv', index=False)

    df_pluviometria_ro = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas, token=token,uf='RO')
    df_pluviometria_ro.to_csv('data/dados-pluviometricos-RO.csv', index=False)

    df_pluviometria_ma = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='MA')
    df_pluviometria_ma.to_csv('data/dados-pluviometricos-MA.csv', index=False)

    df_pluviometria_mt = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='MT')
    df_pluviometria_mt.to_csv('data/dados-pluviometricos-MT.csv', index=False)

    df_pluviometria_am = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='AM')
    df_pluviometria_am.to_csv('data/dados-pluviometricos-AM.csv', index=False)

    df_pluviometria_pa = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='PA')
    df_pluviometria_pa.to_csv('data/dados-pluviometricos-PA.csv', index=False)

    df_pluviometria_to = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_pluviometricas,token=token, uf='TO')
    df_pluviometria_to.to_csv('data/dados-pluviometricos-TO.csv', index=False)

    df_pluviometria_final = pd.concat([df_pluviometria_am, df_pluviometria_ap,df_pluviometria_ac,df_pluviometria_ma,df_pluviometria_mt,df_pluviometria_pa,df_pluviometria_ro,df_pluviometria_rr,df_pluviometria_to])
    df_pluviometria_final.to_csv('data/dados-pluviometricos-final.csv', index=False)

    # Formatação dos códigos de estação de vazão por município
    codigos_estacoes_de_vazao, df_estacoes_vazao = api.filtra_estacoes_de_vazao(estacoes_por_municipio,lista_municipios)

    # Gera df associando a estação de vazão ao municipio
    df_estacoes_vazao.to_csv('estacao-vazao-municipio.csv', index=False)

    # Busca dados de vazão por estação
    df_vazao_ap = api.busca_vazao_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='AP')
    df_vazao_ap.to_csv('data/dados-vazao-AP.csv', index=False)

    df_vazao_ac = api.busca_vazao_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='AC')
    df_vazao_ac.to_csv('data/dados-vazao-AC.csv', index=False)

    df_vazao_rr = api.busca_vazao_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao, token=token,uf='RR')
    df_vazao_rr.to_csv('data/dados-vazao-RR.csv', index=False)

    df_vazao_ro = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao, token=token,uf='RO')
    df_vazao_ro.to_csv('data/dados-vazao-RO.csv', index=False)

    df_vazao_ma = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='MA')
    df_vazao_ma.to_csv('data/dados-vazao-MA.csv', index=False)

    df_vazao_mt = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='MT')
    df_vazao_mt.to_csv('data/dados-vazao-MT.csv', index=False)

    df_vazao_am = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='AM')
    df_vazao_am.to_csv('data/dados-vazao-AM.csv', index=False)

    df_vazao_pa = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='PA')
    df_vazao_pa.to_csv('data/dados-vazao-PA.csv', index=False)

    df_vazao_to = api.busca_chuva_por_estacao_e_uf(dict_estacoes=codigos_estacoes_de_vazao,token=token, uf='TO')
    df_vazao_to.to_csv('data/dados-vazao-TO.csv', index=False)

    df_vazao_final = pd.concat([df_vazao_am,df_vazao_ma,df_vazao_mt,df_vazao_pa,df_vazao_ro,df_vazao_rr,df_vazao_to])
    df_vazao_final.to_csv('data/dados-vazao-final.csv', index=False)

    return


if __name__ == "__main__":
    main()