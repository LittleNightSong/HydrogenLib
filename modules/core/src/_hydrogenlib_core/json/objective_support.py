class Object:
    __slots__ = ('__dct', )

    def __init__(self, dct):
        self.__dct = dct

    def __getattr__(self, item):
        try:
            return self.__dct[item]
        except KeyError as e:
            raise KeyError(e) from None

    def __setattr__(self, key, value):
        if key in self.__slots__:
            super().__setattr__(key, value)
        else:
            self.__dct[key] = value

    def __getitem__(self, item):
        return self.__dct[item]

    def __setitem__(self, key, value):
        self.__dct[key] = value


def object_hook(dct):
    return Object(dct)
