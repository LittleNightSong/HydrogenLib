import sys
from argparse import ArgumentParser
from pathlib import Path
from rich import print
from natsort import natsorted
import rich.traceback
import rich.color
from random import randint, choice

rich.traceback.install(show_locals=True, max_frames=1)

def _hex(int):
    return hex(int)[2:]

def random_color():
    if randint(0, 1):
        return f"#{_hex(randint(0, 255))}{_hex(randint(0, 255))}{_hex(randint(0, 255))}"
    else:
        return choice(list(rich.color.ANSI_COLOR_NAMES.keys()))

class Loop:
    def __init__(self,iterable, do):
        self.iterable = iterable
        self.do = do
        self.index = 0
        self.value = None

    def exec(self):
        for i, v in enumerate(self.iterable):
            self.index, self.value = i, v
            self.do(self)

    @property
    def item(self):
        return self.index, self.value


class MyPath(Path):
    @property
    def ext(self):
        return ''.join(self.suffixes)[1:]

    @property
    def name_with_no_ext(self):
        return self.name.removesuffix(self.suffix)

    def rename(self, name):
        return super().rename(self.parent / name)


class RenameX:
    def __init__(self, args):
        self.parser = ArgumentParser()
        self.parser.add_argument("path", type=Path,
                            help='批量修改名称的根路径.')
        self.parser.add_argument("--dir", '-d', action="store_true",
                            help='指定Path是一个文件夹,如果Path目标不符合此开关的状态,那么报错(不设置则默认为文件).')
        self.parser.add_argument("--format", '-f', type=str, default='{loop.index}.{file.ext}',
                            help='指定目标名称的格式(使用Python的format格式),默认为"{loop.index}.{file.ext}".')
        self.parser.add_argument('--all', '-a', action='store_true',
                            help='批量修改所有文件,包括文件夹.')

        self.parser.parse_args(args, namespace=self)

        self.loop = None
        self.inners = None

    def __hook(self, loop: Loop):
        i: int ; v: MyPath
        i, v = loop.item

        target = self.format.format(loop=loop, file=v)

        print(
            f'[{random_color()}]Rename [{random_color()}]from [green]"{v}" [{random_color()}]to [green]"{target}" ...', end='')
        if (self.all or v.is_file()) and target != v.name:
            v.rename(target)
            print(f' [{random_color()}]Done.[reset]')
        else:
            print(f' [{random_color()}]Skip.[reset]')

    def exec(self):
        if self.dir and not self.path.is_dir():
            raise ValueError("Don't set '--dir' when path is not a directory")
        if not self.dir and not self.path.is_file():
            raise ValueError("Please set '--dir' when path is a directory")
        if self.dir:
            self.inners = natsorted([MyPath(i) for i in self.path.iterdir()], key=lambda x: x.name_or_ordinal)
            # # print('Inners:', self.inners)
            # before = self.inners.copy()
            # self.inners.sort(key=lambda x: x.name_with_no_ext)
            # # print('Inners:', self.inners)
            # # print(before == self.inners)
            self.loop = Loop(self.inners, self.__hook)
            self.loop.exec()


def main():
    main = RenameX(sys.argv[1:])
    main.exec()
