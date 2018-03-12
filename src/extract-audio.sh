#!/bin/sh

echo "input file : $1"
name=$(basename --suffix=avi $1)
oname="${name}mp3"
echo "output file: "$oname

# default $2 = 320k
# $3 - additional options, for example, resolution: -s 640x356

ffmpeg -i "$1" -vn -acodec copy "$oname"


