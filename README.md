# PROJECT IN PROGRESS ! :-)

# APMA - Automated Post Mortem Analysis

## Overview

APMA is a script that automates various forensic action. It helps the analyst to focus on the interesting task: analysis.

## Windows

### Automatic profile finder

Just the `imageinfo` command from `Volatility API` parsed to extract the first suggested profile (cf. profil function in _windows.py_)

### Volatility commands

See function __windows_bunch_cmds__ in _windows.py_
* pstree
* psxview
* dlllist
* cmdscan
* consoles
* envars
* iehistory
* driverscan
* filescan
* symlinkscan
* netscan
* hivescan
* hivelist
* hashdump
* clipboard
* desktops
* editbox
* eventhooks
* messagehooks
* screenshot
* bitlocker (__unofficial__)
* mftparser

Some of those commands are not explained in the official `Volatility commands reference`.

### BitLocker

APMA uses the `bitlocker` Volatility plugin to find __FVEK__ and __TWEAK__ keys (cf. bitlocker_key function in _bitlocker\_mount.py_).

APMA can find the disk offset automatically with `fdisk.py`.

Then, decrypt the disk with `bdemount` and mount it as a standard `NTFS` filesystem (cf. bitlocker_vol_mount function in _bitlocker\_mount.py_)

## Linux

### Profile generation

I tried to automate the linux profil creation process.

APMA extracts kernel and linux version. After that APMA, will check if there is an existing vagrant box to use.

#### Linux and kernel version

To find is it's an Ubuntu linux, Debian or others, APMA parses the memory. (cf. linux_profile_parser function in linux.py)

#### Vagrant

### Volatility commands

### LUKS

## TODO

* Web, pdf or Django server report, but something more "readable"
