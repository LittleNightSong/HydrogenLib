from threading import Thread as _Thread
from weakref import WeakValueDictionary as weakdict
from _hydrogenlib_core.typefunc import alias


thread_mapping = weakdict()  # type: weakdict[int, 'Thread']


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


class Thread:
    worker: ThreadWorker

    ident: int = alias['ident']

    @property
    def worker(self):
        return self._worker

    @worker.setter
    def worker(self, v):
        if self.lived:
            raise RuntimeError('Thread is still running')
        self._worker = v

    def __init__(self, worker):
        self._thread = None
        self._worker = worker

    def start(self):
        self._worker.start()
        self._thread = _Thread(target=self.run)
        self._thread.start()
        register(self)

    def run(self):
        self._worker.run()
        unregister(self)

    def stop(self):
        self._worker.stop()
        self._thread = None

    def join(self, timeout=None):
        self._thread.join(timeout)

    @property
    def lived(self):
        return self._thread.is_alive()

