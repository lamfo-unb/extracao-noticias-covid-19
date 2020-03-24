# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""

from scrapers.brasil_io import BrasilIO
import pandas as pd 

brasil_io = BrasilIO()
casos = brasil_io.extrair_dados()

csv_args = {'sep': ';', 'decimal': ',', 'encoding': 'cp1252', 'index': False}
casos.to_csv('resultados/brasil-covid19-brasil-io.csv', **csv_args)
