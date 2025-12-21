from pathlib import Path
from ..cache_info import CacheInfo, CacheControlFlags


class IndexDir:
    def __init__(self, path):
        self.path = Path(path)

    def get_cache_info(self, hash_value):
        if not (self.path / hash_value).exists():
            return None

        else:
            with (self.path / hash_value).open() as fp:
                return CacheInfo.load(fp)