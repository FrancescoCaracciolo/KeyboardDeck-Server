pip install pyinstaller
pip install -r ../../../requirements_windows.txt
pyinstaller -D -F -n main -c --icon --windowed "..\..\..\keyboarddeck.ico"  "..\..\..\main.py"