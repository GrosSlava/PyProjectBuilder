# Copyright (c) 2022 - 2023 GrosSlava. All rights reserved.

from sys import exit
import multiprocessing





'''
	Mutex for console print.
'''
LogMutex = multiprocessing.Lock()



'''
	Log message in universal format.
'''
def Log(Message: str) -> None:
	global LogMutex
	LogMutex.acquire()
	print(Message)
	LogMutex.release()
#------------------------------------------------------#
'''
	Log error message in universal format.
'''
def ErrorLog(Message: str) -> None:
	Log("Error: {Message}".format(Message = Message))
	exit(0)	
#------------------------------------------------------#
'''
	Log warning message in universal format.
'''
def WarningLog(Message: str) -> None:
	Log("Warning: {Message}".format(Message = Message))
#------------------------------------------------------#
