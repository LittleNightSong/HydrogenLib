import os.path
import pathlib
import urllib.parse
from os import PathLike
from urllib.parse import urlencode

import fs.opener.parse

from . import HRSCore
import dataclasses
from _hydrogenlib_core.typefunc import iter_attributes


class Resources:
    __mounttab__ = None
    def __init_subclass__(cls, **kwargs):
        # 收集挂载信息
        if cls.__mounttab__ is None:
            cls.__mounttab__ = HRSCore.MountTab()

        for name, value in iter_attributes(cls):
            if isinstance(value, HRSCore.MountBase):
                cls.__mounttab__.mount(name+':', value)

    @classmethod
    def mounttab(cls):
        return cls.__mounttab__


class ResourceSystemBase:
    Resources: type[Resources] = None

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls.Resources, 'mounttab') or not callable(cls.Resources.mounttab):
            raise TypeError(f"{cls.Resources} don't have 'mounttab'.")

    @classmethod
    def mounttab(cls) -> HRSCore.MountTab:
        return cls.Resources.mounttab()

    def mount(self, name: str, uri: str):
        # res = fs.opener.parse(uri)
        # path = res.resource
        self._rs.mount(name + ':', fs.open_fs(uri))

    def auto_mount(self):
        mtb = self.mounttab()
        name: str
        mtinfo: HRSCore.MountBase
        for name, mtinfo in mtb.mounts:
            if isinstance(mtinfo, HRSCore.RMount):
                path = fs.opener.parse(mtinfo.uri).resource
                uri = pathlib.PurePosixPath(self.appdir).joinpath(path).__str__()
                mtinfo = HRSCore.Mount(uri, mtinfo.mount_point)
            self.mount(name, mtinfo.uri)

    def __init__(self, appdir: PathLike[str], appname: str, appauchor:str = 'unknown'):
        if not os.path.isabs(appdir):
            appdir = os.path.abspath(appdir)

        if not os.path.exists(appdir):
            raise FileNotFoundError(f"Cannot find appdir {appdir}")

        self._rs = HRSCore.ResourceSystem()

        self.appdir = urllib.parse.quote(str(appdir))
        self.appname = appname
        self.appauchor = appauchor
        # 挂载虚拟资源系统目录
        print(f"osfs://{str(self.appdir)}")
        self.mount('app', f"osfs://{self.appdir}")
        self.auto_mount()

