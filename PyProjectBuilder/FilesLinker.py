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
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile, ObjectFiles: list[str]):
        self.ProgramOptions = ProgramOptions    # cached program options
        self.ConfigFile = ConfigFile            # cached config file
        self.ObjectFiles = ObjectFiles          # cached array of paths to object files
    #------------------------------------------------------#



    def __GetCommandForLinux(self) -> list[str]:
        LSubprocessOptions = list[str]()
        #TODO
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