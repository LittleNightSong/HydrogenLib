import typing
from inspect import Signature, Parameter

from _hydrogenlib_core.typefunc import alias
from _hydrogenlib_core.utils import InstanceMapping, lazy_property
from .base import *
from ..basic_types.type_realities import ubyte


class Pointer[T](AbstractCData):
    __slots__ = ()

    ptr = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, ptr, tp=None):
        self.ptr = ptr
        self.type = tp

    def cast(self, tp):
        return cast(self, tp)

    def as_functype(self, prototype):
        return ctypes.cast(
            as_cdata(self),
            as_ctype(prototype)
        )

    @property
    def value(self) -> T:
        return self.ptr.contents

    @value.setter
    def value(self, v: T):
        c_obj = as_cdata(v)
        c_type = type(c_obj)
        if not issubclass(c_type, self.ptr._type_):
            raise TypeError(f'{c_type} cannot be assigned to {self.ptr._type_}')  # 无法使指针指向另一类型的对象

        self.ptr.contents = c_obj

    @classmethod
    def from_integer(cls, address: int, type=None):
        ptr = cls(None)
        ptr.ptr = ctypes.POINTER(type)(address)
        return ptr

    def __getitem__(self, item) -> T:
        return self.ptr[item]

    def __convert_ctype__(self, target):
        from .type_realities import TPointer, TRef
        if not isinstance(target, (TPointer, TRef)):
            raise TypeError(f'{Pointer} cannot be assigned to {target}')

        return cast(self, as_ctype(target))

    def __str__(self):
        return f"Pointer({int(self.ptr or 0)})"

    def __eq__(self, other):
        if other == 0:
            return self.ptr is None or self.ptr == 0
        return self.ptr == other


class Ref[T](AbstractCData):
    __slots__ = ()

    ref = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, obj: T):
        self.ref = byref(obj)

    def __convert_ctype__(self, target):
        raise NotImplementedError


class Array(AbstractCData):
    array = alias['__cdata__'](mode=alias.mode.read_write)

    def __init__(self, array):
        self.array = array

    @property
    def length(self):
        return self.array._length_

    @property
    def element_type(self):
        return self.array._type_

    @property
    def np_array(self):
        import numpy as np
        return np.ctypeslib.as_array(self.array)

    def __len__(self):
        return self.length

    def __getitem__(self, item):
        return self.array[item]

    def __setitem__(self, item, value):
        self.array[item] = value


class ArrayPointer(Array):
    length = alias['_length']

    @property
    def element_type(self):
        return self._type

    @element_type.setter
    def element_type(self, type):
        self._type = type
        self.array = cast(self.array, type)  # 将指针的元素类型改为type

    def __init__(self, pointer, length=1, type=ubyte):
        super().__init__(pointer)
        self._length = length
        self._type = type

    def check(self, index):
        if index < 0:
            index += self.length

        if index >= self.length or index < 0:
            raise IndexError(f"Index {index} out of range.")

        return index

    def __getitem__(self, index):
        return super().__getitem__(self.check(index))

    def __setitem__(self, index, value):
        super().__setitem__(self.check(index), value)


class Structure(AbstractCData):
    __ctype__ = ...

    def __init__(self, *args, **kwargs):
        self.__cdata__ = self.__ctype__(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.__cdata__, name)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            super().__setattr__(name, value)
        else:
            setattr(self.__cdata__, name, value)

    def __convert_ctype__(self, target):
        from .type_realities import TPointer, TRef

        if isinstance(target, TPointer):
            return Pointer(pointer(self))
        elif isinstance(target, TRef):
            return Ref(self)
        else:
            raise NotImplementedError

    def __str__(self):
        head = f"struct {self.__class__.__name__}:\n"
        body = ''
        for field, type in self.__ctype__._fields_:
            value = getattr(self, field)
            body += f"\t{field} = {value}  # type: {type.__name__}\n"

        return head + body

    def __repr__(self):
        field_dct = {
            k: getattr(self, k) for k in self.__ctype__._fields_
        }
        return f"{self.__class__.__name__}({', '.join([f'{field}={value}' for field, value in field_dct.items()])})"


class WrapedArguments:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def call(self, func):
        return func(*self.args, **self.kwargs)


class Function[*Targs, Tret]:
    _methods = InstanceMapping()

    _restype = alias['_prototype']['restype']

    @lazy_property
    def _signature(self):
        if self._signature_:
            return self._signature_

        if self._prototype.signature:
            return self._prototype.signature

        # 尽可能复用已有的 signature

        return Signature(  # 生成 signature 来方便类型检查
            [
                Parameter(f'Arg__{i}', Parameter.POSITIONAL_OR_KEYWORD, annotation=tp)
                for i, tp in enumerate(self._prototype.argtypes)
            ],
            return_annotation=self._prototype.restype
        )

    def __init__(self, ptr, prototype: 'ProtoType' = None, signature: Signature = None, func=None):
        self._ptr = ptr
        self._prototype = prototype
        self._signature_ = signature

        self._func = func

    # @classmethod
    # def wrap(cls, maybe_func=None, *, name: str = None, dll=None, real_prototype=None):
    #     def decorator(func):
    #         prototype = real_prototype or ProtoType.from_pyfunc(func, name=name)
    #         prototype.name = prototype.name or name
    #         fnc = cls(prototype, dll=dll, signature=prototype.py_signature)
    #
    #         def wrapper(*args, **kwargs):
    #             arguments = func(*args, **kwargs)  # type: WrapedArguments
    #             if not isinstance(arguments, WrapedArguments):
    #                 # 必须返回 WrapedArguments
    #                 raise TypeError("return must be WrapedArguments")
    #             return arguments.call(fnc)
    #
    #         return wrapper
    #
    #     if maybe_func is None:
    #         return decorator
    #     else:
    #         return decorator(maybe_func)

    def convert_args(self, args, kwargs):
        bound_args = self._signature.bind(*args, **kwargs).arguments.values()
        for tp, arg in zip(self._prototype.argtypes, bound_args):
            try:
                yield as_cdata(convert_cdata(arg, tp))
            except TypeError as e:
                raise TypeError(str(e))

    __call__: typing.Callable[[*Targs], Tret]
    def __call__(self, *args, **kwargs):
        # 首先 调用原函数
        new_args = self._func(*args, **kwargs) if self._func else None

        if new_args is not None:
            args = (
                *new_args,
                *args[len(new_args):]
            )

        res = self._ptr(*self.convert_args(args, kwargs))  # 不要用 kwargs
        # 现在, 我们需要对返回值二次转换
        # ctypes 的调用不会返回 hyctypes 中的类型
        if self._restype is None:
            return

        real_type = self._restype
        if isinstance(real_type, AbstractCType):
            real_type = get_real_type(real_type)
        return real_type(res)

    def __get__(self, inst, cls):
        if inst in self._methods:
            return self._methods[inst]
        else:
            self._methods[inst] = Method(inst, self)
            return self._methods[inst]


class Method:
    __self__ = None

    def __init__(self, inst, func: Function):
        self.__self__ = inst
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        return self.__func__(self.__self__, *args, **kwargs)


if typing.TYPE_CHECKING:
    from .type_realities import *
