# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from os import getcwd
from os.path import join as JoinPath
from enum import IntEnum
from optparse import OptionParser

from PyProjectBuilder.Logger import *
from PyProjectBuilder.PyProjectBuildLibrary import *





'''
	Project build type.
'''
class EBuildType(IntEnum):
	DEBUG = 1,          # Build in debug mode
	SHIPPING = 2        # Build in release mode

	def __str__(self):
		return self.name
	#------------------------------------------------------#

'''
	Target architecture.
'''
class ETargetArch(IntEnum):
	X86 = 1,            # Build for x86
	X86_64 = 2,         # Build for x86-64
	ARM = 3,            # build for arm
	ARM_64 = 4          # build for arm-64

	def __str__(self):
		return self.name
	#------------------------------------------------------#

'''
	Tool action.
'''
class EAction(IntEnum):
	BUILD = 1,          # Build project
	REBUILD = 2,        # Clear intermediate and build project
	CLEAR = 3           # Clear intermediate files

	def __str__(self):
		return self.name
	#------------------------------------------------------#




'''
	Helper structure to contain execution options.
'''
class FProgramOptions:
	def __init__(self):
		self.ConfigFilePath = JoinPath(getcwd(), "PyBuildFile.txt")  # absolute path to config file
		self.ProjectRoot = getcwd()                                  # absolute path to project root dir
		self.Action = EAction.BUILD                                  # current action
		self.BuildType = EBuildType.DEBUG                            # build type
		self.TargetArch = ETargetArch.X86_64                         # build target architecture
		self.Silent = False                                          # mark to not print messages
		self.UseMultiprocessing = True                               # use all cores for parallel compilation


		LParser = OptionParser(version = PY_PROJECT_BUILD_VERSION, conflict_handler = "error", add_help_option = True, description = "Tool to build c/c++ project.")
		
		# -h --help already exists
		# --version already exists
		LParser.add_option("-a", "--Action", action = "store", type = "choice", dest = "Action", metavar = "TYPE", choices = ["Build", "Rebuild", "Clear"], help = "select tool action [Build, Rebuild, Clear]") 
		LParser.add_option("-b", "--BuildType", action = "store", type = "choice", dest = "BuildType", metavar = "TYPE", choices = ["Debug", "Shipping"], help = "type of build [Debug, Shipping]") 
		LParser.add_option("-t", "--TargetArch", action = "store", type = "choice", dest = "TargetArch", metavar = "ARCH", choices = ["x86", "x86_64", "arm", "arm_64"], help = "build target architecture [x86, x86_64, arm, arm_64]") 
		LParser.add_option("-s", "--SILENT", action = "store_true", dest = "SILENT", help = "disable compilation logs") 
		LParser.add_option("--NO_MULTIPROCESSING", action = "store_true", dest = "NO_MULTIPROCESSING", help = "disable parallel compilation") 

		LOptions, LArgs = LParser.parse_args()
		LOptions = LOptions.__dict__

		if len(LArgs) > 0:
			self.ConfigFilePath = LArgs[0]
			self.ProjectRoot = GetFilePath(self.ConfigFilePath)

		LActionType = LOptions["Action"]
		if LActionType == "Build":
			self.Action = EAction.BUILD 
		elif LActionType == "Rebuild":
			self.Action = EAction.REBUILD 
		elif LActionType == "Clear":
			self.Action = EAction.CLEAR 

		LBuildType = LOptions["BuildType"]
		if LBuildType == "Debug":
			self.BuildType = EBuildType.DEBUG 
		elif LBuildType == "Shipping":
			self.BuildType = EBuildType.SHIPPING  

		LTargetArch = LOptions["TargetArch"]
		if LTargetArch == "x86":
			self.TargetArch = ETargetArch.X86 
		elif LTargetArch == "x86_64":
			self.TargetArch = ETargetArch.X86_64
		elif LTargetArch == "arm":
			self.TargetArch = ETargetArch.ARM
		elif LTargetArch == "arm_64":
			self.TargetArch = ETargetArch.ARM_64 
			
		self.Silent = LOptions["SILENT"] 

		self.UseMultiprocessing = not LOptions["NO_MULTIPROCESSING"]    
	#------------------------------------------------------#