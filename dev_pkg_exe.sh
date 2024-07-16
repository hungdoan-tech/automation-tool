#!/bin/bash

if [ -d dist ]; then
  rm -rf dist
fi

if [ ! -d venv ]; then
  python3.10 -m venv venv
  echo "Virtual environment created: venv"
fi

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

#sudo apt-get install policykit-1

pyinstaller automation_tool.spec

if [ -d dist ]; then
  cp -r input output script release_note dist/
fi

deactivate
