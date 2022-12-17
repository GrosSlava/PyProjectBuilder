# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import shutil
import pathlib
import glob
import multiprocessing

import FunctionLibrary
import Logger
import ProgramOptions
import ConfigFileParser
import CompileFile






'''
    Main class to implement project building.
'''
class FBuildPipeline:
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile):
        self.ProgramOptions = ProgramOptions        # cached program options
        self.ConfigFile = ConfigFile                # cached config file info
        self.FilesToCompile = []                    # array of files to build
    

        self.ProcessesManager = multiprocessing.Manager()
        self.BuildProgress = self.ProcessesManager.Value("BuildProgress", 0)                      # count of compiled files
        self.ProgessMutex = multiprocessing.Lock()  # mutex for BuildProgress

        self.CPUCount = multiprocessing.cpu_count()
        for i in range(len(self.ConfigFile.Ignore)):
            self.ConfigFile.Ignore[i] = os.path.join(self.ProgramOptions.ProjectRoot, self.ConfigFile.Ignore[i])
    #------------------------------------------------------#



    '''
        @return absolute path to project intermediate folder.
    '''
    def __GetIntermediateFolderPath(self) -> str:
        return os.path.join(self.ProgramOptions.ProjectRoot, self.ConfigFile.IntermediateFolder)
    #------------------------------------------------------#
    '''
        @return absolute path to project build folder.
    '''
    def __GetBuildFolderPath(self) -> str:
        return os.path.join(self.ProgramOptions.ProjectRoot, self.ConfigFile.BuildFolder)
    #------------------------------------------------------#
    '''
        @return absolute path to project module folder.
    '''
    def __GetModuleFolderPath(self, ModuleRelativePath: str) -> str:
        return os.path.join(self.ProgramOptions.ProjectRoot, ModuleRelativePath)
    #------------------------------------------------------#
    '''
        Check that path is ignored by any from ingore array.
    '''
    def __IsPathIgnored(self, FilePath: str) -> bool:
        for LIgnorePath in self.ConfigFile.Ignore:
            if FilePath.startswith(LIgnorePath) or LIgnorePath == FilePath:
                return True
        return False
    #------------------------------------------------------#

    '''
        Thread safe to increment build progress.
    '''
    def __IncrementBuildProcess(self, CompiledFile: str) -> None:
        self.ProgessMutex.acquire()
        self.BuildProgress.value += 1
        Logger.Log("[{Progress}/{Total}] {File}".format(Progress = str(self.BuildProgress.value), Total = str(len(self.FilesToCompile)), File = CompiledFile))
        self.ProgessMutex.release()
    #------------------------------------------------------#



    def __CheckFileNeedToBuild(self, FilePath: str) -> bool:
        #TODO
        return True
    #------------------------------------------------------#
    '''
        Prepere for building. Crete needed folders. Check modules.
    '''
    def __PrepareForBuild(self) -> None:
        FunctionLibrary.CreateDirIfNotExist(self.__GetIntermediateFolderPath())
        FunctionLibrary.CreateDirIfNotExist(os.path.join(self.__GetIntermediateFolderPath(), str(self.ProgramOptions.BuildType)))  

        LBuildDir = self.__GetBuildFolderPath()
        if os.path.exists(LBuildDir) and os.path.isdir(LBuildDir):
            shutil.rmtree(LBuildDir)
        FunctionLibrary.CreateDirIfNotExist(LBuildDir)
        FunctionLibrary.CreateDirIfNotExist(os.path.join(LBuildDir, str(self.ProgramOptions.BuildType)))  

        for LModule in self.ConfigFile.BuildModules:
            LModulePath = self.__GetModuleFolderPath(LModule)
            if not os.path.exists(LModulePath) or not os.path.isdir(LModulePath):
                Logger.WarningLog("Module '{ModulePath}' not exist.".format(ModulePath = LModule))
                continue

            FunctionLibrary.CreateDirIfNotExist(os.path.join(self.__GetIntermediateFolderPath(), str(self.ProgramOptions.BuildType), LModule))  

            for LFileName in glob.iglob(os.path.join(LModulePath, "**"), recursive = True):
                if not os.path.isfile(LFileName):
                    continue
                if pathlib.Path(LFileName).suffix == ".cpp" or pathlib.Path(LFileName).suffix == ".c":
                    if self.__IsPathIgnored(LFileName) or not self.__CheckFileNeedToBuild(LFileName):
                        continue
                    self.FilesToCompile.append(CompileFile.FCompilingFile(self.ProgramOptions.ProjectRoot, self.ConfigFile, LModule, LFileName))
    #------------------------------------------------------#
   
    '''
        Do parallel build work.
    '''
    def __ProcessParallelBuild(self, ProcessIndex: int) -> None:
        for i in range(ProcessIndex, len(self.FilesToCompile), self.CPUCount):
            self.FilesToCompile[i].Compile()
            self.__IncrementBuildProcess(self.FilesToCompile[i].FilePath + "  " + str(ProcessIndex))
    #------------------------------------------------------#
    '''
        Do build actions.
    '''
    def __ProcessBuild(self) -> None:
        Logger.Log("Compiling {CountOfFiles} by {CPUCount} processes...".format(CountOfFiles = str(len(self.FilesToCompile)), CPUCount = str(self.CPUCount)))
        
        LWorkersPool = []
        for i in range(self.CPUCount):
            p = multiprocessing.Process(target = self.__ProcessParallelBuild, args=(i,))
            LWorkersPool.append(p)
            p.start()

        for i in range(self.CPUCount):
            LWorkersPool[i].join()
    #------------------------------------------------------#
   
    '''
        Call linker to link compiled object files.
    '''
    def __LinkObjectFiles(self) -> None:
        #TODO
        pass
    #------------------------------------------------------#



    '''
        Start project build.
    '''
    def Build(self) -> None:
        self.__PrepareForBuild()
        self.__ProcessBuild()
        self.__LinkObjectFiles()
    #------------------------------------------------------#
    '''
        Clear intermediate files.
    '''
    def Clear(self) -> None:
        LIntermediateDir = self.__GetIntermediateFolderPath()
        if os.path.exists(LIntermediateDir) and os.path.isdir(LIntermediateDir):
            shutil.rmtree(LIntermediateDir)
    #------------------------------------------------------#