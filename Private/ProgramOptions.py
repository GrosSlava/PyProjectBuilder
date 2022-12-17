# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import enum

import FunctionLibrary
import Logger





'''
    Project build type.
'''
class EBuildType(enum.Enum):
    DEBUG = 1,      # Build in debug mode
    SHIPPING = 2    # Build in release mode

    def __str__(self):
        if self.value == 1:
            return "DEBUG"
        else:
            return "SHIPPING"
    #------------------------------------------------------#

'''
    Tool action.
'''
class EAction(enum.Enum):
    BUILD = 1,      # Build project
    REBUILD = 2,    # Clear intermediate and build project
    CLEAR = 3       # Clear intermediate files



'''
    Helper structure to contain execution options.
'''
class FProgramOptions:
    def __init__(self, argv: list):
        self.ConfigFilePath = os.path.join(os.getcwd(), "PyBuildFile.txt")  # absolute path to config file
        self.Action = EAction.BUILD                                         # current action
        self.BuildType = EBuildType.DEBUG                                   # build type
        self.ProjectRoot = os.getcwd()                                      # absolute path to project root dir

        for LArg in argv:
            LOption = LArg.strip() 
            if len(LOption) < 2:
                Logger.ErrorLog("Invalid option '{Option}'.".format(Option = LOption))

            if LOption == "--help" or LOption == "-h":
                self.__PrintInfoAboutOption("--help", "List all options")
                self.__PrintInfoAboutOption("--BuildType=[Debug, Shipping]", "Type of build")
                self.__PrintInfoAboutOption("--BUILD", "Build project")
                self.__PrintInfoAboutOption("--REBUILD", "Clear intermediate and build project")
                self.__PrintInfoAboutOption("--CLEAR", "Clear intermediate files")
                sys.exit(0)
            elif LOption == '--BuildType=Debug':
                self.BuildType = EBuildType.DEBUG
            elif LOption == '---BuildType=Shipping':
                self.BuildType = EBuildType.SHIPPING
            elif LOption == '--BUILD':
                self.BuildType = EAction.BUILD
            elif LOption == '--REBUILD':
                self.BuildType = EAction.REBUILD
            elif LOption == '--CLEAR':
                self.BuildType = EAction.CLEAR
            elif LOption[0] != '-':
                self.ConfigFilePath = LOption
            else:
                Logger.ErrorLog("Invalid option '{Option}'.".format(Option = LOption))

        self.ProjectRoot = os.path.dirname(self.ConfigFilePath)
    #------------------------------------------------------#


    def __PrintInfoAboutOption(self, Option: str, Description: str) -> None:
        print(f"{Option : <50}{'---' + Description : <50}")
    #------------------------------------------------------#