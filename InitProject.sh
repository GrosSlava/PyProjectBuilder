#!/bin/bash

SCRIPT_PATH=`realpath "$0"`
SCRIPT_DIR=`dirname "$SCRIPT_PATH"`



# install needed tools
echo "------------------Tools-----------------"
sudo apt-get update
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo python3 -m pip install --upgrade pip
echo "----------------------------------------"

# create enviroment
python3 -m venv venv

# set enviroment
source $SCRIPT_DIR/venv/bin/activate

# install requirements
pip3 install -r $SCRIPT_DIR/Requirements.txt

# show versions
echo "------------Current veriosns------------"
python3 --version
pip3 --version
pip3 list
echo "----------------------------------------"
