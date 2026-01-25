"""
Usage:
    from ... import ...
    user32 = Dll('user32')

    @user32
    def MessageBoxW(hwnd: AnyPointer, text: str, caption: str, uType: int) -> int: ...

    @user32(name='MessageBoxA')
    def MessageBox(hWnd: AnyPointer, text: bytes, caption: bytes, uType: int) -> int: ...
"""

from ._dll import DLL
from ._func import c_function
from ._types import *
