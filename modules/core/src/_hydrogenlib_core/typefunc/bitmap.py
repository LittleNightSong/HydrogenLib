from typing import Iterable, Union, Optional

from bitarray import bitarray


class Bitmap:
    def __init__(self, bits: Optional[Union[int, Iterable[int]]] = None):
        """
        初始化 Bitmap 对象。

        :param bits: 可以是整数、可迭代的位序列或 None。
                     如果是整数，则将其作为位图的初始值。
                     如果是可迭代的位序列，则将其转换为位图。
                     如果是 None，则初始化为空位图。
        """
        self.bits = bitarray()
        if bits is None:
            self.bits = bitarray()
        elif isinstance(bits, int):
            self.bits = bitarray(format(bits, 'b'))
        elif isinstance(bits, Iterable):
            self.bits = bitarray(map(int, bits))
        else:
            raise TypeError("bits must be an int, an iterable of bits, or None")

    def get_bit(self, index: int) -> bool:
        """
        获取指定索引的位值。

        :param index: 位的索引。
        :return: 指定索引的位值（True 或 False）。
        """
        if index >= len(self.bits):
            return False
        return bool(self.bits[index])

    def set_bit(self, index: int, on: bool = True):
        """
        设置指定索引的位值。

        :param index: 位的索引。
        :param on: 如果为 True，则将位设置为 1；否则设置为 0。
        """
        if index >= len(self.bits):
            self.bits.extend([False] * (index - len(self.bits) + 1))
        self.bits[index] = on

    def pack(self) -> bytes:
        """
        将位图打包为字节序列。

        :return: 字节序列。
        """
        return self.bits.tobytes()

    @classmethod
    def unpack(cls, data: bytes) -> 'Bitmap':
        """
        从字节序列解包为 Bitmap 对象。

        :param data: 字节序列。
        :return: Bitmap 对象。
        """
        bits = bitarray()
        bits.frombytes(data)
        return cls(bits)

    def extend(self, other: 'Bitmap'):
        """
        将另一个 Bitmap 对象扩展到当前 Bitmap 对象中。

        :param other: 另一个 Bitmap 对象。
        """
        self.bits.extend(other.bits)

    def __setitem__(self, key: int, value: bool):
        """
        设置指定索引的位值。

        :param key: 位的索引。
        :param value: 位的值（True 或 False）。
        """
        self.set_bit(key, value)

    def __getitem__(self, item: int) -> bool:
        """
        获取指定索引的位值。

        :param item: 位的索引。
        :return: 指定索引的位值（True 或 False）。
        """
        return self.get_bit(item)

    def __iter__(self):
        """
        返回一个迭代器，用于遍历位图中的每一位。

        :return: 迭代器。
        """
        return iter(self.bits)

    def __len__(self) -> int:
        """
        返回位图的长度（即位的数量）。

        :return: 位图的长度。
        """
        return len(self.bits)

    def __str__(self) -> str:
        """
        返回位图的字符串表示。

        :return: 字符串表示。
        """
        return f"{self.__class__.__module__}.{self.__class__.__name__}({self.bits.to01()})"

    __repr__ = __str__
