import sys
import subprocess as sp
from scripts.base import console, Module


def main():
    module_name = sys.argv[1]
    module = Module.find(module_name)
    info = module.project_info

    try:
        version = module.version
    except sp.CalledProcessError as e:
        print(e.output.decode("utf-8"))
        version = 'unknown'
    console.print(
        f"""
Module [bold]{info.name}[/bold]

packages: {', '.join(info.packages)}
dependencies: {', '.join(info.dependencies)}
version: {version}
"""
    )


if __name__ == '__main__':
    main()
