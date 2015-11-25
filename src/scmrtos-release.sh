#!/bin/bash

RTOS_NAME=scmrtos
SAMPLES_NAME=scmrtos-sample-projects

RTOS_URL=https://github.com/$RTOS_NAME/$RTOS_NAME.git
SAMPLES_URL=https://github.com/$RTOS_NAME/$SAMPLES_NAME.git

DOC_PATH=~/pro/scmRTOS/scmrtos-doc

#--------------------------------------------------
#
#    Check argument[s]
#
if [ -z $1 ]; then
    echo 'E: release number must be specified'
	exit
fi

#--------------------------------------------------
#
#    Clean up working directory
#
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

#--------------------------------------------------
#
#    Get data  
#
git clone $SAMPLES_URL $RELEASE_NAME

if [ $? -ne 0 ]; then
    echo 'E: clone operation unsuccessfull'
    exit
fi

#--------------------------------------------------
#
#    Replace line endings to windows style 
#
cd $RELEASE_NAME
ls | xargs rm -rf
echo '* text eol=crlf' > .gitattributes

#read -n1 -r -p "Press any key to continue..." key

git reset --hard
git submodule init
git submodule update

#--------------------------------------------------
#
#    Replace line endings to windows style (in submodule)
#
cd scmRTOS
ls | xargs rm -rf
echo '* text eol=crlf' > .gitattributes
git reset --hard
cd ..

#--------------------------------------------------
#
#    Remove service data
#
cd $RELEASE_NAME
rm -rf .git*
rm -rf scmRTOS/.git*

#--------------------------------------------------
#
#    Put documentation
#
mkdir -p doc/

cp -R $DOC_PATH/pdf/* doc

if [ $? -ne 0 ]; then
    exit
fi

cd ..

#--------------------------------------------------
#
#    Create archive
#
if [ -f $RELEASE_NAME.zip ]; then
    rm $RELEASE_NAME.zip

	if [ $? -ne 0 ]; then
  		echo 'E: cannot remove release zip archive'
	    exit
	fi
fi

zip -r $RELEASE_NAME.zip $RELEASE_NAME
