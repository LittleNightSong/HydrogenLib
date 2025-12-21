import inspect
import os

import psutil

from .process import Process

if os.name == 'nt':
    def shutdown(mode: str, time: int = 1):
        if time < 1:
            time = 1
        return os.system(f'shutdown -{mode} -t {time}')


class Runtime:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._process = Process(os.getpid())

    @property
    def pid(self):
        return self._process.pid

    def cpu_count(self):
        return os.cpu_count()

    def num_threads(self):
        return self._process.num_threads()

    def cpu_percent(self):
        return self._process.cpu_percent()

    def memory_percent(self):
        return self._process.memory_percent()

    def memory_info(self):
        return self._process.memory_info()

    def memory_full_info(self):
        return self._process.memory_full_info()

    def kill(self):
        self._process.kill()

    def exit(self, code):
        exit(code)

    def environ(self):
        return self._process.environ()

    def cmdline(self):
        return self._process.cmdline()

    def exec(self, command):
        return psutil.Popen(command)

    def execute(self, command):
        return Process(psutil.Popen(command).pid)

