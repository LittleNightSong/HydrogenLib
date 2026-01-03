from __future__ import annotations

import builtins
import tempfile
import typing
from pathlib import PurePosixPath, Path
from typing import Any

from . import Resource
from .base import ResourceProvider

if typing.TYPE_CHECKING:
    from ..system import CoreResourceSystem

import zipfile


class LocalResource(Resource):
    def __init__(self, local_path: str | Path):
        self.local_path = local_path

    def __fspath__(self) -> str:
        return str(self.local_path)


class URLProvider(ResourceProvider):
    def __init__(self, prefix):
        self.prefix = PurePosixPath(prefix)

    def fullpath(self, path):
        return self.prefix / path

    def get(self, path: PurePosixPath, query: dict[str, Any],
            resource_system: CoreResourceSystem) -> Resource | None:
        return resource_system.get(
            self.fullpath(path)
        )

    def list(self, path: PurePosixPath, query: dict[str, Any],
             resource_system: CoreResourceSystem) -> builtins.list:
        return resource_system.list(
            self.fullpath(path)
        )

    def set(self, path: PurePosixPath, data: Any, query: dict[str, Any],
            resource_system: CoreResourceSystem) -> None:
        resource_system.set(
            self.fullpath(path), data
        )

    def exists(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> bool:
        return resource_system.exists(
            self.fullpath(path)
        )

    def remove(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> bool:
        return resource_system.remove(
            self.fullpath(path)
        )


class FSProvider(ResourceProvider):
    # 拼接路径
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def fullpath(self, path):
        return self.root / str(path)[1:]
        # Fix: PurePosixPath 的根目录是 /，但是这样会导致拼接的时候被识别成盘符根目录
        # 比如 C:/xxx/xxx/xx + /resource 会变成 C:/resource

    def list(self, path: PurePosixPath, query: dict[str, Any],
             resource_system: CoreResourceSystem) -> builtins.list:
        return list(self.fullpath(path).iterdir())

    def get(self, path: PurePosixPath, query: dict[str, Any],
            resource_system: CoreResourceSystem) -> Resource | None:
        return LocalResource(
            self.fullpath(path)
        )

    def set(self, path: PurePosixPath, data: Any, query: dict[str, Any],
            resource_system: CoreResourceSystem) -> None:
        if isinstance(data, str):
            fmode = 'w'
        elif isinstance(data, bytes | memoryview | bytearray):
            fmode = 'wb'
        else:
            raise TypeError(f'unwritable data type: {type(data)!r}')
        f = open(self.fullpath(path), fmode)
        f.write(data)
        f.close()

    def exists(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> bool:
        return self.fullpath(path).exists()

    def remove(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem):
        self.fullpath(path).unlink()


class TempProvider(ResourceProvider):
    def __init__(self, suffix=None, prefix=None):
        self.temp_dir_manager = tempfile.TemporaryDirectory(suffix, prefix)
        self.temp_dir = Path(self.temp_dir_manager.name)

    def list(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> builtins.list:
        return []

    def get(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> Resource | None:
        return LocalResource(
            self.temp_dir / path
        )

    def set(self, path: PurePosixPath, data: Any, query: dict[str, Any], resource_system: CoreResourceSystem) -> None:
        raise NotImplementedError('Use the `get` function instead')

    def exists(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> bool:
        return (
                self.temp_dir / path
        ).exists()

    def remove(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem):
        (self.temp_dir / path).unlink()

    def close(self):
        self.temp_dir_manager.cleanup()
        self.temp_dir_manager = None

    def __del__(self):
        self.close()


class ZipResource(Resource):
    def __init__(self, zipio):
        self._io = zipio

    def release(self) -> None:
        self._io.close()

    def __fspath__(self):
        raise NotImplemented


class ZipProvider(ResourceProvider):
    def list(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> builtins.list:
        raise NotImplemented

    def get(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> Resource | None:
        pwd = query.get('pwd', None)
        return ZipResource(
            self._zip.open(str(path), force_zip64=True, pwd=pwd)
        )

    def set(self, path: PurePosixPath, data: Any, query: dict[str, Any], resource_system: CoreResourceSystem) -> None:
        raise NotImplemented

    def exists(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem) -> bool:
        raise NotImplemented

    def remove(self, path: PurePosixPath, query: dict[str, Any], resource_system: CoreResourceSystem):
        raise NotImplemented

    def __init__(self, file):
        self._zipfile = file
        self._zip = zipfile.ZipFile(file)

    def close(self):
        self._zip.close()
