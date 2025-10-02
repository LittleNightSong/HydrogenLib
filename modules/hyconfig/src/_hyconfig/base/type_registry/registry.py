from typing import Callable, Any, Iterable

from _hycore.utils import InstanceMapping

type Validator[F=Any, T=Any] = Callable[[F], T]  # From To
type Enumerator[T=Any, V=Any] = Callable[[T], Iterable[V]]


class TypeRegistry[_TS, _TT=_TS]:
    def __init__(self, mro=None):
        # 基本类型映射
        self._mro = mro or InstanceMapping()  # type: InstanceMapping[type[_TS], InstanceMapping[type[_TT], Validator]]
        # 容器类型枚举器映射
        self._container_mro = InstanceMapping()  # type: InstanceMapping[type[_TS], InstanceMapping[type[_TT], Enumerator]]

    def validate(self, data: object, target: type[_TT]):
        return self.validator(type(data), target)(data)

    def validator(self, source, target):
        sources = source.__mro__
        for source in sources:
            if source in self._mro:
                if target in self._mro[source]:
                    return self._mro[source][target]

        raise TypeError(f'{source} cannot be cast to {target}')

    def register(self, source: type[_TS], target: type[_TT], method: Validator):
        if source not in self._mro:
            self._mro[source] = InstanceMapping()

        self._mro[source][target] = method

    def get(self, source: type[_TS], target: type[_TT]) -> Validator:
        if not self.exists(source, target):
            raise TypeError(f'{source} does not have a validator for {target}')

        return self._mro[source][target]

    def unregister(self, source: type[_TS], target: type[_TT]):
        if not self.exists(source, target):
            raise TypeError(f'{source} does not have a validator for {target}')
        del self._mro[source][target]

    def exists(self, source: type[_TS], target: type[_TT]):
        return source in self._mro and target in self._mro[source]

    def __getitem__(self, item: tuple[type[_TS], type[_TT]]):
        return self.get(*item)

    def __setitem__(self, key: tuple[type[_TS], type[_TT]], value: Validator):
        self.register(*key, value)

    def __delitem__(self, key: tuple[type[_TS], type[_TT]]):
        self.unregister(*key)

    def __contains__(self, item: tuple[type[_TS], type[_TT]]):
        return self.exists(*item)
