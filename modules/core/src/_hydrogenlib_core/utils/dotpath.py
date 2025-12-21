class Dotpath:
    def __init__(self, path: str = ''):
        self._path = path
        self._splited = self._path.split('.')
        self._length = len(self._splited)

    def _get(self, index):
        if index < 0:
            index += self._length

        if index < 0 or index >= self._length:
            return Dotpath('')
        else:
            return Dotpath(self._splited[index])

    @property
    def parent(self):
        if self._length > 1:
            return Dotpath('.'.join(self._splited[:-1]))
        else:
            return Dotpath('')

    @property
    def name(self):
        return self._get(-1)

    @property
    def root(self):
        return self._get(0)

    def check(self, error=True):
        """
        Check if the path is valid.
        """
        if not all([str(x).isidentifier() for x in self._splited]):
            if error:
                raise ValueError(f'Invalid path: {self._path}')
            else:
                return False
        return True

    def create(self, obj):
        """
        Create the path in the object.
        """
        for attr in self:
            if not hasattr(obj, attr):
                setattr(obj, attr, object())
            else:
                continue

            obj = getattr(obj, attr)

    def get(self, obj):
        cur = obj
        for attr in self:
            if not hasattr(cur, attr):
                return None
            else:
                cur = getattr(cur, attr)
        return cur

    def __iter__(self):
        return iter(self._splited)

    def __len__(self):
        return self._length

    def __str__(self):
        return f'Dotpath({self._path})'

    __repr__ = __str__
