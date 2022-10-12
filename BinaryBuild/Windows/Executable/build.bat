pip install pyinstaller
pip install -r ../../../requirements_windows.txt
#pyinstaller -D -F -n main -c --icon "..\..\..\keyboarddeck.ico" --windowed  "..\..\..\main.py"
pyinstaller main.spec