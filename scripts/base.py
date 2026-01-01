import contextlib
import dataclasses
import sys
import tomllib
from collections import deque
from pathlib import Path
from typing import Iterable

import rich.traceback
from rich import print


@dataclasses.dataclass
class ProjectInfo:
    name: str
    require_python: str
    keywords: list[str]
    authors: list[dict]
    dependencies: list[str]
    packages: list[str]


class Module:
    def __init__(self, module_path):
        self.module_path = module_path

    def __fspath__(self):
        return str(self.module_path)

    def get_version(self):
        import scripts.commands.hatchc
        return scripts.commands.hatchc.get_version(self)

    def set_version(self, version):
        import scripts.commands.hatchc
        return scripts.commands.hatchc.set_version(self, version)

    def project_info(self):
        with open(Path(self) / 'pyproject.toml', 'rb') as f:
            toml = tomllib.load(f)
            project = toml['project']
            return ProjectInfo(
                name=project['name'],
                keywords=project['keywords'],
                require_python=project['requires-python'],
                authors=project['authors'],
                dependencies=project['dependencies'],
                packages=toml['tool']['hatch']['build']['targets']['wheel']['packages']
            )

    @classmethod
    def find(cls, name, project_dir=None):
        return cls(find_module(name, project_dir))


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
