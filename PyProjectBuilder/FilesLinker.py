# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import platform
import subprocess

import ProjectConfigFile
import ProgramOptions
import FilesPath
import PyProjectBuildLibrary





'''
    Man class to link object files.
'''
class FLinker:
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile, ObjectFiles: list[str], UsedExtensions: set[str]):
        self.ProgramOptions = ProgramOptions        # cached program options
        self.ConfigFile = ConfigFile                # cached config file
        self.ObjectFiles = ObjectFiles              # cached array of absolute paths to object files
        self.UsedExtensions = UsedExtensions        # cahced set of used extensions in project
    #------------------------------------------------------#



    def __GetCommandForLinuxExecutable(self) -> list[str]:
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

        LSubprocessOptions.append("-o" + FilesPath.GetBuildResultPath(self.ProgramOptions, self.ConfigFile))

        for LObjectFile in self.ObjectFiles:
            LSubprocessOptions.append(LObjectFile + ".o")

        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForLinuxDynamic(self) -> list[str]:
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

        LSubprocessOptions.extend(["-shared", "-fPIC"])

        LSubprocessOptions.append("-o" + FilesPath.GetBuildResultPath(self.ProgramOptions, self.ConfigFile))

        for LObjectFile in self.ObjectFiles:
            LSubprocessOptions.append(LObjectFile + ".o")

        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForLinuxStatic(self) -> list[str]:
        LSubprocessOptions = list[str]()
        
        LSubprocessOptions.extend(["ar", "rcs"])

        LSubprocessOptions.append(FilesPath.GetBuildResultPath(self.ProgramOptions, self.ConfigFile))

        for LObjectFile in self.ObjectFiles:
            LSubprocessOptions.append(LObjectFile + ".o")

        return LSubprocessOptions
    #------------------------------------------------------#
  
  
    def __GetCommandForWindowsExecutable(self) -> list[str]:
        LSubprocessOptions = list[str]()
        #TODO
        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForWindowsDynamic(self) -> list[str]:
        LSubprocessOptions = list[str]()
        #TODO
        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForWindowsStatic(self) -> list[str]:
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
            if self.ConfigFile.ResultType == ProjectConfigFile.EResultType.EXECUTABLE:
                LSubprocessOptions = self.__GetCommandForLinuxExecutable()
            elif self.ConfigFile.ResultType == ProjectConfigFile.EResultType.DYNAMIC_LIB:
                LSubprocessOptions = self.__GetCommandForLinuxDynamic()
            elif self.ConfigFile.ResultType == ProjectConfigFile.EResultType.STATIC_LIB:
                LSubprocessOptions = self.__GetCommandForLinuxStatic()
        elif LPlatform == PyProjectBuildLibrary.WINDOWS_PLATFORM:
            if self.ConfigFile.ResultType == ProjectConfigFile.EResultType.EXECUTABLE:
                LSubprocessOptions = self.__GetCommandForWindowsExecutable()
            elif self.ConfigFile.ResultType == ProjectConfigFile.EResultType.DYNAMIC_LIB:
                LSubprocessOptions = self.__GetCommandForWindowsDynamic()
            elif self.ConfigFile.ResultType == ProjectConfigFile.EResultType.STATIC_LIB:
                LSubprocessOptions = self.__GetCommandForWindowsStatic()
        else:
            return "Unsupported os."

        if len(LSubprocessOptions) == 0:
            return "Invalid command for linker."
        LProcess = subprocess.run(LSubprocessOptions, capture_output=True)
        return LProcess.stderr.decode("utf-8")
    #------------------------------------------------------#