import inspect
from typing import OrderedDict

from _hydrogenlib_core.typefunc import iter_annotations
from .field import FieldInfo, Field


class ConfigBase:
    __config_fields__: OrderedDict[str, Field]
    __config_type_registry__ = 'global'

    def __init_subclass__(cls, **kwargs):
        middle = kwargs.get('middle', False)
        if middle:
            return

        cls.__config_fields__ = OrderedDict()

        for name, anno, value in iter_annotations(cls):
            # 构造描述符
            if isinstance(value, FieldInfo):
                field_info = value

                if field_info.name is None:
                    field_info.name = name
                if field_info.type is None:
                    field_info.type = anno
            elif not (inspect.ismethoddescriptor(value) or inspect.isdatadescriptor(value)):
                field_info = FieldInfo(
                    name, anno, default=value
                )
            else:
                continue

            field = Field(field_info)

            setattr(cls, name, field)
            cls.__config_fields__[name] = field
