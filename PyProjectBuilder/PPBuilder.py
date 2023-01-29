# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from PyProjectBuilder.Logger import *
from PyProjectBuilder.PyProjectBuildLibrary import CheckCurrentPlatform
from PyProjectBuilder import ProgramOptions
from PyProjectBuilder import ProjectConfigFile
from PyProjectBuilder import BuildPipeline





'''
	Run builder standard logic.
'''
def Run():
	if not CheckCurrentPlatform():
		ErrorLog("Your os is not supported.")

	LProgramOptions = ProgramOptions.FProgramOptions()
	LProjectConfig = ProjectConfigFile.ParseConfigFile(LProgramOptions.ConfigFilePath)
	
	LBuildPipeline = BuildPipeline.FBuildPipeline(LProgramOptions, LProjectConfig)

	if LProgramOptions.Action == ProgramOptions.EAction.BUILD:
		LBuildPipeline.Build()
	elif LProgramOptions.Action == ProgramOptions.EAction.CLEAR:
		LBuildPipeline.Clear()
	elif LProgramOptions.Action == ProgramOptions.EAction.REBUILD:
		LBuildPipeline.Clear()
		LBuildPipeline.Build()
	else:
		ErrorLog("Invalid builder action.")
#------------------------------------------------------#



if __name__ == "__main__":
	Run()
	