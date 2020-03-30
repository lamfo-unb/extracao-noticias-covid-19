# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 18:06:26 2020

@author: piphi
"""
from ErrorLogger import Error_Logger
try:
    from scraper import Scraper
except Exception:
    from scrapers.scraper import Scraper

class Scraper_Manager:
    """
    This manages all scrapers and the error logger
    """
    def __init__(self, path):
        self.scrapers = []
        self.logger = Error_Logger(path)
    
    def add(self, scraper: Scraper):
        self.scrapers.append(scraper)
    
    def run_all(self):
        self.logger.start_log()
        for scraper in self.scrapers:
            try:
                scraper.run()
            except Exception as e:

                self.logger.log_error(scraper.get_name(), e)
        self.logger.end_log()
        