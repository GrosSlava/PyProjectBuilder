# Copyright (c) 2022 GrosSlava

import os
import sys





'''
    Log message in universal format.
'''
def Log(Message: str) -> None:
    print(Message)
#------------------------------------------------------#
'''
    Log error message in universal format.
'''
def ErrorLog(Message: str) -> None:
    Log("Error: {Message}".format(Message = Message))
    sys.exit(0)	
#------------------------------------------------------#
'''
    Log warning message in universal format.
'''
def WarningLog(Message: str) -> None:
    Log("Warning: {Message}".format(Message = Message))
#------------------------------------------------------#
