# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 12:35:06 2020

@author: INFOWAY
"""

import pandas as pd
from googlesearch import search
import functools

jornais = pd.read_csv("dados/jornais.csv", sep=";")
dominios_interesse = list(jornais["jornais"])


def get_link(link):
    print(link)
    return link


def filtrar_jornal(noticias, jornal):
    index = [noticia for noticia in noticias if jornal in noticia]
    return index


def unlist(l1, l2):
    "Transforma junta duas lista"
    return [*l1, *l2]


busca = "coronavirus covid"
resposta = search(
    busca, tpe="nws", stop=200, user_agent="Mozilla/5.0"
)  # , tld=dominios_interesse)

links = [get_link(link) for link in resposta]

# filtrar_jornal(links, 'https://g1.globo.com')
noticias_filtradas = [filtrar_jornal(links, jornal) for jornal in dominios_interesse]

# Transformando lista de lista em umma lista
noticias_filtradas = functools.reduce(unlist, noticias_filtradas)
links_ = pd.DataFrame({"links_covid": links})
noticias_filtradas_ = pd.DataFrame({"noticias_filtradas": noticias_filtradas})

csv_params = {"sep": ";", "decimal": ",", "index": False, "encoding": "cp1252"}
links_.to_csv("resultados/noticias.csv", **csv_params)
noticias_filtradas_.to_csv("resultados/noticias-filtradas.csv", **csv_params)
