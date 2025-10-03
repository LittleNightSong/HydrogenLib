from typing import Any

from .basic_types import *
from .compound_types import *
from .py_types import *

AnyPtr = TPointer[None]  # like ctypes.c_void_p
AnyRef = TRef[object]  # ctypes 的 Ref 没有类型, 按照我们的类型框架, 应该用 object 表示泛型

if typing.TYPE_CHECKING:
    AnyPtr = Pointer[Any]
    AnyRef = Ref[Any]
