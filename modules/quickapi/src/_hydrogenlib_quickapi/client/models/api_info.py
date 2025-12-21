import dataclasses
import inspect
from typing import OrderedDict
from _hydrogenlib_core.dataclasses_methods import default_factory

import yarl


@dataclasses.dataclass(frozen=True)
class APIInfo:
    url: yarl.URL = default_factory(yarl.URL)

    needed_arguments: OrderedDict[str, inspect.Parameter] = default_factory(dict)

    querys: list = default_factory(dict)
    path: list = default_factory(dict)

    addon_args: dict = default_factory(dict)
    addon_headers: dict = default_factory(dict)
