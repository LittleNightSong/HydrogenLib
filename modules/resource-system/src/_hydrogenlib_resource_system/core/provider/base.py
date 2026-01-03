from __future__ import annotations

import builtins
import typing
from abc import ABC, abstractmethod
from pathlib import PurePosixPath
from typing import Any

if typing.TYPE_CHECKING:
    from _hydrogenlib_resource_system.core.system import CoreResourceSystem


class ResourceProvider(ABC):
    @abstractmethod
    def list(self, path: PurePosixPath, query: dict[str, Any],
             resource_system: CoreResourceSystem) -> builtins.list: ...

    @abstractmethod
    def get(self, path: PurePosixPath, query: dict[str, Any],
            resource_system: CoreResourceSystem) -> Resource | None: ...

    @abstractmethod
    def set(self, path: PurePosixPath, data: Any, query: dict[str, Any],
            resource_system: CoreResourceSystem) -> None: ...

    @abstractmethod
    def exists(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> bool: ...

    @abstractmethod
    def remove(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem): ...

    def close(self):
        pass

    def __del__(self):
        self.close()


class Resource(ABC):
    url: str | Any = None

    @abstractmethod
    def __fspath__(self) -> str:
        ...

    def open(
            self,
            mode='r',
            encoding=None,
            buffering=-1,
            errors: str | None = None,
            opener: typing.Callable[[str, int], int] | None = None) -> typing.IO:
        """
        打开资源内容

        :return: 资源 IO 流，实现了 typing.IO 接口
        """
        return open(self, mode, buffering, encoding, errors, opener=opener)

    def release(self) -> None:
        """
        释放资源

        有些资源可能限制只能有一个访问者
        调用此函数可以主动释放资源，但这可能会让你无法继续正常使用资源

        当对象被回收时，此函数自动被调用
        """
        ...

    def parse_as[T](self, type: type[T] | typing.Callable[[typing.Self], T]) -> T:
        """
        获取资源，并尝试转换为 type 类型

        :param type: 一个可调用对象，调用时接受一个类型为 Resource 的参数，返回一个转换后的对象
        :return: 经过转换的对象
        :raises: 不定
        """
        if hasattr(type, '__from_resource__'):
            return type.__from_resource__(type)
        else:
            return type(self)

    @property
    def text(self) -> str:
        """
        读取自身的 text 内容
        """
        with self.open() as f:
            return f.read()

    @property
    def binary(self) -> builtins.bytes:
        """
        读取自身的 bytes 内容
        """
        with self.open('rb') as f:
            return f.read()

    def __bytes__(self):
        return self.binary

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"""
<Resource: {self.url}>
size: 
content: {self.text}
content(bytes): {self.binary}
"""
