# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:29:45 2020

@author: piphi
"""


from corona_feed import CoronaFeed
from scraper_artigos_abertos import ScraperArtigosAbertos

corona_feed = CoronaFeed()
noticias = corona_feed.extrair_dados()
noticias = noticias.iloc[0:10,]
artigos_abertos = ScraperArtigosAbertos(noticias['links'], noticias['titulo'])
textos = artigos_abertos.dados_extraidos
index = artigos_abertos.index_noticias
artigos_abertos.salvar_texto(path_dir = 'resultados/')
