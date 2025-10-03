class GettingPath:
    def __init__(self, path, getter=None, setter=None):
        if not self.check(path):
            raise ValueError(f"Path {path} is not valid")

        self.path = path
        self._getter = getter
        self._setter = setter

    @property
    def parent(self):
        """
        Get parent object
        """
        return GettingPath(self.path[:-1])

    @property
    def name(self):
        """
        Get name of object
        """
        return self.path[-1]

    def check(self, path):
        """
        Check if path is valid
        """
        return True

    def getnext(self, current, next):
        """
        Get next object from current object
        """
        if self._getter is None:
            return getattr(current, next)
        else:
            return self._getter(current, next)

    def setnext(self, current, name, value):
        """
        Set next object from current object
        """
        setattr(current, name, value)

    def iter_path(self):
        return self.path

    def touch(self, obj):
        cur = obj
        for part in self.iter_path():
            cur = self.getnext(cur, part)
        return cur

    def set(self, obj):
        cur = obj
        for part in self.iter_path()[:-1:]:
            cur = self.getnext(cur, part)
        self.setnext(cur, self.iter_path()[-1], obj)
