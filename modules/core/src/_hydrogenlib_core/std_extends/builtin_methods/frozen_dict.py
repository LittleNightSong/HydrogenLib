from collections import UserDict as _UserDict
from types import MappingProxyType as _MappingProxyType


class _FrozenDict(_UserDict):
    def __init__(self, dic):
        super().__init__()
        self.__dic = dic  # 正常来说, UserDict 将数据储存在 self.data 中, 但这里将数据储存在 self.__dic 中, 避免被修改

    def __getitem__(self, item):
        return self.__dic[item]  # 从自定义的属性中获取数据

    def _error(self):
        raise TypeError('frozendict is immutable')

    __setitem__ = __delitem__ = pop = update = _error


FROZEN_DICT = _FrozenDict
MAPPING_PROXY = _MappingProxyType


def frozendict(dic, backend=FROZEN_DICT):
    """
    创建一个不可修改(只读)的字典
    :param dic: 字典
    :param backend: 创建字典的类, 默认为 _FrozenDict, 可以传入 MappingProxyType,
                    这些类型位于常量 `FROZEN_DICT` 和 `MAPPING_PROXY`中
    :return:
    """
    return backend(dic)


def is_frozendict(obj):
    """
    判断对象是否为不可修改的字典
    :param obj:
    :return:
    """
    return isinstance(obj, FROZEN_DICT) or isinstance(obj, MAPPING_PROXY)
