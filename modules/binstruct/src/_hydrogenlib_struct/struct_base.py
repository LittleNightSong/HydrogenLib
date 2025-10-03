from .struct_info import StructInfo, FieldInfo
from collections import OrderedDict
from _hydrogenlib_core.typefunc import iter_annotations


class StructBase:
    def __init_subclass__(cls, **kwargs):
        big_endian = kwargs.get('big_endian', False)
        fields = OrderedDict()

        for name, type_, value in iter_annotations(cls):
            fields[name] = FieldInfo(name, type_)
