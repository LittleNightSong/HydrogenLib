from pathlib import Path

from scripts.commands import hatchc, uvc
from . import convert_to_import_name
from .base import convert_to_package_name
from .project_info import ProjectInfo


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
        return Project().find_module(name)

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
    def project_info(self) -> ProjectInfo:
        return ProjectInfo.load(self.path / 'pyproject.toml')

    @project_info.setter
    def project_info(self, v):
        v.dump(self.path / 'pyproject.toml')

    @property
    def package_name(self):
        return convert_to_package_name(self.name)

    @property
    def import_name(self):
        return convert_to_import_name(self.name)

    @property
    def files(self):
        return ModuleFiles(self.path)
