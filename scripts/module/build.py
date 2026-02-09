import dataclasses
import os
import re
import sys

from packaging.version import Version

from scripts.base import Project, console, Module

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
        if current_ver > ver:
            raise RuntimeError(f"Module [bold]{name}[/bold]: You cannot be downgraded")
    module.version = ver


def main():
    project = Project.find()

    builds = sys.argv[1:]
    # builds = []
    # dependencies = []
    #
    # for i in range(len(sys.argv[1:])):
    #     _s = sys.argv[i + 1]
    #
    #     if _s == '-d' or _s == '--dependencies':
    #         break
    #
    #     builds.append(_s)
    #
    # dependencies.extend(sys.argv[i + 1:])

    vaild_modules = []

    for s in builds:
        name, ver = parse_build_config(s)
        module = project.find_module(name)
        vaild_modules.append((module, ver))
        console.info(f'Get module [bold]{name}[/bold] (now {module.version})')

    for module, ver in vaild_modules:
        if ver:
            with console.status(f'Update version for [bold]{module.name}[/bold]'):
                reset_version(module, ver)
            console.print(f'Module {module.name} is {module.version}')

        # if dependencies:
        #     current_dependencies = module.project_info.dependencies
        #     for dep in dependencies:
        #         dep_module = re.match('[a-zA-Z0-9]+', dep)
        #         if not dep_module:
        #             raise RuntimeError(f'Invalid module name [bold]{dep}[/bold]')

        with console.status(f'Build [bold]{module.name}[/bold]'):
            module.build()


if __name__ == "__main__":
    main()
