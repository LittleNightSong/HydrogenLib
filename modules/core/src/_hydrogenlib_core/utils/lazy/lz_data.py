from typing import Callable


class LazyData[T, **P]:
    """
    Call me when you need to load data.
    """
    def __init__(self, loader: Callable[P, T]):
        self._loader = loader
        self._is_set = False
        self._cache = None

    @property
    def loader(self):
        return self._loader

    @loader.setter
    def loader(self, v):
        if callable(v):
            self._loader = v

    def __call__(self, *args, **kwargs):
        if self._is_set:
            return self._cache

        self._cache = self._loader(*args, **kwargs)
        self._is_set = True

        return self._cache
