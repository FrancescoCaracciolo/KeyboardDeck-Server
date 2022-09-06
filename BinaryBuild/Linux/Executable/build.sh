#!/bin/bash
pip3 install pyinstaller
pip3 install -r ../../../requirements_linux.txt
pyinstaller -D -F -n main -c "../../../main.py"