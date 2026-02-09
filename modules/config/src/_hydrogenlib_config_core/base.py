import inspect
import sys
import typing
import warnings
from collections import OrderedDict
from typing import Any, ClassVar

from typing_inspection.typing_objects import is_annotated

from _hydrogenlib_core.typefunc import iter_annotations
from .field import FieldInfo, Field
from .type_registry import TypeRegistry


class ConfigBase:
    __config_fields__: ClassVar[OrderedDict[str, Field]] = None
    __config_alias__: ClassVar[dict[str, str]] = None
    __config_type_registry__: ClassVar[str | TypeRegistry]

    def __init_subclass__(cls, *, middle=False, **kwargs):
        if middle:  # 中间层
            return

        cls.__config_fields__ = cls.__config_fields__ or OrderedDict()
        cls.__config_alias__ = cls.__config_alias__ or dict()

        for name, type, value in iter_annotations(cls, with_value=True):
            if is_descriptor(value):
                continue  # 忽略描述符

            field_info = None
            name = sys.intern(name)

            # 构造字段信息

            if is_annotated(typing.get_origin(type)):  # Annotated 特殊处理
                type, field_info = typing.get_args(type)

                if not isinstance(field_info, FieldInfo):  # 检查类型，但不强制一定是一个 FieldInfo
                    warnings.warn(f'{name} is not a valid field (except FieldInfo, but got {field_info})')

                field_info.type = type  # 绑定

            if isinstance(value, FieldInfo):  # 如果 value 是 FieldInfo
                if field_info is not None:  # 并且注解是 Annotated
                    raise TypeError(f'Invalid field {name} (gave too many info)')  # 抛出错误

                field_info = value

            else:  # 不是 FieldInfo 的 value，则视作默认值
                if field_info is not None:  # 如果 FieldInfo 已经存在
                    field_info.default = value  # 直接设置
                    # WARN: 这里可能会覆盖掉原本的默认值
                else:
                    field_info = FieldInfo(  # 否则重新构造 FieldInfo
                        name=name, type=type, default=value
                    )

            if field_info.name is None:  # 最后检查
                field_info.name = name
            if field_info.type is None:
                field_info.type = type

            # 现在一切就绪

            field = Field(field_info)  # 从 info 初始化 Field 描述符

            cls.__config_alias__[field_info.key] = name  # 纪录别名和配置名的映射
            setattr(cls, name, field)  # 写入到类中
            cls.__config_fields__[name] = field  # 在 fields 中纪录


def is_descriptor(value: Any | None):
    return inspect.ismethoddescriptor(value) or inspect.isdatadescriptor(value)
