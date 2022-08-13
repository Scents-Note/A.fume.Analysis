#!/bin/bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

mkdir -p "${BASEDIR}/../out"
cd "${BASEDIR}/../out" || exit
pyinstaller --onefile -n A_fume_Excel_Converter --paths "../../venv/lib/python3.8/site-packages" --clean ../src/run.py
mkdir -p ./dist
cp ../../.env ./dist/.env
cp ../script/run.sh ./dist/run.sh
