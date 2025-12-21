from types import NoneType
from typing import Union

jsontypes = (
    dict, list, int, float, str, bool, NoneType
)


type JsonType = Union[
    dict, list, int, float, str, bool, NoneType
]
