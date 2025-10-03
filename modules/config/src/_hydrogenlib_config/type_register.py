from typing import Callable
from _hydrogenlib_core.utils import InstanceMapping
from _hydrogenlib_core.typefunc import iter_attributes, is_method, Function

type Validator[T, R] = Callable[[T], R]


class TypeRegister:
    def __init__(self):
        self._register = InstanceMapping()  # type: InstanceMapping[type, InstanceMapping[type, Validator]]

    def register(self, cls: type, target_type: type, validator: Validator) -> None:
        if cls not in self._register:
            self._register[cls] = InstanceMapping()

        self._register[cls][target_type] = validator

    def exists(self, cls: type, target_type: type) -> bool:
        return cls in self._register and target_type in self._register[cls]

    def validator(self, cls: type, target_type: type) -> Validator:
        return self._register[cls][target_type]

    def validate(self, data: object, target: type):
        return self.validator(type(data), target)(data)

    # Sugar
    def __call__(self, cls: type):
        config_metadata = getattr(cls, 'Config_Metadata')
        if not isinstance(config_metadata, type):
            raise TypeError(f'{cls} is not a valid config class')
        obj = config_metadata()

        for name, value in iter_attributes(obj):
            if is_method(value):
                func = Function(value)
                type_ = func.signature.return_annotation
                self.register(cls, type_, func)
