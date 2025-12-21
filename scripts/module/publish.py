import sys

import scripts.base
import scripts.commands.uvc as uvc
import scripts.module.build as libbuild

console = scripts.base.Console()


def main():
    libbuild.main()

    modules = sys.argv[1:]
    for mname in modules:
        module, ver = libbuild.parse_build_config(mname)
        uvc.publish(module)


if __name__ == "__main__":
    main()
