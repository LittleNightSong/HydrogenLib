from pathlib import Path


def copy_directory_tree(src, dst):
    src = Path(src)
    dst = Path(dst)
    for root, dirs, files in src.walk():
        root = Path(root)
        for directory in dirs:
            (dst / root.relative_to(src) / directory).mkdir(parents=True, exist_ok=True)
