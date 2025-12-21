from abc import ABC
from copy import deepcopy


class Auto(ABC):
    pass


class AutoRegDict(Auto):
    """
    自动注册未存在于字典的键，同时访问时返回默认值

    可以通过指定`isdeepcopy`属性来说明是否对默认值进行copy操作
    """
    default_value = None
    isdeepcopy = True

    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def pop(self, key):
        return self._dict.pop(key)

    def copy(self):
        return self._dict.copy()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def clear(self):
        return self._dict.clear()

    def __contains__(self, key):
        return self._dict.__contains__(key)

    def __len__(self):
        return self._dict.__len__()

    def __getitem__(self, key):
        if key not in self._dict:
            if self.isdeepcopy:
                v = deepcopy(self.default_value)
            else:
                v = self.default_value
            self._dict[key] = v
            return v
        return self._dict[key]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]


class AutoCompare(Auto):
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


class AutoState(Auto):
    """
    自动完成对象的状态导出和恢复

    如果`_state_attrs`为None，那么将导出所有属性，恢复时同上
    """
    __state_attrs__ = ()

    def __getstate__(self):
        if self.__state_attrs__ is None:
            return self.__dict__
        return {attr: getattr(self, attr) for attr in self.__state_attrs__}

    def __setstate__(self, state):
        if self.__state_attrs__ is None:
            self.__dict__ = state
        else:
            for attr in self.__state_attrs__:
                setattr(self, attr, state[attr])


class _AutoInfo(Auto):
    ...


class AutoRepr(_AutoInfo):
    __repr_attrs__ = ()

    def __repr__(self):
        return str(
            {attr: getattr(self, attr) for attr in self.__repr_attrs__}
        )


class AutoStr(_AutoInfo):
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


class AutoSingleton(Auto):
    _single_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._single_instance is None:
            cls._single_instance = super().__new__(cls, *args, **kwargs)
        return cls._single_instance
