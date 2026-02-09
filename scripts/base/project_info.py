from __future__ import annotations

import dataclasses
import tomllib

import tomlkit


@dataclasses.dataclass
class ProjectInfo:
    name: str
    require_python: str
    keywords: list[str]
    authors: list[dict]
    dependencies: list[str]
    packages: list[str]

    @classmethod
    def load(cls, file) -> ProjectInfo:
        with open(file, 'rb') as f:
            toml = tomllib.load(f)
            project = toml['project']
            return cls(
                name=project['name'],
                keywords=project['keywords'],
                require_python=project['requires-python'],
                authors=project['authors'],
                dependencies=project['dependencies'],
                packages=toml['tool']['hatch']['build']['targets']['wheel']['packages']
            )

    def dump(self, file) -> None:
        with open(file, 'r+') as f:
            data = tomlkit.load(f)
            data['project'] = self.to_dict()
            f.truncate(0)
            tomlkit.dump(data, f)

    def to_dict(self):
        dct = dataclasses.asdict(self)
        dct['requires-python'] = self.require_python
        del dct['require_python']
        return dct
