import shutil
import sys

import scripts.base

console = scripts.base.Console()


def main():
    modules = sys.argv[1:]
    for m in modules:
        module = scripts.base.find_module(m)
        if not module:
            console.error(f"Could not find module: {m}")
        shutil.rmtree(module / 'dist', ignore_errors=True)


if __name__ == "__main__":
    main()
