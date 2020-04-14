# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:29:45 2020

@author: piphi
"""

import os

try:
    from scraper import Scraper
    from corona_feed import CoronaFeed
    from scraper_artigos_abertos import ScraperArtigosAbertos
except Exception:
    from scrapers.scraper import Scraper
    from scrapers.corona_feed import CoronaFeed
    from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos

class Artigos_Abertos_Runner(Scraper):
    def __init__(self, path_dir):
        self.path_dir = path_dir
        
    def run(self):
        corona_feed = CoronaFeed()
        noticias = corona_feed.extrair_dados()
        noticias = noticias.iloc[10:14,]
        artigos_abertos = ScraperArtigosAbertos(noticias['links'], noticias['titulo'])    
        artigos_abertos.salvar_texto(self.path_dir)
    
    def get_name(self):
        return "Scraper Artigos Abertos and Corona Feed"
    
if __name__ == "__main__":
    PATH_DIR = os.getcwd() + "\\dados"
    runner = Artigos_Abertos_Runner(PATH_DIR)
    runner.run()
