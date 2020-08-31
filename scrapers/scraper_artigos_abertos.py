# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:37:08 2020

@author: INFOWAY
"""
import pandas as pd
import numpy as np
import requests
import time
from bs4 import BeautifulSoup


class ScraperArtigosAbertos:
    """
    Scraper de notícias de sites sem restrições

    parametros:
    -------------
        **links (pd.Series)**: Links das notícias\n
        **titulo (pd.Series)**: título da notícias\n
        **sleep (int)**: Tempo de espera para fazer requisição, 3s é o padrão

    atributos:
    -------------
        **dados_extraidos (list)**: Lista de dicionarios contendo o id e
        o conteúdo das notícias\n

        **index_noticias (pd.DataFrame)**: Título, link e id das notícias.
    """

    def __init__(self, links: pd.Series, titulo: pd.Series, sleep=3):
        self._links = links
        self._ids = self._criar_id(links)
        self._index = pd.DataFrame(
            {"titulo": titulo, "link": self._links, "id": self._ids}
        )
        self._paginas = self._obter_paginas(sleep)
        self._data = self._extrair_texto()

    def _criar_id(self, links: pd.Series):
        len_id = 69

        def slice_str(string):
            try:
                return string[0:len_id]
            except TypeError:
                return np.nan

        ids = (
            links.str.replace("\W", "-")
            .str.replace("--", "-")
            .str.replace("--", "-")
            .str.replace("https-", "")
            .str.replace("www-", "")
            .apply(slice_str)
        )

        return ids

    def _obter_paginas(self, sleep):
        def download_pages(link, sleep):
            try:
                time.sleep(sleep)
                print("|Download: {}..".format(link))
                user_agent = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
                }
                pagina = requests.get(url=link, headers=user_agent)
                pagina = BeautifulSoup(pagina.content, "html.parser")
                return pagina
            except:
                return None

        paginas = {
            id_: download_pages(link, sleep)
            for id_, link in zip(self._ids, self._links)
        }
        return paginas

    def _extrair_texto(self):
        def extrair(id_, pagina):
            try:
                texto = [v.text.strip() for v in pagina.findAll("p")]
                texto = "\n".join(texto)
                return {id_: pd.DataFrame({id_: [texto]})}
            except AttributeError:
                return {id_: None}

        return [extrair(id_, pagina) for id_, pagina in self._paginas.items()]

    def _write_txt(self, data: dict, path_dir: str, id_: str, txt_args=None):
        if txt_args is None:
            txt_args = {
                "sep": ";",
                "index": False,
                "header": False,
                "encoding": "cp1252",
            }

        name_file = list(data.keys())[0]
        data_frame = list(data.values())[0]
        path_file = f"{path_dir}{id_}-{name_file}.txt"

        data_frame = pd.DataFrame(data_frame)

        try:
            data_frame.to_csv(path_file, **txt_args)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        return True

    def salvar_texto(self, path_dir: str, id_=None, index_csv_args=None):
        """
        Salvar localmente os dados extraidos
        """
        if id_ is None:
            id_ = np.random.randint(20245, 67458, size=1)[0]
            id_ = str(id_)

        [self._write_txt(v, path_dir, id_) for v in self._data]

        if index_csv_args is None:
            index_csv_args = {"sep": ";", "index": False, "encoding": "cp1252"}
        path_index = f"{path_dir}{id_}-index-noticias.csv"
        self._index.to_csv(path_index, **index_csv_args)

        return True

    @property
    def dados_extraidos(self):
        return self._data

    @property
    def index_noticias(self):
        return self._index


if __name__ == "__main__":

    from scrapers.corona_feed import CoronaFeed

    corona_feed = CoronaFeed()
    noticias = corona_feed.extrair_dados()
    noticias = noticias.iloc[
        0:10,
    ]
    artigos_abertos = ScraperArtigosAbertos(noticias["links"], noticias["titulo"])
    textos = artigos_abertos.dados_extraidos
    index = artigos_abertos.index_noticias
    artigos_abertos.salvar_texto(path_dir="resultados/")
