#! /bin/bash
echo "Raspagem/Zipagem"
echo "Parte 1: Formato de extrair arquivos COVID-LAMFO 2020"
cd "pasta-a-se-inserir"
eval "$(conda shell.bash hook)"
python main.py

echo "Parte 2: Script para compactar arquivos"
echo "Parte 2.1: Pasta Brasil.io"
cd "pasta-projeto" + /resultados/brasil_io
zip -r "brasil.io-$(date +"%Y-%m-%d").zip"*csv
echo "Zipado"

echo "Parte 2.2: John Hopkins"
cd "pasta-projeto" + /resultados/brasil_io
zip -r "jhon-hopkins-$(date +"%Y-%m-%d").zip" *csv
echo "Zipado"

echo "Parte 2.3: Corona Feeds"
cd "pasta-projeto" + /resultados/corona_feed"
zip -r "corona-feed-$(date +"%Y-%m-%d").zip" *txt
echo "Zipado"

echo "Parte 3: Envio ao Dropbox Lamfo"
echo "Parte 3.1: Brasil IO"
cd "pasta-projeto" + /resultados/brasil_io
mv  "brasil.io-$(date +"%Y-%m-%d").zip" "/home/alixandro/Dropbox/resultados/brasil_io"
echo "Copiado"

echo "Parte 3.2: John Hopkins"
cd "pasta-projeto" + /resultados/brasil_io
mv  "jhon-hopkins-$(date +"%Y-%m-%d").zip" "/home/alixandro/Dropbox/resultados/jhon_hopkins"
echo "Copiado"

echo "Parte 3.3: Corona Feeds"
cd "pasta-projeto" + /resultados/corona_feed"
mv "corona-feed-$(date +"%Y-%m-%d").zip" "/home/alixandro/Dropbox/resultados/corona_feed"
echo "Copiado"

echo "OK! Script Finalizado"

