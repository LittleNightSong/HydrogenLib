from __future__ import annotations

import ctypes
import inspect
import typing
from collections.abc import Buffer, Callable
from typing import Sequence, Any, Literal

ParamFlagsType = tuple[tuple[Literal[1, 2], str] | tuple[Literal[1, 2], str, Any]]

from _hydrogenlib_core.typefunc import iter_annotations, alias
from ._special_methods import _bind_py_type

short = _bind_py_type(int, ctypes.c_short)
ushort = _bind_py_type(int, ctypes.c_ushort)
long = _bind_py_type(int, ctypes.c_long)
longlong = _bind_py_type(int, ctypes.c_longlong)
ulonglong = _bind_py_type(int, ctypes.c_ulonglong)
double = _bind_py_type(float, ctypes.c_double)
byte = _bind_py_type(int, ctypes.c_byte)
ubyte = _bind_py_type(int, ctypes.c_ubyte)


def make_struct(name: str, fields: Sequence[tuple[str, Any]], endian='big') -> type[ctypes.Structure]:
    base = ctypes.Structure
    match endian:
        case 'little':
            base = ctypes.LittleEndianStructure
        case 'big':
            base = ctypes.BigEndianStructure
        case _:
            raise ValueError(f"Bad endianness {endian}")

    return type(
        name, (base,), {
            '_fields_': tuple(fields)
        }
    )


def make_union(name: str, fields: Sequence[tuple[str, Any]], endian='big') -> type[ctypes.Union]:
    base = ctypes.Union
    match endian:
        case 'little':
            base = ctypes.LittleEndianUnion
        case 'big':
            base = ctypes.BigEndianUnion
        case _:
            raise ValueError(f"Bad endianness {endian}")

    return type(
        name, (base,), {
            '_fields_': tuple(fields)
        }
    )


class CType:
    __ctype__ = None

    def __class_getitem__(cls, item):
        if isinstance(item, tuple):
            return cls(*item)
        else:
            return cls(item)

    @staticmethod
    def as_ctype(ctype):
        if isinstance(ctype, type):
            if issubclass(ctype, str):
                return ctypes.c_wchar_p
            elif issubclass(ctype, int):
                return ctypes.c_int
            elif issubclass(ctype, Buffer):
                return ctypes.c_char_p
            elif ctype is None:
                return None

        while inner_ctype := getattr(ctype, '__ctype__', None):
            ctype = inner_ctype
        return ctype

    def __getattr__(self, item):
        return getattr(self.__ctype__, item)


class CObject:
    __cobj__ = None
    __ctype__ = None

    @staticmethod
    def as_cobj(obj):
        while inner_obj := getattr(obj, '__cobj__', None):
            obj = inner_obj
        return obj

    def __getattr__(self, item):
        return getattr(self.__cobj__, item)

    @property
    def _as_parameter_(self):
        return self.__cobj__

    @classmethod
    def new(cls, *args, **kwargs) -> _PointerObjectWrapper[typing.Self]:
        return _PointerObjectWrapper(cls(*args, **kwargs))


class _PointerObjectWrapper[T]:
    def __init__(self, cobj: T):
        self._obj = cobj

    @property
    def __cobj__(self):
        return ctypes.pointer(CObject.as_cobj(self._obj))

    _as_parameter_ = __cobj__

    def __getattr__(self, item):
        return getattr(self._obj, item)

    def __setattr__(self, key, value):
        if key == '_obj':
            super().__setattr__(key, value)
        else:
            setattr(self._obj, key, value)

    def __repr__(self):
        return f"<Wrapped {self._obj.__class__.__name__}>"


class Pointer(CType):  # Pointer Type
    dtype = alias['_dtype']

    def __init__(self, dtype):
        self._dtype = dtype
        self.__ctype__ = ctypes.POINTER(CType.as_ctype(dtype))

    def __repr__(self):
        return f"{self.dtype}*"


class Array(CType):
    dtype = alias['_dtype']

    def __init__(self, dtype, length=0):
        self.__ctype__ = ctypes.ARRAY(CType.as_ctype(dtype), length)
        self._dtype = dtype

    def __repr__(self):
        return f'<{self.__class__.__name__} dtype={self.dtype}>'


class StructType(type):
    def __init__(cls, name, bases, attrs, *, endian='big'):
        super().__init__(name, bases, attrs)
        cls.__endian__ = endian
        cls.__ctype__ = make_struct(
            cls.__name__,
            [
                (k, tp) for k, tp, _ in iter_annotations(cls)
            ],
            endian=cls.__endian__
        )

    def __repr__(self):
        return self.__name__


class Struct(CObject, metaclass=StructType):
    __ctype__ = alias['__class__.__ctype__']

    def __init__(self, *args, **kwargs):
        self.__cobj__ = self.__ctype__(*args, **kwargs)

    def __init_subclass__(cls, *, endian='big'): ...

    # def __getattr__(self, item):
    #     return getattr(self.__cobj__, item)


class UnionType(type):
    def __init__(cls, name, bases, attrs, *, endian='big'):
        super().__init__(name, bases, attrs)
        cls.__endian__ = endian
        cls.__ctype__ = make_union(
            cls.__name__,
            [(name, CType.as_ctype(anno)) for name, anno, _ in iter_annotations(cls)],
            endian=cls.__endian__
        )

    def __repr__(self):
        return self.__name__


class Union(CObject, metaclass=UnionType):
    __ctype__ = alias['__class__.__ctype__']

    def __init__(self, *args, **kwargs):
        self.__cobj__ = self.__ctype__(*args, **kwargs)

    def __init_subclass__(cls, *, endian='big'): ...


class Prototype:
    __slots__ = (
        '_restype', '_argtypes', '_protocol',
        '_signature', '_functype_factory', '_functype',
        '_output_param', '_paramflags'
    )
    restype = alias['_restype']
    argtypes = alias['_argtypes']
    protocol: str = alias['_protocol']
    output_param: str = alias['_output_param']
    paramflags: ParamFlagsType | None

    _signature: inspect.Signature

    def __init__(
            self, restype, *argtypes,
            protocol: Literal['c', 'py', 'win'] = 'c', output_param: str = None, signature=None,
            paramflags: ParamFlagsType | None = None
    ):

        self._restype = restype
        self._argtypes = argtypes
        self._protocol = protocol
        self._paramflags = paramflags
        self._output_param = output_param
        self._functype = None
        self._functype_factory = {
            'c': ctypes.CFUNCTYPE,
            'win': ctypes.WINFUNCTYPE,
            'py': ctypes.PYFUNCTYPE
        }.get(protocol)

        self._signature = signature

    def replace(self, **kwargs):
        return self.__class__(
            self.restype or kwargs.get('restype'), *kwargs.get('argtypes', self._argtypes),
            **{
                # 'restype': self._restype,
                'protocol': self._protocol,
                'output_param': self._output_param,
                'signature': self._signature,
                'paramflags': self._paramflags,
                **kwargs
            }
        )

    def _generate_signature(self):
        return inspect.Signature(
            [inspect.Parameter(f'Arg__{i}', inspect.Parameter.POSITIONAL_OR_KEYWORD)
             for i in range(len(self._argtypes))],
        )  # 由于只需要参数绑定的功能，所以 annotation 全部不设置

    @property
    def signature(self):
        if self._signature is None:
            self._signature = self._generate_signature()
        return self._signature

    @property
    def paramflags(self):
        if self._paramflags is None and self._signature:
            # 生成 paramflags
            paramflags = []
            for param in self._signature.parameters.values():
                if param.name == self.output_param:
                    paramflags.append(
                        (2, param.name) if param.default is param.empty else (2, param.name, param.default))
                elif param.default is not param.empty:
                    paramflags.append((1, param.name, param.default))
                else:
                    paramflags.append((1, param.name))
            self._paramflags = tuple(paramflags)

        return self._paramflags

    def bind(self, dll, name):
        if self.paramflags:
            return FuncPtr(self.__ctype__((name, CObject.as_cobj(dll)), self.paramflags), dll=dll)
        else:
            return FuncPtr(self.__ctype__((name, CObject.as_cobj(dll))), dll=dll)

    def as_callback(self, callback: Callable):
        return self(callback)

    def from_address(self, address):
        return self(CObject.as_cobj(address))

    @classmethod
    def from_pyfunc(cls, func, ftype: str = 'c'):
        signature = inspect.signature(func)

        restype = signature.return_annotation

        if restype is signature.empty:
            restype = None

        argtypes = [
            param.annotation
            for param in signature.parameters.values()
        ]

        return cls(restype, *argtypes, protocol=ftype, signature=signature)

    def __call__(self, *args, **kwargs):
        return FuncPtr(self.__ctype__(*args, **kwargs), self)

    @property
    def __ctype__(self):
        if self._functype is None:
            self._functype = self._functype_factory(
                CType.as_ctype(self._restype), *map(CType.as_ctype, self._argtypes)
            )
        return self._functype

    def __repr__(self):
        return (
            '<'
            f'{self.__class__.__name__} '
            f'signature={self.signature} '
            f'c_signature={self.restype}({", ".join(map(str, self.argtypes))})'
            '>'
        )


class FuncPtr(CObject):
    _funcptr = alias['__cobj__'](mode=alias.mode.read_write)

    enable_arg_complete = alias['_uac'](mode=alias.mode.read_write)

    def __init__(self, ptr, prototype=None, enable_arg_complete=False, dll=None):
        self._funcptr = CObject.as_cobj(ptr)
        self._prototype = prototype
        self._uac = enable_arg_complete
        self._dll = dll

    def with_prototype(self, prototype) -> typing.Self:
        return self.__class__(prototype.from_address(self._funcptr), prototype, True)

    def __call__(self, *args, **kwargs):
        if self._uac:
            s = self._prototype.signature
            bound_args = s.bind(*args, **kwargs)
            args = bound_args.arguments.values()
            kwargs = {}
        return self._funcptr(*args, **kwargs)

    def __repr__(self):
        dll_start = int(CObject.as_cobj(self._dll)._handle) if self._dll else 0
        offset = int.from_bytes(self._funcptr) - dll_start
        if dll_start == 0: dll_start = None
        return (
            f"<"
            f"{self.__class__.__name__}"
            f"(0x{dll_start:X}+{offset}) "
            f"prototype={self._prototype}"
            f">"
        )


if typing.TYPE_CHECKING:
    type _PointerObjectWrapper[T] = T
    type Pointer[T] = Pointer | int | None | _PointerObjectWrapper[T]
    type Array[T] = Sequence[T]

AnyPointer = Pointer[None]
