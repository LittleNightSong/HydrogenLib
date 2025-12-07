import typing
from abc import ABC, abstractmethod
from typing import Any

from _hydrogenlib_core.typefunc import AutoSlots


class ResourceProvider(ABC):
    @abstractmethod
    def list(self) -> list: ...

    @abstractmethod
    def get(self, path, **kwargs) -> Any: ...

    @abstractmethod
    def set(self, path, data, **kwargs) -> None: ...

    @abstractmethod
    def exists(self, path, **kwargs) -> bool: ...

    @abstractmethod
    def remove(self, path, **kwargs) -> bool: ...


class Resource(ABC, AutoSlots):
    name: str

    @abstractmethod
    def __fspath__(self) -> str: ...

    def open(self,
             mode='r',
             encoding=None,
             buffering=-1,
             errors: str | None = None,
             opener: typing.Callable[[str, int], int] | None = 0) -> typing.IO:
        return open(self, mode, buffering, encoding, errors, opener=opener)

    def close(self, **kwargs) -> None: ...

    def parse_as[T](self, type_: type[T] | typing.Callable[[typing.Self], T]) -> T:
        if hasattr(type_, '__from_resource__'):
            return type_.__from_resource__(type_)
        else:
            return type_(self)

    @property
    def text(self) -> str:
        with self.open() as f:
            return f.read()

    @property
    def bytes(self) -> bytes:
        with self.open('rb') as f:
            return f.read()

    def __bytes__(self):
        return self.bytes

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"""
<Resource: {self.name}>
size: 
content: {self.text}
content(bytes): {self.bytes}
"""
