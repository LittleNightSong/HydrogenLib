from typing import MutableMapping


class ObjectiveDict:
    def __init__(self, **kwargs):
        object.__setattr__(self, "_dict", kwargs)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    @property
    def get_dict(self):
        return self._dict


def build_from_tuple(tuple, *keys):
    return {
        k: v for k, v in zip(keys, tuple)
    }


# 字典解包
def unpack_to_tuple(dct, *keys):
    return (dct[k] for k in keys)


class SubDict(MutableMapping):
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

    def __init__(self, parent, keys):
        self._par = parent
        self._keys = set(keys)
        self._data = {}

