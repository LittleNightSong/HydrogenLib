class Visited:
    @property
    def visited(self) -> set:
        return self._visited
    
    def __init__(self):
        self._visited = set()

    def add(self, obj):
        self._visited.add(obj)

    def remove(self, obj):
        if obj in self._visited:
            self._visited.remove(obj)

    def clear(self):
        self._visited.clear()

    def __len__(self):
        return len(self._visited)

    def __iter__(self):
        return iter(self._visited)

    def __repr__(self):
        return repr(self._visited)

    def __contains__(self, obj):
        return obj in self._visited

    def __getitem__(self, item):
        return item in self._visited

    def __setitem__(self, key, value):
        if value:
            self.add(key)
        else:
            self.remove(key)
