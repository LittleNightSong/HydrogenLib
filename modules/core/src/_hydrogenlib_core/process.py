import time
from typing import Any, Optional, Union

import psutil


class Process(psutil.Process):
    def runtime(self):
        return time.time() - self.create_time()

    def as_dict(self, attrs: Union[list[str], tuple[str, ...], set[str], frozenset[str], None] = (),
                ad_value: Any = None):
        dct = super(Process, self).as_dict(attrs, ad_value=ad_value)
        dct["runtime"] = self.runtime()
        return dct

    def pause(self):
        self.suspend()

    def recover(self):
        self.resume()

    def exitcode(self) -> Optional[int]:
        return self.wait()


class ProcessInfo:
    def __init__(self, ps: Process):
        self._dict = ps.as_dict()

    def name(self):
        return self._dict["name"]

    @property
    def pid(self):
        return self._dict["pid"]

    def pwd(self):
        return self._dict["pwd"]

    def exe(self):
        return self._dict["exe"]

    def create_time(self):
        return self._dict["create_time"]

    def runtime(self):
        return self._dict["runtime"]

    def status(self):
        return self._dict["status"]

    def environ(self):
        return self._dict["environ"]

    def cmdline(self):
        return self._dict["cmdline"]

    def username(self):
        return self._dict["username"]

    def open_files(self):
        return self._dict["open_files"]

    def threads(self):
        return self._dict["threads"]

    @property
    def ppid(self):
        return self._dict["ppid"]

    def num_threads(self):
        return self._dict["num_threads"]

    def __str__(self):
        return f"name:{self.name()}\n" \
               f"pid:{self.pid}\n" \
               f"pwd:{self.pwd()}\n" \
               f"exe:{self.exe()}\n" \
               f"create_time:{self.create_time()}\n" \
               f"runtime:{self.runtime()}\n" \
               f"status:{self.status()}\n"

    def __repr__(self):
        return f"name:{self.name()}\n" \
               f"pid:{self.pid}\n" \
               f"pwd:{self.pwd()}\n" \
               f"exe:{self.exe()}\n" \
               f"create_time:{self.create_time()}\n" \
               f"runtime:{self.runtime()}\n" \
               f"status:{self.status()}\n"


def sys_process() -> list[Process]:
    """
    return Process()
    """
    p = Any
    process_list = []
    for p in psutil.process_iter():
        try:
            process_list.append(Process(p.pid),)
        except psutil.NoSuchProcess:
            continue

    return process_list


def find_processes(name):
    p = sys_process()
    results = []
    for i in p:
        if i.name() == name:
            results.append(i)
    return results


def kill_process_by_name(process_name):
    ps_list = find_processes(process_name)
    for i in ps_list:
        try:
            i.terminate()
        except psutil.NoSuchProcess:
            continue


def kill_process_by_pid(pid: int):
    if pid in psutil.pids():
        try:
            ps = psutil.Process(pid)
            ps.terminate()
        except psutil.NoSuchProcess:
            raise psutil.NoSuchProcess(pid, None, "process no longer exists")


def to_info(ps: tuple[Process, ...]):
    process_info_list = []
    for i in ps:
        o = ProcessInfo(i)
        process_info_list.append(o)
    return process_info_list


