from _hydrogenlib_core.utils import InstanceMapping


class SyncResourceContextManager:
    def __init__(self, lock, data=None):
        self._lock = lock
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()


class SyncResource:
    def __init__(self, lock):
        self._data = InstanceMapping()
        self._lock = lock

    def __get__(self, instance, owner) -> SyncResourceContextManager:
        if instance not in self._data:
            self._data[instance] = SyncResourceContextManager(self._lock)

        return self._data[instance]
