import sys

from scripts.base import console, Module


def main():
    module_name = sys.argv[1]
    module = Module.find(module_name)
    info = module.project_info

    console.print(
        f"""
Module [bold]{info.name}[/bold]

packages: {', '.join(info.packages)}
dependencies: {', '.join(info.dependencies)}
version: {module.version()}
"""
    )


if __name__ == '__main__':
    main()
