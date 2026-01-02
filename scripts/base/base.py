from collections import deque
from pathlib import Path


def create_dir_by_struct(root: Path, dct: dict[str, dict | str | None]):
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
                for f in v:
                    (root / k / f).touch()
                continue
            (root / k).touch()
            if v:
                (root / k).write_text(v)


def convert_to_import_name(name: str):
    name = name.lower().replace(' ', '-').replace('-', '_')
    name = "_hydrogenlib_" + name
    return name


def convert_to_package_name(name: str):
    if not name.startswith('HydrogenLib-'):
        name = "HydrogenLib-" + name

    return name.title()


