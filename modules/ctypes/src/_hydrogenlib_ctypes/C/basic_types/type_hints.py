# Type hints
# 这里所有的类型注解仅仅用于类型检查,实际运行时对它的导入会因 typing.TYPE_CHECKING 失效, 转为 real_types 内的实际类型
import builtins
import ctypes

type StructureType = ctypes.Structure | ctypes.Union | ctypes.BigEndianStructure | ctypes.LittleEndianStructure

# type int = int
type uint = int
type short = int
type ushort = int
type long = int
type longlong = int
type ulong = int
type ulonglong = int
type double = float
type longdouble = float
type char = int | bytes  # uint8_t  也可以看做单字符的 string
type wchar = int | str # uint16_t
# type char_p = bytes | None
# type wchar_p = str | None
# char_p 和 wchar_p 不需要另外表示
type void_p = int

type size_t = int
type ssize_t = int
type time_t = int

type int8_t = int
type int16_t = int
type int32_t = int
type int64_t = int
type uint8_t = int
type uint16_t = int
type uint32_t = int
type uint64_t = int

type byte = int
type ubyte = int

type bool = int | builtins.bool | None | object
