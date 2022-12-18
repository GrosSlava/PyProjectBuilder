# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import glob
import multiprocessing

import PyProjectBuildLibrary
import FilesPath
import Logger
import ProgramOptions
import ConfigFileParser
import CompileFile
import FilesLinker





'''
    Main class to implement project building.
'''
class FBuildPipeline:
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ConfigFileParser.FConfigFile):
        self.ProgramOptions = ProgramOptions                            # cached program options
        self.ConfigFile = ConfigFile                                    # cached config file info
        self.FilesToCompile = list[CompileFile.FCompilingFile]()        # array of files to build
        self.ObjectFiles = list[str]()                                  # array of paths to object files to link (without platform specific extension)
        self.UsedExtensions = set[str]()                                # set of all used files extensions in project
    
        self.ProcessesManager = multiprocessing.Manager()
        self.BuildProgress = self.ProcessesManager.Value("BuildProgress", 0)                   
        self.ProgessMutex = multiprocessing.Lock()

        if self.ProgramOptions.UseMultiprocessing:
            self.CPUCount = multiprocessing.cpu_count()
        else:
            self.CPUCount = 1


        LBuildModules = list[str]()
        for i in range(len(self.ConfigFile.BuildModules)):
            if self.ConfigFile.BuildModules[i].strip() == "":
                continue
            LBuildModules.append(self.ConfigFile.BuildModules[i].strip())
        self.ConfigFile.BuildModules = LBuildModules

        LIgnoreFiles = list[str]()
        for i in range(len(self.ConfigFile.Ignore)):
            if self.ConfigFile.Ignore[i].strip() == "":
                continue
            LIgnoreFiles.append(os.path.join(self.ProgramOptions.ProjectRoot, self.ConfigFile.Ignore[i].strip()))
        self.ConfigFile.Ignore = LIgnoreFiles

        LAdditionalIncludeDirs = list[str]()
        for i in range(len(self.ConfigFile.AdditionalIncludeDirs)):
            if self.ConfigFile.AdditionalIncludeDirs[i].strip() == "":
                continue
            LAdditionalIncludeDirs.append(self.ConfigFile.AdditionalIncludeDirs[i].strip())
        self.ConfigFile.AdditionalIncludeDirs = LAdditionalIncludeDirs

        LAdditionalLibsDirs = list[str]()
        for i in range(len(self.ConfigFile.AdditionalLibsDirs)):
            if self.ConfigFile.AdditionalLibsDirs[i].strip() == "":
                continue
            LAdditionalLibsDirs.append(self.ConfigFile.AdditionalLibsDirs[i].strip())
        self.ConfigFile.AdditionalLibsDirs = LAdditionalLibsDirs

        LLibs = list[str]()
        for i in range(len(self.ConfigFile.Libs)):
            if self.ConfigFile.Libs[i].strip() == "":
                continue
            LLibs.append(self.ConfigFile.Libs[i].strip())
        self.ConfigFile.Libs = LLibs
    #------------------------------------------------------#



    '''
        Log message with silent check.
    '''
    def __Log(self, Message: str) -> None:
        if self.ProgramOptions.Silent:
            return
        Logger.Log(Message)
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
    def __IncrementBuildProcess(self) -> None:
        self.ProgessMutex.acquire()
        self.BuildProgress.value += 1
        self.ProgessMutex.release()
    #------------------------------------------------------#




    '''
        Check that file need to be rebuild.
    '''
    def __CheckFileNeedToBuild(self, FilePath: str) -> bool:
        #TODO
        return True
    #------------------------------------------------------#
    '''
        Prepere for building. Create needed folders. Check modules.
    '''
    def __PrepareForBuild(self) -> None:
        PyProjectBuildLibrary.CreateDirIfNotExist(FilesPath.GetIntermediateFolderRootPath(self.ProgramOptions, self.ConfigFile))
        PyProjectBuildLibrary.CreateDirIfNotExist(FilesPath.GetIntermediateFolderPath(self.ProgramOptions, self.ConfigFile))  

        PyProjectBuildLibrary.CreateDirIfNotExist(FilesPath.GetBuildFolderRootPath(self.ProgramOptions, self.ConfigFile))
        PyProjectBuildLibrary.CreateDirIfNotExist(FilesPath.GetBuildFolderPath(self.ProgramOptions, self.ConfigFile))  

        for LModule in self.ConfigFile.BuildModules:
            LModulePath = FilesPath.GetModuleFolderPath(self.ProgramOptions, LModule)
            if not PyProjectBuildLibrary.CheckDirExists(LModulePath):
                Logger.WarningLog("Module '{ModulePath}' not exist.".format(ModulePath = LModule))
                continue

            PyProjectBuildLibrary.CreateDirIfNotExist(FilesPath.GetModuleIntermediateFolderPath(self.ProgramOptions, self.ConfigFile, LModule))  

            for LFileName in glob.iglob(os.path.join(LModulePath, "**"), recursive = True):
                if not PyProjectBuildLibrary.IsFileSupported(LFileName) or self.__IsPathIgnored(LFileName):
                    continue
                if self.__CheckFileNeedToBuild(LFileName):
                    self.FilesToCompile.append(CompileFile.FCompilingFile(self.ProgramOptions, self.ConfigFile, LModule, LFileName))
                self.ObjectFiles.append(FilesPath.GetObjectFilePath(self.ProgramOptions, self.ConfigFile, LModule, PyProjectBuildLibrary.GetFileName(LFileName), ""))
                self.UsedExtensions.add(PyProjectBuildLibrary.GetFileExtension(LFileName))
    #------------------------------------------------------#

    '''
        Do parallel build work.
    '''
    def __ProcessParallelBuild(self, ProcessIndex: int) -> None:
        for i in range(ProcessIndex, len(self.FilesToCompile), self.CPUCount):
            LStdErr = self.FilesToCompile[i].Compile()

            self.__IncrementBuildProcess()

            if len(LStdErr) > 0:
                self.__Log(LStdErr)
            self.__Log("[{Progress}/{Total}] {File}".format(Progress = str(self.BuildProgress.value), Total = str(len(self.FilesToCompile)), File = self.FilesToCompile[i].FilePath))
    #------------------------------------------------------#
    '''
        Do build actions.
    '''
    def __ProcessBuild(self) -> None:
        self.__Log("Compiling {CountOfFiles} actions by {CPUCount} processes...".format(CountOfFiles = str(len(self.FilesToCompile)), CPUCount = str(self.CPUCount)))
        
        if self.CPUCount > 1:
            LWorkersPool = list[multiprocessing.Process]()
            for i in range(self.CPUCount):
                p = multiprocessing.Process(target = self.__ProcessParallelBuild, args=(i,))
                LWorkersPool.append(p)
                p.start()

            for i in range(self.CPUCount):
                LWorkersPool[i].join()
        else:
            self.__ProcessParallelBuild(0)
    #------------------------------------------------------#

    '''
        Call linker to link compiled object files.
    '''
    def __LinkObjectFiles(self) -> None:
        self.__Log("Linking...")
        LLinker = FilesLinker.FLinker(self.ProgramOptions, self.ConfigFile, self.ObjectFiles, self.UsedExtensions)
        LStdErr = LLinker.Link()
        if len(LStdErr) > 0:
            self.__Log(LStdErr)
    #------------------------------------------------------#




    '''
        Start project build internal.
    '''
    def __Build(self):
        self.__PrepareForBuild()
        self.__ProcessBuild()
        self.__LinkObjectFiles()
    #------------------------------------------------------#
    '''
        Start project build.
    '''
    def Build(self) -> None:
        LBuildTime = PyProjectBuildLibrary.ClockFunction(self.__Build)
        self.__Log("Process finished at {Seconds} seconds.".format(Seconds = str(LBuildTime)))
    #------------------------------------------------------#
    '''
        Clear intermediate files.
    '''
    def Clear(self) -> None:
        PyProjectBuildLibrary.RemoveDirIfExists(FilesPath.GetIntermediateFolderPath(self.ProgramOptions, self.ConfigFile))
    #------------------------------------------------------#