import requests
from env import Env

class ApiAnaGov:
    def __init__(self):
        self.url = 'https://www.ana.gov.br/hidrowebservice'

    def get_token(self):
        path = '/EstacoesTelemetricas/OAUth/v1'
        response = requests.get(url = self.url + path, headers={'Identificador': Env.ID, 'Senha': Env.SENHA})
        print(response.json())
        return response


classe = ApiAnaGov()
classe.get_token()