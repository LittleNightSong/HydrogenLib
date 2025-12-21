import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run as _run

from scripts.base import reset_toml_infomation

threadpool = ThreadPoolExecutor(max_workers=128)


def get_package_name(project_name):
    return '_' + project_name.replace('-', '_').lower()


def run(*args, **kwargs):
    return _run(*args, **kwargs, encoding="utf-8")


def hatch_new(name):
    run(["hatch", "new", name])


def copy(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)


def refact_import(file):
    text = Path(file).read_text(encoding='utf-8')
    for match in re.findall(r'(\.*)(_hy\w+)', text):
        _, dots, name = match
        text = text.replace(f'{dots}{name}', f'{name}')

    Path(file).write_text(text)


def create_reimport(m, lib_dir):
    if m.name == 'hytools': return

    package_name = '_' + to_name(m.name)
    with open(lib_dir / (m.name.removeprefix('hy') + '.py'), 'w') as f:
        f.write(f'from {package_name} import *' '\n')


def to_name(name: str) -> str:
    return name.replace(' ', '_').replace('-', '_')


def main():
    cwd = Path.cwd()
    if cwd.name == 'scripts':
        cwd = cwd.parent

    src_dir = cwd / 'modules'
    lib_dir = cwd / 'hydrogenlib'

    modules = [i for i in src_dir.iterdir() if i.is_dir()]
    for m in modules:
        if m.name != 'tools':
            reset_toml_infomation(m / 'pyproject.toml', m)  # Job 1

        try:
            copy(m / 'src' / to_name(m.name), m / 'src' / ('_' + to_name(m.name)))  # Job 2
        except FileNotFoundError:
            print('Ignore module:', m.name)

        (m / 'LICENSE.txt').unlink(True)
        (m / 'README.md').write_text('')

        create_reimport(m, lib_dir)


if __name__ == '__main__':
    main()
    threadpool.shutdown()
