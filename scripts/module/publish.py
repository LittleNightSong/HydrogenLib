import sys

import scripts.module.build as libbuild
from scripts.base import console, Module


def main():
    libbuild.main()

    modules = sys.argv[1:]
    for string in modules:
        name, ver = libbuild.parse_build_config(string)
        module = Module.find(name)
        with console.status("Publishing [bold]%s[/bold]" % name):
            if ver:
                module.publish(
                    f"*-{module.version}-*"
                )
            else:
                module.publish()


if __name__ == "__main__":
    main()
