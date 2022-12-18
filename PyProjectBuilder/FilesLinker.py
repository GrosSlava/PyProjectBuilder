# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import platform
import subprocess

import ConfigFileParser
import ProgramOptions
import FilesPath
import PyProjectBuildLibrary





'''
    Man class to link object files.
'''
class FLinker:
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile, ObjectFiles: list[str], UsedExtensions: set[str]):
        self.ProgramOptions = ProgramOptions    # cached program options
        self.ConfigFile = ConfigFile            # cached config file
        self.ObjectFiles = ObjectFiles          # cached array of absolute paths to object files
        self.UsedExtensions = UsedExtensions    # cahced set of used extensions in project
    #------------------------------------------------------#



    def __GetCommandForLinux(self) -> list[str]:
        LSubprocessOptions = list[str]()
        if "CPP" in self.UsedExtensions or "cpp" in self.UsedExtensions:
            LSubprocessOptions.append("g++")
        else:
            LSubprocessOptions.append("gcc")

        for LLibSearchDir in self.ConfigFile.AdditionalLibsDirs:
            LSubprocessOptions.append("-L" + LLibSearchDir)

        for LLib in self.ConfigFile.Libs:
            LSubprocessOptions.append("-l" + LLib)

        if self.ConfigFile.EntryPointName != "":
            LSubprocessOptions.append("-nostartfiles")
            LSubprocessOptions.append("-e" + self.ConfigFile.EntryPointName)

        if self.ConfigFile.IsLibrary:
            LSubprocessOptions.extend(["-shared", "-fPIC"])

        LSubprocessOptions.append("-o" + FilesPath.GetBuildResultPath(self.ProgramOptions, self.ConfigFile))

        for LObjectFile in self.ObjectFiles:
            LSubprocessOptions.append(LObjectFile + ".o")

        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForWindows(self) -> list[str]:
        LSubprocessOptions = list[str]()
        #TODO
        return LSubprocessOptions
    #------------------------------------------------------#




    '''
        Process file linking by third-party linker.
        @return stderr string.
    '''
    def Link(self) -> str:
        LPlatform  = platform.system()
        LSubprocessOptions = list[str]()

        if LPlatform == PyProjectBuildLibrary.LINUX_PLATFORM:
            LSubprocessOptions = self.__GetCommandForLinux()
        elif LPlatform == PyProjectBuildLibrary.WINDOWS_PLATFORM:
            LSubprocessOptions = self.__GetCommandForWindows()
        else:
            return "Unsupported os."

        if len(LSubprocessOptions) == 0:
            return "Invalid command for linker."
        LProcess = subprocess.run(LSubprocessOptions, capture_output=True)
        return LProcess.stderr.decode("utf-8")
    #------------------------------------------------------#