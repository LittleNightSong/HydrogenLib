from __future__ import annotations

import hashlib
from pathlib import Path

from _hydrogenlib_core.hash import get_hash_func_by_method
from _hydrogenlib_core.utils import lazy_property
from _hydrogenlib_httpcache.cache_info import CacheInfo


class _CacheFiles:
    index: Path
    content: Path
    hash: str

    __slots__ = ('_url', '_lihf', '_cd')

    def __init__(self, cache_directory: CacheDirectory, url, lihf=None):
        self._url = url
        self._lihf = lihf or hashlib.sha256
        self._cd = cache_directory

    @lazy_property
    def hash(self):
        return self._lihf(self._url).hexdigest()

    @lazy_property
    def index(self) -> Path:
        return self._cd.indexdir / self.hash

    @lazy_property
    def content(self):
        return self._cd.filedir / self.hash

    @property
    def url(self):
        return self._url

    @lazy_property
    def cacheinfo(self):
        with open(self.index, 'r') as fp:
            return CacheInfo.load(fp)


class CacheDirectory:
    def __init__(self, tempdir, indexdir=None, filedir=None, index_hash_method='sha256'):
        self.tempdir = Path(tempdir)
        self.indexdir = indexdir or self.tempdir / 'index'
        self.filedir = filedir or tempdir / 'files'

        self.tempdir.mkdir(parents=True, exist_ok=True)
        self.indexdir.mkdir(parents=True, exist_ok=True)
        self.filedir.mkdir(parents=True, exist_ok=True)

        self._lihm = index_hash_method
        self._lihf = get_hash_func_by_method(index_hash_method)

    @property
    def index_hash_method(self):
        return self._lihm

    @index_hash_method.setter
    def index_hash_method(self, value):
        if value == self._lihm:
            return

        self._lihm = value
        self._lihf = get_hash_func_by_method(value)

    def calc_hash(self, string):
        return self._lihf(string)

    def get_cache_info(self, url):
        hash_v = self.calc_hash(url)

