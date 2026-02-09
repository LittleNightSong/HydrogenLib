import pathlib

from .module import Module


def is_project_dir(directory):
    p = pathlib.Path(directory)

    return (
            p.is_dir() and
            (p / 'pyproject.toml').exists() and
            (p / 'modules').is_dir() and
            (p / 'hydrogenlib').is_dir()
    )


class Project:
    _instance = None
    path: pathlib.Path

    def __new__(cls, path=None):
        if cls._instance is None:
            if path is None:
                cls._instance = cls.find()
            else:
                cls._instance = super().__new__(cls)
                cls._instance.path = pathlib.Path(path)

        return cls._instance

    def __init__(self, path=None):
        ...

    def __fspath__(self):
        return str(self.path)

    @classmethod
    def find(cls, path=None):
        if cls._instance is not None:
            return cls._instance

        current_dir = pathlib.Path(path) if path else pathlib.Path().cwd()

        cnt = 0
        while not is_project_dir(current_dir):
            print(current_dir)
            current_dir = current_dir.parent
            cnt += 1
            if cnt > 1000:
                raise RuntimeError("Project not found")

        project_dir = current_dir
        return cls(project_dir)

    def find_module(self, name: str, check=True, allow_ignored_modules: bool = False):
        module_dir = (self.path / 'modules' / name)

        if (not allow_ignored_modules) and (module_dir / '.hydro-ignore').exists():
            raise FileNotFoundError(f"Module {name} is ignored")

        if check:
            self.check_module(name)

        return Module(module_dir)

    def iter_modules(self, allow_ignored_modules: bool = False):
        for module_dir in (self.path / 'modules').iterdir():
            if (not allow_ignored_modules) and (module_dir / '.hydro-ignore').exists():
                continue

            if module_dir.is_dir():
                yield Module(module_dir)

    def check_module(self, name):
        module_dir = (self.path / 'modules' / name)
        if not module_dir.exists():
            raise FileNotFoundError(f"Module {name} not found in {self.path}")

        if not module_dir.is_dir():
            raise NotADirectoryError(f"Find {name}, but it is not a module")

        if (module_dir / '.hydro-ignore').exists():
            raise ValueError(f"Module {name} is ignored")

    def is_module(self, name):
        module_dir = (self.path / 'modules' / name)
        return (
            module_dir.is_dir()
        )

