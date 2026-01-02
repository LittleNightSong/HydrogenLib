import dataclasses
import os
import subprocess as sp
import sys

from packaging.version import Version

from scripts.base import Project, console, Module
from scripts.commands import hatchc

special_version_strings = {"patch", 'major', 'minor'}


@dataclasses.dataclass
class BuildConfig:
    name: str
    version: str | None | Version
    path: os.PathLike[str]


def parse_build_config(arg: str):
    if "==" in arg:
        name, ver = arg.split("==")
        if ver in special_version_strings:
            return name.lower(), ver

        return name.lower(), Version(ver)

    else:
        return arg.lower(), None


def reset_version(module: Module, ver: str):
    name = module.name
    current_ver = module.version
    if ver not in special_version_strings:
        if current_ver == ver:
            console.print(f"Module [bold]{name}[/bold] is [green]up-to-date[/green]")
        elif current_ver < ver:
            module.version = ver
            console.print(f"Module [bold]{name}[/bold] is [green]{hatchc.get_version(module)}[/green]")
        else:
            console.error(f"Module [bold]{name}[/bold]: You cannot be downgraded")
    else:
        module.version = ver
        console.info(f"Module [bold]{name}[/bold] is [green]{ver}[/green]")


def main():
    project = Project.find()

    builds = sys.argv[1::]

    vaild_modules = []

    for build_string in builds:
        name, ver = parse_build_config(build_string)
        module = project.get_module(name)
        vaild_modules.append((module, ver))

    for module, ver in vaild_modules:
        if ver:
            reset_version(module, ver)

        with console.status(f'Building [bold]{module.name}[/bold]'):
            module.build()


if __name__ == "__main__":
    main()
