import array
import dataclasses
import re
from typing import List

from _hydrogenlib_core.typefunc import AutoSlots


@dataclasses.dataclass(frozen=True)
class Field(AutoSlots):
    name: str               # 字段名
    type: str               # 字段数据类型
    optional: bool = False  # 是否可选
    re: str = None          # re表达式约束
    start: int = 0
    end: int = 0
    mark: str = ''


class RoutePath(AutoSlots):
    _mark_re = re.compile(r"<\s*([a-zA-Z0-9_]+)?\s*:\s*([a-zA-Z0-9_]+)\s*(\?)?>")

    path: str
    _fields: list[Field]

    def __init__(self, path: str):
        self.path = path
        self._compile()

    def _compile(self):
        self._fields = []
        for mark in self._mark_re.finditer(self.path):
            type, name, optional = mark.groups()
            field = Field(
                name, type, optional == '?', mark=mark.group(),
                start=mark.start(), end=mark.end()
            )
            self._fields.append(field)

    def format(self, **kwargs) -> str:
        buffer = ''

        i = 0
        while i < len(self._fields):
            field = self._fields[i]
            if i == 0:
                buffer += self.path[0:field.start]
            else:
                buffer += self.path[self._fields[i-1].end+1:field.start]

            buffer += str(kwargs[field.name])

            i += 1
        return buffer  # TODO: test me