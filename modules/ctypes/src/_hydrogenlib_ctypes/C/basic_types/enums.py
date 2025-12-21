import ctypes
import platform
from enum import *


class CallingConvention(int, Enum):
    """
    调用约定
    """
    auto: int

    cdecl = 0
    stdcall = 1
    fastcall = 2
    vectorcall = 3
    pythoncall = 4

    # 目前 ctypes 只支持这些调用约定

    @property
    def functype(self):
        if self in {self.stdcall, self.fastcall}:
            return ctypes.WINFUNCTYPE
        return ctypes.CFUNCTYPE


CV = CallingConvention

if platform.system() == 'Windows':
    CV.auto = CV.stdcall

elif platform.system() == 'Linux':
    CV.auto = CV.cdecl

elif platform.system() == 'Darwin':
    CV.auto = CV.cdecl

del CV

if __name__ == '__main__':
    CV = CallingConvention
    print(CV.cdecl.functype)
    print(CV.stdcall.functype)
