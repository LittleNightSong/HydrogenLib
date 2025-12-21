from __future__ import annotations

import typing
from typing import Any


class Descriptor:
    __instance_mapping__: 'InstanceMapping' = None
    __dspt_name__ = None
    __dspt_return_self__ = True

    def __init__(self):
        from .utils.instance_dict import InstanceMapping
        if self.__instance_mapping__ is None:
            self.__instance_mapping__ = InstanceMapping()

    def __init_subclass__(cls, **kwargs):
        if instance_class := getattr(cls, 'Instance', None):
            def new(self, inst):
                return instance_class()

            cls.__dspt_new__ = new

    def __instance__(self, inst, owner):
        if inst not in self.__instance_mapping__:
            self.__instance_mapping__[inst] = x = self.__dspt_new__(inst)
            x.__dspt_init__(inst, owner, self.__dspt_name__, self)
        return self.__instance_mapping__[inst]

    def __dspt_get__(self, inst, owner) -> Any:
        """
        获取描述符的值。
        :param inst: 访问描述符的实例。
        :param owner: 描述符所属的类。
        :return: 描述符的值。
        """
        return self.__instance__(inst, owner).__dspt_get__(inst, owner, self)

    def __dspt_set__(self, inst, value):
        """
        设置描述符的值。
        :param inst: 访问描述符的实例。
        :param value: 要设置的值。
        """
        self.__instance__(inst, None).__dspt_set__(inst, value, self)

    def __dspt_del__(self, inst):
        """
        删除描述符的值。
        :param inst: 访问描述符的实例。
        """
        self.__instance__(inst, None).__dspt_del__(inst, self)

    def __dspt_new__(self, inst) -> DescriptorInstance:
        """
        创建一个新的 DescriptorInstance 实例。
        :return: 新的 DescriptorInstance 实例。
        """
        return DescriptorInstance()

    def __dspt_init__(self, name, owner):
        ...

    def __get__(self, instance, owner) -> Any:
        """
        实现描述符协议的 __get__ 方法。
        :param instance: 访问描述符的实例。
        :param owner: 描述符所属的类。
        :return: 描述符的值。
        """
        if instance is None and self.__dspt_return_self__:
            return self
        else:
            return self.__dspt_get__(instance, owner)

    def __set__(self, instance, value):
        """
        实现描述符协议的 __set__ 方法。
        :param instance: 访问描述符的实例。
        :param value: 要设置的值。
        """
        self.__dspt_set__(instance, value)

    def __delete__(self, instance):
        """
        实现描述符协议的 __delete__ 方法。
        :param instance: 访问描述符的实例。
        """
        self.__dspt_del__(instance)

    def __set_name__(self, owner, name):
        """
        设置描述符的名称。
        :param owner: 描述符所属的类。
        :param name: 描述符的名称。
        """
        self.__dspt_name__ = name
        self.__dspt_init__(name, owner)


class DescriptorInstance:
    def __dspt_get__(self, instance, owner, parent) -> Any:
        """
        获取描述符的值（需子类实现）。
        :param instance: 访问描述符的实例。
        :param owner: 描述符所属的类。
        :param parent: 父级描述符。
        :raises NotImplementedError: 如果子类未实现该方法。
        """
        return self

    def __dspt_set__(self, instance, value, parent):
        """
        设置描述符的值（需子类实现）。
        :param instance: 访问描述符的实例。
        :param value: 要设置的值。
        :param parent: 父级描述符。
        :raises NotImplementedError: 如果子类未实现该方法。
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement __better_set__")

    def __dspt_del__(self, instance, parent):
        """
        删除描述符的值（需子类实现）。
        :param instance: 访问描述符的实例。
        :param parent: 父级描述符。
        :raises NotImplementedError: 如果子类未实现该方法。
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement __better_del__")

    def __dspt_init__(self, inst, owner, name, dspt):
        """
        初始化描述符(需子类实现)。
        """


def get_descriptor_instance(descriptor, instance, owner=None):
    return descriptor.__instance__(instance, owner or type(instance))


if typing.TYPE_CHECKING:
    from .utils.instance_dict import InstanceMapping
