#!/bin/bash

if [ -z "$1" ] || [ -z "$2" ]
then
    echo "usage: cppo.sh <srce-dir> <dst-dir>"
    exit 1
fi

a=`find "$1" -type f | sort | sed -e 's/\.\///'` 

readarray -t files <<<"$a"

for i in "${files[@]}"; do

    if [ ! -d "$2"/"$(dirname "$i")" ]; then
        echo "create dir: "$2"/$(dirname "$i")"
        mkdir "$2"/"$(dirname "$i")"
    fi
    
    echo "copy $i to $2/$i" 
    cp "$i" "$2"/"$i"
    
done



