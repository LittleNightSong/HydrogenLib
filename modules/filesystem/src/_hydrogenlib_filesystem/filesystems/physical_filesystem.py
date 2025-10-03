from io import IOBase
from typing import Generator, Any, IO

from ..abstract import AbstractFileSystem
from pathlib import Path
from shutil import rmtree


# 物理文件系统
class PhysicalFileSystem(AbstractFileSystem):
    def __init__(self, root_path):
        self.root = Path(root_path).absolute()

    def mkfile(self, file) -> None:
        open(self.root / file, 'wx').close()
        # 设置 x 模式，如果文件已存在则报错

    def mkdirs(self, path) -> None:
        (self.root / path).mkdir(parents=True, exist_ok=True)

    def remove(self, file) -> None:
        (self.root / file).unlink()

    def rmdir(self, path):
        (self.root / path).rmdir()

    def rmdirs(self, path):
        rmtree(self.root / path)

    def open(self, file, mode='r', encoding=None) -> IO[Any]:
        return open(self.root / file, mode, encoding=encoding)

    def iterdir(self, path) -> Generator[Path, None, None]:
        for path in (self.root / path).iterdir():
            yield path.relative_to(self.root)

    def close(self):
        pass  # 物理文件系统没什么需要关闭的
