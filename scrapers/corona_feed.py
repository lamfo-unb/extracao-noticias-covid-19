# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:40:35 2020

@author: INFOWAY
"""
import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup

class CoronaFeed:
    """
    Extração dos links e títulos de notícias no site: https://jerrybrito.com/coronafeed/
    """
    
    def __init__(self):
        self._url = 'https://jerrybrito.com/coronafeed/'
        self._user_agent = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
                }
        self._pag = self._download_page()
    
    def _try_requests(self):
        for _ in range(3):
            try:
                return requests.get(url = self._url, headers = self._user_agent)
            except requests.ConnectionError:
                print('Problemas com a conexão..\nTentando novamente em 5s.')
                time.sleep(5)
        else:
            raise Exception('Não foi possível estabelecer conexão!')
    
    def _download_page(self):
        tempo_espera = 3
        time.sleep(tempo_espera)
        pag = self._try_requests()
        pag = BeautifulSoup(pag.content, 'html.parser')
        return pag
    
    def _obter_titulo(self):
        return [k.text for k in self._pag.findAll('li')]
    
    def _obter_links(self):
        def link(k):
            try:
                return k.a.get('href')
            except AttributeError:
                return np.nan
        
        return [link(k) for k in self._pag.findAll('li')]
    
    def extrair_dados(self):
        dados = {
                'titulo': self._obter_titulo(),
                'links': self._obter_links()
                }
        dados = pd.DataFrame(dados)
        return dados

if __name__ == "__main__":
    corona_feed = CoronaFeed()
    noticias = corona_feed.extrair_dados()
