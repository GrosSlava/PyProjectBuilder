# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import time
import random

import Logger
import ConfigFileParser





class FCompilingFile:
    def __init__(self, ProjectRoot: str, ConfigFile: ConfigFileParser.FConfigFile, ModuleName: str, FilePath: str):
        self.ProjectRoot = ProjectRoot
        self.ConfigFile = ConfigFile
        self.ModuleName = ModuleName
        self.FilePath = FilePath
    #------------------------------------------------------#


    def Compile(self):
        time.sleep(random.randint(1, 3))
    #------------------------------------------------------#
