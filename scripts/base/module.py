import dataclasses
import tomllib
from pathlib import Path

from scripts.commands import hatchc, uvc
from . import convert_to_import_name
from .base import convert_to_package_name


@dataclasses.dataclass
class ProjectInfo:
    name: str
    require_python: str
    keywords: list[str]
    authors: list[dict]
    dependencies: list[str]
    packages: list[str]


class ModuleFiles:
    pyproject: Path
    readme: Path
    src: Path

    def __init__(self, module_path):
        self.path = Path(module_path)

    @property
    def pyproject(self):
        return self.path / 'pyproject.toml'

    @property
    def readme(self):
        return self.path / 'README.md'

    @property
    def src(self):
        return self.path / 'src'


class Module:
    def __init__(self, module_path):
        self.path = module_path

    def __fspath__(self):
        return str(self.path)

    def build(self):
        uvc.build(self)

    def publish(self, pattern=None):
        if pattern is None:
            uvc.publish(self)
        else:
            uvc.publish(
                self, dist_dir="./dist/" + pattern
            )

    @classmethod
    def find(cls, name: str):
        from .project import Project
        return Project().get_module(name)

    @property
    def version(self):
        return hatchc.get_version(self)

    @version.setter
    def version(self, version):
        hatchc.set_version(self, version)

    @property
    def name(self):
        return self.path.name

    @property
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

    @property
    def package_name(self):
        return convert_to_package_name(self.name)

    @property
    def import_name(self):
        return convert_to_import_name(self.name)

    @property
    def files(self):
        return ModuleFiles(self.path)
