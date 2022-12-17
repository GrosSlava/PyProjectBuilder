# Copyright (c) 2022 GrosSlava

import os
import sys





'''
    Create a new directory only if it does not exist.
'''
def CreateDirIfNotExist(Dir: str) -> None:
    if not os.path.exists(Dir):
        os.mkdir(Dir)
#------------------------------------------------------#




'''
    @return absolute path for given relative to script path.
'''
def GetRelativePath(ReativePath: str) -> str:
    SourceDir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(SourceDir, ReativePath)
#------------------------------------------------------#

'''
    Check that Path is absolute and exists.
'''
def CheckAbsPath(Path: str) -> bool:
    return os.path.isabs(Path) and os.path.exists(Path)
#------------------------------------------------------#




'''
    Comvert str to bool.
    @return Bool by str.
'''
def StrToBool(S: str) -> bool:
    return S in ["1", "yes", "Yes", "YES", "on", "On", "true", "True", "TRUE"]
#------------------------------------------------------#