import asyncio
import contextlib


# 使用 asyncio 的功能尽可能复现 trio 的功能


class Cancelled(BaseException): ...


class Nursery:
    def __init__(self):
        self.tasks = set()  # type: set[asyncio.Task]

    async def _wrapper(self, coro):
        await coro
        task = asyncio.current_task()
        if task is not None:
            self.tasks.remove(task)

    async def start_soon(self, coro):
        task = asyncio.create_task(self._wrapper(coro))
        self.tasks.add(task)
        return task

    async def cancel(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def wait(self):
        await asyncio.gather(*self.tasks)

    def __await__(self):
        return self.wait().__await__()


@contextlib.asynccontextmanager
async def create_nursery():
    nursery = Nursery()
    try:
        yield nursery
        await nursery
    except Exception as e:
        await nursery.cancel()
        raise e


class CancelScope:
    def __init__(self, timeout=None):
        self.timeout = timeout
        self.tasks = []
        self._cancelled = False

    def _clean(self, task):
        self.tasks.remove(task)

    async def __aenter__(self):
        if self.timeout:
            self._timeout_task = asyncio.create_task(self._timeout_handler())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, '_timeout_task'):
            self._timeout_task.cancel()

        if exc_type == asyncio.CancelledError:
            return True
        return None

    async def _timeout_handler(self):
        await asyncio.sleep(self.timeout)
        await self.cancel()

    async def cancel(self):
        for t in self.tasks:
            if not t.done():
                t.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

    def spawn(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        task.add_done_callback(self._clean)
        return task

    def cancelled_caught(self):
        return self._cancelled


