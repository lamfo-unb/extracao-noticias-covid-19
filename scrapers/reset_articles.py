# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 23:04:51 2020

@author: piphi
"""
import pickle

# sends an empty list to article

# ONLY USE IN EMERGENCY
article_list = []
pickle_out = open("article.pickle", "wb")
pickle.dump(article_list, pickle_out)
pickle_out.close()
