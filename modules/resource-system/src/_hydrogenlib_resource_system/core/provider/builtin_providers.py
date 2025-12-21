import builtins
from pathlib import PurePosixPath, Path
from typing import Any

from . import Resource
from .base import ResourceProvider
from ..system import ResourceSystem


class HRLProvider(ResourceProvider):
    def get(self, source, path: PurePosixPath, query: dict[str, Any],
            resource_system: ResourceSystem) -> Resource | None:
        source = PurePosixPath(source)
        return resource_system.get(
            str(source / path)
        )

    def list(self, source, path: PurePosixPath, query: dict[str, Any],
             resource_system: ResourceSystem) -> builtins.list:
        source = PurePosixPath(source)
        return resource_system.list(
            str(source / path)
        )

    def set(self, source, path: PurePosixPath, data: Any, query: dict[str, Any],
            resource_system: ResourceSystem) -> None:
        source = PurePosixPath(source)
        resource_system.set(
            str(source / path), data
        )

    def exists(self, source, path: PurePosixPath, query: dict[str, Any], resource_system: ResourceSystem) -> bool:
        source = PurePosixPath(source)
        return resource_system.exists(
            str(source / path)
        )

    def remove(self, source, path: PurePosixPath, query: dict[str, Any], resource_system: ResourceSystem) -> bool:
        source = PurePosixPath(source)
        return resource_system.remove(
            str(source / path)
        )


class FSProvider(ResourceProvider):
    # 拼接路径
    def fullpath(self, source, path: PurePosixPath):
        return Path(source) / path

    def list(self, source, path: PurePosixPath, query: dict[str, Any],
             resource_system: ResourceSystem) -> builtins.list:
        return list(self.fullpath(source, path).iterdir())

    def get(self, source, path: PurePosixPath, query: dict[str, Any],
            resource_system: ResourceSystem) -> Resource | None:
        pass

    def set(self, source, path: PurePosixPath, data: Any, query: dict[str, Any],
            resource_system: ResourceSystem) -> None:
        pass

    def exists(self, source, path: PurePosixPath, query: dict[str, Any], resource_system: ResourceSystem) -> bool:
        pass

    def remove(self, source, path: PurePosixPath, query: dict[str, Any], resource_system: ResourceSystem) -> bool:
        pass