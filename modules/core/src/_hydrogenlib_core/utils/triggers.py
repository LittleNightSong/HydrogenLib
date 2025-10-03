import asyncio
from typing import Callable
from threading import Lock


class SignalInstance:
    def __init__(self):
        self.hooks = []
        self._lck = Lock()

    def connect(self, func):
        # with self._lck:
        self.hooks.append(func)

    def disconnect(self, func):
        # with self._lck:
        self.hooks.remove(func)

    def clear(self):
        # with self._lck:
        self.hooks.clear()

    def emit(self, *args, **kwargs):
        with self._lck:
            for hook in self.hooks.copy():  # Copy保证线程安全
                hook(*args, **kwargs)


class Signal:
    _instance_to_signal = {}

    def __get_signal(self, instance):
        key = id(instance)
        if key not in self._instance_to_signal:
            signal = SignalInstance()
            self._instance_to_signal[key] = signal
        return self._instance_to_signal[key]

    def __get__(self, instance, owner):
        if isinstance is None:
            return self
        return self.__get_signal(instance)

    def __delete__(self, instance):
        self._instance_to_signal.clear()

    def __init__(self):
        self._instance_to_signal = {}


class Hook:
    def __init__(self, func):
        self._pre = []
        self._fc = func
        self._post = []

    def pre(self, func):
        self._pre.append(func)

    def post(self, func):
        self._post.append(func)

    def get(self, name) -> list[Callable]:
        if name == 'pre':
            return self._pre
        elif name == 'post':
            return self._post
        else:
            raise ValueError('name must be "pre" or "post"')

    def __call__(self, *args, **kwargs):
        for func in self._pre:
            func(*args, **kwargs)
        Res = self._fc(*args, **kwargs)
        for func in self._post:
            func(Res, *args, **kwargs)  # 添加返回值


class AsyncHook:
    def __init__(self, func, loop=None):
        self._fc = func
        self.loop = loop or asyncio.get_running_loop()

        self._pre = []
        self._post = []

    async def __call__(self, *args, **kwargs):
        for func in self._pre:
            await func(*args, **kwargs)
        res = await self._fc(*args, **kwargs)
        for func in self._post:
            await func(res, *args, **kwargs)  # 添加返回值

    def pre(self, func):
        self._pre.append(func)

    def post(self, func):
        self._post.append(func)

