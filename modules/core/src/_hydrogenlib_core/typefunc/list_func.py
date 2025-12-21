import fractions
from collections import deque
from collections.abc import Iterable


def d1(value, lenght):
    return [value for _ in range(lenght)]


def d2(value, lenght, width):
    return [d1(value, width) for _ in range(lenght)]


def d3(value, lenght, width, height):
    return [d2(value, lenght, width) for _ in range(height)]


def d1_init(ls, value):
    lenght = len(ls)
    return d1(value, lenght)


def d2_init(ls, value):
    lenght = len(ls)
    width = len(ls[0])
    return d2(value, lenght, width)


def d3_init(ls, value):
    lenght = len(ls)
    width = len(ls[0])
    height = len(ls[0][0])
    return d3(value, lenght, width, height)


def sub(list1, list2):
    # is lst1 in lst2
    return list1 in list2


def parent(list1, list2):
    # is lst1 of lst2
    return list2 in list1


def match(list1, list2):
    return list1 == list2


def indexs_of(lst, indexs=None):
    if indexs is None:
        return []
    return [lst[i] for i in indexs]


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
        yield [i for i in ls[cursor:cursor + l]]
        cursor += l


class _ListConcater:
    """
    逻辑连接两个列表
    """

    def __init__(self, *ls):
        self.ls_list = ls
        self.lg_list = []

        self.flush()

    def flush(self):
        self.lg_list = [len(i) for i in self.ls_list]

    def _find_list(self, idx, num):
        if num < 0:
            num += sum(self.lg_list)
        if idx >= len(self.lg_list):
            raise IndexError('index out of the range')
        if num >= self.lg_list[idx]:
            return self._find_list(idx + 1, num - self.lg_list[idx])
        return idx, num

    def _get(self, idx):
        last_idx, list_idx = self._find_list(0, idx)
        return self.ls_list[last_idx][list_idx]

    def _set(self, idx, value):
        last_idx, list_idx = self._find_list(0, idx)
        self.ls_list[last_idx][list_idx] = value

    def _get_range_length(self, start, stop, step):
        return (stop - start) // step

    def append(self, v):
        self.ls_list[-1].append(v)
        self.flush()

    def extend(self, v):
        self.ls_list[-1].extend(v)
        self.flush()

    def list(self):
        return [
            item for ls in self.ls_list for item in ls
        ]

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._get(key)

        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or len(self)
            step = key.step or 1
            return [self._get(i) for i in range(start, stop, step)]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._set(key, value)

        if isinstance(key, slice):
            start = key.start or 0
            stop = key.stop or len(self)
            step = key.step or 1
            if not len(value) == self._get_range_length(start, stop, step):
                raise ValueError('length of value is not equal to the range')
            for si, oi in zip(range(start, stop, step), range(len(value))):
                self._set(si, value[oi])

    def __len__(self):
        return sum(self.lg_list)


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

    def __init__(self, fill_ls, main_ls):
        self.ls_fill, self.main_ls = fill_ls, main_ls

    def _get(self, item):
        if item >= len(self):
            raise IndexError('index out of the range')
        if hasindex(self.ls_fill, item):
            return self.ls_fill[item]
        if not hasindex(self.main_ls, item):
            raise IndexError('index out of the range')
        return self.main_ls[item]

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
        return len(self.main_ls)


def fill_concat(fill_ls, main_ls):
    return _ListFillConcater(fill_ls, main_ls)


class _ListReplaceConcater:
    class ReplaceIndex:
        def __init__(self, value, length):
            self.value = value
            self.length = length

    def __init__(self, main_ls):
        self.main_ls = main_ls
        self.replace_ls = []
        self.fore_sum = deque([0])  # 前缀和

    def list(self):
        return [
            self._get(i) for i in range(len(self)-1)
        ]

    def _replace_length(self):
        return self.fore_sum[-1]

    def replace_one(self, value, length):
        """
        将一个值作为逻辑代替项代替main_ls中的length个项
        """
        self.replace_ls.append(self.ReplaceIndex(value, length))
        self.fore_sum.append(
            self.fore_sum[-1] + length - 1
        )

    def _get(self, item):
        if item >= len(self):
            raise IndexError('index out of the range')
        if item < len(self.replace_ls):
            return self.replace_ls[item].value
        else:
            return self.main_ls[item + self._replace_length()]

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._get(item)
        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or len(self)
            step = item.step or 1
            return [self._get(i) for i in range(start, stop, step)]

    def __len__(self):
        s = sum(i.length - 1 for i in self.replace_ls)
        return len(self.main_ls) - s  # 减去逻辑替换项的长度


def replace_concat(main_ls):
    return _ListReplaceConcater(main_ls)
