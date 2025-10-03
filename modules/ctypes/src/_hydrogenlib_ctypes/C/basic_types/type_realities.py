import ctypes

from _hydrogenlib_core.typefunc import alias
from .base import AbstractCType, AbstractCData


class SimpleCData(AbstractCData):
    cdata = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, cdata):
        self.cdata = cdata

    def __getattr__(self, item):
        return getattr(self.cdata, item)

    def __setattr__(self, key, value):
        if key == 'cdata':
            super().__setattr__(self, key, value)
        else:
            setattr(self.cdata, key, value)


class SimpleCType(AbstractCType, real=SimpleCData):
    rc = alias['__real_ctype__'](mode=alias.mode.read_write)

    def __init__(self, real_ctype):
        self.rc = real_ctype


uint = SimpleCType[ctypes.c_uint]
short = SimpleCType[ctypes.c_short]
ushort = SimpleCType[ctypes.c_ushort]
long = SimpleCType[ctypes.c_long]
longlong = SimpleCType[ctypes.c_longlong]
ulong = SimpleCType[ctypes.c_ulong]
ulonglong = SimpleCType[ctypes.c_ulonglong]
double = SimpleCType[ctypes.c_double]
longdouble = SimpleCType[ctypes.c_longdouble]

void_p = SimpleCType[ctypes.c_void_p]

size_t = SimpleCType[ctypes.c_size_t]
ssize_t = SimpleCType[ctypes.c_ssize_t]
time_t = SimpleCType[ctypes.c_time_t]

int8_t = SimpleCType[ctypes.c_int8]
int16_t = SimpleCType[ctypes.c_int16]
int32_t = SimpleCType[ctypes.c_int32]
int64_t = SimpleCType[ctypes.c_int64]
uint8_t = SimpleCType[ctypes.c_uint8]
uint16_t = SimpleCType[ctypes.c_uint16]
uint32_t = SimpleCType[ctypes.c_uint32]
uint64_t = SimpleCType[ctypes.c_uint64]

byte = SimpleCType[ctypes.c_byte]
ubyte = SimpleCType[ctypes.c_ubyte]

bool = SimpleCType[ctypes.c_bool]
