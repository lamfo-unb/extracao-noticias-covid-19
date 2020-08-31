# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 22:00:27 2020

@author: INFOWAY
"""
from datetime import datetime, timedelta, date
import pandas as pd
from urllib.error import HTTPError
import time
from collections import namedtuple


class DataJhonHopkins:
    def __init__(self):
        self._url_root = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
        self._date = None
        self._url_data = None
        self._data = None

    def _set_date_link(self, date=None):
        """
        Cria link para dados da data estabelecida
        """
        if date is None:
            hoje = datetime.today()
            ontem = hoje - timedelta(days=1)
            date = ontem.strftime("%m-%d-%Y")

        link_data = "{}{}.csv".format(self._url_root, date)
        self._date = date
        self._url_data = link_data
        return None

    def _get_data(self):

        try:
            data = pd.read_csv(self._url_data)
        except HTTPError:
            print("Dados não disponíveis!")
            data = None
        return data

    def download_data(self, date=None, sleep=3, verbose=False):
        """
        date: '%m-%d-%Y'
        """
        self._set_date_link(date=date)
        date = self._date
        if verbose:
            print("|Obtendo dados do dia {}..".format(date))
        time.sleep(sleep)
        self._set_date_link(date=date)
        self._data = self._get_data()
        return None

    @property
    def dados(self):
        return self._data

    @property
    def dict_data(self):
        return {self._date: self._data}

    def salvar_dados(self, path_dir: str, csv_param=None):
        if csv_param is None:
            csv_param = {
                "sep": ";",
                "decimal": ",",
                "encoding": "cp1252",
                "index": False,
            }

        name = self._date
        df = self._data
        path_file = f"{path_dir}jhon-hopkins-{name}.csv"

        try:
            df.to_csv(path_file, **csv_param)
            status = True
        except AttributeError:
            print("| Dados nulos!")
            status = False

        return status


if __name__ == "__main__":
    PATH_DIR = "C:/Users/INFOWAY/projetos/extracao-noticias-covid-19/"
    PATH_DADOS = PATH_DIR + "dados/"
    PATH_RESULTADOS = PATH_DIR + "resultados/jhon-hopkins-data/"

    # data_jhon_hopkins = DataJhonHopkins()
    # datas = pd.read_csv(PATH_DADOS+'date-john-hopkins.txt')
    # datas = list(datas['date'])

    # dados = {v:data_jhon_hopkins.download_data(v, verbose=True) for v in datas}
    # dados2 = [{k:dados[k]} for k in dados.keys()]
    # [write_csv(data, path_dir=PATH_RESULTADOS) for data in dados2]

    # hoje = date.today()
    # hoje - timedelta(days = 1)
    djh = DataJhonHopkins()
    djh.download_data(verbose=True)
    djh.salvar_dados(path_dir=PATH_RESULTADOS)
