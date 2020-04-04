# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 12:23:15 2020

@author: INFOWAY
"""
import os
from zipfile import ZipFile
from datetime import datetime
import pandas as pd

class ZiparArquivos:
    
    def __init__(self, diretorio, nome_destino):
        self._diretorio = diretorio
        self._nome_destino = nome_destino
        self._files = self._get_files()
        self._path_files = self._set_path_files()
    
    
    def _get_files(self):
        files = os.listdir(self._diretorio)
        files = pd.Series(files)
        files = files[files.str.contains('\.txt$|\.csv$')]
        files = files.tolist()
        return files
    
    
    def _set_path_files(self):
        dir_ = self._diretorio
        path_files = [''.join([dir_, f]) for f in self._files]
        return path_files
    
    
    def remove_files(self):
        if self._path_files is None: raise FileNotFoundError
        if len(self._path_files) < 1: raise FileNotFoundError
        
        path_files = self._path_files
        for file in path_files:
            os.unlink(file)
        self._files, self._path_files = None, None
        return None
    
        
    def zipar(self):
        if self._path_files is None: raise FileNotFoundError
        if len(self._path_files) < 1: raise FileNotFoundError
        
        dest_file = self._diretorio+self._nome_destino
        with ZipFile(dest_file, 'w') as zip_:
            [zip_.write(path_file, file) 
                for path_file, file
                in zip(self._path_files, self._files)
            ]
        return None


if __name__ == '__main__':
    
    PATH_DIR = 'C:/Users/INFOWAY/projetos/extracao-noticias-covid-19/'

    hoje = datetime.today().strftime('%Y-%m-%d')
    zipar_google = ZiparArquivos(PATH_DIR+'resultados/google-copia/', f'{hoje}-google.zip')
    zipar_google.zipar()
    zipar_google.remove_files()    
