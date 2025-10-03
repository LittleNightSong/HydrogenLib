import os
import pathlib

from .path import *


def open_folder(path):
    path = pathlib.Path(path)
    if path.exists():
        folder, file = path.parent, path.name
        os.system(f'explorer.exe /select, "{folder}\\{file}"')

    else:
        raise FileNotFoundError(path)



