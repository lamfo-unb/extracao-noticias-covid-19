# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 18:03:39 2020

@author: INFOWAY
"""
#from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import numpy as np

class CoronaFeed:
    
    def __init__(self):
        self._url = 'https://jerrybrito.com/coronafeed/'
        self._user_agent = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
                }
        self._pag = self._download_page()

    def _download_page(self):
        pag = requests.get(url = self._url, headers = self._user_agent)
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


class ScraperArtigosAbertos:
    
    def __init__(self, links: pd.Series, titulo: pd.Series, sleep = 3):
        self._links = artigos['links']
        self._ids = self._criar_id(links)
        self._index = pd.DataFrame({'titulo': titulo, 'link': self._links, 'id': self._ids})
        self._paginas = self._obter_paginas(sleep)
        self._data = self._extrair_texto()
    
    def _criar_id(self, links: pd.Series):
        len_id = 69
        def slice_str(string):
            try:
                return string[0:len_id]
            except TypeError:
                return np.nan
        
        ids = links.str.replace('\W', '-')\
            .str.replace('--','-')\
            .str.replace('--','-')\
            .str.replace('https-', '')\
            .str.replace('www-','')\
            .apply(slice_str)
            
        return ids
        
    def _obter_paginas(self, sleep):
        def download_pages(link, sleep):
            try:
                time.sleep(sleep)
                print('|Download: {}..'.format(link))
                user_agent = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
                    }
                pagina = requests.get(url = link, headers = user_agent)
                pagina = BeautifulSoup(pagina.content, 'html.parser')
                return pagina
            except:
                return None
        paginas = {id_: download_pages(link, sleep) for id_,link in zip(self._ids,self._links)}
        return paginas
    
    def _extrair_texto(self):
        def extrair(id_,pagina):
            try:
                texto = [v.text.strip() for v in pagina.findAll('p')]
                texto = '\n'.join(texto)
                return {id_: pd.DataFrame({id_:[texto]})}
            except AttributeError:
                return {id_: None}
        
        return [extrair(id_,pagina) for id_,pagina in self._paginas.items()]
    
    def _write_txt(self, data: dict, path_dir: str, id_: str, txt_args = None):
        if txt_args is None:
            txt_args = {'sep': ';', 'index': False, 'header': False, 'encoding': 'cp1252'}
        
        name_file = list(data.keys())[0]
        data_frame = list(data.values())[0]
        path_file = f'{path_dir}{id_}-{name_file}.txt'
        
        data_frame = pd.DataFrame(data_frame)
        
        try:
             data_frame.to_csv(path_file, **txt_args)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        return True
    
    def salvar_texto(self, path_dir: str, id_=None, index_csv_args=None):
        """
        self._data = [{'str':'pd.DataFrame'}, {'str':'pd.DataFrame'}, ...]
        """
        if id_ is None:
            id_ = np.random.randint(20245, 67458, size = 1)[0]
            id_ = str(id_)
        
        [self._write_txt(v, path_dir, id_) for v in self._data]
        
        if index_csv_args is None:
            index_csv_args = {'sep': ';', 'index': False, 'encoding': 'cp1252'}
        path_index = f'{path_dir}{id_}-index-noticias.csv'
        self._index.to_csv(path_index, **index_csv_args)
        
        return True   
    
    @property
    def dados_extraidos(self):
        return self._data
    
    @property
    def index_noticias(self):
        return self._index


if __name__ == "__main__":
    
    corona_feed = CoronaFeed()
    artigos = corona_feed.extrair_dados()
    artigos_abertos = ScraperArtigosAbertos(links=artigos['links'], titulo=artigos['titulo'])
    data_ = artigos_abertos.dados_extraidos
    index = artigos_abertos._index
    artigos_abertos.salvar_texto(path_dir='resultados/')
