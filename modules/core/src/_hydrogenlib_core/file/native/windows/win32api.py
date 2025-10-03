from _hydrogenlib_ctypes import *


# 需要定义 Set/GetFileAttributes 函数

kernel32 = Dll("kernel32.dll")


@kernel32
def GetFileAttributes(path: str):
    ...


@kernel32
def SetFileAttributes(path: str, attributes: int):
    ...
