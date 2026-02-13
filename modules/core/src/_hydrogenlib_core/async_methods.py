import asyncio
from functools import partial

from .threading_methods import run_new_thread


def run_in_new_loop(coro):
    loop = asyncio.new_event_loop()
    return loop, loop.run_until_complete(coro)


def run_in_existing_loop(coro, loop: asyncio.AbstractEventLoop):
    return loop.run_until_complete(coro)


def new_event_loop():
    return asyncio.new_event_loop()


async def to_coro(func, *args, **kwargs):
    return func(*args, **kwargs)


class FutureFunction:
    def __init__(self, func, *args, **kwargs):
        self._partial = partial(func, *args, **kwargs)
        self._future = asyncio.Future()

    def __call__(self, *args, **kwargs):
        self._future.set_result(self._partial(*args, **kwargs))

    @property
    def done(self):
        return self._future.done()

    @property
    def result(self):
        return self._future.result()

    def __await__(self):
        return self._future.__await__()


def wrap(func, *args, **kwargs):
    return FutureFunction(func, *args, **kwargs)


class ProtectedTask:
    """
    受保护的任务对象,保证线程安全
    """

    def __init__(self, task, loop):
        self._loop: asyncio.AbstractEventLoop = loop
        self._task: asyncio.Task = task

    def done(self):
        return self._task.done()

    def cancel(self):
        self._loop.call_soon_threadsafe(self._task.cancel)

    def result(self):
        return self._task.result()


class ThreadEventLoop:
    """
    独立运行的事件循环,保证线程安全
    """

    def __init__(self):
        self._thread = None
        self._loop: asyncio.AbstractEventLoop = None

    def __run_threadsafe(self, func, *args, **kwargs):
        wraped_func = wrap(func, *args, **kwargs)
        self._loop.call_soon_threadsafe(wraped_func)
        return wraped_func.result

    def __thread_main(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def start(self, loop=None):
        self._loop = loop or new_event_loop()
        self._thread = run_new_thread(self.__thread_main)

    def is_running(self):
        return self._loop.is_running()

    def create_task(self, coro):
        task = self.__run_threadsafe(self._loop.create_task, coro)
        return ProtectedTask(self._loop, task)

    def run_until_complete(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def run_coroutine(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    def all_task(self):
        return asyncio.all_tasks(self._loop)

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()
