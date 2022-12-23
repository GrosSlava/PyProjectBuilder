# Copyright (c) 2022 GrosSlava

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import PyProjectBuildLibrary
import Logger
import CppHeaderParser





'''
    Already analyzed dependencies.
'''
DependenciesCache = dict[str, set[str]]()



'''
    Parse file and return array of includes.
'''
def __GetFileIncludes(FilePath: str) -> list[str]:
    LFileExtension = PyProjectBuildLibrary.GetFileExtension(FilePath)
    if LFileExtension in ["C", "c", "CPP", "cpp", "H", "h", "HPP", "hpp"]:
        try:
            return list(map(lambda X: X[1: -1], CppHeaderParser.CppHeader(FilePath).includes))
        except Exception as ex:
            Logger.ErrorLog(ex)
            return list[str]()
    else:
        return list[str]()
#------------------------------------------------------#

'''
    Add file dependency to cache if file exists.
    @return updated DependenciesSet.
'''
def __AddDependency(DependenciesSet: set[str], FilePath: str, IncludePath: str, AdditionalIncludeDirs: list[str]) -> set[str]:
    LIncludeFullPath = os.path.join(PyProjectBuildLibrary.GetFilePath(FilePath), IncludePath)
    if PyProjectBuildLibrary.CheckFileExists(LIncludeFullPath):
        LIncludeFullPath = os.path.abspath(LIncludeFullPath)
        DependenciesSet.add(LIncludeFullPath)
    else:
        LFound = False
        for LAdditionalSerach in AdditionalIncludeDirs:
            LIncludeFullPath = os.path.join(LAdditionalSerach, IncludePath)
            if PyProjectBuildLibrary.CheckFileExists(LIncludeFullPath):    
                LIncludeFullPath = os.path.abspath(LIncludeFullPath)  
                DependenciesSet.add(LIncludeFullPath)
                LFound = True
                break
        if not LFound:
            return DependenciesSet
    return DependenciesSet.union(GetFileDependencies(LIncludeFullPath, AdditionalIncludeDirs))
#------------------------------------------------------#





'''
    Extract all dependencies from source file.
    @return array of absolute paths to dependencies.
'''
def GetFileDependencies(FilePath: str, AdditionalIncludeDirs: list[str]) -> set[str]:
    global DependenciesCache
    if not PyProjectBuildLibrary.CheckFileExists(FilePath):
        return set[str]()
    LFilePath = os.path.abspath(FilePath)
    
    if LFilePath in DependenciesCache:
        return DependenciesCache[LFilePath]

    DependenciesCache[LFilePath] = set[str]()
    LDependenciesSet = set[str]()

    LIncludes = __GetFileIncludes(LFilePath)
    for LInclude in LIncludes:
        LDependenciesSet = __AddDependency(LDependenciesSet, LFilePath, LInclude, AdditionalIncludeDirs)  
   
    if LFilePath in LDependenciesSet:
        LDependenciesSet.remove(LFilePath)

    for LDependencyFile in LDependenciesSet:
        if LFilePath in DependenciesCache[LDependencyFile]:
            DependenciesCache[LDependencyFile] = DependenciesCache[LDependencyFile].union(LDependenciesSet)
    
    DependenciesCache[LFilePath] = LDependenciesSet
    return LDependenciesSet
#------------------------------------------------------#
'''
    @return true if file contains one or more modified dependency files.
'''
def HasFileChangedDependency(FilePath: str, ObjectFilePath: str, AdditionalIncludeDirs: list[str]) -> bool:
    LDependencies = GetFileDependencies(FilePath, AdditionalIncludeDirs) 
    for LDependency in LDependencies:
        if os.path.getmtime(ObjectFilePath) < os.path.getmtime(LDependency):
            return True
    return False
#------------------------------------------------------#
