# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import FunctionLibrary
import Logger





'''
    Project build connfig.
'''
class FConfigFile:
    def __init__(self, ConfigFilePath: str):
        self.ConfigFilePath = ConfigFilePath        # absolute path to project config file
        self.IntermediateFolder = "Intermediate"    # relative path to folder for intermediate files
        self.BuildFolder = "Build"                  # relative path to folder for build files
        self.BuildModules = []                      # array of paths to modules(folders) to build
        self.Ignore = []                            # array of relative paths to files/folders to ignore
        self.IsLibrary = False                      # build as library or not
        self.ResultName = "a"                       # name of building result
    #------------------------------------------------------#



'''
    Read project config form "PyBuildFile.txt" file.
    @param ConfigFilePath - absolute path to project config file.
    @return FConfigFile.
'''
def ParseConfigFile(ConfigFilePath: str) -> FConfigFile:
    if not FunctionLibrary.CheckAbsPath(ConfigFilePath):
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
            elif LLeft == "BuildFolder":
                LProjectConfig.BuildFolder = LRight
            elif LLeft == "IsLibrary":
                LProjectConfig.IsLibrary = FunctionLibrary.StrToBool(LRight)
            elif LLeft == "Modules":
                LProjectConfig.BuildModules.extend(LRight.split(';'))
            elif LLeft == "Ignore":
                LProjectConfig.Ignore.extend(LRight.split(';'))
            elif LLeft == "ResultName":
                LProjectConfig.ResultName = LRight
            else:
                Logger.ErrorLog("Invalid configuration key: '{Key}'.".format(Key = LLeft))

        LIntermediateFolderStripped = LProjectConfig.IntermediateFolder.strip()
        if LIntermediateFolderStripped == "" or LIntermediateFolderStripped == "." or LIntermediateFolderStripped == "..":
            Logger.ErrorLog("Intermediate folder should be set as directory.")
        LBuildFolderStripped = LProjectConfig.BuildFolder.strip()
        if LBuildFolderStripped == "" or LBuildFolderStripped == "." or LBuildFolderStripped == "..":
            Logger.ErrorLog("Build folder should be set as directory.")

    return LProjectConfig
#------------------------------------------------------#