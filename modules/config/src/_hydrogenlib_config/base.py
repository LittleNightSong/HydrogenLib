import sys
from functools import wraps
from typing import Any

from . import core
from . import pre_mixin as _pre_mixin
from .global_type_registry import global_type_registry


def make_validator_for_namedtuple(namedtuple_type):
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
        try:
            return issubclass(field.type, tuple) and field.type is not tuple
        except TypeError:
            return False

    def apply(self, field: core.field.FieldInfo, type_registry: core.type_registry.TypeRegistry):
        if field.validator is None:
            field.validator = make_validator_for_namedtuple(field.type)


default_mixins = (NamedTupleMixin(),)


class ConfigBase(core.base.ConfigBase, middle=True):
    __config_type_registry__ = 'global'
    __config_alias_mapping__ = None

    def __init_subclass__(cls, *, middle=False, mixins=default_mixins, **kwargs):
        if middle:
            return

        if cls.__config_type_registry__ == 'global':
            cls.__config_type_registry__ = global_type_registry.create_sub_registry()  # 创建子注册表

        super().__init_subclass__()
        cls.__config_alias_mapping__ = mapping = dict(
            cls.__config_alias_mapping__) if cls.__config_alias_mapping__ else {}

        for name, field in cls.__config_fields__.items():
            for mixin in mixins:
                mixin_ins = mixin() if isinstance(mixin, type) else mixin
                if mixin_ins.check(field.field_info):
                    mixin_ins.apply(field.field_info, cls.__config_type_registry__)
                del mixin_ins

            mapping[sys.intern(field.key)] = sys.intern(name)

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
        pairs = ", ".join(
            map(
                lambda x: f'{x}={getattr(self, x)!r}',
                self.__config_fields__
            )
        )
        string = f'{self.__class__.__name__}({pairs})'
        return string

    def __setattr__(self, key, value):
        if key in self.__config_fields__:
            super().__setattr__(key, value)
        elif key in self.__config_alias_mapping__:
            super().__setattr__(self.__config_alias_mapping__[key], value)
        else:
            super().__setattr__(key, value)
