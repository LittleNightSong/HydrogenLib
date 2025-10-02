from typing import Any, Callable
from _hycore.better_descriptor import Descriptor, DescriptorInstance, get_descriptor_instance
from .global_ import global_convertor as gtc
#                                   (self, value: From) -> To
type Validator[From=Any, To=Any] = Callable[[Any, From], To]


class FieldInstance[T](DescriptorInstance):
    validator: Validator | None

    def __dspt_init__(self, inst, owner, name, dspt):
        self.__self__ = inst
        self.name = name
        self.parent = dspt
        self.model = None

    def validate(self, value):
        if self.validator:
            return self.validator(self, value)
        else:
            return gtc.validate(value, self.type)

    @property
    def value(self) -> T:
        return self.model.get(self.key, self.default)

    @value.setter
    def value(self, v: T):
        self.model.set(self.key, v)

    def __getattr__(self, item):
        return getattr(self.parent, item, None)

    def __dspt_get__(self, instance, owner, parent) -> Any:
        return self.value

    def __dspt_set__(self, instance, value, parent):
        self.value = self.validate(value)

    def __dspt_del__(self, instance, parent):
        self.value = self.default


class Field(Descriptor):
    field_instance_type = FieldInstance

    def __init__(self, typ, *, default=None, name=None, key=None, model=None):
        super().__init__()
        self.type, self.default = typ, default
        self.name = name
        self._key = key

        self.model = model

        self.validator: Validator | None = None  # 验证器, 返回转换后的值

    @property
    def key(self):
        return self._key or self.name

    def get_field_by_obj(self, __i):
        return get_descriptor_instance(self, __i)

    def __dspt_init__(self, name, owner):
        self.name = name

    def __dspt_new__(self, inst) -> DescriptorInstance:
        return self.field_instance_type()
