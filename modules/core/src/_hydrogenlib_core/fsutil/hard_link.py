from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .copy import copy_directory_tree


def _hard_link(src, dst):
    Path(src).hardlink_to(dst)


def hard_link(src, dst, concurrently=False, max_workers=None):
    copy_directory_tree(src, dst)
    if concurrently:
        pool = ThreadPoolExecutor(max_workers=max_workers)
        pool.map(_hard_link, src.rglob("*"), dst.rglob("*"))
    else:
        for src_file, dst_file in zip(src.rglob("*"), dst.rglob("*")):
            _hard_link(src_file, dst_file)
