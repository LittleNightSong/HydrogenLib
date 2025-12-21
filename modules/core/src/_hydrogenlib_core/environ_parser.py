import os
from typing import Union, Any, Callable, Iterable
from functools import lru_cache

from contextlib import contextmanager

from .typefunc import get_type_name

os_envsep = ':'

if os.name == 'nt':
    os_envsep = ';'


class EnvironmentVariable:
    def __init__(self, name, value, sep=os_envsep, on_change: Callable[[Any, Any], None] = None):
        self._name = name
        self._value = value
        self._ls = None
        self._sep = sep
        self._on_change = on_change

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: str | Iterable):
        old = self.value
        if not isinstance(v, str):
            v = self._sep.join(map(str, v))

        self._value = v

        if self._on_change:
            self._on_change(old, v)

        self._ls = None

    def list(self, sep=os_envsep):
        if self._ls is None:
            self._ls = self.value.split(sep=sep)
        return self._ls


class Environment:
    def __init__(self, dct=None, sep=os_envsep):
        self._environ = dct or os.environ

        self.sep = sep

    def set(self, name, value: str | Iterable, sep=os_envsep):
        if isinstance(value, str):
            self._environ[name] = value
        else:
            self._environ[name] = sep.join(map(str, value))

    def get(self, name):
        return EnvironmentVariable(name, self._environ[name], self.sep, lambda old, new: self.set(name, new))

    def get_copy(self, name):
        return EnvironmentVariable(name, self._environ, self.sep)

    def keys(self):
        return self._environ.keys()

    def __getitem__(self, item):
        return self._environ[item]


def update_environ(env: Environment):
    os.environ.update(dict(env))


def clear_environ():
    os.environ.clear()


def set_environ(env: Environment):
    clear_environ()
    update_environ(env)


@contextmanager
def environ(env: Environment):
    old_env = Environment()
    update_environ(env)
    yield
    update_environ(old_env)
