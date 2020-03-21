# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 13:32:07 2020

@author: INFOWAY
"""

import requests
import json
import pandas as pd
import numpy as np
from googlesearch import search

query = 'coronavirus'
resposta = search(query, domains = ['elpais.com'])

[print(k) for k in resposta] 

resposta = requests.get('http://plataforma.saude.gov.br/novocoronavirus/resources/scripts/database.js')

resposta.status_code
info = resposta.text
info = info.replace('var database=', '')
data = json.loads(info)

data_brasil = data['brazil']


def apply_day(data: list):
    
    dia = [k['date'] for k in data]
    time = [k['time'] for k in data]
    
    return pd.DataFrame({'dia': dia, 'time': time})


t = {k['date']:k['values'] for k in data_brasil}


def extrair_info(info: list) -> pd.DataFrame:
    """
    Extrai informação para cada atualização
    """
    
    chaves = ['uid', 'suspects', 'refuses', 'cases', 'deaths', 'broadcast', 'comments']
    
    def extrair(k,dic):
        try:
            return dic[k]
        except KeyError:
            return np.nan
        
    def extrair_(dic, chaves):
        info_ = {chave: extrair(chave, dic) for chave in chaves} 
        return info_
    
    data_ = [extrair_(k, chaves) for k in info]
    
    data = {
     'uid': [k['uid'] for k in data_],
     'suspects': [k['suspects'] for k in data_],
     'refuses': [k['refuses'] for k in data_],
     'cases': [k['cases'] for k in data_],
     'deaths': [k['deaths'] for k in data_],
     'broadcast': [k['broadcast'] for k in data_],
     'comments': [k['comments'] for k in data_]
     }
    
    return pd.DataFrame(data)


# Extração com vulnerabilidade: Caso haja mais de atualização por dia,
# ela quebrará. Uma vez que os dicionários têm chave únicas.
data_semi = {k:extrair_info(v) for k,v in t.items()}

def to_df(k, df):
    #date = [k for j in range(df.shape[0])]
    df['date'] = k #date
    return df

data_quase = [to_df(k,df) for k,df in data_semi.items()]
data_fim = pd.concat(data_quase)

# Exportando dados
new_order = ['date','uid', 'suspects', 'refuses', 'cases', 'deaths', 'broadcast','comments']
data_fim = data_fim[new_order]
csv_exp = {'sep': ';', 'index': False, 'encoding': 'cp1252', 'decimal': ','}
data_fim.to_csv('resultados/covid-brasil.csv', **csv_exp)

