# Copyright (c) 2022 GrosSlava

from os import system
from os.path import getmtime, join as JoinPath
from glob import iglob
import multiprocessing

from PyProjectBuilder.PyProjectBuildLibrary import *
from PyProjectBuilder.FilesPath import *
from PyProjectBuilder.Logger import *
from PyProjectBuilder.FileDependencies import HasFileChangedDependency
from PyProjectBuilder import ProgramOptions
from PyProjectBuilder import ProjectConfigFile
from PyProjectBuilder import FileCompiler
from PyProjectBuilder import FilesLinker





'''
    Main class to implement project building.
'''
class FBuildPipeline:
    def __init__(self, ProgramOptions: ProgramOptions.FProgramOptions, ConfigFile: ProjectConfigFile.FConfigFile):
        self.ProgramOptions = ProgramOptions                            # cached program options
        self.ConfigFile = ConfigFile                                    # cached config file info
        self.FilesToCompile = list[FileCompiler.FCompilingFile]()       # array of files to build
        self.ObjectFiles = list[str]()                                  # array of paths to object files to link (without platform specific extension)
        self.UsedExtensions = set[str]()                                # set of all used files extensions in project
    
        self.ProcessesManager = multiprocessing.Manager()
        self.BuildProgress = self.ProcessesManager.Value("BuildProgress", 0)                   
        self.ProgessMutex = multiprocessing.Lock()

        if self.ProgramOptions.UseMultiprocessing:
            self.CPUCount = multiprocessing.cpu_count()
        else:
            self.CPUCount = 1


        self.ConfigFile.BuildModules = list(map(lambda x: x.strip(), self.ConfigFile.BuildModules))
        self.ConfigFile.BuildModules = list(filter(lambda x: x != "", self.ConfigFile.BuildModules))

        self.ConfigFile.Ignore = list(map(lambda x: x.strip(), self.ConfigFile.Ignore))
        self.ConfigFile.Ignore = list(filter(lambda x: x != "", self.ConfigFile.Ignore))
        self.ConfigFile.Ignore = list(map(lambda x: JoinPath(self.ProgramOptions.ProjectRoot, x), self.ConfigFile.Ignore))

        self.ConfigFile.AdditionalIncludeDirs = list(map(lambda x: x.strip(), self.ConfigFile.AdditionalIncludeDirs))
        self.ConfigFile.AdditionalIncludeDirs = list(filter(lambda x: x != "", self.ConfigFile.AdditionalIncludeDirs))
        self.ConfigFile.AdditionalIncludeDirs = list(map(lambda x: JoinPath(self.ProgramOptions.ProjectRoot, x), self.ConfigFile.AdditionalIncludeDirs))

        self.ConfigFile.AdditionalLibsDirs = list(map(lambda x: x.strip(), self.ConfigFile.AdditionalLibsDirs))
        self.ConfigFile.AdditionalLibsDirs = list(filter(lambda x: x != "", self.ConfigFile.AdditionalLibsDirs))

        self.ConfigFile.Libs = list(map(lambda x: x.strip(), self.ConfigFile.Libs))
        self.ConfigFile.Libs = list(filter(lambda x: x != "", self.ConfigFile.Libs))
    #------------------------------------------------------#



    '''
        Log message with silent check.
    '''
    def __Log(self, Message: str) -> None:
        if self.ProgramOptions.Silent:
            return
        Log(Message)
    #------------------------------------------------------#

    '''
        Check that path is ignored by any from ingore array.
    '''
    def __IsPathIgnored(self, FilePath: str) -> bool:
        return any(FilePath.startswith(LIgnorePath) or LIgnorePath == FilePath for LIgnorePath in self.ConfigFile.Ignore)
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
    def __CheckFileNeedToBuild(self, ModuleName: str, FilePath: str) -> bool:
        LObjectFilePath = GetPlatformObjectFilePath(self.ProgramOptions, self.ConfigFile, ModuleName, GetFileName(FilePath))
        if (not CheckFileExists(LObjectFilePath)) or (getmtime(LObjectFilePath) < getmtime(FilePath)):
           return True
        return HasFileChangedDependency(FilePath, LObjectFilePath, self.ConfigFile.AdditionalIncludeDirs)
    #------------------------------------------------------#
    '''
        Prepere for building. Create needed folders. Check modules.
    '''
    def __PrepareForBuild(self) -> None:
        CreateDirWithChildren(GetIntermediateFolderPath(self.ProgramOptions, self.ConfigFile))  
        CreateDirWithChildren(GetBuildFolderPath(self.ProgramOptions, self.ConfigFile))  

        for LModule in self.ConfigFile.BuildModules:
            LModulePath = GetModuleFolderPath(self.ProgramOptions, LModule)
            if not CheckDirExists(LModulePath):
                WarningLog("Module '{ModulePath}' not exist.".format(ModulePath = LModule))
                continue

            CreateDirWithChildren(GetModuleIntermediateFolderPath(self.ProgramOptions, self.ConfigFile, LModule))  

            for LFilePath in iglob(JoinPath(LModulePath, "**"), recursive = True):
                if (not IsFileSupported(LFilePath)) or (self.__IsPathIgnored(LFilePath)):
                    continue
                if self.__CheckFileNeedToBuild(LModule, LFilePath):
                    self.FilesToCompile.append(FileCompiler.FCompilingFile(self.ProgramOptions, self.ConfigFile, LModule, LFilePath))
                self.ObjectFiles.append(GetObjectFilePath(self.ProgramOptions, self.ConfigFile, LModule, GetFileName(LFilePath), ""))
                self.UsedExtensions.add(GetFileExtension(LFilePath))
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

            for LWorker in LWorkersPool:
                LWorker.join()
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
    def __Build(self) -> None:
        self.__ProcessBuild()
        if self.ConfigFile.ResultType != ProjectConfigFile.EResultType.NO_LINK:
            self.__LinkObjectFiles()
        if self.ConfigFile.PostBuildAction != "":
            system(self.ConfigFile.PostBuildAction)
    #------------------------------------------------------#
    '''
        Start project build.
    '''
    def Build(self) -> None:
        LPrepareTime = ClockFunction(self.__PrepareForBuild)
        self.__Log("Build preparing finished.")
        LBuildTime = ClockFunction(self.__Build)

        self.__Log("Process finished at {Seconds} seconds.".format(Seconds = str(round(LPrepareTime + LBuildTime, 5))))
        self.__Log("Prepare time: {Seconds} seconds.".format(Seconds = str(round(LPrepareTime, 5))))
        self.__Log("Build time: {Seconds} seconds.".format(Seconds = str(round(LBuildTime, 5))))
    #------------------------------------------------------#
    '''
        Clear intermediate files.
    '''
    def Clear(self) -> None:
        RemoveDirIfExists(GetIntermediateFolderPath(self.ProgramOptions, self.ConfigFile))
    #------------------------------------------------------#