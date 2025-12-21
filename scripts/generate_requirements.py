import re
from pathlib import Path
from subprocess import check_call
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(128)

class Visited:
    def __init__(self):
        self._visited = set()

    def add(self, obj):
        self._visited.add(obj)

    def remove(self, obj):
        if obj in self._visited:
            self._visited.remove(obj)

    def clear(self):
        self._visited.clear()

    def __len__(self):
        return len(self._visited)

    def __iter__(self):
        return iter(self._visited)

    def __repr__(self):
        return repr(self._visited)

    def __contains__(self, obj):
        return obj in self._visited

    def __getitem__(self, item):
        return item in self._visited

    def __setitem__(self, key, value):
        if value:
            self.add(key)
        else:
            self.remove(key)


cwd = Path.cwd()

item_expr = re.compile(r'([\w-]+)((==|<|>|>=|<=|!=|~=)(.+))?')


def generate_requirements(src):
    check_call(
        [
            'pipreqs', '--force', '--ignore',
            r'E:\@PythonProjects\HydrogenLib\.venv\Lib\site-packages,E:\@PythonProjects\HydrogenLib\.temp',
            str(src)
        ]
        # , check=True
    )


def parse_requirements(src):
    with open(src) as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            try:
                name, _, opt, version = item_expr.match(line.strip()).groups()
                yield name, opt, version
            except:
                continue


def sort_requirements(src):
    dct = {}
    vis = Visited()
    res = []
    for name, opt, version in list(parse_requirements(src)):
        dct[name] = (opt, version)
        if vis[name]:
            continue
        else:
            vis[name] = True
            res.append(name)

    lines = []
    for name in res:
        opt, version = dct[name]
        lines.append(f'{name}{opt}{version}')

    if not lines:
        print('Error:', src)
        return

    with open(src, 'w') as f:
        for line in lines:
            f.write(line)
            f.write('\n')


def run(module):
    print(f"Start run on {module}")
    generate_requirements(module)
    sort_requirements(module / 'requirements.txt')

def main():
    cwd = Path.cwd().parent
    modules = cwd / 'modules'

    for module in modules.iterdir():
        if module.is_dir():
            pool.submit(run, module)


if __name__ == '__main__':
    main()
