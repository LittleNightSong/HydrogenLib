import inspect
import types
import typing
from inspect import stack as call_stack

from .list_func import hasindex


def get_parameters(func):
    for i in inspect.signature(func).parameters.values():
        yield i


def get_name(func):
    return func.__name__


def get_doc(func):
    return func.__doc__


def get_code(func):
    return func.__code__


def get_source(func):
    return inspect.getsource(func)


def get_module(func) -> str:
    return func.__module__


def is_instance(ins_or_cls):
    return not isinstance(ins_or_cls, type)


def get_full_qualname(func_type_or_ins: typing.Union[types.FunctionType, type, object]):
    if is_instance(func_type_or_ins) and not is_function(func_type_or_ins):
        return get_full_qualname(func_type_or_ins.__class__)
    return f'{func_type_or_ins.__module__}.{func_type_or_ins.__qualname__}'


FunctionTypes = types.FunctionType, types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType


def is_function(obj):
    return inspect.isfunction(obj)


def is_method(obj):
    return inspect.ismethod(obj)


def is_function_type(obj):
    return isinstance(obj, FunctionTypes)


def get_signature(func):
    return inspect.signature(func)


class Function:
    __slots__ = ['_func', '_signature']

    def __new__(cls, func):
        if isinstance(func, cls):
            return func

        self = super().__new__(cls)
        self._func = func
        self._signature = None

        return self

    @property
    def name(self):
        return get_name(self._func)

    @property
    def doc(self):
        return get_doc(self._func)

    @property
    def code(self):
        return get_code(self._func)

    @property
    def source(self):
        return get_source(self._func)

    @property
    def module(self):
        return get_module(self._func)

    @property
    def full_qualname(self):
        return get_full_qualname(self._func)

    @property
    def qualname(self):
        return self._func.__qualname__

    @property
    def signature(self):
        if not self._signature:
            self._signature = inspect.signature(self._func)
        return self._signature

    @property
    def params(self):
        return tuple(get_parameters(self._func))

    def match(self, *args, **kwargs):
        return self._signature.bind(*args, **kwargs)

    def __str__(self):
        return f'<Func {self.full_qualname} ({self._signature})>'

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __setattr__(self, key, value):
        if key not in self.__slots__:
            setattr(self._func, key, value)
        else:
            super().__setattr__(key, value)


class FunctionGroup:
    def __init__(self, funcs: typing.Iterable):
        self._funcs = list(funcs)

    def __iter__(self):
        return iter(self._funcs)

    def __len__(self):
        return len(self._funcs)

    def __getitem__(self, item):
        return self._funcs[item]

    def __setitem__(self, key, value):
        self._funcs[key] = value

    def __delitem__(self, key):
        del self._funcs[key]

    def __contains__(self, item):
        return item in self._funcs

    def __call__(self, *args, **kwargs):
        for func in self._funcs:
            func(*args, **kwargs)

    def __add__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self._funcs + other._funcs)
        elif isinstance(other, typing.Callable):
            return type(self)(self._funcs + [other])
        return None

    def __iadd__(self, other):
        if isinstance(other, type(self)):
            self._funcs += other._funcs
            return self
        return None


def get_called_func(depth=1):
    call_stck = call_stack()
    if not hasindex(call_stck, depth):
        return None
    return call_stck[depth].frame.f_code.co_qualname


class _Oneshot[T]:
    """
    This idea comes from《Oneshot》.
    """

    def __init__(self, func, num=1):
        self._func = func
        self._call_num = 0
        self._max_call_num = num

    __call__: T

    def __call__(self, *args, **kwargs):
        if self._call_num >= self._max_call_num:
            raise RuntimeError('This function has been called.')
        self._call_num += 1

        return self._func(*args, **kwargs)

    def __get__(self, instance, owner):
        return types.MethodType(self, instance)

    def reset(self):
        self._call_num = 0

    def set_max_call_num(self, num: int):
        self._max_call_num = num


def oneshot[T: 'typing.Callable'](func: T | None = None, num=1) -> _Oneshot[T]:
    """
    确保函数只执行一次, 多次执行会抛出错误
    :param func: 函数
    :return:
    """

    def decorator(func):
        return _Oneshot(func, num)

    return decorator(func) if func else decorator


once = oneshot  # 别名
