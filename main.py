# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:21:26 2020

@author: INFOWAY
"""

from scrapers.brasil_io import BrasilIO

brasil_io = BrasilIO()
casos = BrasilIO.extrair_dados()