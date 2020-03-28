# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""
import pandas as pd
from scrapers.brasil_io import BrasilIO
from scrapers.corona_feed import CoronaFeed
from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos
from scrapers.data_jhon_hopkins import DataJhonHopkins
from datetime import datetime 

HOJE = datetime.today().strftime('%Y-%m-%d')

# Extração brasil.io
brasil_io = BrasilIO()
casos = brasil_io.extrair_dados()

# Extração dados Jhon Hopkins University
djh = DataJhonHopkins()
djh.download_data(verbose=True)
djh.salvar_dados(path_dir='resultados/jhon_hopkins/')

# Extração Corona Feed
corona_feed = CoronaFeed()
noticias = corona_feed.extrair_dados()
artigos_abertos = ScraperArtigosAbertos(
        links=noticias['links'],
        titulo=noticias['titulo']
        )
artigos_abertos.salvar_texto(path_dir = 'resultados/corona_feed/')
csv_args = {'sep': ';', 'decimal': ',', 'encoding': 'cp1252', 'index': False}
casos.to_csv(f'resultados/brasil_io/{HOJE}-brasil-covid19-brasil-io.csv', **csv_args)
