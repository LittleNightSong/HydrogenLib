from __future__ import annotations

import dataclasses
from io import BytesIO, StringIO
from pathlib import Path
from os import PathLike
from collections import deque


@dataclasses.dataclass
class FileMeta:
    """
    文件元数据
    """
    name: str | None = None
    pre_alloc_size: int = 0
    mode: int = 0o666
    exists_ok: bool = True
    content: str | bytes | memoryview | bytearray = None


def _create_file(file: Path, meta: FileMeta):
    file.touch(exist_ok=meta.exists_ok, mode=meta.mode)
    if meta.content:
        with open(file, 'w' if isinstance(meta.content, str) else 'wb') as f:
            f.write(meta.content)

    if meta.pre_alloc_size:
        with open(file, 'a') as f:
            f.truncate(meta.pre_alloc_size)


type TreeDict = dict[str, TreeDict | set[str | FileMeta] | str | bytes | int | None]


def create_tree_from_dict(root: PathLike[str], dct, default_mode=0o666, default_exists_ok=True):
    """
    从一个嵌套字典中创建目录树

    字典中的键将作为文件/目录名

    不同值的类型会影响函数的行为：
        - `str`: 文件内容（text）
        - `bytes | bytearray | memoryview`: 文件内容（bin）
        - `int`: 文件模式
        - `FileMeta`: 文件的基本数据由 FileMeta 提供


    :param root: 创建目录树的根位置
    :param dct: 目录树结构
    :param default_mode: 默认创建文件时的模式
    :param default_exists_ok: 默认处理存在文件的方式
    :return:
    """
    root = Path(root)
    stack = deque([(root, dct)])  # type: deque[tuple[Path, dict]]
    while stack:
        root, dct = stack.popleft()
        root.mkdir(exist_ok=True, parents=True)
        for k, v in dct.items():
            if isinstance(v, dict):
                stack.append((root / k, v))
                continue
            if isinstance(v, set):
                (root / k).mkdir(exist_ok=True, parents=True)
                for file in v:
                    if isinstance(file, FileMeta):
                        _create_file(root / k / file.name, file)
                continue
            if v:
                if isinstance(v, FileMeta):
                    _create_file(root / k, v)
                elif isinstance(v, str):
                    (root / k).write_text(v)
                elif isinstance(v, (bytes, bytearray, memoryview)):
                    (root / k).write_bytes(v)
                elif isinstance(v, int):
                    (root / k).touch(exist_ok=default_exists_ok, mode=v)
                else:
                    raise TypeError(f'Invalid type: {type(v)}')
            else:
                (root / k).touch(exist_ok=default_exists_ok, mode=default_mode)
