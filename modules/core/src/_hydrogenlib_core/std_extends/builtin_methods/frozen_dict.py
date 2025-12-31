import types


def frozendict(dic) -> dict:
    """
    创建一个不可修改(只读)的字典
    :return:
    """
    return types.MappingProxyType(dic)
