import pathlib

from . import convert_to_package_name
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

    @classmethod
    def find(cls, path=None):
        if cls._instance is not None:
            return cls._instance

        current_dir = pathlib.Path(path) if path else pathlib.Path().cwd()

        while not is_project_dir(current_dir):
            current_dir = current_dir.parent
            if current_dir.root == current_dir:
                raise FileNotFoundError("Cannot find project ")

        project_dir = current_dir
        return cls(project_dir)

    def get_module(self, name: str, check=True):
        module_dir = (self.path / name)

        if check:
            self.is_module(name)

        return Module(module_dir)

    def iter_modules(self):
        for module_dir in (self.path / 'modules').iterdir():
            if module_dir.is_dir():
                yield Module(module_dir)

    def is_module(self, name):
        module_dir = (self.path / 'modules' / name)
        if not module_dir.exists():
            raise FileNotFoundError(f"Module {name} not found in {self.path}")

        if not module_dir.is_dir():
            raise NotADirectoryError(f"Find {name}, but it is not a module")

