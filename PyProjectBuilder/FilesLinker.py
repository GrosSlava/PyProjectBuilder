# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from platform import system
import subprocess

from PyProjectBuilder.PyProjectBuildLibrary import *
from PyProjectBuilder.FilesPath import *
from PyProjectBuilder import ProjectConfigFile
from PyProjectBuilder import ProgramOptions





'''
	Man class to link object files.
'''
class FLinker:
	def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile, ObjectFiles: list[str], UsedExtensions: set[str]):
		self.ProgramOptions = ProgramOptions        # cached program options
		self.ConfigFile = ConfigFile                # cached config file
		self.ObjectFiles = ObjectFiles              # cached array of absolute paths to object files
		self.UsedExtensions = UsedExtensions        # cached set of used extensions in project
	#------------------------------------------------------#



	def __GetCommandForLinuxExecutable(self) -> list[str]:
		LSubprocessOptions = list[str]()
		if "CPP" in self.UsedExtensions or "cpp" in self.UsedExtensions:
			LSubprocessOptions.append("g++")
		else:
			LSubprocessOptions.append("gcc")

		LSubprocessOptions.extend(map(lambda LLibSearchDir : "-L" + LLibSearchDir, self.ConfigFile.AdditionalLibsDirs))
		LSubprocessOptions.extend(map(lambda LLib : "-l" + LLib, self.ConfigFile.Libs))

		if self.ConfigFile.EntryPointName != "":
			LSubprocessOptions.append("-nostartfiles")
			LSubprocessOptions.append("-e" + self.ConfigFile.EntryPointName)

		LSubprocessOptions.append("-o" + GetBuildResultPath(self.ProgramOptions, self.ConfigFile))
		LSubprocessOptions.extend(map(lambda LObjectFile : LObjectFile + ".o", self.ObjectFiles))
		   
		return LSubprocessOptions
	#------------------------------------------------------#
	def __GetCommandForLinuxDynamic(self) -> list[str]:
		LSubprocessOptions = list[str]()
		if "CPP" in self.UsedExtensions or "cpp" in self.UsedExtensions:
			LSubprocessOptions.append("g++")
		else:
			LSubprocessOptions.append("gcc")

		LSubprocessOptions.extend(map(lambda LLibSearchDir : "-L" + LLibSearchDir, self.ConfigFile.AdditionalLibsDirs))
		LSubprocessOptions.extend(map(lambda LLib : "-l" + LLib, self.ConfigFile.Libs))

		if self.ConfigFile.EntryPointName != "":
			LSubprocessOptions.append("-nostartfiles")
			LSubprocessOptions.append("-e" + self.ConfigFile.EntryPointName)

		LSubprocessOptions.extend(["-shared", "-fPIC"])

		LSubprocessOptions.append("-o" + GetBuildResultPath(self.ProgramOptions, self.ConfigFile))
		LSubprocessOptions.extend(map(lambda LObjectFile : LObjectFile + ".o", self.ObjectFiles))

		return LSubprocessOptions
	#------------------------------------------------------#
	def __GetCommandForLinuxStatic(self) -> list[str]:
		LSubprocessOptions = list[str]()
		LSubprocessOptions.extend(["ar", "rcs"])

		LSubprocessOptions.append(GetBuildResultPath(self.ProgramOptions, self.ConfigFile))
		LSubprocessOptions.extend(map(lambda LObjectFile : LObjectFile + ".o", self.ObjectFiles))

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
		LPlatform  = system()
		LSubprocessOptions = list[str]()

		if LPlatform == LINUX_PLATFORM:
			if self.ConfigFile.ResultType == ProjectConfigFile.EResultType.EXECUTABLE:
				LSubprocessOptions = self.__GetCommandForLinuxExecutable()
			elif self.ConfigFile.ResultType == ProjectConfigFile.EResultType.DYNAMIC_LIB:
				LSubprocessOptions = self.__GetCommandForLinuxDynamic()
			elif self.ConfigFile.ResultType == ProjectConfigFile.EResultType.STATIC_LIB:
				LSubprocessOptions = self.__GetCommandForLinuxStatic()
		elif LPlatform == WINDOWS_PLATFORM:
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