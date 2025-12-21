from pathlib import Path
import hashlib
from _hydrogenlib_core.hash import get_hash_func_by_method, calc_hash_by_method


class CacheControl:
    def __init__(self, tempdir, indexdir=None, filedir=None, local_index_hashmethod='sha256'):
        self.tempdir = Path(tempdir)
        self.indexdir = indexdir or self.tempdir / 'index'
        self.filedir = filedir or tempdir / 'files'

        self.tempdir.mkdir(parents=True, exist_ok=True)
        self.indexdir.mkdir(parents=True, exist_ok=True)
        self.filedir.mkdir(parents=True, exist_ok=True)

        self._lihm = local_index_hashmethod
        self._lihf = get_hash_func_by_method(local_index_hashmethod)

    @property
    def local_index_hash_method(self):
        return self._lihm

    @local_index_hash_method.setter
    def local_index_hash_method(self, value):
        if value == self._lihm:
            return

        self._lihm = value
        self._lihf = get_hash_func_by_method(value)

    def calc_hash(self, string):
        return self._lihf(string)

    def get_cache_control_headers(self, url):
        url = str(url).encode()
        hash_ = self.calc_hash(url)

