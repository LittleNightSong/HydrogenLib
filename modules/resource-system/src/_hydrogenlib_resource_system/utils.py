from __future__ import annotations

from typing import Callable

from .builtin_providers import OverlayerProvider
from .core.provider import Resource, ResourceProvider
from .system import ResourceSystem


def registry_resource_type[T](type_: type[T]):
    """
    注册资源类型装饰器
    类型被注册后, 可以通过 resource_system.get("...").parse_as(T) 的格式来直接获取这个类型的实例
    :param type_: 需要注册的类型
    :return: 一个装饰器, 应通过此装饰器来指定 ``Resource`` -> ``Type`` 的转换函数
    """

    def decorator(func: Callable[[type[T], Resource], T]):
        type_.__from_resource__ = func
        return func

    return decorator


class _WrappedResourceType:
    def __init__(self, typ, convert_func):
        self._typ = typ
        self._cf = convert_func

    def __getattribute__(self, item):
        if item in {'_typ', '_cf', '__call__'}:
            return super().__getattribute__(item)

        return getattr(self._typ, item)

    def __call__(self, *args, **kwargs):
        return self._cf(*args, **kwargs)


def wrap_type[T](typ: type[T], convert_func) -> type[T]:
    return _WrappedResourceType(typ, convert_func)


# class _MTB(TypedDict):
#     provider: ResourceProvider | type[ResourceProvider]
#     children: MountTab
#
#
# type MountTab = dict[str, str | MountTab | ResourceProvider | type[ResourceProvider] | _MTB]
#
#
# def make_system_by_tab(
#         tab: MountTab
# ):
#     from .system import ResourceSystem
#     system = ResourceSystem()
#
#
#
#     return system

type _ProviderSpec = str | ResourceProvider | type[ResourceProvider]


def create_system(mounts: dict[str, _ProviderSpec | list[_ProviderSpec]]):
    system = ResourceSystem()

    def solve_provider(provider):
        if isinstance(provider, list):
            return OverlayerProvider(list(map(solve_provider, provider)))
        elif isinstance(provider, ResourceProvider):
            return provider
        else:
            raise ValueError(f'Not a provider: {provider}')

    for prefix, provider in mounts.items():
        if isinstance(provider, str):
            system.bind(prefix, provider)
            continue
        provider = solve_provider(provider)
        system.mount(prefix, provider)

    return system
