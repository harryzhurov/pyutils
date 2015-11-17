#!/bin/bash

RTOS_NAME=scmrtos
SAMPLES_NAME=scmrtos-sample-projects

RTOS_URL=https://github.com/harryzhurov/$RTOS_NAME.git
SAMPLES_URL=https://github.com/scmrtos/$SAMPLES_NAME.git

DOC_PATH=~/pro/scmRTOS/scmrtos-doc

if [ -z $1 ]; then
    echo 'E: release number must be specified'
	exit
fi

RELEASE_NAME=$RTOS_NAME'-release-'$1

if [ -e $RELEASE_NAME ]; then
    echo 'removing old data...'
    rm -rf $RELEASE_NAME
    if [ $? -eq 0 ]; then
        echo 'done'
	else 
        echo 'E: cannot remove old data'
        exit
    fi
fi

git clone --recursive -b develop $SAMPLES_URL $RELEASE_NAME

if [ $? -ne 0 ]; then
    echo 'E: clone operation unsuccessfull'
    exit
fi


cd $RELEASE_NAME
rm -rf .git*
rm -rf scmRTOS/.git*

mkdir -p doc/ru
mkdir -p doc/en

cp $DOC_PATH/ru/*.pdf doc/ru
cp $DOC_PATH/en/*.pdf doc/en

cd ..

if [ -f $RELEASE_NAME.zip ]; then
    rm $RELEASE_NAME.zip

	if [ $? -ne 0 ]; then
  		echo 'E: cannot remove release zip archive'
	    exit
	fi
fi

zip -r $RELEASE_NAME.zip $RELEASE_NAME
