# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import enum

import PyProjectBuildLibrary
import Logger





'''
    Project build result type.
'''
class EResultType(enum.IntEnum):
    EXECUTABLE = 1,         # Build as executable
    STATIC_LIB = 2,         # Build as static library
    DYNAMIC_LIB = 3         # Build as dynamic library

    def __str__(self):
        return self.name
    #------------------------------------------------------#



'''
    Project build connfig.
'''
class FConfigFile:
    def __init__(self, ConfigFilePath: str):
        self.ConfigFilePath = ConfigFilePath        # absolute path to project config file
        self.IntermediateFolder = "Intermediate"    # relative path to folder for intermediate files
        self.FlatIntermediate = False               # put all intermediate files in one folder
        self.BuildFolder = "Build"                  # relative path to folder for build files
        self.FlatBuild = False                      # put all build files in one folder
        self.BuildModules = list[str]()             # array of relative paths to modules(folders) to build
        self.Ignore = list[str]()                   # array of relative paths to files/folders to ignore
        self.AdditionalIncludeDirs = list[str]()    # array of relative paths to dirs for includes search 
        self.AdditionalLibsDirs = list[str]()       # array of absolute paths to dirs for libraries search 
        self.Libs = list[str]()                     # array of absolute paths to libs files or its name to link
        self.ResultType = EResultType.EXECUTABLE    # result of result of building
        self.ResultName = "a"                       # name of building result
        self.EntryPointName = ""                    # name of the function that will be the entry point (empty means compiler default)
        self.ConvertWarningsToErrors = False        # tell compiler convert warnings into errors
    #------------------------------------------------------#



'''
    Read project config form "PyBuildFile.txt" file.
    @param ConfigFilePath - absolute path to project config file.
    @return FConfigFile.
'''
def ParseConfigFile(ConfigFilePath: str) -> FConfigFile:
    if not PyProjectBuildLibrary.CheckAbsPath(ConfigFilePath):
        Logger.ErrorLog("Invalid config file path.")

    LProjectConfig = FConfigFile(ConfigFilePath)
    with open(ConfigFilePath, "r", encoding = 'utf-8') as ProjectConfigFile:
        for LLine in ProjectConfigFile:
            S = LLine.strip()
            if len(S) < 1:
                continue
            if S[0] == '#':
                continue
            S = S.split('=')
            if len(S) != 2:
                continue
            
            LLeft = S[0].strip()
            LRight = S[1].strip()
            if LLeft == "IntermediateFolder":
                LProjectConfig.IntermediateFolder = LRight
            elif LLeft == "FlatIntermediate":
                LProjectConfig.FlatIntermediate = PyProjectBuildLibrary.StrToBool(LRight)
            elif LLeft == "BuildFolder":
                LProjectConfig.BuildFolder = LRight
            elif LLeft == "FlatBuild":
                LProjectConfig.FlatBuild = PyProjectBuildLibrary.StrToBool(LRight)
            elif LLeft == "Modules":
                LProjectConfig.BuildModules.extend(PyProjectBuildLibrary.SplitAndStrip(LRight, ';'))
            elif LLeft == "Ignore":
                LProjectConfig.Ignore.extend(PyProjectBuildLibrary.SplitAndStrip(LRight, ';'))
            elif LLeft == "AdditionalIncludeDirs":
                LProjectConfig.AdditionalIncludeDirs.extend(PyProjectBuildLibrary.SplitAndStrip(LRight, ';'))
            elif LLeft == "AdditionalLibsDirs":
                LProjectConfig.AdditionalLibsDirs.extend(PyProjectBuildLibrary.SplitAndStrip(LRight, ';'))
            elif LLeft == "Libs":
                LProjectConfig.Libs.extend(PyProjectBuildLibrary.SplitAndStrip(LRight, ';'))
            elif LLeft == "ResultType":
                if LRight in ["Executable", "EXECUTABLE", "executable", "exe"]:
                    LProjectConfig.ResultType = EResultType.EXECUTABLE
                elif LRight in ["StaticLib", "STATIC_LIB", "Static", "STATIC", "static"]:
                    LProjectConfig.ResultType = EResultType.STATIC_LIB
                elif LRight in ["DynamicLib", "DYNAMIC_LIB", "Dynamic", "DYNAMIC", "dynamic"]:
                    LProjectConfig.ResultType = EResultType.DYNAMIC_LIB
                else:
                    Logger.ErrorLog("Invalid configuration value: '{Value}'.".format(Value = LRight))
            elif LLeft == "ResultName":
                LProjectConfig.ResultName = LRight
            elif LLeft == "EntryPointName":
                LProjectConfig.EntryPointName = LRight
            elif LLeft == "ConvertWarningsToErrors":
                LProjectConfig.ConvertWarningsToErrors = PyProjectBuildLibrary.StrToBool(LRight)
            else:
                Logger.ErrorLog("Invalid configuration key: '{Key}'.".format(Key = LLeft))

        if LProjectConfig.IntermediateFolder in ["", ".", ".."]:
            Logger.ErrorLog("Intermediate folder should be set as directory.")
        if LProjectConfig.BuildFolder in ["", ".", ".."]:
            Logger.ErrorLog("Build folder should be set as directory.")
        if LProjectConfig.ResultName in ["", ".", ".."]:
            Logger.ErrorLog("Invalid result name.")

    return LProjectConfig
#------------------------------------------------------#