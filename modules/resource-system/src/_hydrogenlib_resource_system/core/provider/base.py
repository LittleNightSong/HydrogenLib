from __future__ import annotations

import builtins
import typing
from abc import ABC, abstractmethod
from pathlib import PurePosixPath
from typing import Any

from _hydrogenlib_core.typefunc import AutoSlots

if typing.TYPE_CHECKING:
    from _hydrogenlib_resource_system.core.system import ResourceSystem


class ResourceProvider(ABC):
    @abstractmethod
    def list(self, source, path: PurePosixPath, query: dict[str, Any],
             resource_system: ResourceSystem) -> builtins.list: ...

    @abstractmethod
    def get(self, source, path: PurePosixPath, query: dict[str, Any],
            resource_system: ResourceSystem) -> Resource | None: ...

    @abstractmethod
    def set(self, source, path: PurePosixPath, data: Any, query: dict[str, Any],
            resource_system: ResourceSystem) -> None: ...

    @abstractmethod
    def exists(self, source, path: PurePosixPath, query: dict[str, Any], resource_system: ResourceSystem) -> bool: ...

    @abstractmethod
    def remove(self, source, path: PurePosixPath, query: dict[str, Any], resource_system: ResourceSystem) -> bool: ...


class Resource(ABC, AutoSlots):
    name: str

    @abstractmethod
    def __fspath__(self) -> str:
        ...

    def open(
            self,
            mode='r',
            encoding=None,
            buffering=-1,
            errors: str | None = None,
            opener: typing.Callable[[str, int], int] | None = 0) -> typing.IO:
        return open(self, mode, buffering, encoding, errors, opener=opener)

    def close(self, **kwargs) -> None:
        ...

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
    def binary(self) -> builtins.bytes:
        with self.open('rb') as f:
            return f.read()

    def __bytes__(self):
        return self.binary

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"""
<Resource: {self.name}>
size: 
content: {self.text}
content(bytes): {self.binary}
"""
