#!/bin/bash
# Copyright (c) 2022-2023 GrosSlava

SCRIPT_PATH=`realpath "$0"`
SCRIPT_DIR=`dirname "$SCRIPT_PATH"`



# Install tool
pip3 install -e $SCRIPT_DIR
