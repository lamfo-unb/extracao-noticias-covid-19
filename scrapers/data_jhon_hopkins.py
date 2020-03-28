# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 22:00:27 2020

@author: INFOWAY
"""
from datetime import datetime
import pandas as pd
from urllib.error import HTTPError
import time

class DataJhonHopkins:
    
    def __init__(self):
        self._url_root = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        self.data = None
    
    def _set_link(self, date=None):
        """
        Cria link para dados da data estabelecida
        """
        if date is None: date = datetime.today().strftime('%m-%d-%Y')
        link_data = '{}{}.csv'.format(self._url_root,date)
        return link_data 
    
    def _get_data(self, url):
        try:
            data = pd.read_csv(url)
        except HTTPError:
            print('Dados não disponíveis!')
            data = None
        return data
    
    def download_data(self, date = None, sleep=3, verbose=False):
        """
        date: '%m-%d-%Y'
        """
        if verbose:
            print('|Obtendo dados do dia {}..'.format(date))
        time.sleep(sleep)
        url = self._set_link(date=date)
        data = self._get_data(url=url)
        
        return data

def write_csv(data: dict, path_dir: str, csv_param=None):
    if csv_param is None:
        csv_param = {'sep': ';', 'decimal': ',', 'encoding': 'cp1252', 'index': False}
    
    name = list(data.keys())[0]
    df = list(data.values())[0]
    path_file = f'{path_dir}{name}.csv'
    df.to_csv(path_file, **csv_param)
    return True
    

if __name__ == '__main__':
    PATH_DIR = 'C:/Users/INFOWAY/projetos/extracao-noticias-covid-19/'
    PATH_DADOS = PATH_DIR+'dados/'
    PATH_RESULTADOS = PATH_DIR+'resultados/jhon-hopkins-data/'
    
    data_jhon_hopkins = DataJhonHopkins()
    datas = pd.read_csv(PATH_DADOS+'date-john-hopkins.txt')
    datas = list(datas['date'])
    
    dados = {v:data_jhon_hopkins.download_data(v, verbose=True) for v in datas}
    dados2 = [{k:dados[k]} for k in dados.keys()]
    [write_csv(data, path_dir=PATH_RESULTADOS) for data in dados2]
    
    
    
    
