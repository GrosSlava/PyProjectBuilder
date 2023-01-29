# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from os.path import join as JoinPath
from platform import system

from PyProjectBuilder.PyProjectBuildLibrary import *
from PyProjectBuilder import ProgramOptions
from PyProjectBuilder import ProjectConfigFile





'''
	@return absolute path to project intermediate folder root.
'''
def GetIntermediateFolderRootPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile) -> str:
	return JoinPath(ProgramOptions.ProjectRoot, ConfigFile.IntermediateFolder)
#------------------------------------------------------#
'''
	@return absolute path to project intermediate folder.
'''
def GetIntermediateFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile) -> str:
	if ConfigFile.FlatIntermediate:
		return GetIntermediateFolderRootPath(ProgramOptions, ConfigFile)
	return JoinPath(GetIntermediateFolderRootPath(ProgramOptions, ConfigFile), str(ProgramOptions.BuildType))
#------------------------------------------------------#
'''
	@return absolute path to project module intermediate folder.
'''
def GetModuleIntermediateFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile, ModuleName: str) -> str:
	return JoinPath(GetIntermediateFolderPath(ProgramOptions, ConfigFile), ModuleName)
#------------------------------------------------------#

'''
	@return absolute path to project build folder root.
'''
def GetBuildFolderRootPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile) -> str:
	return JoinPath(ProgramOptions.ProjectRoot, ConfigFile.BuildFolder)
#------------------------------------------------------#
'''
	@return absolute path to project build folder.
'''
def GetBuildFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile) -> str:
	if ConfigFile.FlatBuild:
		return GetBuildFolderRootPath(ProgramOptions, ConfigFile)
	return JoinPath(GetBuildFolderRootPath(ProgramOptions, ConfigFile), str(ProgramOptions.BuildType))
#------------------------------------------------------#
'''
	@return absolute path to resulting file.
'''
def GetBuildResultPath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile) -> str:
	return JoinPath(GetBuildFolderPath(ProgramOptions, ConfigFile), ConfigFile.ResultName)
#------------------------------------------------------#

'''
	@return absolute path to project module folder.
'''
def GetModuleFolderPath(ProgramOptions: ProgramOptions.FProgramOptions, ModuleRelativePath: str) -> str:
	return JoinPath(ProgramOptions.ProjectRoot, ModuleRelativePath)
#------------------------------------------------------#

'''
	@return absolute path to compiled object file.
'''
def GetObjectFilePath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile, ModuleName: str, FileName: str, Extension: str) -> str:
	LFileName = FileName
	if len(Extension) > 0:
		if Extension[0] != ".":
			LFileName += "." + Extension
		else:
			LFileName += Extension
	return JoinPath(GetModuleIntermediateFolderPath(ProgramOptions, ConfigFile, ModuleName), LFileName)
#------------------------------------------------------#
'''
	@return absolute path to compiled object file with platform specific object file extension.
'''
def GetPlatformObjectFilePath(ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile, ModuleName: str, FileName: str):
	LPlatform  = system()
	if LPlatform == LINUX_PLATFORM:
		return GetObjectFilePath(ProgramOptions, ConfigFile, ModuleName, FileName, "o")
	elif LPlatform == WINDOWS_PLATFORM:
		return GetObjectFilePath(ProgramOptions, ConfigFile, ModuleName, FileName, "obj") 
	else:
		return ""
#------------------------------------------------------#
