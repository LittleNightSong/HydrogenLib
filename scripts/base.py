from collections import deque
from pathlib import Path
import tomlkit


def reset_toml_infomation(file, m: Path):
    with open(file, "r") as f:
        data = f.read().replace('\\h', '/h')

    toml = tomlkit.loads(data)  # type: tomlkit.TOMLDocument
    project = toml['project']

    # reset Name
    project['name'] = project_name  = "HydrogenLib-" + m.name.title()

    # reset authors
    project['authors'] = [{'name': 'LittleSong2025', 'email': 'LittleSong2024@outlook.com'}]

    if 'license' in project:
        del project['license']

    # reset Urls
    urls = project['urls']
    urls['Documentation'] = \
        "https://github.com/LittleSong2025/HydrogenLib#readme"
    urls['Issues'] = "https://github.com/LittleSong2025/HydrogenLib/issues"
    urls['Source'] = "https://github.com/LittleSong2025/HydrogenLib"

    # reset Version
    hatch = toml['tool']['hatch']
    package_path = Path('src') / convert_to_package_name(project_name)
    hatch['version']['path'] = str(package_path / '__about__.py').replace('\\', '/')

    # reset Packages
    hatch['build'] = {
        "targets": {
            'wheel': {
                "packages": [str(package_path).replace('\\', '/')]
            }
        }
    }

    # reset require-python
    project['requires-python'] = ">=3.12"  # 因为使用了 3.12 的类型注解语法

    # reset classifiers
    project['classifiers'] = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]

    with open(file, "w") as f:
        tomlkit.dump(toml, f)


def unlink_with_glob(path: Path, pattern, rglob=False):
    for file in path.glob(pattern) if not rglob else path.rglob(pattern):
        file.unlink()


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


def convert_to_package_name(name: str):
    name = name.lower().replace('-', '_')
    return name


def convert_to_module_name(name: str):
    if not name.startswith('HydrogenLib-'):
        name = "HydrogenLib-" + name

    return name.title()
