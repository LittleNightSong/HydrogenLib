import dataclasses as dc
import enum

import struct
from collections import OrderedDict

from _hydrogenlib_core.utils import lazy_property


@dc.dataclass
class FieldInfo:  # 名称, 类型, 字节序
    name: str
    type: type
    big_endian: bool = False

    @lazy_property
    def size(self):
        return struct.calcsize()


@dc.dataclass
class StructInfo:
    fields: OrderedDict[str, FieldInfo]
    big_endian: bool = False
