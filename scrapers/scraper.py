# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:58:47 2020

@author: piphi
"""
from abc import ABC, abstractmethod 


class Scraper(ABC):
    """
    The Scraper abstract class serves as a frame work for the scraping scripts
    Each Scraper has a run method that runs the code necessary for it to perform its task
    and a get_name method to return its name (for identification and logging).
    """
    
    @abstractmethod 
    def run(self): 
        pass
    @abstractmethod
    def get_name(self):
        pass

