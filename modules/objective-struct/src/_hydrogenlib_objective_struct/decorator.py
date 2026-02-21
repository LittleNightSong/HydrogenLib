import dataclasses
import typing

from . import struct_type
from .aot import pack, unpack
from .methods import to_format_string

endian_control_characters = tuple('<@=!>')


def struct(maybe_cls=None, *, endian='@'):
    def decorator[T](cls: T) -> type[struct_type.Struct]:
        import struct

        # module = sys.modules[cls.__module__]

        fields = dataclasses.fields(cls)
        # namesp = module.__dict__
        # print(namesp)
        real_annotations = typing.get_type_hints(cls)
        # print(cls, real_annotations)

        for field in fields:
            print(cls, field.name, repr(field.type))
            if isinstance(field.type, str):
                field.type = real_annotations[field.name]

        cls.__ctype__ = to_format_string([field.type for field in fields])
        # print(cls.__ctype__)
        cls.__cfields__ = tuple(fields)  # type: tuple[dataclasses.Field, ...]
        cls.__cstruct__ = struct.Struct(endian + cls.__ctype__)  # 构造 Struct 类型
        cls.__cendian__ = endian

        cls.pack, cls.pack_into = pack.create_pack_methods(cls)
        cls.unpack, cls.update, cls.unpack_from, cls.update_from, cls.iter_unpack, cls.iter_update = (
            unpack.create_unpack_methods(cls)
        )

        return cls

    return decorator(maybe_cls) if maybe_cls is not None else decorator
