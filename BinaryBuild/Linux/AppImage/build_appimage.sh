#!/bin/bash
rm -rf AppDir
mkdir AppDir
mkdir AppDir/usr
mkdir AppDir/usr/bin
cp -a ../Executable/dist/main AppDir/usr/bin/main
cp ../../../keyboarddeck.png keyboarddeck.png
./linuxdeploy-x86_64.AppImage --appdir AppDir --desktop-file keyboarddeck.desktop --output appimage -i keyboarddeck.png
rm -rf AppDir
rm -rf keyboarddeck.png
