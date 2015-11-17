#!/bin/bash

if [ -z $1 ]; then
    echo 'E: tag name must be specified'
    exit
fi

curl --get https://api.github.com/repos/scmrtos/scmrtos/releases/tags/$1 2> /dev/null | grep download_count
