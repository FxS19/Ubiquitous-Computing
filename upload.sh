#!/bin/bash
# Upload script for Linux/Ubuntu using rsync


wdir=$(pwd)
rsync --exclude=.vscode --include "*.py" --include "drive_mode" --include "lib/***" --exclude "*" --delete -r --progress -v -c . /media/$USER/CIRCUITPY/
cd /media/$USER/CIRCUITPY/
sleep 4
echo $(date +"%s") > uploaded
sync -f /media/$USER/CIRCUITPY/
cd $wdir
