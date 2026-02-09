from __future__ import annotations

import builtins
import dataclasses
from typing import Any, Callable

from _hydrogenlib_core.typefunc import AutoSlots
from _hydrogenlib_core.utils import InstanceMapping
from .type_registry import validate


@dataclasses.dataclass
class FieldInfo:
    name: str | None = None
    type: builtins.type | None = None
    default: Any = None
    default_factory: Callable | None = None
    alias: str | None = None
    validator: Callable[[Any], type] | None = None
    extra_validators: list[Callable[[Any], type]] = dataclasses.field(
        default_factory=list
    )
    serializer: Callable[[Any], Any] | None = None

    @property
    def key(self) -> str:
        if self.alias is not None:
            return self.alias
        elif self.name is not None:
            return self.name
        else:
            raise ValueError('No name or alias provided')


class Field(AutoSlots):
    info: FieldInfo
    values: InstanceMapping[Any, Any]

    def __init__(self, field_info: FieldInfo):
        super().__init__()
        self.info = field_info
        self.values = InstanceMapping()

    def value(self, instance, value=...):
        if value is ...:
            return self.values.get(instance)
        else:
            self.values[instance] = value
            return None

    @property
    def default(self):
        return (
            self.info.default_factory()
            if self.info.default_factory is not None
            else self.info.default
        )

    def value_for_serializer(self, instance):
        if self.info.serializer is None:
            return self.value(instance)
        return self.info.serializer(self.value(instance))

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.value(instance)

    def __set__(self, instance, value):
        info = self.info

        if info.validator is not None:  # 首先检查是否有专用的验证器
            value = info.validator(value)  # 有，执行验证

        elif (tr := getattr(instance, "__config_type_registry__")) is not None:  # 否则查看容器实例的类型注册表
            try:
                value = validate(  # 有效，尝试从注册表执行验证函数
                    tr, value, info.type  # ty:ignore[invalid-argument-type]
                )
            except KeyError:
                pass  # 注册表内没有符合这个类型的验证函数
        # else:
        #   否则不执行验证

        # continue
        for i in info.extra_validators:  # 执行所有拓展验证器
            if not i(value):
                raise RuntimeError("Validating failed")

        self.value(instance, value)

    def __delete__(self, instance):
        self.value(instance, self.default)
