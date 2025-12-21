from collections import UserDict


class DoubleDict(UserDict):
    def __init__(self, dct=None):
        super().__init__()
        if dct:
            for k, v in dct.items():
                self[k] = v
                self[v] = k

        self._same_values = set()

    def get(self, k, default=None):
        if k in self._same_values:
            return k

        if k not in self:
            return default

        return self[k]

    def __getitem__(self, k):
        if k in self._same_values:
            return k
        return super().__getitem__(k)

    def __setitem__(self, key, value):
        if key == value:
            self._same_values.add(key)
            return
        super().__setitem__(key, value)
        super().__setitem__(value, key)

    def __delitem__(self, key):
        if key in self._same_values:
            self._same_values.remove(key)
            return
        super().__delitem__(self[key])
        super().__delitem__(key)
