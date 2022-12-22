#!/bin/bash


SCRIPT_PATH=`realpath "$0"`
SCRIPT_DIR=`dirname "$SCRIPT_PATH"`



# create enviroment
python3 -m venv venv

# set enviroment
source $SCRIPT_DIR/venv/bin/activate


#.......................Requirements.................................#

echo "------------------Tools-----------------"
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
pip3 install -r $SCRIPT_DIR/Requirements.txt
echo "----------------------------------------"

echo "------------Current veriosns------------"
python3 --version
pip3 --version
pip3 list
echo "----------------------------------------"

#...................................................................#
