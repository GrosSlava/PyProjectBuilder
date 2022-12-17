# Copyright (c) 2022 GrosSlava

import os
import sys

import PyProjectBuilder.PyProjectBuildLibrary
import PyProjectBuilder.Logger
import PyProjectBuilder.ProgramOptions
import PyProjectBuilder.ConfigFileParser
import PyProjectBuilder.BuildPipeline





if __name__ == "__main__":
    if not PyProjectBuilder.PyProjectBuildLibrary.CheckCurrentPlatform():
        PyProjectBuilder.Logger.ErrorLog("Your os is not supported.")

    LProgramOptions = PyProjectBuilder.ProgramOptions.FProgramOptions(sys.argv[1:])
    LProjectConfig = PyProjectBuilder.ConfigFileParser.ParseConfigFile(LProgramOptions.ConfigFilePath)
    
    LBuildPipeline = PyProjectBuilder.BuildPipeline.FBuildPipeline(LProgramOptions, LProjectConfig)

    if LProgramOptions.Action is PyProjectBuilder.ProgramOptions.EAction.BUILD:
        LBuildPipeline.Build()
    elif LProgramOptions.Action is PyProjectBuilder.ProgramOptions.EAction.CLEAR:
        LBuildPipeline.Clear()
    elif LProgramOptions.Action is PyProjectBuilder.ProgramOptions.EAction.REBUILD:
        LBuildPipeline.Clear()
        LBuildPipeline.Build()