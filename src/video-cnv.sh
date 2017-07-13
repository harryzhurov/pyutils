#!/bin/sh

echo "input file : $1"
name=$(basename --suffix=mp4 $1)
oname="${name}avi"
echo "output file: "$oname

ffmpeg -i $1 -vcodec copy -acodec mp3 -ab 128k $oname
