from typing import Callable, Self


class call_property[T]:
    """
    类似内置的 ``@property`` 装饰器, 但是使用了另一种设置和获取值的方法

    读取: ``.property()``

    写入: ``.property(value)``

    删除: ``del .property``

    除了读取值的逻辑与 ``@property`` 装饰器不同, 写入和删除都可以沿用 ``@property`` 的逻辑

    比如: ``.property(value)`` 等同于 ``.property = value``

    """

    def __init__(self, fget: Callable[[Self], T], fset: Callable[[Self, T], None] = None,
                 fdel: Callable[[Self], None] = None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel

    def getter(self, fget: Callable[[Self], T]):
        if not callable(fget):
            raise TypeError("fget must be callable")

        self._fget = fget

        return self

    def setter(self, fset: Callable[[Self, T], None]):
        if not callable(fset):
            raise TypeError("fset must be callable")

        self._fset = fset

        return self

    def deleter(self, fdel: Callable[[Self], None]):
        if not callable(fdel):
            raise TypeError("fdel must be callable")

        self._fdel = fdel

        return self

    def __get__(self, instance, owner) -> Callable[[], T] | Self | Callable[[T], None]:
        if instance is None:
            return self

        def wrapper(*args):
            if args:
                self._fset(instance, *args)
            else:
                return self._fget(instance)

        return wrapper

    def __set__(self, instance, value):
        self._fset(instance, value)

    def __delete__(self, instance):
        self._fdel(instance)
