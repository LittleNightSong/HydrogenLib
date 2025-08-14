from __future__ import annotations
import dataclasses as dc
import typing

if typing.TYPE_CHECKING:
    from _hyconfig import AbstractModel, AbstractBackend, FileOpener, HyConfig


@dc.dataclass
class ConfigMeta:
    model: AbstractModel = None
    backend: AbstractBackend = None
    file_opener: FileOpener = None
    file: str = None


def get_meta(obj: HyConfig) -> ConfigMeta | None:
    return getattr(obj, '__meta__', None)


def get_model(obj: HyConfig) -> AbstractModel:
    return get_meta(obj).model


def get_backend(obj: HyConfig) -> AbstractBackend:
    return get_meta(obj).backend


def get_file_opener(obj: HyConfig) -> FileOpener:
    return get_meta(obj).file_opener


def get_file(obj: HyConfig) -> str:
    return get_meta(obj).file
