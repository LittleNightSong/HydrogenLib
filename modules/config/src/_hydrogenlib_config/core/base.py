import inspect
import sys
import typing
from typing import OrderedDict, Any

import typing_inspection.typing_objects

from _hydrogenlib_core.typefunc import iter_annotations
from .field import FieldInfo, Field


class ConfigBase:
    __config_fields__: OrderedDict[str, Field]
    __config_type_registry__ = 'global'

    def __init_subclass__(cls, *, middle=False, **kwargs):
        if middle:
            return

        cls.__config_fields__ = OrderedDict()

        for name, type, value in iter_annotations(cls, with_value=True):
            field_info = None
            name = sys.intern(name)

            if is_descriptor(value):
                continue  # 忽略描述符
            # 构造字段信息
            if typing_inspection.typing_objects.is_annotated(typing.get_origin(type)):
                type, field_info = typing.get_args(type)
                if not isinstance(field_info, FieldInfo):
                    raise TypeError(f'{name} is not a valid field')
                field_info.type = type

            if isinstance(value, FieldInfo):
                if field_info is not None:
                    raise TypeError(f'{name} is not a valid field (gave too many info)')

                field_info = value

                if field_info.name is None:
                    field_info.name = name
                if field_info.type is None:
                    field_info.type = type

            else:
                if field_info:
                    field_info.default = value
                else:
                    field_info = FieldInfo(
                        name=name, type=type, default=value
                    )

            field = Field(field_info)

            setattr(cls, name, field)
            cls.__config_fields__[name] = field


def is_descriptor(value: Any | None):
    return inspect.ismethoddescriptor(value) or inspect.isdatadescriptor(value)
