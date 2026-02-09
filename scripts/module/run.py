import sys

from . import (
    ignore as libignore,
    build as libbuild,
    clear as libclear,
    info as libinfo,
    new as libnew,
    publish as libpublish
)

from scripts.commands import uvc, hatchc
from scripts.base import console


def main():
    opt_target = sys.argv[1]
    command = sys.argv[2]

    # sys.argv.pop(1)
    sys.argv.pop(2)

    console.info(f'Received command: {command}')
    console.info(f'Restructured `Argv`: {sys.argv[1:]}')  # 重组后的 argv

    match command:
        case 'build':
            libbuild.main()
        case 'clear':
            libclear.main()
        case 'info':
            libinfo.main()
        case 'new':
            libnew.main()
        case 'publish':
            # Publish 特殊处理
            argv_1 = f'{sys.argv[1]}=={sys.argv[2]}'
            sys.argv[1] = argv_1
            sys.argv.pop(2)
            libpublish.main()
        case 'ignore':
            libignore.main()
        case 'hatch':
            hatchc.hatch(*sys.argv[1:])
        case 'uv':
            uvc.uv(sys.argv[1:])
        case _:
            console.error(f"Unknown command {command}")


if __name__ == "__main__":
    main()
