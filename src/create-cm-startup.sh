#!/bin/sh

BASEDIR=$(dirname "$0")

find . -type f -exec dos2unix {} \;
find . -type f -exec "$BASEDIR"/cmhgen.py {} \; 