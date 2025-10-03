from threading import Thread as _Thread
from weakref import WeakValueDictionary as weakdict
from _hydrogenlib_core.typefunc import alias


thread_mapping = weakdict()  # type: weakdict[int, 'HyThread']


def register(thread):
    thread_mapping[thread.ident] = thread


def unregister(thread):
    del thread_mapping[thread.ident]


class ThreadWorker:
    def run(self):
        ...

    def stop(self):
        ...

    def start(self):
        ...


class FuncWorker(ThreadWorker):
    def __init__(self, func, args=(), kwargs=None):
        kwargs = kwargs or {}

        self._func, self._args, self._kwargs = func, args, kwargs

    def run(self):
        self._func(*self._args, **self._kwargs)


class HyThread(_Thread):
    worker: ThreadWorker

    worker = alias['_worker']

    def __init__(self, worker):
        super().__init__()
        self._worker = worker

    def start(self):
        self._worker.start()
        super().start()
        register(self)

    def run(self):
        self._worker.run()
        unregister(self)

    def stop(self):
        self._worker.stop()

