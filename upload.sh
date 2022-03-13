#!/bin/bash
# Upload script for Linux/Ubuntu using rsync


wdir=$(pwd)
for i in *.py; do
    [ -f "$i" ] || break
    ./mpy-cross.static-amd64-linux-7.1.1 $i
done
rsync --exclude=.vscode --include "*.mpy" --include "code.py" --include "drive_mode/***" --include "lib/***" --exclude "*" --delete -r --progress -v -c . /media/$USER/CIRCUITPY/
cd /media/$USER/CIRCUITPY/
sleep 4
echo $(date +"%s") > uploaded
sync -f /media/$USER/CIRCUITPY/
cd $wdir
