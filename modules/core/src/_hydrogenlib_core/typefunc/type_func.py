import inspect
import typing


def get_subclasses(cls):
    """
    获取所有子类
    """
    if cls is type:
        return []
    return cls.__subclasses__()


def get_subclass_counts(cls):
    """
    获取所有子类的数量
    """
    if cls is type:
        return 0
    return len(cls.__subclasses__())


def get_subclasses_recursion(cls):
    """
    递归地获取所有子类
    """
    if cls is type:
        return []
    return (
            cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_subclasses_recursion(s)]
    )


def get_subclass_counts_recursion(cls):
    """
    获取所有子类的数量
    """
    if cls is type:
        return 0
    return len(cls.__subclasses__()) + sum(get_subclass_counts_recursion(s) for s in cls.__subclasses__())


def iter_annotations(obj, *, globals=None, locals=None, eval_str=False):
    """
    迭代对象中的所有注解以及值(不存在为None)
    """
    for name, typ in inspect.get_annotations(obj, globals=globals, locals=locals, eval_str=eval_str).items():
        yield name, typ, getattr(obj, name, None)


def iter_attributes(obj):
    """
    迭代对象中的所有属性
    """
    for name in dir(obj):
        if name.startswith("_"):
            continue
        yield name, getattr(obj, name)


class AutoSlotsMeta(type):
    __slots__: tuple
    __no_slots__: tuple

    def __new__(cls, name, bases, attrs):
        slots = set(attrs.get("__slots__", ()))
        slots |= set(attrs.get('__annotations__', {}).keys())
        no_slots = set(attrs.get('__no_slots__', frozenset()))
        attrs['__slots__'] = tuple(slots - no_slots)
        return super().__new__(cls, name, bases, attrs)


class AutoSlots(metaclass=AutoSlotsMeta):
    pass


def get_origin(tp):
    origin = typing.get_origin(tp)
    return origin if origin is not None else tp


def split_type(tp):
    return get_origin(tp), typing.get_args(tp)


class SingletonType:
    _single_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._single_instance is None:
            cls._single_instance = super().__new__(cls, *args, **kwargs)
        return cls._single_instance


class AutoRepr:
    __repr_attrs__ = ()

    def __repr__(self):
        return str(
            {attr: getattr(self, attr) for attr in self.__repr_attrs__}
        )


class AutoStr:
    _str_attrs = ()

    def __str__(self):
        return str(
            {attr: getattr(self, attr) for attr in self._str_attrs}
        )


class AutoInfo(AutoRepr, AutoStr):
    _info_attrs = ()

    def __repr__(self):
        self._repr_attrs = self._info_attrs
        return super().__repr__()

    def __str__(self):
        self._str_attrs = self._info_attrs
        return super().__str__()


class AutoCompare:
    """
    自动完成比较操作
    通过指定`__compare_attrs__`属性来指定比较的属性，默认为None，
    如果`__compare_attrs__`为None，那么自动比较将不会生效，而是根据比较符返回一个默认值
    如果被比较的对象不是 `AutoCompare` 的实例，那么比较时会按比较列表的第一个属性作为比较属性
    """
    __compare_attrs__ = ()
    __cmp_funcs__ = {
        'eq': lambda x, y: x == y,
        'ne': lambda x, y: x != y,
        'lt': lambda x, y: x < y,
        'gt': lambda x, y: x > y,
        'le': lambda x, y: x <= y,
        'ge': lambda x, y: x >= y
    }

    def _auto_compare_attrs(self, opt, other, defautl=False):
        if opt not in self.__cmp_funcs__:
            return defautl

        func = self.__cmp_funcs__[opt]

        if not isinstance(other, AutoCompare):
            if self.__compare_attrs__:
                value = getattr(self, self.__compare_attrs__[0])
                return func(value, other)

        if self.__compare_attrs__ is None or other.__compare_attrs__ is None:
            return defautl

        my_attr_values = (
            getattr(self, attr) for attr in self.__compare_attrs__)
        other_attr_values = (
            getattr(other, attr) for attr in other.__compare_attrs__)
        return func(my_attr_values, other_attr_values)

    def __eq__(self, other):
        return self._auto_compare_attrs('eq', other, False)

    def __ne__(self, other):
        return self._auto_compare_attrs('ne', other, True)

    def __lt__(self, other):
        return self._auto_compare_attrs('lt', other, False)

    def __gt__(self, other):
        return self._auto_compare_attrs('gt', other, False)

    def __le__(self, other):
        return self._auto_compare_attrs('le', other, True)

    def __ge__(self, other):
        return self._auto_compare_attrs('ge', other, True)
