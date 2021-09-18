#!/bin/bash
# Upload script for Linux/Ubuntu using rsync

wdir=$(pwd)
cp *.py /media/$USER/CIRCUITPY/
cp -r drive_mode /media/$USER/CIRCUITPY/
cp -r lib /media/$USER/CIRCUITPY/
cd /media/$USER/CIRCUITPY/
sleep 1
echo $(date +"%s") > uploaded
cd $wdir
