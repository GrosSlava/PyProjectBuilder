# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import ProgramOptions
import ConfigFileParser





'''
    @return absolute path to project intermediate folder root.
'''
def GetIntermediateFolderRootPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile) -> str:
    return os.path.join(ProgramOptions.ProjectRoot, ConfigFile.IntermediateFolder)
#------------------------------------------------------#
'''
    @return absolute path to project intermediate folder.
'''
def GetIntermediateFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile) -> str:
    if ConfigFile.FlatIntermediate:
        return GetIntermediateFolderRootPath(ProgramOptions, ConfigFile)
    return os.path.join(GetIntermediateFolderRootPath(ProgramOptions, ConfigFile), str(ProgramOptions.BuildType))
#------------------------------------------------------#
'''
    @return absolute path to project module intermediate folder.
'''
def GetModuleIntermediateFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile, ModuleName: str) -> str:
    return os.path.join(GetIntermediateFolderPath(ProgramOptions, ConfigFile), ModuleName)
#------------------------------------------------------#

'''
    @return absolute path to project build folder root.
'''
def GetBuildFolderRootPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile) -> str:
    return os.path.join(ProgramOptions.ProjectRoot, ConfigFile.BuildFolder)
#------------------------------------------------------#
'''
    @return absolute path to project build folder.
'''
def GetBuildFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile) -> str:
    if ConfigFile.FlatBuild:
        return GetBuildFolderRootPath(ProgramOptions, ConfigFile)
    return os.path.join(GetBuildFolderRootPath(ProgramOptions, ConfigFile), str(ProgramOptions.BuildType))
#------------------------------------------------------#
'''
    @return absolute path to resulting file.
'''
def GetBuildResultPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile) -> str:
    return os.path.join(GetBuildFolderPath(ProgramOptions, ConfigFile), ConfigFile.ResultName)
#------------------------------------------------------#

'''
    @return absolute path to project module folder.
'''
def GetModuleFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ModuleRelativePath: str) -> str:
    return os.path.join(ProgramOptions.ProjectRoot, ModuleRelativePath)
#------------------------------------------------------#

'''
    @return absolute path to compiled object file.
'''
def GetObjectFilePath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile, ModuleName: str, FileName: str, Extension: str) -> str:
    return os.path.join(GetModuleIntermediateFolderPath(ProgramOptions, ConfigFile, ModuleName), FileName + Extension)
#------------------------------------------------------#
