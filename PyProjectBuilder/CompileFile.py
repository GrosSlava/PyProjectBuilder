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
    Source file wrapper to implement it compilation.
'''
class FCompilingFile:
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile, ModuleName: str, FilePath: str):
        self.ProgramOptions = ProgramOptions    # cached program options
        self.ConfigFile = ConfigFile            # cached config file
        self.ModuleName = ModuleName            # cachd file module name
        self.FilePath = FilePath                # ceched file absolute path
    #------------------------------------------------------#



    def __GetCommandForGCC(self) -> list[str]:
        LSubprocessOptions = list[str]()
        LSubprocessOptions.append("gcc")
        if self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.X86:
            LSubprocessOptions.append("-m32")
        elif self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.X86_64:
            LSubprocessOptions.append("-m64")
        elif self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.ARM:
            LSubprocessOptions.append("-marm")
        elif self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.ARM_64:
            LSubprocessOptions.append("-marm")
        else:
            return []

        LSubprocessOptions.extend(["-c", "-Wextra", "-Wall"])
        LSubprocessOptions.extend(["-fexec-charset=UTF-8", "-finput-charset=UTF-8"])
        LSubprocessOptions.extend(["-masm=intel"])

        if self.ProgramOptions.BuildType == ProgramOptions.EBuildType.DEBUG:
            LSubprocessOptions.extend(["-O0", "-g"])
        elif self.ProgramOptions.BuildType == ProgramOptions.EBuildType.SHIPPING:
            LSubprocessOptions.extend(["-Ofast"])
        else:
            return []

        if self.ConfigFile.ConvertWarningsToErrors:
            LSubprocessOptions.append("-Werror")

        for LIncludeDir in self.ConfigFile.AdditionalIncludeDirs:
            LSubprocessOptions.append("-I" + os.path.join(self.ProgramOptions.ProjectRoot, LIncludeDir))

        LSubprocessOptions.append("-o" + os.path.join(FilesPath.GetModuleIntermediateFolderPath(self.ProgramOptions, self.ConfigFile, self.ModuleName), PyProjectBuildLibrary.GetFileName(self.FilePath) + ".o"))
        LSubprocessOptions.append(self.FilePath)
        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForGPP(self) -> list[str]:
        LSubprocessOptions = list[str]()
        LSubprocessOptions.append("g++")
        if self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.X86:
            LSubprocessOptions.append("-m32")
        elif self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.X86_64:
            LSubprocessOptions.append("-m64")
        elif self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.ARM:
            LSubprocessOptions.append("-marm")
        elif self.ProgramOptions.TargetArch == ProgramOptions.ETargetArch.ARM_64:
            LSubprocessOptions.append("-marm")
        else:
            return []

        LSubprocessOptions.extend(["-c", "-Wextra", "-Wall"])
        LSubprocessOptions.extend(["-fexec-charset=UTF-8", "-finput-charset=UTF-8"])
        LSubprocessOptions.extend(["-masm=intel"])

        if self.ProgramOptions.BuildType == ProgramOptions.EBuildType.DEBUG:
            LSubprocessOptions.extend(["-O0", "-g"])
        elif self.ProgramOptions.BuildType == ProgramOptions.EBuildType.SHIPPING:
            LSubprocessOptions.extend(["-Ofast"])
        else:
            return []

        if self.ConfigFile.ConvertWarningsToErrors:
            LSubprocessOptions.append("-Werror")

        for LIncludeDir in self.ConfigFile.AdditionalIncludeDirs:
            LSubprocessOptions.append("-I" + os.path.join(self.ProgramOptions.ProjectRoot, LIncludeDir))

        LSubprocessOptions.append("-o" + FilesPath.GetObjectFilePath(self.ProgramOptions, self.ConfigFile, self.ModuleName, PyProjectBuildLibrary.GetFileName(self.FilePath), ".o"))
        LSubprocessOptions.append(self.FilePath)
        return LSubprocessOptions
    #------------------------------------------------------#
    def __GetCommandForMSVC(self) -> list[str]:
        LSubprocessOptions = list[str]()
        #TODO
        return LSubprocessOptions
    #------------------------------------------------------#




    '''
        Process file compilation by third-party compiler.
        @return stderr string.
    '''
    def Compile(self) -> str:
        LPlatform  = platform.system()
        LFileExtension = PyProjectBuildLibrary.GetFileExtension(self.FilePath)
        LSubprocessOptions = list[str]()

        if LPlatform == PyProjectBuildLibrary.LINUX_PLATFORM:
            if LFileExtension in ["c", "C"]:
                LSubprocessOptions = self.__GetCommandForGCC()
            elif LFileExtension in ["cpp", "CPP"]:
                LSubprocessOptions = self.__GetCommandForGPP()
            else:
                return "Invalid file extension."
        elif LPlatform == PyProjectBuildLibrary.WINDOWS_PLATFORM:
            if LFileExtension in ["c", "C"]:
                LSubprocessOptions = self.__GetCommandForMSVC()
            elif LFileExtension in ["cpp", "CPP"]:
                LSubprocessOptions = self.__GetCommandForMSVC()
            else:
                return "Invalid file extension."
        else:
            return "Unsupported os."

        if len(LSubprocessOptions) == 0:
            return "Invalid command for compiler."
        LProcess = subprocess.run(LSubprocessOptions, capture_output=True)
        return LProcess.stderr.decode("utf-8")
    #------------------------------------------------------#
