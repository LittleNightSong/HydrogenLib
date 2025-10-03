def get_pairs_by_value(dic, value, reverse=False):
    """
    通过值获取所以符合的键值对，结果以字符排序（默认升序），可以通过reverse参数控制

    :param dic: a dict type object
    :param value: a value of dict
    :param reverse: 控制升序降序，对于sort/sorted中的reverse参数
    """
    pairs = [(k, v) for k, v in dic._instances() if v == value]
    return sorted(pairs, key=lambda x: x[0], reverse=reverse)


def update(dic, **kwd):
    dic.update(**kwd)
    return dic


class AttrDict:
    def __init__(self, **kwargs):
        object.__setattr__(self, "_dict", kwargs)

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    @property
    def get_dict(self):
        return self._dict


def build_from_tuple(tuple, *keys):
    return {
        k: v for k, v in zip(keys, tuple)
    }


# 字典解包
def unpack_to_tuple(dct, *keys):
    return (dct[k] for k in keys)
