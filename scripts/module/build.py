import dataclasses
import os
import subprocess as sp
import sys

from packaging.version import Version
from rich import print

from scripts.base import find_module, console, project_dir
from scripts.commands import hatchc, uvc

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


def reset_version(ver, module, name):
    if ver:
        try:
            current_ver = hatchc.get_version(module)
            if ver not in special_version_strings:
                if current_ver == ver:
                    console.info(f"Module [bold]{name}[/bold] is [green]up-to-date[/green]")
                elif current_ver < ver:
                    hatchc.set_version(module, str(ver))
                    console.info(f"Module [bold]{name}[/bold] is [green]{ver}[/green]")
                else:
                    console.error(f"Module [bold]{name}[/bold] is not [red]up-to-date[red]")
            else:
                hatchc.set_version(module, str(ver))
                console.info(f"Module [bold]{name}[/bold] is [green]{ver}[/green]")
        except sp.CalledProcessError as e:
            console.error("[red]Cannot set info successfully[/red]")


def main():
    builds = sys.argv[1::]

    vaild_modules = []

    for build_string in builds:
        module_name, module_version = parse_build_config(build_string)

        module = find_module(module_name, project_dir)
        if module is None:
            console.error('Module', module_name, "not found")
        else:
            print(f"Found module [bold]{module_name}[/bold]")
            vaild_modules.append(
                BuildConfig(
                    module_name, module_version, module
                )
            )

    for bc in vaild_modules:
        name, ver, module = bc.name, bc.version, bc.path
        reset_version(ver, module, name)
        with console.status(f'Building [bold]{name}[/bold]'):
            uvc.build(module)


if __name__ == "__main__":
    main()
