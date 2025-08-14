import json
import typing

from .base import *


class Model(AbstractModel):
    def __init__(self):
        self._data = {}

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value

    def exists(self, key):
        return key in self._data

    def init(self, data):
        self._data = dict(data)

    def as_dict(self) -> dict:
        return self._data


class JsonBackend(AbstractBackend):
    def load(self, fp: typing.IO) -> typing.Any:
        try:
            return json.load(fp)
        except json.JSONDecodeError:
            return {}

    def dump(self, fp: typing.IO, obj: typing.Any) -> None:
        json.dump(obj, fp, default=self.my_serialize)

    def my_serialize(self, obj):
        if isinstance(obj, AbstractModel):
            return obj.as_dict()
        return obj


def config_validate(name: str):
    def decorator(func):
        return validator_mark(func, name)

    return decorator
