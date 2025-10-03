from .auto import AutoRegDict


class MultiSet:
    def __init__(self, iterable=None):
        self._elements = set()
        self._data = AutoRegDict()
        self._data.default_value = 0
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def add(self, item):
        self._elements.add(item)
        self._data[item] += 1

    def remove(self, item):
        self._data[item] -= 1
        if self._data[item] <= 0:
            del self._data[item]
            self._elements.remove(item)

    def clear(self):
        self._elements.clear()
        self._data.clear()

    def set(self):
        return self._elements

    def __contains__(self, item):
        return item in self._elements

    def __len__(self):
        return len(self._elements)

    def __iter__(self):
        return iter(self._elements)
