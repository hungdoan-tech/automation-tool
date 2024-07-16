#!/bin/bash

check_python_version() {
  if ! command -v python3.10 &> /dev/null; then
    echo "Python 3.10 is not installed. Please install Python 3.10."
    exit 1
  fi
}

check_python_version

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

if [ "$1" == "console" ]; then
    echo "Console app"
    python3.10 -m src.console.EntryPoint
elif [ -z "$1" ] || [ "$1" == "gui" ]; then
    echo "GUI app"
    python3.10 -m src.gui.GUIApp
else
    echo "Invalid argument. Usage: $0 [console|gui]"
fi

deactivate