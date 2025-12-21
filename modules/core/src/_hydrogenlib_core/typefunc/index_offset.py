from abc import abstractmethod
from typing import Any, Callable, Optional, final


class OffsetFunction:
    @abstractmethod
    def offset(self, length): ...

    @abstractmethod
    def n_offset(self, length): ...

    @abstractmethod
    def back(self, length): ...

    @abstractmethod
    def n_back(self, length): ...

    @abstractmethod
    def offseter(self, length): ...

    @abstractmethod
    def backer(self, length): ...

    @abstractmethod
    def isend(self): ...

    @abstractmethod
    def isstart(self): ...

    @abstractmethod
    def n_offseter(self, length): ...

    @abstractmethod
    def n_backer(self, length): ...

    @abstractmethod
    def add_start(self, length): ...

    @abstractmethod
    def less_start(self, length): ...

    @abstractmethod
    def get_add_start(self, length): ...

    @abstractmethod
    def get_less_start(self, length): ...

    @abstractmethod
    def init_start(self): ...

    @abstractmethod
    def get_start_less(self, other): ...


class IterableOffsetFunction(OffsetFunction):
    @final
    def __init__(self, fat):
        self.fat = fat

    def init_start(self):
        self.fat.start = 0

    def less_start(self, length):
        self.fat.start -= length

    def add_start(self, length):
        self.fat.start += length

    def get_add_start(self, length):
        return self.fat.start + length

    def get_less_start(self, length):
        return self.fat.start - length

    def get_start_less(self, other):
        return other - self.fat.start

    def offset(self, length):
        # print(self.fat.start, length)
        if self.fat.start + length > len(self.fat.iterable):
            raise RuntimeError(
                "Cannot offset {} lengths (only {}).".format(length, len(self.fat.iterable) - self.fat.start))
        data = self.fat.iterable[self.fat.start: self.get_add_start(length)]
        self.add_start(length)
        if isinstance(data, tuple):
            return data[0]
        return data

    def n_offset(self, length):
        data = self.fat.iterable[self.fat.start: self.get_add_start(length)]
        return data

    def back(self, length):
        if self.fat.start < length:
            raise ValueError("Cannot back {} lengths (only {}).".format(length, self.fat.start))
        data = self.fat.iterable[self.get_less_start(length): self.fat.start]
        self.less_start(length)
        return data

    def n_back(self, length):
        data = self.fat.iterable[self.get_less_start(length): self.fat.start]
        return data

    def offseter(self, length):
        return self.fat.__class__(self.offset(length), self)

    def backer(self, length):
        return self.fat(self.back(length), self)

    def isend(self):
        return self.fat.start >= len(self.fat.iterable) - 1

    def isstart(self):
        return self.fat.start <= 0

    def n_offseter(self, length):
        return self.fat(self.n_offset(length), self)

    def n_backer(self, length):
        return self.fat(self.n_back(length), self)


class Offset:
    offset_func: OffsetFunction

    offset = lambda self, length: self.offset_func.offset(length)
    n_offset = lambda self, length: self.offset_func.n_offset(length)
    back = lambda self, length: self.offset_func.back(length)
    n_back = lambda self, length: self.offset_func.n_back(length)
    add_start = lambda self, length: self.offset_func.add_start(length)
    less_start = lambda self, length: self.offset_func.less_start(length)
    offseter = lambda self, length: self.offset_func.offseter(length)
    backer = lambda self, length: self.offset_func.backer(length)
    n_offseter = lambda self, length: self.offset_func.n_offseter(length)
    n_backer = lambda self, length: self.offset_func.n_backer(length)
    isend = lambda self: self.offset_func.isend()
    isstart = lambda self: self.offset_func.isstart()

    def __init__(self, iterable, offset_func: Optional[OffsetFunction] = None):
        if offset_func is None:
            offset_func = IterableOffsetFunction(self)
        self.iterable = iterable

        self.start = None

        self.offset_func = offset_func
        self.offset_func.init_start()

    def __iter__(self):
        return self.iterable[self.start:]

    def __getitem__(self, item):
        return self.iterable[item]

    def __len__(self):
        return len(self.iterable)

    def __setitem__(self, key, value):
        self.iterable[key] = value

    def to(self, _Type):
        try:
            return _Type(self.iterable)
        except TypeError as e:
            raise e from None
        except Exception as e:
            raise e from None

    def surplus(self, _Type: Optional[Callable] = None):
        if _Type is None:
            return self.n_offset(self.offset_func.get_start_less(len(self)))
        else:
            return _Type(self.surplus())

    # >
    def __gt__(self, length) -> Any:
        """
        get_offset.get_offset(length)
        :param length: an int value of length
        :return: Iterable
        """
        return self.offset(length)

    # <
    def __lt__(self, length) -> Any:
        """
        get_offset.get_offset(length)
        :param length: an int value of length
        :return: Iterable
        """
        return self.back(length)

    # >=
    def __ge__(self, length) -> Any:
        """
        get_offset.n_offset(length)
        :param length: an int value of length
        :return: Iterable
        """
        return self.n_offset(length)

    # <=
    def __le__(self, length) -> Any:
        """
        get_offset.get_offset(length)
        :param length: an int value of length
        :return: Iterable
        """
        return self.n_back(length)

    # +
    def __add__(self, length) -> Any:
        """
        start += length
        :param length: an int value of length 
        :return: None
        """
        self.add_start(length)

    # -
    def __sub__(self, length) -> Any:
        """
        start -= length
        :param length: an int value of length
        :return: None
        """
        self.less_start(length)

    # +=
    def __iadd__(self, length) -> Any:
        """
        start += length
        :param length: an int value of length
        :return: None
        """
        self.add_start(length)
        return self

    # -=
    def __isub__(self, length) -> Any:
        """
        start -= length
        :param length: an int value of length
        :return: None
        """
        self.less_start(length)
        return self

    def __lshift__(self, other):
        return self.back(other)

    def __rshift__(self, other):
        return self.offset(other)
