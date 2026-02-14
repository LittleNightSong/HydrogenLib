import copy
import inspect
import struct
from collections import OrderedDict
from collections.abc import Buffer
from typing import Self, Generator

from _hydrogenlib_core.typefunc import AutoSlots

endian_control_characters = tuple('<@=!>')

_AOT_TEMPLATE = """
def pack(self):
    return self.__st_struct__.pack({selfattrs})

def pack_into(self, buffer, offset=0):
    self.__st_struct__.pack_into(buffer, offset, {selfattrs})

@classmethod
def unpack(cls, buffer):
    self = object.__new__(cls)
    {selfattrs} = self.__st_struct__.unpack(buffer)
    return self

@classmethod
def unpack_from(cls, buffer, offset=0):
    self = object.__new__(cls)
    {selfattrs} = cls.__st_struct__.unpack_from(buffer, offset)
    return self

@classmethod
def iter_unpack(cls, buffer):
    for values in cls.__st_struct__.iter_unpack(buffer):
        self = object.__new__(cls)
        {selfattrs} = values
        yield self

@classmethod
def iter_unpack_reused(cls, buffer):
    self = object.__new__(cls)
    for values in cls.__st_struct__.iter_unpack(buffer):
        {selfattrs} = values
        yield self

def update_from(self, buffer, offset=0):
    {selfattrs} = self.__st_struct__.unpack_from(buffer, offset)
    return self
    
def __init__(self, {init_signature}):
    {selfattrs} = {attrs}
    
"""


class Struct(AutoSlots):
    """
    Base class for creating structured data with a defined format, suitable for packing and unpacking binary data.

    This class allows the creation of a structure that can be used to pack and unpack binary data according to a
    specified format. It supports type annotations for defining the fields of the structure.
    The class automatically generates the necessary format string for the `struct` module based on the provided
    field types. It also provides methods for comparing instances, packing and unpacking data,
    and converting the structure to a dictionary representation.

    Usage:
        class MyStruct(Struct):
            a: int
            b: bool
            c: float
    """
    __no_slots__ = (
        '__st_fields__', '__st_struct__', '__st_format__', '__st_order__',
        '__ost_fields__'
    )

    __st_fields__: dict[str, type] = None
    __st_struct__: struct.Struct = None
    __st_format__: str = ''
    __st_order__: str = '@'

    # optimize attributes
    __ost_fields__: tuple[str, ...] = None

    # __ost_methods__: dict[str, Callable] = None

    def __init_subclass__(cls, *, middle=False, endian: str = '@', **kwargs):
        if middle:
            return

        from .types import get_ctype

        cls.__st_fields__ = copy.copy(cls.__st_fields__) or OrderedDict()  # 继承父类型的字段

        new_fields = OrderedDict()
        for name, anno in inspect.get_annotations(cls).items():
            if name in cls.__st_fields__:
                raise TypeError(f"Field {name!r} is already defined")
            new_fields[name] = get_ctype(anno)

        cls.__st_fields__.update(new_fields)
        cls.__st_format__ += ''.join(new_fields.values())  # 更新新字段的 format string

        if cls.__st_format__.startswith(endian_control_characters):  # 修改字节序
            if cls.__st_format__[0] != endian:
                cls.__st_format__ = endian + cls.__st_format__[1:]

        cls.__st_struct__ = struct.Struct(cls.__st_format__)  # 构造 Struct 类型

        # 优化
        # 生成 ost-fields
        # cls.__ost_fields__ = tuple(cls.__st_fields__.keys())

        cls.__ost_fields__ = field_names = tuple(cls.__st_fields__.keys())

        selfattrs = ', '.join(
            map(
                lambda x: f'self.{x}',
                field_names
            )
        )

        def _processor(name):
            if name in cls.__migrated__:
                return f'{name}={cls.__migrated__[name]}'
            else:
                return f'{name}'

        # 生成 init 方法的签名
        init_signature = ', '.join(
            map(
                _processor,
                field_names
            )
        )

        # 普通的字段元组
        simple_attrs = ', '.join(field_names)

        # 生成 ost-methods
        gl = {}
        exec(
            _AOT_TEMPLATE.format(
                selfattrs=selfattrs,
                init_signature=init_signature,
                attrs=simple_attrs,
            ),
            globals=gl
        )

        cls.__ost_methods__ = gl

        cls.pack = gl['pack']
        cls.pack_into = gl['pack_into']
        cls.unpack = gl['unpack']
        cls.unpack_from = gl['unpack_from']
        cls.iter_unpack = gl['iter_unpack']
        cls.iter_unpack_reused = gl['iter_unpack_reused']
        cls.update_from = gl['update_from']
        cls.__init__ = gl['__init__']

    def __init__(self, *args, **kwargs) -> None:
        ...

    def __eq__(self, other):
        if isinstance(other, Struct):
            return other.__st_format__ == other.__st_format__ and self.to_dict() == other.to_dict()
        elif isinstance(other, dict):
            return self.to_dict() == other
        elif isinstance(other, bytes):
            return self.unpack(other) == self
        else:
            raise NotImplementedError(other)

    def pack(self) -> bytes:
        ...

    def pack_into(self, buffer: Buffer, offset=0) -> None:
        ...

    @classmethod
    def unpack(cls, buffer) -> Self:
        ...

    @classmethod
    def unpack_from(cls, buffer, offset=0) -> Self:
        ...

    @classmethod
    def iter_unpack(cls, buffer) -> Generator[Self, None, None]:
        ...

    @classmethod
    def iter_unpack_reused(cls, buffer) -> Generator[Self, None, None]:
        ...

    def update_from(self, buffer: Buffer, offset=0) -> None:
        ...

    def to_dict(self):
        return {
            k: getattr(self, k)
            for k in self.__ost_fields__
        }

    def __str__(self):
        dct = self.to_dict()
        kv_string = ', '.join(
            map(
                lambda x: f"{x[0]}={x[1]!r}"
                , dct.items()
            )
        )
        return f'{self.__class__.__name__}' f"({kv_string})"

    def __repr__(self):
        dct = self.to_dict()
        kv_string = ', '.join(
            map(
                lambda x: f"{x[0]}={x[1]!r}"
                , dct.items()
            )
        )
        return f'{self.__class__.__name__}[{self.__st_format__}]' f"({kv_string})"
