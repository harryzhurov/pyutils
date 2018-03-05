#!/bin/sh

echo "input file : $1"
name=$(basename --suffix=mp4 $1)
oname="${name}avi"
echo "output file: "$oname

# default $2 = 320k
# $3 - additional options, for example, resolution: -s 640x356

ffmpeg -i $1 -c:v libxvid $3 -b:v $2 -vtag DX50 -c:a libmp3lame -b:a 128k $oname


