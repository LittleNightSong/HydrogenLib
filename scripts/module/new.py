import re
import sys
from pathlib import Path

from scripts.base import create_dir_by_struct, convert_to_package_name, convert_to_module_name, find_project_dir

template = """
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{module_name}"
dynamic = ["version"]
description = ''
readme = "README.md"
requires-python = ">=3.12"
keywords = []
classifiers = ["Development Status :: 3 - Alpha", "Programming Language :: Python", "Programming Language :: Python :: 3.11", "Programming Language :: Python :: 3.12", "Programming Language :: Python :: 3.13", "Programming Language :: Python :: Implementation :: CPython", "Programming Language :: Python :: Implementation :: PyPy"]
dependencies = []

[[project.authors]]
name = "LittleSong2025"
email = "LittleSong2024@outlook.com"
[project.urls]
Documentation = "https://github.com/LittleSong2025/HydrogenLib#readme"
Issues = "https://github.com/LittleSong2025/HydrogenLib/issues"
Source = "https://github.com/LittleSong2025/HydrogenLib"

[tool.hatch.version]
path = "src/{package_name}/__about__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]

"""

name_matcher = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

if __name__ == '__main__':
    name = '-'.join(sys.argv[1:])
    project_dir = find_project_dir()

    modules = project_dir / 'modules'

    # Check the name
    if not name_matcher.match(name):
        raise ValueError("The given name is wrong.")

    # Create the project
    new_project_dir = modules / name
    full_pkgname = '_hydrogenlib_' + convert_to_package_name(name)
    create_dir_by_struct(new_project_dir, {
            'src': {
                full_pkgname: {
                    '__init__.py': None,
                    '__about__.py': 'version = "0.0.1" '
                }
            },
            'README.md': None,
            'pyproject.toml': None,
    })

    # Clean
    with open(new_project_dir / 'pyproject.toml', 'r+') as f:
        f.write(
            template.format(module_name=convert_to_module_name(name), package_name=full_pkgname)
        )
