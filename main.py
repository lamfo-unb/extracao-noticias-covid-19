# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""

import pandas as pd
from scrapers.brasil_io import BrasilIO
from scrapers.corona_feed import CoronaFeed
from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos 
from scrapers.WorldometerScraper import Worldometer_Scraper
from scrapers.CNN.CNN_Scraper_script import CNN_Scraper
from scrapers.CNN.CNN_Scraper_script import Article


PATH_DIR = 'C:\\Users\\piphi\\Documents\\CoronaVirusScraper\\extracao-noticias-covid-19\\dados'

CNN_DIR = "C:\\Users\\piphi\\Documents\\CoronaVirusScraper\\extracao-noticias-covid-19\\resultados\\CNN Articles\\"
# Extração brasil.io
brasil_io = BrasilIO()
casos = brasil_io.extrair_dados()


worldometer = Worldometer_Scraper(PATH_DIR + "\\worldometer.csv")
CNN = CNN_Scraper(CNN_DIR)

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
worldometer.run_scraper()
CNN._to_output()
