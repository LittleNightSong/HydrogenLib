from __future__ import annotations

import dataclasses
import functools
import inspect
import typing
from typing import Callable, overload, Any, Generator

from _hydrogenlib_core.data_structures import Stack
from _hydrogenlib_core.typefunc import split_type, get_origin
from _hydrogenlib_core.utils import InstanceMapping

IMP = InstanceMapping
type Validator[DataType, TargetType, *subtypes] = Callable[[DataType, TargetType, tuple[*subtypes]], TargetType]
type TypeRegistryDataStructure = \
    InstanceMapping[type, InstanceMapping[type, dict[tuple[type, ...], ValidatorMetadata]]]


@dataclasses.dataclass(frozen=True, slots=True)
class ValidatorMetadata[DT, TT, *subtypes]:
    validator: Validator[DT, TT, *subtypes]
    target_type: type[TT]


def wraps_as_generator_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
        yield

    return wrapper


class TypeRegistry:
    __slots__ = ("_registry", "_validators_no_source_type", "_default_validator")

    def __init__(self):
        self._validators_no_source_type: InstanceMapping[
            type,
            dict[tuple[type, ...], ValidatorMetadata]
        ]
        self._validators_no_source_type = IMP()
        self._registry = IMP()  # type: TypeRegistryDataStructure
        self._default_validator: Validator | None = None

    def default_validator(self, *args):
        if args:
            self._default_validator = args[0]
            return None
        else:
            return self._default_validator

    def register_validator_with_source_type(self, source_type: type, target_type: type, validator: Validator):
        if target_type is None or source_type is None:
            raise TypeError("target_type or source_type is None")

        target_type, type_args = split_type(target_type)

        if source_type not in self._registry:
            self._registry[source_type] = IMP()

        if target_type not in self._registry[source_type]:
            self._registry[source_type][target_type] = {}

        self._registry[source_type][target_type][type_args] = ValidatorMetadata(
            validator=validator,
            target_type=target_type  # type: ignore
        )
        # 设置验证器信息：
        # validator 验证器函数
        # target_type 转换目标类型，validator 应严格返回这个类型的数据

    def register_validator_without_source_type(self, target_type: type, validator: Validator):
        target_type, type_args = split_type(target_type)

        if target_type not in self._validators_no_source_type:
            self._validators_no_source_type[target_type] = {}

        self._validators_no_source_type[target_type][type_args] = ValidatorMetadata(
            validator=validator,
            target_type=target_type
        )

    def register(self, source_type: type | None, target_type: type, validator: Validator) -> None:
        if target_type is None:
            raise ValueError(f"target_type cannot be None")

        if not inspect.isgeneratorfunction(validator):
            validator = wraps_as_generator_function(validator)

        if source_type is None:  # 针对特定目标类型的专用验证器
            return self.register_validator_without_source_type(target_type, validator)

        else:
            return self.register_validator_with_source_type(source_type, target_type, validator)

    def exists(self, source_type: type, target_type: type) -> bool:
        return source_type in self._registry and target_type in self._registry[
            source_type] or target_type in self._validators_no_source_type

    def get_validator_metadata[SourceType, TargetType](
            self, source_type: type[SourceType], target_type: type[TargetType], default=True
    ) -> ValidatorMetadata[SourceType, TargetType, Any]:
        # print('lasdjflkasdjf')
        tp, args = split_type(target_type)

        # 1. 尝试从有源类型的注册表中查找（带参数）
        result = (self._registry
                  .get(source_type, {})
                  .get(tp, {})
                  .get(args))

        # 2. 尝试从有源类型的注册表中查找（不带参数）
        if result is None:
            result = (self._registry
                      .get(source_type, {})
                      .get(tp, {})
                      .get(()))

        # 3. 尝试从无源类型的注册表中查找
        if result is None:
            # 先尝试带参数的查找
            no_source_dict = self._validators_no_source_type.get(tp, {})
            result = no_source_dict.get(args) or no_source_dict.get(())

        # result = (
        #         (_ := self._registry.get(source_type)) and (_ := _.get(tp)) and (_.get(args))
        # ) or (
        #
        # )

        if result is None:
            if default:
                result = ValidatorMetadata(self._default_validator, None)
                return result
            raise TypeError(f"No validators found for this type {target_type}")

        return result

    def get_validator(self, source_type: type, target_type: type) -> Validator:
        return self.get_validator_metadata(source_type, target_type).validator  # type: ignore

    def get_validator_metadata_allow_base_classes(self, st, tt):
        mro = tt.__mro__
        for cls in tt:
            try:
                return self.get_validator_metadata(st, cls)
            except TypeError:
                pass
        raise TypeError(f"No validators found for these types {mro}")

    def create_sub_registry(self):
        return SubTypeRegistry(self)

    def register_self_validating_type(self, typ: type | list[type]):
        if isinstance(typ, list):
            for i in typ:
                self.register_self_validating_type(i)

        self.register(
            None, typ,
            lambda data, target_type, subtypes: target_type(data)
        )
        return typ

    def list_validators(self):
        validators = []
        for source_type, target_types in self._registry.items():
            for target_type, subtypes in target_types.items():
                for subtype, metadata in subtypes.items():
                    validators.append((source_type, target_type, subtype, metadata.validator))
        for target_type, subtypes in self._validators_no_source_type.items():
            for subtype, metadata in subtypes.items():
                validators.append((None, target_type, subtype, metadata.validator))
        return validators

    # Decorators
    @overload
    def add_validator[FT, TT](self, *, from_: FT = None, to: TT) -> Callable[
        [Callable[[FT], TT]],
        Callable[[FT], TT]
    ]:
        ...

    @overload
    def add_validator[FT, TT](self, func: Callable[[FT], TT]) -> Callable[[FT], TT]:
        ...

    def add_validator(self, func=None, *, from_=None, to=None):
        def decorator(fnc):
            self.register(from_, to, fnc)
            return fnc

        return decorator if func is None else decorator(func)


class SubTypeRegistry(TypeRegistry):
    def __init__(self, parent: TypeRegistry):
        self.parent = parent
        super().__init__()

    def get_validator_metadata(self, source_type, target_type):
        try:
            return super().get_validator_metadata(source_type, target_type, default=False)
        except TypeError:
            try:
                return self.parent.get_validator_metadata(source_type, target_type)
            except TypeError:
                return super().get_validator_metadata(source_type, target_type)

    def exists(self, source_type, target_type) -> bool:
        return super().exists(source_type, target_type) or self.parent.exists(source_type, target_type)


def validate[T, R](type_registry: TypeRegistry, data: T, target_type: type[R]):
    stack: Stack[tuple[ValidatorMetadata, Generator]] = Stack()
    return_value = None

    def push_stack(data, target_type):
        validator_metadata = type_registry.get_validator_metadata(type(data), target_type)
        gen = validator_metadata.validator(data, get_origin(target_type), typing.get_args(target_type))
        stack.push(
            (
                validator_metadata,
                gen
            )
        )

    push_stack(data, target_type)

    while stack:
        validator_metadata, validator_generator = stack.top
        try:
            next_data, next_target_type = validator_generator.send(return_value)
            push_stack(next_data, next_target_type)
            return_value = None
        except StopIteration as e:
            return_value = e.value
            stack.pop()
        # except TypeError as e:
        #     ...

    return return_value
