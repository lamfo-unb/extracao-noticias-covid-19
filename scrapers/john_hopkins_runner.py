# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:45:47 2020

@author: piphi
"""
import os
try:
    from scraper import Scraper
    from data_jhon_hopkins import DataJhonHopkins
except Exception:
    from scrapers.scraper import Scraper
    from scrapers.data_jhon_hopkins import DataJhonHopkins

class JH_Runner(Scraper):
    def __init__(self, path_dir):
        self.path = os.path.split(os.getcwd())[0] + "\\" + path_dir
    def run(self):
        djh = DataJhonHopkins()
        djh.download_data(verbose=True)
        djh.salvar_dados(path_dir=self.path)
    def get_name(self):
        return "John Hopkins Scraper"
    
if __name__ == "__main__":
    runner = JH_Runner('resultados/jhon_hopkins/')
    runner.run()