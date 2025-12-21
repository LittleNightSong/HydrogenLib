from abc import ABCMeta

from .enums import *


class CDataMeta(ABCMeta):
    __cdata__ = ...


class AbstractCData(metaclass=CDataMeta):
    """
    抽象基类，代表 ctypes 数据类型的通用行为。
    """

    __cdata__ = ...

    def __as_ctype__(self):
        """
        将当前实例转换为 ctypes 数据类型。

        :return: ctypes 数据类型。
        """
        return self.__cdata__

    def __convert_ctype__(self, target):
        """
        转换当前实例为指定类型的 ctypes 数据类型。
        :param target: 目标 ctypes 数据类型。
        :return:
        """
        raise NotImplementedError

    @property
    def _b_base_(self):
        """
        获取根 ctypes 对象，该对象拥有当前实例所共享的内存块。

        :return: 根 ctypes 对象。
        """
        return self._b_base_

    @property
    def _b_needsfree_(self):
        """
        判断当前实例是否分配了内存块。

        :return: 布尔值，表示是否需要释放内存。
        """
        return self.__cdata__._b_needsfree_

    @property
    def _objects(self):
        """
        获取需要保持存活的 Python 对象集合。

        :return: 包含相关对象的字典。
        """
        return self.__cdata__._objects

    def __eq__(self, other):
        return self.__cdata__ == other


class AbstractCType:
    """
    Properties:
        - __real_type__: 类型在 hyctypes 类型系统中表示的真实类型, 比如 PointerType 的真实类型为 Pointer
        - __real_ctype__: 类型在 ctypes 类型系统表示的真实类型

    如果不重写 __call__ 方法,那么默认返回 __real_type__(*args, **kwargs)
    """
    __real_type__: type[AbstractCData | object] = None
    __real_ctype__: type = None

    def __init_subclass__(cls, **kwargs):
        real = kwargs.get('real')
        if real:
            cls.__real_type__ = real

    def __class_getitem__(cls, item):
        if isinstance(item, tuple):
            return cls(*item)
        return cls(item)

    def __call__(self, *args, **kwargs) -> '__real_type__':
        return self.__real_type__(*args, **kwargs)

    def __convert_ctype__(self, obj):
        """
        将一个对象转换成自己代表的类型
        :param obj: 一个对象
        :return:
        """

        return obj

    def __instancecheck__(self, instance):
        return \
            isinstance(instance, self.__real_type__) or \
            isinstance(instance, self.__real_ctype__)


class AlwaysEquals:
    def __eq__(self, other):
        return True


def as_cdata(obj):
    if isinstance(obj, AbstractCData):
        return as_cdata(
            obj.__as_ctype__())  # 一定要保证它返回是一个 ctypes 类型值
    return obj


def convert_cdata(obj, tp):
    if isinstance(obj, AbstractCData):
        if isinstance(tp, AbstractCType) and isinstance(obj, tp.__real_type__):
            return obj  # 类型一致，直接返回
        try:
            obj = obj.__convert_ctype__(tp)
        except (TypeError, NotImplementedError):
            if isinstance(tp, AbstractCType):
                obj = tp.__convert_ctype__(obj)
            else:
                return obj
        return convert_cdata(obj, tp)

    else:
        if isinstance(tp, AbstractCType):
            return tp(obj)

    return obj


def as_ctype(tp):
    if isinstance(tp, AbstractCType):
        return as_ctype(tp.__real_ctype__)
    return tp


def pointer(obj):
    if obj is None or isinstance(obj, int):
        return 0
    return ctypes.pointer(as_cdata(obj))


def byref(obj):
    return ctypes.byref(as_cdata(obj))


def sizeof(obj):
    if isinstance(obj, AbstractCData):
        obj = as_cdata(obj)
    elif isinstance(obj, AbstractCType):
        obj = as_ctype(obj)

    return ctypes.sizeof(obj)


def cast(obj, target_type):
    return ctypes.cast(as_cdata(obj), ctypes.POINTER(as_ctype(target_type)))


def as_functype(obj, prototype):
    return prototype(as_cdata(obj))


def get_real_type(ctype) -> type[AbstractCData]:
    if isinstance(ctype, AbstractCType):
        return ctype.__real_type__
    else:
        return ctype
