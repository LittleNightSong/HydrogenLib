from typing import Callable
from ..core.provider import Resource

def registry_resource_type[T](type_: type[T]):
    """
    注册资源类型装饰器
    类型被注册后, 可以通过 resource_system.get[Type]("...") 的格式来直接获取这个类型的实例
    :param type_: 需要注册的类型
    :return: 一个装饰器, 应通过此装饰器来指定 ``Resource`` -> ``Type`` 的转换函数
    """
    def decorator(func: Callable[[type[T], Resource], T]):
        type_.__from_resource__ = func
        return func

    return decorator