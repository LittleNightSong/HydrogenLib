import re
import sys

from scripts.base import create_dir_by_struct, Project, console

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
name = "LittleNightSong"
email = "LittleNightSongYO@outlook.com"
[project.urls]
Documentation = "https://github.com/LittleNightSong/HydrogenLib#readme"
Issues = "https://github.com/LittleNightSong/HydrogenLib/issues"
Source = "https://github.com/LittleNightSong/HydrogenLib"

[tool.hatch.version]
path = "src/{package_name}/__about__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]

"""

name_matcher = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

if __name__ == '__main__':
    name = '-'.join(sys.argv[1:])
    project = Project()

    # Check the name
    if not name_matcher.match(name):
        raise ValueError("The given name is wrong.")

    if project.is_module(name):
        console.error(f"Module [bold]{name}[/bold] is already exists.")

    # Create the module
    module = project.get_module(name, check=False)
    import_name = module.import_name
    create_dir_by_struct(module.path, {
        'src': {
            import_name: {
                '__init__.py': None,
                '__about__.py': 'version = "0.0.1" '
            }
        },
        'README.md': None,
        'pyproject.toml': template.format(module_name=module.package_name, package_name=import_name),
    })
