#!/bin/bash

echo "[!] For libbde, edit the PKGBUILD and change the pkgver=20160731 to pkgver=20170902"
yaourt -S community/volatility extra/tree aur/libbde
pip2 install -r requirements.txt
