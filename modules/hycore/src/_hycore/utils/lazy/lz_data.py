from typing import Callable


class LazyData:
    def __init__(self, callable: Callable, *args, **kwargs):
        self._callable = callable
        self._is_set = False
        self._args = args
        self._kwargs = kwargs
        self._cache = None

    def update_callable(self, callable: Callable):
        self._callable = callable

    @property
    def value(self):
        return self.get()

    def get(self, *args, **kwargs):
        if self._is_set:
            return self._cache

        if len(args) == 0 and len(kwargs) == 0:
            args = self._args
            kwargs = self._kwargs

        self._cache = self._callable(*args, **kwargs)
        self._is_set = True

        return self._cache

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)
