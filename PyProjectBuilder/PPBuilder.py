# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import PyProjectBuildLibrary
import Logger
import ProgramOptions
import ProjectConfigFile
import BuildPipeline





'''
    Run builder standard logic.
'''
def Run():
    if not PyProjectBuildLibrary.CheckCurrentPlatform():
        Logger.ErrorLog("Your os is not supported.")

    LProgramOptions = ProgramOptions.FProgramOptions(sys.argv[1:])
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
        Logger.ErrorLog("Invalid builder action.")
#------------------------------------------------------#



if __name__ == "__main__":
    Run()
    