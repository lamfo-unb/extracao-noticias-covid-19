# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:32:39 2020

@author: jpfsv
"""

'''
IMPORTANTE: como o scraper deste código é o mesmo daquele usado
    nos artigos abertos, faz-se necessário a importação dessa classe.
    
    Créditos de criação da classe ScraperArtigosAbertos: @NeurembergMatos
'''
import pandas as pd
from scrapers.scraper_artigos_abertos import ScraperArtigosAbertos
PATH_DIR='resultados/google'
    

# Importando lista de veículos de notícias; arquivo usado: 'News_en.csv'
'''
    O arquivo .csv contém uma enxuta lista dos principais sites de notícias
    da língua inglesa dos EUA, Canadá e Reino Unido. Escolhi os sites com base
    em resultados prévios de facilidade de acesso ao conteúdo.
'''

df_news = pd.read_csv('News_en.csv', delimiter=';')

# Convertendo coluna de links em uma lista
ls_news = df_news['Link'].to_list()

# Pacote usado na realização das buscas
from googlesearch import search 
  
# Palavras-chave
'''
IMPORTANTE: As escolhas das palavras-chave é subjetiva. Qualquer palavra
    pode ser adicionada/alterada/removida, conforme a necessidade.
    
    Cabe notar que as palavras abaixo foram escolhidas visando uma busca
    em sites de língua inglesa.
'''
query = ["coronavirus", "covid-19", "economic", "measures", 
                  "quarantine", "fiscal", "monetary", "bill", 
                  "funding", "relief", "financial", "stimulus", 
                  "interest rates", "credit", "central bank"]

# Iterando a busca pelos resultados (10 por palavra-chave, no útlimo mês).
lista_de_noticias=[]
for i in query:
    for j in search(i, tld='com', lang='en', tbs='qdr:m',
                domains=ls_news, num=50, stop=10, pause=5): 
        lista_de_noticias.append(j)
        print(j)


# Agora vamos extrair o texto das notícias.
        
'''
IMPORTANTE: o código de extração usado é o mesmo do CoronaFeed.
    A única diferença é que usei o link das notícias tanto como 'link'
    quanto como 'titulo'.
'''

noticias = pd.Series(lista_de_noticias)
noticias_abertas = ScraperArtigosAbertos(
        links=noticias,
        titulo=noticias
        )
noticias_abertas.salvar_texto(PATH_DIR)
        