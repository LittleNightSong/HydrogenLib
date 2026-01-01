import contextlib
import sys
from collections import deque
from pathlib import Path
from typing import Iterable

import rich.traceback
from rich import print


# def reset_toml_infomation(file, m: Path):
#     with open(file, "r") as f:
#         data = f.read().replace('\\h', '/h')
#
#     toml = tomlkit.loads(data)  # type: tomlkit.TOMLDocument
#     project = toml['project']
#
#     # reset Name
#     project['name'] = project_name  = "HydrogenLib-" + m.name.title()
#
#     # reset authors
#     project['authors'] = [{'name': 'LittleSong2025', 'email': 'LittleSong2024@outlook.com'}]
#
#     if 'license' in project:
#         del project['license']
#
#     # reset Urls
#     urls = project['urls']
#     urls['Documentation'] = \
#         "https://github.com/LittleSong2025/HydrogenLib#readme"
#     urls['Issues'] = "https://github.com/LittleSong2025/HydrogenLib/issues"
#     urls['Source'] = "https://github.com/LittleSong2025/HydrogenLib"
#
#     # reset Version
#     hatch = toml['tool']['hatch']
#     package_path = Path('src') / convert_to_package_name(project_name)
#     hatch['version']['path'] = str(package_path / '__about__.py').replace('\\', '/')
#
#     # reset Packages
#     hatch['build'] = {
#         "targets": {
#             'wheel': {
#                 "packages": [str(package_path).replace('\\', '/')]
#             }
#         }
#     }
#
#     # reset require-python
#     project['requires-python'] = ">=3.12"  # 因为使用了 3.12 的类型注解语法
#
#     # reset classifiers
#     project['classifiers'] = [
#         "Development Status :: 3 - Alpha",
#         "Programming Language :: Python",
#         "Programming Language :: Python :: 3.11",
#         "Programming Language :: Python :: 3.12",
#         "Programming Language :: Python :: 3.13",
#         "Programming Language :: Python :: Implementation :: CPython",
#         "Programming Language :: Python :: Implementation :: PyPy",
#     ]
#
#     with open(file, "w") as f:
#         tomlkit.dump(toml, f)


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
    name = name.lower().replace(' ', '-').replace('-', '_')
    return name


def convert_to_module_name(name: str):
    if not name.startswith('HydrogenLib-'):
        name = "HydrogenLib-" + name

    return name.title()


project_dir = None


def find_project_dir(start_dir: Path | None = None) -> Path | None:
    global project_dir

    if project_dir is not None:
        return project_dir

    start_dir = start_dir or Path.cwd()

    while start_dir.name != 'HydrogenLib':
        last_dir = start_dir
        start_dir = start_dir.parent

        if last_dir == start_dir:
            return None

    project_dir = start_dir
    return project_dir


def clear_runtime_cache():
    global project_dir
    project_dir = None


def find_module(mname: str, project_dir: Path | None = None) -> Path | None:
    project_dir = project_dir or find_project_dir()
    modules = project_dir / 'modules'
    module = modules / mname

    if module.exists():
        return module
    else:
        return None

def iter_modules(project_dir: Path | None = None) -> Iterable[Path]:
    if project_dir is None:
        project_dir = find_project_dir()

    modules = project_dir / 'modules'
    return filter(
        lambda m: (m.is_dir() and (m / 'pyproject.toml').exists()),
        modules.iterdir()
    )


class Console:
    _instance: 'Console' = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def error(self, *msg, exit=1):
        print('[red]Error:[/red]', *msg, file=sys.stderr)

        if exit is not None:
            sys.exit(exit)

    def info(self, *msg):
        print('[green]Info:[/green]', *msg, file=sys.stderr)

    @contextlib.contextmanager
    def status(self, msg, exit=1, print_reason=True, print_traceback=False):
        try:
            print(msg, '...', file=sys.stderr, end='')
            yield
            print('[green]Success![/green]')
        except Exception as e:
            print("[red][bold]Failed![/bold][/red]", end='')
            if print_reason:
                print(f'    [red]{e.__class__.__name__}: {e}[/red]', sep='')
            if print_traceback:
                print()
                print(
                    rich.traceback.Traceback.extract(type(e), e, e.__traceback__)
                )
            if exit:
                sys.exit(exit)
            print()

    def print(self, *args, **kwargs):
        return print(*args, **kwargs)


console = Console()
