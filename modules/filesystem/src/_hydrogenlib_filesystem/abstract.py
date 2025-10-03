from abc import ABC, abstractmethod
from io import IOBase
from pathlib import Path
from typing import Generator
import dataclasses


class Permission(int):
    def has_read(self):
        return self & 4

    def has_write(self):
        return self & 2

    def has_execute(self):
        return self & 1

    def has_all(self):
        return self & 7


@dataclasses.dataclass
class FSAttrs:
    mode: Permission = 0
    size: int = 0
    atime: float = 0
    mtime: float = 0
    ctime: float = 0
    uid: int = 0
    gid: int = 0
    dev: int = 0
    ino: int = 0
    nlink: int = 0
    rdev: int = 0
    block_size: int = 0
    blocks: int = 0
    is_dir: bool = False
    is_file: bool = False
    is_symlink: bool = False


class AbstractFileSystem(ABC):
    root = '/'

    @abstractmethod
    def mkfile(self, file) -> None: ...

    @abstractmethod
    def mkdirs(self, path) -> None: ...

    @abstractmethod
    def remove(self, file) -> None: ...

    @abstractmethod
    def rmdir(self, path): ...

    @abstractmethod
    def rmdirs(self, path): ...

    @abstractmethod
    def open(self, file, mode, encoding=None) -> IOBase: ...

    @abstractmethod
    def iterdir(self, path) -> Generator[FSInfo, None, None]: ...

    @abstractmethod
    def close(self): ...

    @abstractmethod
    def exists(self, path): ...


class AbstractFSNode(ABC):
    children: dict[str, 'AbstractFSNode']
    parent: 'AbstractFSNode'
    root: AbstractFileSystem
    path: Path
    name: str

    def __init__(self, name, root=None, parent: 'AbstractFSNode' = None):
        self.name = name
        self.root = root
        self.parent = parent

        if parent:
            self.path = parent.path / self.name

    @property
    @abstractmethod
    def attrs(self) -> FSAttrs:
        ...

    def on_create(self):
        ...

    def on_delete(self):
        ...

    def add_child(self, node: 'AbstractFSNode'):
        self.children[node.name] = node

    def remove_child(self, name_or_node):
        if isinstance(name := name_or_node, str):
            self.children.pop(name)

        elif isinstance(node := name_or_node, AbstractFSNode):
            self.children.pop(node.name)

    def get_child(self, name):
        return self.children.get(name)

    def has_child(self, name):
        return name in self.children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        yield from self.children.values()

    def __getitem__(self, name):
        return self.children[name]

    def __setitem__(self, name, node):
        self.children[name] = node
