import copy
import fractions
from collections.abc import Iterable


def hasindex(iterable, index):
    if isinstance(index, slice):
        return True  # Slice 不会引发错误，不需要检查
    if index < 0:
        index += len(iterable)
    return len(iterable) > index


def split(ls, split_nums: Iterable[int]):
    """
    将列表按照**整数**比例分割，返回分割后的列表
    如:
        a = [1, 2, 3, 4, 5, 6]
        b, c, d = split(a, 1, 2, 3)  # b: [1], c: [2, 3], d: [4, 5, 6]
    """
    sm = sum(split_nums)
    lengths = [fractions.Fraction(i) * sm for i in split_nums]
    cursor = 0
    for l in lengths:
        yield ls[cursor:cursor + l]
        cursor += l


def _get_range_length(start, stop, step):
    return (stop - start) // step


class _ListConcater:
    """
    逻辑连接两个列表
    """
    __slots__ = ('lists', 'lengths')

    def __init__(self, *ls):
        self.lists = list(ls)

    def _find_list(self, num):
        if num < 0:
            num += len(self)

        for i, ls in enumerate(self.lists):
            delta = num - len(ls)
            if delta > 0:
                num = delta
            else:
                return i, delta

        raise IndexError('index out of the range')

    def _get(self, i):
        outter_index, inner_index = self._find_list(i)
        return self.lists[outter_index][inner_index]

    def _set(self, i, value):
        outter_index, inner_index = self._find_list(i)
        self.lists[outter_index][inner_index] = value

    def append(self, v):
        if self.lists:
            self.lists[-1].append(v)
        else:
            self.lists.append([v])

    def extend(self, v):
        if self.lists:
            self.lists[-1].extend(v)
        else:
            self.lists.append(copy.copy(v))

    def list(self):
        return [
            item for ls in self.lists for item in ls
        ]

    def __getitem__(self, key):
        if isinstance(key, int) or (key := getattr(key, '__index__', lambda: None)()):
            return self._get(key)

        elif isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or len(self)
            step = key.step or 1
            return [self._get(i) for i in range(start, stop, step)]
        else:
            raise IndexError(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._set(key, value)

        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or len(self)
            step = key.step or 1

            if not len(value) == _get_range_length(start, stop, step):
                raise ValueError('length of value is not equal to the range')

            for i, v in zip(range(start, stop, step), value):
                self._set(i, v)

    def __len__(self):
        lenght = 0
        for ls in self.lists:
            lenght += len(ls)

        return lenght


def concat(*ls):
    return _ListConcater(*ls)


class _ListFillConcater:
    """
    以填充覆盖方式连接两个列表，如:
        a = [1, 2, 3, 4, 5, 6]
        b = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        fill_concat_ls = fill_concat(a, b)  # [1, 2, 3, 4, 5, 6, 11, 12, 13, 14]
        其中a列表被逻辑覆写进了b列表的开头
        如果fill_ls的长度大于main_ls，那么无论怎样访问，都将优先返回fill_ls的值，但是**合并长度不改变**
        列表的元数据以main_ls为基准
        len(fill_concat_ls)  # 10
    """
    __slots__ = ('ls_fill', 'ls_main')

    def __init__(self, fill_ls, main_ls):
        self.ls_fill, self.ls_main = fill_ls, main_ls

    def _get(self, item):
        if item >= len(self):
            raise IndexError('index out of the range')
        if hasindex(self.ls_fill, item):
            return self.ls_fill[item]
        if not hasindex(self.ls_main, item):
            raise IndexError('index out of the range')
        return self.ls_main[item]

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._get(item)

        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or len(self)
            step = item.step or 1
            return [self._get(i) for i in range(start, stop, step)]

    def list(self):
        return [
            self[i] for i in range(len(self))
        ]

    def __setitem__(self, key, value):
        raise NotImplementedError('Fill concat cannot be modified')

    def __len__(self):
        return len(self.ls_main)


def fill_concat(fill_ls, main_ls):
    return _ListFillConcater(fill_ls, main_ls)
