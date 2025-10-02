from typing import Callable, Any, get_origin, get_args

from .registry import TypeRegistry

type DefaultValidator = Callable[[Any, type], Any]  # (value, target) -> Any


class TypeConvertor:
    def __init__(self, registry):
        self._registry = registry  # type: TypeRegistry
        self._default_validator = None  # type: DefaultValidator | None

    def validate_generic(self, data, target):
        origin = get_origin(target)
        args = get_args(target)
        if origin is list:
            inner_type, = args
            return [self.validate(item, inner_type) for item in data]

        if origin is tuple:
            if args[-1] is Ellipsis:
                inner_type, = args[:-1]
                return tuple(self.validate(item, inner_type) for item in data)
            else:
                inner_types = args
                return tuple(self.validate(item, inner_type) for item, inner_type in zip(data, inner_types))

        if origin is dict:
            key_type, value_type = args
            return {
                self.validate(key, key_type): self.validate(value, value_type)
                for key, value in data.items()
            }

        if origin is set:
            inner_type, = args
            return {self.validate(item, inner_type) for item in data}

        if origin is frozenset:
            inner_type, = args
            return frozenset(self.validate(item, inner_type) for item in data)

        return data  # 无法识别的类型

    def validate(self, data, target):
        origin = get_origin(target)

        if origin:
            return self.validate_generic(data, target)

        try:
            return self._registry.validate(data, target)
        except TypeError as e:
            if self._default_validator:
                return self._default_validator(data, target)
            raise e from None

    def set_default(self, validator: DefaultValidator):
        self._default_validator = validator
