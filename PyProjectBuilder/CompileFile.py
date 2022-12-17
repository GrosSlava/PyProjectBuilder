# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import time
import random

import Logger
import ConfigFileParser





'''
    Source file wrapper to implement it compilation.
'''
class FCompilingFile:
    def __init__(self, ProjectRoot: str, ConfigFile: ConfigFileParser.FConfigFile, ModuleName: str, FilePath: str):
        self.ProjectRoot = ProjectRoot          # cached project root
        self.ConfigFile = ConfigFile            # cached config file
        self.ModuleName = ModuleName            # cachd file module name
        self.FilePath = FilePath                # ceched file absolute path
    #------------------------------------------------------#

    '''
        Process file compilation by third-party compiler.
    '''
    def Compile(self) -> None:
        time.sleep(random.randrange(1, 3))
        #TODO
    #------------------------------------------------------#
