import sys
from pathlib import Path
from argparse import ArgumentParser
from importlib import util


class Enter:
    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('path', type=str,
                                 help='path to the utility script')

        self.parser.parse_args(sys.argv[1:2], namespace=self)
        self.root = Path(__file__).parent

    def _run_utility(self, path):
        spec = util.spec_from_file_location('utility', path)
        if spec is None or spec.loader is None:
            raise ImportError(f'Cannot load module {self.path}(One attribute is None)')
        module = util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.argv = [str(path)] + sys.argv[2:]
        module.main()

    def exec(self):
        if not self.path.endswith('.py'):
            self.path += '.py'

        path = self.root / self.path
        if not path.exists():
            raise FileNotFoundError(f'Cannot find file {self.path}')

        self._run_utility(path)


def main():
    Enter().exec()


if __name__ == '__main__':
    main()

