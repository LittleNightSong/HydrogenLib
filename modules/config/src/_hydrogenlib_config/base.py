import json
from functools import wraps
from typing import Any

from _hydrogenlib_core.typefunc import ObjectiveDict
from . import core
from .global_type_registry import global_type_registry
from . import pre_mixin as _pre_mixin


def create_validator_for_namedtuple(namedtuple_type):
    # Validates and converts input to namedtuple type
    @wraps(namedtuple_type)
    def validator(data, *args):
        if isinstance(data, dict):
            value = namedtuple_type(**data)
        elif isinstance(data, namedtuple_type):
            value = data
        elif isinstance(data, tuple):
            value = namedtuple_type(*data)
        else:
            raise ValueError(f"Invalid value for {namedtuple_type.__name__}: {data}")
        return value

    return validator


class NamedTupleMixin(_pre_mixin.Mixin):
    def check(self, field: core.field.FieldInfo):
        return issubclass(field.type, tuple) and field.type is not tuple

    def apply(self, field: core.field.FieldInfo, type_registry: core.type_registry.TypeRegistry):
        if field.validator is None:
            field.validator = create_validator_for_namedtuple(field.type)


class ConfigBase(core.base.ConfigBase, middle=True):
    __config_type_registry__ = 'global'

    def __init_subclass__(cls, **kwargs):
        if kwargs.get("middle", False): return
        mixins = kwargs.get('mixins', [NamedTupleMixin])

        if cls.__config_type_registry__ == 'global':
            cls.__config_type_registry__ = global_type_registry.create_sub_registry()  # 创建子注册表

        super().__init_subclass__()

        for field in cls.__config_fields__.values():
            for mixin in mixins:
                mixin_ins = mixin()
                if mixin_ins.check(field.field_info):
                    mixin_ins.apply(field.field_info, cls.__config_type_registry__)
                del mixin_ins

    @classmethod
    def from_obj(cls, obj: dict | tuple[tuple[str, Any], ...], extra='allow'):
        obj = dict(obj)
        config = cls()

        for name, field in cls.__config_fields__.items():
            key = field.key
            if key in obj:
                setattr(config, name, obj[key])
                del key

        if len(obj):
            if extra == 'allow':
                config.__dict__.update(obj)
            else:
                raise ValueError(f"Extra fields: {list(obj.keys())}")

        return config

    def to_dict(self):
        return {
            name: getattr(self, name)
            for name in self.__config_fields__
        }

    def __str__(self):
        string = f'{self.__class__.__name__}('
        for name in self.__config_fields__:
            value = getattr(self, name)
            string += f'{name}={value}, '
        string = string[:-2]
        string += ')'
        return string