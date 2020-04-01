#! /bin/bash
echo "Formato de extrair arquivos COVID-LAMFO 2020"
cd "pasta-a-se-inserir"
eval "$(conda shell.bash hook)"
python main.py
echo "OK! Script Finalizado"

