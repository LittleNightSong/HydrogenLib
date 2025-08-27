from typing import Callable, Any

from _hycore.utils import InstanceMapping

type Validator = Callable[[Any], Any]


class TypeRegistry[_TS, _TT=_TS]:
    def __init__(self, mro=None):
        self._mro = mro or InstanceMapping()  # type: InstanceMapping[type[_TS], InstanceMapping[type[_TT], Validator]]

    def validate(self, data: object, target: type[_TT]):
        sources = type(data).__mro__
        for source in sources:
            if self.exists(source, target):
                return self.get(source, target)(data)
        raise TypeError(f'{type(data)} cannot be cast to {target}')

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
