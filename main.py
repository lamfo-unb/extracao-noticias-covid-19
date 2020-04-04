# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""
#import pandas as pd
from scrapers.brasil_io import BrasilIO
from scrapers.corona_feed import CoronaFeed
from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos 
from scrapers.WorldometerScraper import Worldometer_Scraper
#from scrapers.CNN.CNN_Scraper_script import CNN_Scraper
#from scrapers.CNN.CNN_Scraper_script import Article
from scrapers.data_jhon_hopkins import DataJhonHopkins
from helpers.zipar_arquivos import ZiparArquivos
from datetime import datetime 

HOJE = datetime.today().strftime('%Y-%m-%d')
PATH_RES = 'resultados/'
CNN_DIR = "resultados/cnn-articles/"

# Extração brasil.io
print('-'*45)
print('Extraindo dado de brasil.io')
print('-'*45)
brasil_io = BrasilIO()
casos = brasil_io.extrair_dados()

# Extração dados Jhon Hopkins University
print('-'*45)
print('Extraindo dados de Jhon Hopkins University')
print('-'*45)
djh = DataJhonHopkins()
djh.download_data(verbose=True)
djh.salvar_dados(path_dir='resultados/jhon_hopkins/')

# Extração Corona Feed
print('-'*45)
print('Extraindo noticias de Corona Feed')
print('-'*45)
corona_feed = CoronaFeed()
noticias = corona_feed.extrair_dados()
artigos_abertos = ScraperArtigosAbertos(
        links=noticias['links'],
        titulo=noticias['titulo']
        )
artigos_abertos.salvar_texto(path_dir = 'resultados/corona_feed/')
csv_args = {'sep': ';', 'decimal': ',', 'encoding': 'cp1252', 'index': False}
casos.to_csv(f'resultados/brasil_io/{HOJE}-brasil-covid19-brasil-io.csv', **csv_args)

# Extração Worldometer
print('-'*45)
print('Extraindo dados de Worldometer')
print('-'*45)

worldometer = Worldometer_Scraper(PATH_RES + "worldometer/worldometer.csv")

# Extração CNN
worldometer.run_scraper()
#CNN = CNN_Scraper(CNN_DIR)
#CNN.run()

## Zipando arquivos extraidos
print('-'*45)
print('Zipando arquivos extraidos')
print('-'*45)

zipar_brasilio = ZiparArquivos(PATH_RES+'brasil-io/', f'{HOJE}-brasil-io.zip')
zipar_brasilio.zipar()
zipar_brasilio.remove_files()

zipar_corona_feed = ZiparArquivos(PATH_RES+'corona-feed/', f'{HOJE}-corona-feed.zip')
zipar_corona_feed.zipar()
zipar_corona_feed.remove_files()

zipar_jhon_hop = ZiparArquivos(PATH_RES+'jhon-hopkins/', f'{HOJE}-jhon-hopkins.zip')
zipar_jhon_hop.zipar()
zipar_jhon_hop.remove_files()

zipar_worldometer = ZiparArquivos(PATH_RES+'worldometer/', f'{HOJE}-worldometer.zip')
zipar_worldometer.zipar()
zipar_worldometer.remove_files()

print('-'*45)
print('Processo completo')
print('-'*45)
