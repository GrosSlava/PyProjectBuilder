#!/bin/bash
# Copyright (c) 2022-2023 GrosSlava

SCRIPT_PATH=`realpath "$0"`
SCRIPT_DIR=`dirname "$SCRIPT_PATH"`



# Install needed tools
echo "------------------Tools-----------------"
sudo apt-get update
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo python3 -m pip install --upgrade pip
echo "----------------------------------------"

# Create enviroment
python3 -m venv venv

# Set enviroment
source $SCRIPT_DIR/venv/bin/activate

# Install requirements
pip3 install -r $SCRIPT_DIR/Requirements.txt

# Show versions
echo "------------Current veriosns------------"
python3 --version
pip3 --version
pip3 list
echo "----------------------------------------"
