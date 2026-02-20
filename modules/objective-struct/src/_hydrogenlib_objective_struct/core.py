import dataclasses
import sys

from . import aot
from . import struct_type
from .methods import to_format_string

endian_control_characters = tuple('<@=!>')


def struct(maybe_cls=None, *, endian='@'):
    def decorator[T](cls: T) -> type[struct_type.Struct]:
        import struct

        fields = {
            field.name: field
            for field in dataclasses.fields(cls)
        }

        cls.__ctype__ = to_format_string([field.type for field in fields.values()])
        cls.__cfields__ = tuple(fields.values())  # type: tuple[dataclasses.Field, ...]
        cls.__cstruct__ = struct.Struct(endian + cls.__ctype__)  # 构造 Struct 类型
        cls.__cendian__ = endian
        # print(cls.__ctype__)
        cls.pack = aot.create_pack_function(cls)
        cls.unpack, cls.update = aot.create_unpack_and_update_function(cls)

        return cls

    return decorator(maybe_cls) if maybe_cls is not None else decorator
