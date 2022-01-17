#!/bin/bash

# This script stashes all changes in the raspiScan repository,
# switches to the master branch and pulls the latest changes.
# Also install dependencies from requirements.txt if the cksum
# of its contents have changed from the previous version. 
# Finally, it starts the FLASK app that listens in on 
# any requests to take images 


echo "Running autostart.sh"
echo "Updating git..."
echo $PWD
cd /home/pi/raspiScan
git config --global user.email "raspi@raspi.com"
git config --global user.name "raspi"
git stash
git checkout master
git pull


echo "Checking if requirements need to be updated..."
mkdir ./build
CURRENT_CKSUM=$( cksum ./requirements.txt | cut -d' ' -f1 )

if [ ! -f ./build/requirements_cksum.txt ];
then
    echo "No requirements.txt cksum found, installing updates..."
    pip3 install -r ./requirements.txt
else
    PREVIOUS_CKSUM=$( cat ./build/requirements_cksum.txt )
    if [ "$PREVIOUS_CKSUM" != "$CURRENT_CKSUM" ];
    then
        echo "requirements.txt cksum does NOT match previous cksum, performings updates..."
        pip3 install -r ./requirements.txt
    else
        echo "requirements.txt cksum matches previous cksum, skipping updates."
    fi
fi

echo $CURRENT_CKSUM > ./build/requirements_cksum.txt

echo "Setting up env Flask..."
HOSTNAME=$( cat /etc/hostname )
echo "HOSTNAME = '$HOSTNAME'" > build/auto_generated.cfg

echo "Starting Flask..."
mkdir images
export APP_SETTINGS=build/auto_generated.cfg
export FLASK_APP=main.py

python3 -m flask run --host=0.0.0.0

# python3 ./main.py