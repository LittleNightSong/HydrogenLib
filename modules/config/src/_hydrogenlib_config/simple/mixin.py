from abc import ABC, abstractmethod

from _hydrogenlib_config_core.type_registry import TypeRegistry
from _hydrogenlib_config_core.field import FieldInfo


class Mixin(ABC):
    @abstractmethod
    def check(self, field: FieldInfo):
        """
        Config Builder 会在配置类型初始化时对每一个字段调用一次 ``.check`` 方法，返回一个 ``bool`` 值，决定是否对这个字段进行额外处理
        :param field: 传入的字段信息
        :return: ``bool``
        """

    @abstractmethod
    def apply(self, field: FieldInfo, type_registry: TypeRegistry):
        """
        Config Builder 在调用 ``.check`` 结果为 ``True`` 时调用此函数。此时你可以修改 ``FieldInfo`` 和增强功能
        :param field: 传入的字段信息
        :param type_registry: 当前配置类型使用的类型注册表
        :return: ``None`` 或者一个 ``Field`` 子类
        """
        ...
