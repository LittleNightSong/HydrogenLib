"""
Use:
    import ...
    dll = Dll('user32')

    @ProtoType.from_pyfunc
    def MessageBoxW(hwnd: int, text: str, caption: str, uType: int) -> int: ...

    dll.connect(MessageBoxW)

"""


from . import C
from .C.basic_types import CallingConvention
from .C.dll import Dll


from .C.c_types import *

from .C.compound_types import (
    TPointer as Pointer,
    TRef as Ref,
    TArray as Array,
    TStructure as Structure,
    Structure as StructureBase,
    TUnion as Union
)



