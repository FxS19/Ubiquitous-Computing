#!/bin/bash
# Upload script for Linux/Ubuntu using rsync


wdir=$(pwd)
rsync --exclude=.vscode --exclude=.git --delete -r --progress -v -c . /media/$USER/CIRCUITPY/
cd /media/$USER/CIRCUITPY/
sleep 4
echo $(date +"%s") > uploaded
cd $wdir
