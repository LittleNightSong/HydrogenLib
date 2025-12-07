import dataclasses
import datetime
import os
from os import PathLike

from _hydrogenlib_core.typefunc import AutoSlots
from _hydrogenlib_core.utils import lazy_property


@dataclasses.dataclass
class FileStatusResult(AutoSlots):
    mode: int
    ino: int
    dev: int
    nlink: int
    uid: int
    gid: int
    size: int
    last_access: datetime.datetime
    last_modify: datetime.datetime
    ctime: datetime.datetime

    @property
    def last_metadata_modified(self) -> datetime.datetime:
        return self.ctime

    @property
    def create_time(self) -> datetime.datetime:
        return self.ctime

    def __post_init__(self):
        fromtimestamp = datetime.datetime.fromtimestamp
        self.last_access = fromtimestamp(self.last_access)
        self.last_modify = fromtimestamp(self.last_modify)
        self.ctime = fromtimestamp(self.ctime)


class File(AutoSlots):
    _path: PathLike[str]
    _stat: FileStatusResult

    def __fspath__(self):
        return self._path

    def __init__(self, path: PathLike[str]):
        self._path = path
        self._stat = FileStatusResult(*os.stat(self._path))

    @property
    def stat(self):
        return self._stat

    @property
    def size(self) -> int:
        return self.stat.size

    @property
    def mode(self):
        return self.stat.mode

    def open(self, *args, **kwargs):
        return open(self._path, *args, **kwargs)
