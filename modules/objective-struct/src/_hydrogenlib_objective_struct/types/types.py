import builtins
import sys
from functools import lru_cache

from .base import make_struct_type


@lru_cache(maxsize=32)
def pad(size: int):
    return make_struct_type(
        f'pad_{size}', builtins.bytes, f'{size}x'
    )


char = make_struct_type(
    'char', builtins.bytes, 'c'
)

signed_char = make_struct_type(
    'signed_char', builtins.int, 'b'
)

unsigned_char = make_struct_type(
    'unsigned_char', builtins.int, 'B'
)

# bool = make_struct_type(
#     'bool', builtins.int, '?'
# )  # 布尔类型不能添加子类，也不允许添加新的类属性，只能特殊处理

short = make_struct_type(
    'short', builtins.int, 'h'
)

unsigned_short = make_struct_type(
    'unsigned_short', builtins.int, 'H'
)

unsigned_int = make_struct_type(
    'unsigned_int', builtins.int, 'I'
)

long = make_struct_type(
    'long', builtins.int, 'l'
)

unsigned_long = make_struct_type(
    'unsigned_long', builtins.int, 'L'
)

long_long = make_struct_type(
    'long_long', builtins.int, 'q'
)

unsigned_long_long = make_struct_type(
    'unsigned_long_long', builtins.int, 'Q'
)

double = make_struct_type(
    'double', builtins.float, 'd'
)

short_float = make_struct_type(
    'short_float', builtins.float, 'e'
)

size_t = make_struct_type(
    'size_t', builtins.int, 'n'
)

ssize_t = make_struct_type(
    'ssize_t', builtins.int, 'N'
)


# string (char[]), length must be specified when used
@lru_cache(maxsize=32)
def string(length):
    return make_struct_type(f'string_{length}', builtins.bytes, f'{length}s')


# pascal string (length-prefixed)
@lru_cache(maxsize=32)
def pascal_string(length):
    return make_struct_type(f'pascal_string_{length}', builtins.bytes, f'{length}p')


# pointer-sized integer (platform dependent)
pointer = make_struct_type(
    'pointer', builtins.int, 'P'
)

# >= 3.14
if sys.version_info.major >= 3 and sys.version_info.minor >= 14:
    float_complex = make_struct_type(
        'complex', builtins.complex, 'F'
    )

    double_complex = make_struct_type(
        'double_complex', builtins.complex, 'D'
    )
