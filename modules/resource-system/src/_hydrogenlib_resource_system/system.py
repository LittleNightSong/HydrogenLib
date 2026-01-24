from typing import overload, Any

from . import core
from .builtin_providers import BindProvider


class TypedResourceSystem[T]:
    __slots__ = ('_system', '_type')

    def __init__(self, system, type):
        self._system = system
        self._type = type

    def get(self, url, **query) -> T:
        return self._system.get(url, **query).parse_as(self._type)


class ResourceSystem:
    def __init__(self):
        self._system = core.system.CoreResourceSystem()

    def get(self, url, **query):
        return self._system.get(url, **query)

    def remove(self, url, **kwargs):
        return self._system.remove(url, **kwargs)

    def set(self, url, data, **query):
        return self._system.set(url, data, **query)

    def list(self, url, **query):
        return self._system.list(url, **query)

    def exists(self, url, **query):
        return self._system.exists(url, **query)

    @overload
    def mount(self, prefix: str, provider: core.provider.ResourceProvider):
        ...

    @overload
    def mount(self, prefix: str, source: Any, provider: core.provider.ResourceProvider = BindProvider):
        ...

    def mount(self, prefix, source, provider=None):
        if isinstance(source, core.provider.ResourceProvider):
            return self._system.mount(prefix, source)
        else:
            return self._system.mount(prefix, provider(source))

    def bind(self, dst, src):
        return self._system.bind(dst, src)

    def open(self, url, mode='r', encoding='utf-8', **query):
        return self.get(url, **query).open(mode, encoding)

    def __getitem__[T](self, item: type[T]) -> TypedResourceSystem[T]:
        return TypedResourceSystem(self, item)

    def close(self):
        self._system.close()
