import threading
import time


class TimedData:
    def __init__(self, data, timeout=60, set_time=True, check_time=True, timeout_delete=True):

        self.data = data
        self.time = None
        self._timeout = timeout

        if set_time:
            self.time = time.time()

        self.set_time = set_time
        self.check_time = check_time
        self.timeout_delete = timeout_delete

        self._is_timeout = False  # 缓存

    @property
    def is_timeout(self):
        return self.check()

    @property
    def remain(self):
        if self.check():
            return 0
        return self._timeout - (time.time() - self.time)

    def delete(self):
        """
        Deletes the data.
        """
        if self.data is not None:
            del self.data
            self.data = None

    def _check(self):
        if self.time is None or self.check_time is False:
            # If the time is not set, or if the check is disabled, return True.
            return False

        if time.time() - self.time > self._timeout:
            if self.timeout_delete:
                self.delete()

            return True

        return False

    def check(self):
        if self._is_timeout:
            return self._is_timeout
        self._is_timeout = self._check()
        return self._is_timeout

    def __get__(self, instance, owner):
        if self.check():
            return self.data
        else:
            raise TimeoutError("TimedData has timed out.")


class TimedDataManager:
    def __init__(self, timeout=60):
        self.timeout = timeout
        self.data = {}  # type: dict[str, TimedData]

        self._lock = threading.Lock()

    def check(self, key):
        return self.data[key].check()

    def delete(self, key):
        if self.exists(key):
            self.data[key].delete()
            del self.data[key]

    def delete_threadsafe(self, key):
        with self._lock:
            self.delete(key)

    def delete_multiple(self, keys):
        for key in keys:
            self.delete(key)

    def delete_multiple_threadsafe(self, keys):
        with self._lock:
            self.delete_multiple(keys)

    def extend(self, dic):
        for key, value in dic._instances():
            self.add(key, value)

    def extend_threadsafe(self, dic):
        with self._lock:
            self.extend(dic)

    def get_multiple(self, keys):
        return {key: self.get_data(key) for key in keys if self.exists(key)}

    def get_multiple_threadsafe(self, keys):
        with self._lock:
            return self.get_multiple(keys)

    def add(self, key, value, timeout=None):
        self.data[key] = TimedData(value, timeout=timeout or self.timeout)

    def get(self, key):
        return self.get_data(key).data

    def add_data(self, key, data):
        self.data[key] = data

    def get_data(self, key):
        if not self.check(key):
            return self.data[key]
        else:
            del self.data[key]

    def add_threadsafe(self, key, value, timeout=None):
        with self._lock:
            self.add(key, value, timeout=timeout)

    def get_threadsafe(self, key):
        with self._lock:
            return self.get(key)

    def add_data_threadsafe(self, key, data):
        with self._lock:
            self.add_data(key, data)

    def exists(self, key):
        return key in self.data and not self.check(key)

    def clear(self):
        self.data.clear()

    def clean_up(self):
        results = set()
        for key in filter(self.check, self.data.keys()):
            results.add(key)

        self.delete_multiple_threadsafe(results)
