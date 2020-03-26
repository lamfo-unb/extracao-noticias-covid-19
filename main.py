# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""

import pandas as pd
from scrapers.brasil_io import BrasilIO
from scrapers.corona_feed import CoronaFeed
from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos 

PATH_DIR = 'C:\\Users\\INFOWAY\\projetos\\extracao-noticias-covid-19\\dados'

# Extração brasil.io
brasil_io = BrasilIO()
casos = brasil_io.extrair_dados()

# Extração Corona Feed
corona_feed = CoronaFeed()
noticias = corona_feed.extrair_dados()
noticias = noticias.iloc[10:14,]
artigos_abertos = ScraperArtigosAbertos(
        links=noticias['links'],
        titulo=noticias['titulo']
        )
artigos_abertos.salvar_texto(path_dir = PATH_DIR)
csv_args = {'sep': ';', 'decimal': ',', 'encoding': 'cp1252', 'index': False}
casos.to_csv('resultados/brasil-covid19-brasil-io.csv', **csv_args)

