import struct
from collections.abc import Buffer
from typing import Any, Sequence, Iterator, get_args, get_origin

from typing_inspection.typing_objects import is_annotated

from .struct_type import CType

mapping = {
    int: 'i', float: 'f', bool: '?'
}

CTypesFields = Sequence[str | CType | type] | Iterator[str | CType | type]


def get_ctype(tp):
    if isinstance(tp, str):
        return tp
    elif _ := getattr(tp, '__ctype__', None):
        return _
    elif _ := mapping.get(tp):
        return _
    elif is_annotated(get_origin(tp)):
        # 目前需要 Annotated 的类型只有 array
        tp_args = get_args(tp)
        dtype = get_args(tp_args[0])[0]
        length = tp_args[1]
        c_size = struct.calcsize(get_ctype(dtype))
        return f'{length * c_size}s'
    else:
        raise ValueError(f'Unrecognized type: {tp}')


def to_format_string(fields: CTypesFields):
    format = ''.join(
        map(
            get_ctype,
            fields
        )
    )
    return format


def pack(format: CTypesFields, *data: Any) -> bytes:
    return struct.pack(to_format_string(format), *data)


def unpack(format: CTypesFields, data: Buffer):
    return struct.unpack(to_format_string(format), data)
