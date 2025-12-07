import subprocess
import sys

import rich

from scripts.base import convert_to_module_name, convert_to_package_name, find_project_dir, find_module
from pathlib import Path
from scripts import uvc


def main():
    module_name = sys.argv[1].lower()
    project_dir = find_project_dir()
    module = find_module(module_name, project_dir)
    if not module:
        rich.print("[red]Error: module not found[/red]")
        exit(1)
    try:
        subprocess.call([uvc.uvexec, 'build'], cwd=module)
    except Exception as e:
        rich.print(e)
        rich.print("[red]Error: build failed[/red]")
        exit(1)


if __name__ == "__main__":
    main()

