import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from subprocess import run as _run

import tomlkit

threadpool = ThreadPoolExecutor(max_workers=128)


def get_package_name(project_name):
    return '_' + project_name.replace('-', '_').lower()


def reset_toml_infomation(file, m: Path):
    if m.name == 'hytools': return

    with open(file, "r") as f:
        data = f.read().replace('\\h', '/h')

    toml = tomlkit.loads(data)  # type: tomlkit.TOMLDocument

    project = toml['project']

    # reset Name
    project['name'] = project_name  = "HydrogenLib-" + m.name.title()

    # reset authors
    project['authors'] = [{'name': 'LittleSong2025', 'email': 'LittleSong2024@outlook.com'}]

    if 'license' in project:
        del project['license']

    # reset Urls
    urls = project['urls']
    urls['Documentation'] = \
        "https://github.com/LittleSong2025/HydrogenLib#readme"
    urls['Issues'] = "https://github.com/LittleSong2025/HydrogenLib/issues"
    urls['Source'] = "https://github.com/LittleSong2025/HydrogenLib"

    # reset Version
    hatch = toml['tool']['hatch']
    package_path = Path('src') / get_package_name(project_name)
    hatch['version']['path'] = str(package_path / '__about__.py').replace('\\', '/')

    # reset Packages
    hatch['build'] = {
        "targets": {
            'wheel': {
                "packages": [str(package_path).replace('\\', '/')]
            }
        }
    }

    # reset require-python
    project['requires-python'] = ">=3.12"  # 因为使用了 3.12 的类型注解语法

    # reset classifiers
    project['classifiers'] = [
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]

    with open(file, "w") as f:
        tomlkit.dump(toml, f)


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
