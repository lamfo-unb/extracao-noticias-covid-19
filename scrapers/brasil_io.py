# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:12:03 2020

@author: INFOWAY
"""

import pandas as pd
import requests
import time


class BrasilIO:
    """
    Download dados covid-19 no Brasil de brasil.io
    """
    
    def __init__(self):
        self.__url_api = 'https://brasil.io/api/dataset/covid19?format=json'
        self.__url_data = self._obter_url_data()
        
    def _try_requisicao(self):
        for _ in range(3):
            try:
                return requests.get(self.__url_api)
            except requests.ConnectionError:
                print('Erro com a conecção, tentanto novamente em 5s..')
                time.sleep(5)
                e = requests.ConnectionError
            except requests.ConnectTimeout:
                print('Servidor demorou para responder, tentanto novamente em 5s..')
                time.sleep(5)
                e = requests.ConnectTimeout
        else:
            raise e
    
    def _obter_url_data(self):
        def requisicao(url):
            return requests.get(url)
        
        def try_requisicao(url_api):
            for _ in range(3):
                resposta = self._try_requisicao()
                if resposta.status_code == 200:
                    return resposta
                print('Refazendo requisição')
                time.sleep(3)
            else:
                raise Exception('Não foi possível acessar api..')
        meta_data = try_requisicao(self.__url_api)
        meta_data = meta_data.json()
        url_data=[k for k in meta_data['tables'] if k['name'] == 'caso'][0]['data_url']
        
        return url_data
        
        
    def extrair_dados(self):
        def extrair_info(lista, chave):    
            info = [k[chave] for k in lista]    
            return info
        
        data = requests.get(self.__url_data)
        if data.status_code == 200:
            data = data.json()['results']
        else:
            raise Exception('Não foi possivel extrair os dados..')
        
        chaves = list(data[0].keys())    
        dados = {chave: extrair_info(data, chave) for chave in chaves}
        
        return pd.DataFrame(dados)
    

if __name__ == "__main__":
    
    brasil_io = BrasilIO()
    casos = brasil_io.extrair_dados()
    estados = casos['state'].value_counts()
