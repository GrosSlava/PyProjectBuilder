# Copyright (c) 2022 GrosSlava

import os
from sys import exit
from enum import IntEnum

from PyProjectBuilder.Logger import *
from PyProjectBuilder.PyProjectBuildLibrary import PY_PROJECT_BUILD_VERSION





'''
    Project build type.
'''
class EBuildType(IntEnum):
    DEBUG = 1,          # Build in debug mode
    SHIPPING = 2        # Build in release mode

    def __str__(self):
        return self.name
    #------------------------------------------------------#

'''
    Target architecture.
'''
class ETargetArch(IntEnum):
    X86 = 1,            # Build for x86
    X86_64 = 2,         # Build for x86-64
    ARM = 3,            # build for arm
    ARM_64 = 4          # build for arm-64

    def __str__(self):
        return self.name
    #------------------------------------------------------#

'''
    Tool action.
'''
class EAction(IntEnum):
    BUILD = 1,          # Build project
    REBUILD = 2,        # Clear intermediate and build project
    CLEAR = 3           # Clear intermediate files

    def __str__(self):
        return self.name
    #------------------------------------------------------#




'''
    Helper structure to contain execution options.
'''
class FProgramOptions:
    def __init__(self, argv: list[str]):
        self.ConfigFilePath = os.path.join(os.getcwd(), "PyBuildFile.txt")  # absolute path to config file
        self.Action = EAction.BUILD                                         # current action
        self.BuildType = EBuildType.DEBUG                                   # build type
        self.TargetArch = ETargetArch.X86_64                                # build target architecture
        self.ProjectRoot = os.getcwd()                                      # absolute path to project root dir
        self.Silent = False                                                 # mark to not print messages
        self.UseMultiprocessing = True                                      # use all cores for parallel compilation

        for LArg in argv:
            LOption = LArg.strip() 
            if len(LOption) < 2:
                ErrorLog("Invalid option '{Option}'.".format(Option = LOption))

            if LOption == "--help" or LOption == "-h":
                self.__PrintInfoAboutOption("--help", "List all options")
                self.__PrintInfoAboutOption("--version", "Print current version")
                self.__PrintInfoAboutOption("--BuildType=[Debug, Shipping]", "Type of build")
                self.__PrintInfoAboutOption("--TargetArch=[x86, x86_64, arm, arm_64]", "Build target architecture")
                self.__PrintInfoAboutOption("--BUILD", "Build project")
                self.__PrintInfoAboutOption("--REBUILD", "Clear intermediate and build project")
                self.__PrintInfoAboutOption("--CLEAR", "Clear intermediate files")
                self.__PrintInfoAboutOption("--SILENT", "Disable compilation logs")
                self.__PrintInfoAboutOption("--NO_MULTIPROCESSING", "Disable parallel compilation")
                exit(0)
            elif LOption == '--version' or LOption == "-v":
                Log(PY_PROJECT_BUILD_VERSION)
                exit(0)
            elif LOption == '--BuildType=Debug':
                self.BuildType = EBuildType.DEBUG
            elif LOption == '--BuildType=Shipping':
                self.BuildType = EBuildType.SHIPPING
            elif LOption == '--TargetArch=x86':
                self.TargetArch = ETargetArch.X86
            elif LOption == '--TargetArch=x86_64':
                self.TargetArch = ETargetArch.X86_64
            elif LOption == '--TargetArch=arm':
                self.TargetArch = ETargetArch.ARM
            elif LOption == '--TargetArch=arm_64':
                self.TargetArch = ETargetArch.ARM_64
            elif LOption == '--BUILD':
                self.Action = EAction.BUILD
            elif LOption == '--REBUILD':
                self.Action = EAction.REBUILD
            elif LOption == '--CLEAR':
                self.Action = EAction.CLEAR
            elif LOption == '--SILENT':
                self.Silent = True
            elif LOption == '--NO_MULTIPROCESSING':
                self.UseMultiprocessing = False
            elif LOption[0] != '-':
                self.ConfigFilePath = LOption
            else:
                ErrorLog("Invalid option '{Option}'.".format(Option = LOption))

        self.ProjectRoot = os.path.dirname(self.ConfigFilePath)
    #------------------------------------------------------#


    def __PrintInfoAboutOption(self, Option: str, Description: str) -> None:
        Log(f"{Option : <50}{'---' + Description : <50}")
    #------------------------------------------------------#