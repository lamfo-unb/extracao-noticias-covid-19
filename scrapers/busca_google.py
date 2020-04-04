# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 11:18:50 2020

@author: INFOWAY
"""
import pandas as pd
from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos
from googlesearch import search
import time

class BuscaGoogle:
    
    def __init__(self, dominios: list, palavras_chaves=None):
        self._dominios = dominios
        self._palavras_chaves = self._set_palavras_chaves(palavras_chaves)
    
    
    def _set_palavras_chaves(self, palavras_chaves=None):
        if palavras_chaves is None:
            palavras_chaves = [
                "coronavirus", "covid-19", "economic", "measures", "quarantine",
                "fiscal", "monetary", "bill", "funding", "relief", "financial",
                "stimulus", "interest rates", "credit", "central bank"]
        
        return palavras_chaves
    
    
    def _buscar(self, query: str):
        dominios = self._dominios
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        busca = search(query, tld='com', lang='en', tbs='qdr:m', domains=dominios, num=50,
               stop=10, pause=5, tpe='nws', user_agent=user_agent)
        return busca

def get_link(k, pause=3):
        print('| ..')
        time.sleep(pause)
        return k

if __name__ == '__main__':
    PATH_DIR = 'C:/Users/INFOWAY/projetos/extracao-noticias-covid-19/'
    PATH_DADOS = PATH_DIR+'dados/'
    PATH_RES = PATH_DIR+'resultados/google/'
    
    # Dominios
    df_news = pd.read_csv(PATH_DADOS+'News_en.csv', delimiter=';')
    dominios = df_news['Link'].to_list()
    
    busca_google = BuscaGoogle(dominios)
    res = busca_google._buscar('covid')
    links = [get_link(k) for k in res]
        
    noticias = pd.Series(links)
    noticias_abertas = ScraperArtigosAbertos(
            links=noticias,
            titulo=noticias
            )
    noticias_abertas.salvar_texto(PATH_RES)