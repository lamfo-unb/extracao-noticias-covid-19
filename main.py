# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""

import os

from scrapers.brasil_io import BrasilIO
from scrapers.WorldometerScraper import Worldometer_Scraper
from scrapers.CNN_Scraper_script import CNN_Scraper
from scrapers.artigos_abertos_runner import Artigos_Abertos_Runner
from scrapers.john_hopkins_runner import JH_Runner
from ScraperManager import Scraper_Manager

PATH_DIR = os.getcwd() + "\\dados"

CNN_DIR = os.getcwd() + "\\resultados\\CNN Articles\\"


manager = Scraper_Manager()

# Add scrapers to manager
worldometer = Worldometer_Scraper(PATH_DIR + "\\worldometer.csv")
CNN = CNN_Scraper(CNN_DIR)
corona_feed = Artigos_Abertos_Runner(PATH_DIR)
brasil_io = BrasilIO()
jh_runner = JH_Runner('resultados\\jhon_hopkins\\')


manager.add(worldometer)
manager.add(corona_feed)
manager.add(brasil_io)
manager.add(jh_runner)
manager.add(CNN)


# Run scrapers
manager.run_all()

