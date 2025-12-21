import concurrent.futures
import importlib.util
import re
import subprocess as sp
import sys
import threading
import time
import tomllib
from pathlib import Path

from packaging.version import Version, InvalidVersion
from rich import print

kwpair_parser = re.compile(r"([\w_]+)=(.+)")


def get_kwpair(string):
    match = kwpair_parser.match(string)
    if match:
        try:
            v = Version(match.group(2))
        except InvalidVersion:
            v = match.group(2)
        return match.group(1), v
    return None


def load_file(path, name=None):
    if name is None:
        name = get_name()

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name}(One attribute is None)")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_name():
    return str(time.time_ns())


root = Path.cwd()
modules_dir = root / 'modules'


class Module:
    @property
    def version(self):
        return Version(self.about.version)

    @property
    def name(self):
        return self.root.name

    def __init__(self, root: Path):
        self.root = root
        self.about = None

    def load(self):
        # [tool.hatch.version]
        # path = "src/_hycore/__about__.py"
        pyproject = tomllib.loads((self.root / 'pyproject.toml').read_text())
        about_file = self.root / pyproject['tool']['hatch']['version']['path']
        self.about = load_file(about_file)

    def is_higher_than(self, other_version: Version | str):
        other_version = Version(other_version)
        return self.version > other_version


def publish(m):
    sp.run(
        [
            'uv',
            'publish',
            'dist/*',
            '--trusted-publishing', 'automatic',
        ], cwd=m.root, check=True,
    )


def build(module: Module, version=None):
    if version:
        sp.run(
            [
                'hatch',
                'version',
                str(version)
            ],
            cwd=module.root, stdout=sp.PIPE, stderr=sp.PIPE
        )
    sp.run(
        [
            'uv',
            'build',
            '--no-build-isolation'
        ],
        cwd=module.root, check=True,
        # stdout=sp.PIPE, stderr=sp.PIPE
    )


lock = threading.Lock()


def main_build(module, versions):
    try:
        build(module, versions.get(module.name))
        print(f'[green]B[/green]uild module {module.name} successcls')
    except sp.CalledProcessError as e:
        print(f'[red]F[/red]ailed to build module {module.name} {e.args}')
        print(e.output)


def main_publish(modules):
    for module in modules:
        try:
            publish(module)
            print('[green]P[/green]ublish module %s successcls'
                  '' % module.name)
        except sp.CalledProcessError as e:
            print('[red]F[/red]ailed to publish module %s, %s' % (module.name, e.args))


def main():
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    versions = {}
    switches = set()

    for arg in sys.argv[1:]:
        if arg.startswith('-'):
            switches.add(arg)
        else:
            k, v = get_kwpair(arg)
            versions[k] = v

    if '--debug' in switches:
        print(versions)

    modules = []

    for module in [i for i in modules_dir.iterdir() if i.is_dir()]:
        module = Module(module)

        if '--only' in switches and module.name not in versions:
            continue

        threadpool.submit(main_build, module, versions)
        modules.append(module)

    threadpool.shutdown()

    if '--publish' in switches:
        main_publish(modules)


if __name__ == '__main__':
    main()
