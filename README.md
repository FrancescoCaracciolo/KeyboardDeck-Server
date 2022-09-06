# KeyboardDeck-Server

This is the server app for [KeyboardDeck-App](https://github.com/FrancescoCaracciolo/KeyboardDeck-App). **For downloads and installation, please refer to the README.md of the main project**.

# Technical details
The app makes UDP json-formatted requests to the server using this [Requests structure](https://github.com/FrancescoCaracciolo/KeyboardDeck-Backend/wiki/KeyboardDeck-requests)

# Building binaries
Everything you need to build binaries is contained in BinaryBuild folder, just run the build*.* executable on your OS after building the binaries.
## Running the script
You need python3 installed, then you install the needed modules with
```
pip install -r requirements.txt
```
To run the **graphical interface** you can run:
```
python3 main.py
```
To run the main server on cli, run
```
python3 server.py
```
To run the capture script (it must be run on the PC the keyboard is attached to), use:
```
python3 capture.py
```
*In both server.py and capture.py, the ip addresses and ports must be edited from the file*

