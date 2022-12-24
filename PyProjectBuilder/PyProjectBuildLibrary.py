# Copyright (c) 2022 GrosSlava

from os import mkdir, makedirs
from os.path import exists, dirname, isabs, isdir, isfile
from platform import system
from pathlib import Path
from shutil import rmtree
from time import time





'''
    Easy to use platform identifiers.
'''
WINDOWS_PLATFORM = "Windows"
LINUX_PLATFORM = "Linux"

'''
    Names of available for build platforms.
'''
SUPPORTED_BUILD_PLATFORMS = [ 
    WINDOWS_PLATFORM, 
    LINUX_PLATFORM 
]

'''
    Suffixes of available for build files.
'''
SUPPORTED_FILES = [ 
    "c", 
    "C",
    "cpp",
    "CPP"
]

'''
    Version of tool.
'''
PY_PROJECT_BUILD_VERSION = "1.2.0"





'''
    Check that Name of platform is available.
    @return true if PlatformName is supported.
'''
def CheckPlatform(PlatformName: str) -> bool:
    return PlatformName in SUPPORTED_BUILD_PLATFORMS
#------------------------------------------------------#
'''
    Check that Name of current platform is available.
    @return true if platform supported.
'''
def CheckCurrentPlatform() -> bool:
    return CheckPlatform(system())
#------------------------------------------------------#




'''
    Create a new directory only if it does not exist.
'''
def CreateDirIfNotExist(Dir: str) -> None:
    if not exists(Dir):
        mkdir(Dir)
#------------------------------------------------------#
'''
    Create a new directory with all subdirs in path only if it does not exist.
'''
def CreateDirWithChildren(Dir: str) -> None:
    if not exists(Dir):
        makedirs(Dir, exist_ok = True)
#------------------------------------------------------#
'''
    Remove directory only if it exists.
'''
def RemoveDirIfExists(Dir: str) -> None:
    if CheckDirExists(Dir):
        rmtree(Dir)
#------------------------------------------------------#




'''
    Extract extension from file path.
    @return file extension without leading dot.
'''
def GetFileExtension(FilePath: str) -> str:
    LSuffix = Path(FilePath).suffix
    if len(LSuffix) < 2:
        return ""
    return LSuffix[1:]
#------------------------------------------------------#
'''
    Extract file name from file path.
    @return file name only.
'''
def GetFileName(FilePath: str) -> str:
    return Path(FilePath).stem
#------------------------------------------------------#
'''
    Extract path-only from file path.
    @return file path only without file name at end. 
'''
def GetFilePath(FilePath: str) -> str:
    return dirname(FilePath)
#------------------------------------------------------#




'''
    Check that Path is absolute and exists.
'''
def CheckAbsPath(AnyPath: str) -> bool:
    return isabs(AnyPath) and exists(AnyPath)
#------------------------------------------------------#
'''
    Check that file extension is supported to be build.
'''
def IsFileSupported(FileName: str) -> bool:
    return CheckFileExists(FileName) and GetFileExtension(FileName) in SUPPORTED_FILES
#------------------------------------------------------#
'''
    Check that dir exists and it is dir.
'''
def CheckDirExists(DirPath: str) -> bool:
    return exists(DirPath) and isdir(DirPath)
#------------------------------------------------------#
'''
    Check that file exists and it is file.
'''
def CheckFileExists(DirPath: str) -> bool:
    return exists(DirPath) and isfile(DirPath)
#------------------------------------------------------#




'''
    Comvert str to bool.
    @return Bool by str.
'''
def StrToBool(S: str) -> bool:
    return S in ["1", "yes", "Yes", "YES", "on", "On", "ON", "true", "True", "TRUE"]
#------------------------------------------------------#

'''
    Split string by delimeter and steap each part.
'''
def SplitAndStrip(S: str, Delimeter: str = ';') -> list[str]:
    return list(map(lambda X : X.strip(), S.split(Delimeter)))
#------------------------------------------------------#

'''
    Cleck time of function working time.
    @return working time in seconds.
'''
def ClockFunction(f) -> float:
    LStart = time()
    f()
    return time() - LStart
#------------------------------------------------------#