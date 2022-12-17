# Copyright (c) 2022 GrosSlava

import os
import sys

import platform
import pathlib
import shutil
import time





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
    ".c", 
    ".C"
    ".cpp",
    ".CPP"
]

'''
    Version of tool.
'''
PY_PROJECT_BUILD_VERSION = "0.1.0"





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
    return CheckPlatform(platform.system())
#------------------------------------------------------#




'''
    Create a new directory only if it does not exist.
'''
def CreateDirIfNotExist(Dir: str) -> None:
    if not os.path.exists(Dir):
        os.mkdir(Dir)
#------------------------------------------------------#
'''
    Remove directory only if it exists.
'''
def RemoveDirIfExists(Dir: str) -> None:
    if os.path.exists(Dir) and os.path.isdir(Dir):
        shutil.rmtree(Dir)
#------------------------------------------------------#




'''
    Check that Path is absolute and exists.
'''
def CheckAbsPath(Path: str) -> bool:
    return os.path.isabs(Path) and os.path.exists(Path)
#------------------------------------------------------#
'''
    Check that file extension is supported to be build.
'''
def IsFileSupported(FileName: str) -> bool:
    return os.path.isfile(FileName) and pathlib.Path(FileName).suffix in SUPPORTED_FILES
#------------------------------------------------------#
'''
    Check that dir exists and it is dir.
'''
def CheckDirExists(DirPath: str) -> bool:
    return os.path.exists(DirPath) and os.path.isdir(DirPath)
#------------------------------------------------------#




'''
    Comvert str to bool.
    @return Bool by str.
'''
def StrToBool(S: str) -> bool:
    return S in ["1", "yes", "Yes", "YES", "on", "On", "true", "True", "TRUE"]
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
    LStart = time.time()
    f()
    return time.time() - LStart
#------------------------------------------------------#