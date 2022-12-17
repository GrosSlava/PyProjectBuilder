# Copyright (c) 2022 GrosSlava

import os
import sys

import platform

import Private.BuildInfo
import Private.Logger
import Private.ProgramOptions
import Private.ConfigFileParser
import Private.BuildPipeline





if __name__ == "__main__":
    if not Private.BuildInfo.CheckPlatform(platform.system()):
        Private.Logger.ErrorLog("PyProjectBuilder", "Your os is unsupported.")

    LProgramOptions = Private.ProgramOptions.FProgramOptions(sys.argv[1:])

    LProjectConfig = Private.ConfigFileParser.ParseConfigFile(LProgramOptions.ConfigFilePath)
    LBuildPipeline = Private.BuildPipeline.FBuildPipeline(LProgramOptions, LProjectConfig)

    if LProgramOptions.Action is Private.ProgramOptions.EAction.BUILD:
        LBuildPipeline.Build()
    elif LProgramOptions.Action is Private.ProgramOptions.EAction.CLEAR:
        LBuildPipeline.Clear()
    elif LProgramOptions.Action is Private.ProgramOptions.EAction.REBUILD:
        LBuildPipeline.Clear()
        LBuildPipeline.Build()