#! /bin/bash
echo "Raspagem/Zipagem/Envio ao Google Drive"
echo "Parte 1: Formato de extrair arquivos COVID-LAMFO 2020"
cd "pasta-a-se-inserir"
eval "$(conda shell.bash hook)"
python main.py
echo "Parte 2: Script para compactar arquivos"
echo "Parte 2.1: Pasta Brasil.io"
cd "/home/alixandro/COVID/extracao-noticias-covid-19/brasil_io"
zip -r "archive-$(date +"%Y-%m-%d").zip" *
echo "Zipado"

echo "Parte 2.2: John Hopkins"
cd "/home/alixandro/Área de Trabalho/covi/resultados/jhon_hopkins"
zip -r "archive-$(date +"%Y-%m-%d").zip" *
echo "Zipado"

echo "Parte 2.3: Corona Feeds"
cd "/home/alixandro/Área de Trabalho/covi/resultados/corona_feed"
zip -r "archive-$(date +"%Y-%m-%d").zip" *
echo "Zipado"

echo "OK! Script Finalizado"

