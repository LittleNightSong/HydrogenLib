import sys

import scripts.base
import scripts.module.build as libbuild
import scripts.commands.uvc as uvc

console = scripts.base.Console()

def main():
    libbuild.main()

    modules = sys.argv[1:]
    for mname in modules:
        module, ver = libbuild.parse_build_config(mname)
        uvc.publish(module)