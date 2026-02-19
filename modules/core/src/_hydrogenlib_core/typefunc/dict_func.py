from copy import deepcopy
from typing import MutableMapping


class ObjectiveDict:
    __slots__ = ("_dict",)

    def __init__(self, **kwargs):
        super().__setattr__("_dict", kwargs)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def get_dict(self):
        return self._dict


def dict_pack(values, *keys):
    return {
        k: v for k, v in zip(keys, values)
    }


# 字典解包
def dict_unpack(dct, *keys):
    return (dct[k] for k in keys)


def dict_extract(dct, *keys):
    return {
        k: dct[k] for k in keys
    }


class SubDict(MutableMapping):
    __slots__ = ("_data", "_par", '_keys')

    def __getitem__(self, item):
        try:
            return self._data[item]
        except KeyError:
            return self._par[item]

    def __setitem__(self, key, value, /):
        self._data[key] = value

    def __delitem__(self, key, /):
        try:
            del self._data[key]
        except KeyError:
            self._keys.remove(key)

    def __len__(self):
        return len(set(self._data.keys()) | self._keys)

    def __iter__(self):
        return iter(
            set(self._data.keys()) | self._keys
        )

    def __init__(self, parent, *keys):
        self._par = parent
        self._keys = set(keys)
        self._data = {}


def dict_get_as(dct, key, type, default=None):
    try:
        return type(dct[key])
    except KeyError:
        return default


class DefaultDict(MutableMapping):
    """
    自动设置未存在于字典的键的值，同时访问时返回默认值

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

    def __iter__(self):
        return self._dict.__iter__()
