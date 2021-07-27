#!/bin/bash
# Upload script for Linux/Ubuntu using rsync
rsync --exclude=.vscode --exclude=.git --delete -r --progress -v -c . /media/$USER/CIRCUITPY/