class Char(int):

    def __str__(self):
        return chr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"


class _Null:
    _inst = None

    def __new__(cls):
        if cls._inst is None:
            cls._inst = super().__new__(cls)

        return cls._inst


null = _Null()
inf = float('inf')
