import dataclasses
import os
import subprocess as sp
import sys

from packaging.version import Version
from rich import print

from scripts.commands import hatchc, uvc
from scripts.base import find_project_dir, find_module, Console


@dataclasses.dataclass
class BuildConfig:
    name: str
    version: str | None | Version
    path: os.PathLike[str]


def parse_build_config(arg: str):
    if "==" in arg:
        name, ver = arg.split("==")
        return name.lower(), Version(ver)

    else:
        return arg.lower(), None


def main():
    builds = sys.argv[1::]
    console = Console()
    project_dir = find_project_dir()

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

        if ver:
            try:
                current_ver = hatchc.get_version(module)
                if ver not in {"patch", 'major', 'minor'}:

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


        print(f'( {name} )\t\t[bold]Building...[/bold]')
        try:
            uvc.build(module)
            print(f"( {name} )\t\t[green]Build successful[/green]")
        except sp.CalledProcessError as e:
            print(f"( {name} )\t\t[red]Error: build failed[/red]")
            exit(1)


if __name__ == "__main__":
    main()
