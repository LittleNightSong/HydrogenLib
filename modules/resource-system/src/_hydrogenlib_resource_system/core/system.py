from pathlib import PurePosixPath
from typing import NamedTuple, Any

from . import errors
from .hrl import parse_hrl, HRLInfo
from .provider import ResourceProvider
from .provider.builtin_providers import HRLProvider


class MountInfo(NamedTuple):
    path: PurePosixPath
    provider: ResourceProvider
    source: Any

    def get(self, path, query, rs):
        return self.provider.get(self.source, path, query, rs)

    def remove(self, path, query, rs):
        return self.provider.remove(self.source, path, query, rs)

    def list(self, path, query, rs):
        return self.provider.list(self.source, path, query, rs)

    def set(self, path, data, query, rs):
        return self.provider.set(self.source, path, data, query, rs)

    def exists(self, path, query, rs):
        return self.provider.exists(self.source, path, query, rs)


class ResourceSystem:

    def __init__(self):
        self._mounttab = {}  # type: dict[str, list[MountInfo]]

    def mount(self, prefix: str, source, provider: ResourceProvider | type[ResourceProvider] = HRLProvider):
        hrlinfo = parse_hrl(prefix)
        scheme, path = hrlinfo.scheme, hrlinfo.path

        if scheme not in self._mounttab:
            self._mounttab[scheme] = []

        if isinstance(provider, type):
            provider = provider()

        self._mounttab[scheme].append(MountInfo(path, provider, source))

    def find_mount(self, hrl: str) -> tuple[MountInfo | None, HRLInfo]:
        hrlinfo = parse_hrl(hrl)
        scheme, path = hrlinfo.scheme, hrlinfo.path

        if scheme in self._mounttab:
            for mountinfo in self._mounttab[scheme]:
                mpath = mountinfo.path
                if mpath.is_relative_to(path):
                    return mountinfo, hrlinfo

        return None, hrlinfo

    def get_mount(self, hrl: str) -> tuple[MountInfo, HRLInfo]:
        minfo, hrlinfo = self.find_mount(hrl)
        if minfo is None:
            raise errors.ResourceNotFound(hrl)
        return minfo, hrlinfo

    def get(self, hrl: str, **kwargs):
        minfo, hrlinfo = self.get_mount(hrl)
        return minfo.get(hrlinfo.path, kwargs, self)

    def remove(self, hrl: str, **kwargs):
        minfo, hrlinfo = self.get_mount(hrl)
        return minfo.remove(hrlinfo.path, kwargs, self)
    
    def set(self, hrl: str, data, **kwargs):
        minfo, hrlinfo = self.get_mount(hrl)
        return minfo.set(hrlinfo.path, data, kwargs, self)

    def list(self, hrl: str, **kwargs):
        minfo, hrlinfo = self.get_mount(hrl)
        return minfo.list(hrlinfo.path, kwargs, self)

    def exists(self, hrl: str, **kwargs):
        minfo, hrlinfo = self.get_mount(hrl)
        return minfo.exists(hrlinfo.path, kwargs, self)
