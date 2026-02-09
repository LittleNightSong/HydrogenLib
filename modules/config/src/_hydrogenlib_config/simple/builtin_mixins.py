from typing import NamedTuple

import typing_inspection.typing_objects

from _hydrogenlib_config_core.field import FieldInfo
from _hydrogenlib_config_core.type_registry import TypeRegistry
from .mixin import Mixin


class NamedTupleMixin(Mixin):
    @staticmethod
    def make_validator(namedtuple_type):
        # Validates and converts input to namedtuple type
        def validator(data):
            if isinstance(data, dict):
                value = namedtuple_type(**data)
            elif isinstance(data, namedtuple_type):
                value = data
            elif hasattr(data, '__iter__'):  # Iterable
                value = namedtuple_type(*data)
            else:
                raise ValueError(f"Invalid value for {namedtuple_type.__name__}: {data}")
            return value

        return validator

    @staticmethod
    def make_serializer(namedtuple_type: type[NamedTuple]):
        # def serializer(data):
        #     return namedtuple_type._asdict(data)
        #
        # return serializer
        return namedtuple_type._asdict

    def check(self, field: FieldInfo):
        try:
            return typing_inspection.typing_objects.is_namedtuple(field.type)
        except TypeError:
            return False

    def apply(self, field: FieldInfo, type_registry: TypeRegistry):
        if field.validator is None:
            field.validator = self.make_validator(field.type)

        if field.serializer is None:
            field.serializer = self.make_serializer(field.type)
