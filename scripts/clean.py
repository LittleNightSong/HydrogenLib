import shutil

from scripts.base import *


def main():
    for module in iter_modules():
        with console.status(f'( {module.name} ) Removing dist folder', exit=False):
            shutil.rmtree(module / 'dist')


if __name__ == '__main__':
    main()
