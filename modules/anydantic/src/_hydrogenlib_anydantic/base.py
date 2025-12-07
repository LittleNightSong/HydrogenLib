from __future__ import annotations

import enum
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TypedDict

from _hydrogenlib_core.utils import InstanceMapping


class ExtraMode(str, enum.Enum):
    ignore = 'ignore'
    forbid = 'forbid'
    allow = 'allow'


class _FieldValidator(classmethod):
    name: str = ...

    def __init__(self, func, name):
        super().__init__(func)
        self.name = name


@dataclass
class ModelConfig:
    fields: OrderedDict[str, Field] = field(default_factory=OrderedDict)
    
    # 位置参数可以通过区分位置来判断是否是可选参数
    # 在后面的一定是可选参数
    position_fields: OrderedDict[str, Field] = field(default_factory=OrderedDict)
    
    # 但是关键字参数是无序的,只能通过分离储存
    keyword_optional_fields: dict[str, Field] = field(default_factory=dict)
    keyword_required_fields: dict[str, Field] = field(default_factory=dict)
    
    extra_mode: ExtraMode = ExtraMode.forbid


class Field:
    keyword_only = False

    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, value):
        self._validator = value

    def validate(self, value):
        if not isinstance(value, self.type):
            raise TypeError(f'field \'{self.name}\' expect {self.type}, but got {type(value)}')

        return value

    def is_optional(self):
        return self.default is not None
    
    def is_required(self):
        return not self.is_optional()  # 不是可选就是必选

    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

        self._mapping = InstanceMapping()
        self._validator = None

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self._mapping.get(instance, self.default)

    def __set__(self, instance, value):
        if self.validator:
            value = self.validator(value)

        self._mapping[instance] = self.validate(value)


class BaseModelConfig(TypedDict):
    extra: ExtraMode
