class Namespace:
    _init = False

    def __init__(self, **kwargs):
        self._namesp = kwargs

    def set(self, key, value):
        self._namesp[key] = value

    def get(self, item):
        if item in self._namesp:
            return self._namesp[item]
        else:
            return self.error

    def __getattr__(self, item):
        if item not in self._namesp:
            raise AttributeError("Namespace has no attribute " + item)

        return self._namesp[item]

    def delete(self, item):
        if item in self._namesp:
            self._namesp.pop(item)

    def set_namespace(self, nsp: dict):
        self._namesp = nsp

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.delete(key)

    def __getitem__(self, item):
        return self.get(item)

    def items(self):
        return self._namesp.items()

    def keys(self):
        return self._namesp.keys()

    def values(self):
        return self._namesp.values()
