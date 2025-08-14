from __future__ import annotations

import typing
from typing import Callable


if typing.TYPE_CHECKING:
    from . import ConfigMeta

from .base import *

type ConfigMetaGenerator = Callable[[], ConfigMeta]


class HyConfig(AnnoationSupportContainerBase, nofields=True):
    __meta__: ConfigMeta
    __meta_generator__: ConfigMetaGenerator = None

    def __init__(self):
        if self.__meta_generator__:
            self.__meta__ = self.__meta_generator__()

        meta = get_meta(self)

        for field in self.__fields__.values():
            _ = field.get_field_by_obj(self)
            _.model = meta.model

    def load(self, filename=None, reuse=False):
        meta = get_meta(self)

        filename = filename or meta.file
        fp = meta.file_opener.open(filename, FileOpener.mode.load)
        data = meta.backend.load(fp)
        meta.model.init(data)

        if reuse:
            meta.file = filename

    def save(self, filename=None):
        meta = get_meta(self)

        filename = filename or meta.file

        if filename is None:
            raise ValueError("No filename specified")

        fp = meta.file_opener.open(filename, FileOpener.mode.save)
        meta.backend.dump(fp, meta.model)

