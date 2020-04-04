#! /bin/bash
echo "Raspagem/Zipagem"
echo "Parte 1: Formato de extrair arquivos COVID-LAMFO 2020"
cd "pasta-a-se-inserir"
eval "$(conda shell.bash hook)"
python main.py

echo "Parte 2: Script para compactar arquivos"
echo "Parte 2.1: Pasta Brasil.io"
cd "pasta-projeto + /resultados/brasil-io"
zip -r "brasil.io-$(date +"%Y-%m-%d").zip" *csv
echo "Zipado"

echo "Parte 2.2: John Hopkins"
cd "pasta-projeto + /resultados/jhon-hopkins"
zip -r "jhon-hopkins-$(date +"%Y-%m-%d").zip" *csv
echo "Zipado"

echo "Parte 2.3: Corona Feeds"
cd "pasta-projeto + /resultados/corona-feed"
zip -r "corona-feed-$(date +"%Y-%m-%d").zip" *txt
echo "Zipado"

#Antes, você precisa instalar o dropbox no seu computador.

echo "Parte 3: Envio ao Dropbox Lamfo"
echo "Parte 3.1: Brasil IO"
cd "pasta-projeto + /resultados/brasil-io"
mv  "brasil.io-$(date +"%Y-%m-%d").zip" "pasta remota do Dropbox + resultados/brasil_io"
echo "Copiado"

echo "Parte 3.2: John Hopkins"
cd "pasta-projeto + /resultados/jhon-hopkins"
mv  "jhon-hopkins-$(date +"%Y-%m-%d").zip" "pasta remota do Dropbox + /resultados/jhon_hopkins"
echo "Copiado"

echo "Parte 3.3: Corona Feeds"
cd "pasta-projeto + /resultados/corona-feed"
mv "corona-feed-$(date +"%Y-%m-%d").zip" "pasta remota do Dropbox + /resultados/corona_feed"
echo "Copiado"

echo "OK! Script Finalizado"

