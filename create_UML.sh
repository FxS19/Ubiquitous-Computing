#!/bin/bash
pyreverse -o png -f ALL -p UbiComp_all $(pwd)/*.py
pyreverse -o png -p UbiComp $(pwd)/*.py
mv *.png ./UML