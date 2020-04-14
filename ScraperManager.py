# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 18:06:26 2020

@author: piphi
"""
import logging
try:
    from scraper import Scraper
except Exception:
    from scrapers.scraper import Scraper

class Scraper_Manager:
    """
    This manages all scrapers and the error logger
    """
    def __init__(self):
        self.scrapers = []
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='scrapers.log',
                    filemode='w+')

    def add(self, scraper: Scraper):
        self.scrapers.append(scraper)
    
    def run_all(self):
        FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        logging.basicConfig(format = FORMAT)

        logging.info("Starting Program")
        for scraper in self.scrapers:
            try:
                logging.debug("Starting: " + scraper.get_name())
                scraper.run()
                logging.debug("Finishing: " + scraper.get_name())
            except Exception:
                logging.exception(scraper.get_name() + " failed because of: ")
        logging.info("Finished Program")
        logging.shutdown()
        
if __name__ == "__main__":
    manager = Scraper_Manager()
    manager.run_all()                
        