# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from platform import system
import subprocess

from PyProjectBuilder.PyProjectBuildLibrary import *
from PyProjectBuilder.FilesPath import *
from PyProjectBuilder import ProjectConfigFile
from PyProjectBuilder import ProgramOptions





'''
	Source file wrapper to implement it compilation.
'''
class FCompilingFile:
	def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile, ModuleName: str, FilePath: str):
		self.ProgramOptions = ProgramOptions        # cached program options
		self.ConfigFile = ConfigFile                # cached config file
		self.ModuleName = ModuleName                # cachd file module name
		self.FilePath = FilePath                    # ceched file absolute path
	#------------------------------------------------------#



	def __GetCommandForGCC(self) -> list[str]:
		LSubprocessOptions = list[str]()
		LSubprocessOptions.extend(["gcc", "-std=c11", "-c", "-fexec-charset=UTF-8", "-finput-charset=UTF-8", "-masm=intel"])

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

		if self.ProgramOptions.BuildType == ProgramOptions.EBuildType.DEBUG:
			LSubprocessOptions.extend(["-O0", "-g"])
		elif self.ProgramOptions.BuildType == ProgramOptions.EBuildType.SHIPPING:
			LSubprocessOptions.extend(["-Ofast"])
		else:
			return []

		if self.ConfigFile.ConvertWarningsToErrors:
			LSubprocessOptions.append("-Werror")

		if self.ConfigFile.EnableAllWarnings:
			LSubprocessOptions.extend(["-Wextra", "-Wall"])

		LSubprocessOptions.extend(map(lambda LIncludeDir : "-I" + LIncludeDir, self.ConfigFile.AdditionalIncludeDirs))

		LSubprocessOptions.append("-o" + GetPlatformObjectFilePath(self.ProgramOptions, self.ConfigFile, self.ModuleName, GetFileName(self.FilePath)))
		LSubprocessOptions.append(self.FilePath)

		return LSubprocessOptions
	#------------------------------------------------------#
	def __GetCommandForGPP(self) -> list[str]:
		LSubprocessOptions = list[str]()
		LSubprocessOptions.extend(["g++", "-std=c++17", "-c", "-fexec-charset=UTF-8", "-finput-charset=UTF-8", "-masm=intel"])
		
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

		if self.ProgramOptions.BuildType == ProgramOptions.EBuildType.DEBUG:
			LSubprocessOptions.extend(["-O0", "-g"])
		elif self.ProgramOptions.BuildType == ProgramOptions.EBuildType.SHIPPING:
			LSubprocessOptions.extend(["-Ofast"])
		else:
			return []

		if self.ConfigFile.ConvertWarningsToErrors:
			LSubprocessOptions.append("-Werror")

		if self.ConfigFile.EnableAllWarnings:
			LSubprocessOptions.extend(["-Wextra", "-Wall"])

		LSubprocessOptions.extend(map(lambda LIncludeDir : "-I" + LIncludeDir, self.ConfigFile.AdditionalIncludeDirs))

		LSubprocessOptions.append("-o" + GetPlatformObjectFilePath(self.ProgramOptions, self.ConfigFile, self.ModuleName, GetFileName(self.FilePath)))
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
		LPlatform  = system()
		LFileExtension = GetFileExtension(self.FilePath)
		LSubprocessOptions = list[str]()

		if LPlatform == LINUX_PLATFORM:
			if LFileExtension in ["c", "C"]:
				LSubprocessOptions = self.__GetCommandForGCC()
			elif LFileExtension in ["cpp", "CPP"]:
				LSubprocessOptions = self.__GetCommandForGPP()
			else:
				return "Invalid file extension."
		elif LPlatform == WINDOWS_PLATFORM:
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
