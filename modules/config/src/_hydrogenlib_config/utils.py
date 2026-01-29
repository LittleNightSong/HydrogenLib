from __future__ import annotations

import ast
import json
import pickle
from os import PathLike
from typing import Literal, Callable, Any, TypedDict, IO, MutableMapping

from .core.base import ConfigBase

# class _IOFunctionMapping(TypedDict):
#     load_io: Callable[[IO], MutableMapping[str, Any]]
#     load_file: Callable[[PathLike], MutableMapping[str, Any]]
#     dump_io: Callable[[IO, Any], Any]
#     dump_file: Callable[[PathLike[str], Any], Any]


_FnDumpToFile = Callable[[PathLike[str], Any], Any]
_FnDumpToIO = Callable[[IO, Any], Any]
_FnLoadFromFile = Callable[[PathLike], MutableMapping[str, Any]]
_FnLoadFromIO = Callable[[IO], MutableMapping[str, Any]]

type SpecialActions = Literal['open']
type ExtraActions = Literal['ignore', 'allow', 'error']

_IOFunctionMapping = TypedDict(
    '_IOFunctionMapping',
    {
        'load-io': _FnLoadFromIO,
        'load-file': _FnLoadFromFile | SpecialActions,
        'dump-io': _FnDumpToIO,
        'dump-file': _FnDumpToFile | SpecialActions
    }
)

format_mro: (
    dict[
        str,
        _IOFunctionMapping
    ]
) = {}


def registry_data_format(
        format: str,
        load_io: _FnLoadFromIO,
        dump_io: _FnDumpToIO,
        load_file: _FnLoadFromFile | SpecialActions = 'open',
        dump_file: _FnDumpToFile | SpecialActions = 'open'
):
    format_mro[format] = {
        'load-io': load_io,
        'load-file': load_file,
        'dump-io': dump_io,
        'dump-file': dump_file,
    }


def has_field(cfg: ConfigBase, name: str):
    return cfg.__config_fields__.__contains__(name)


def config_from_object(cfg, obj: MutableMapping[str, Any]):
    if isinstance(cfg, type):
        cfg = cfg()

    for k, v in obj.items():
        setattr(cfg, k, v)

    return cfg


def load_from_file(cfg, file, format='json'):
    format_info = format_mro[format]

    load_function = format_info['load-file']
    if load_function == 'open':
        with open(file, 'r') as f:
            return config_from_object(cfg, format_info['load-io'](f))
    else:
        return config_from_object(cfg, load_function(file))


def load_from_io(cfg, io, format='json'):
    format_info = format_mro[format]

    return config_from_object(cfg, format_info['load-io'](io))


def dump_to_file(cfg, file, format='json'):
    format_info = format_mro[format]

    dump_function = format_info['dump-file']
    if dump_function == 'open':
        with open(file, 'w') as f:
            format_info['dump-io'](f, cfg.to_dict())
    else:
        dump_function(file, cfg.to_dict())


def dump_to_io(cfg, io, format='json'):
    format_info = format_mro[format]

    return format_info['dump-io'](io, cfg.to_dict())


# 'json': {
#         'load-io': json.load,
#         'load-file': 'open',
#         'dump-io': json.dump,
#         'dump-file': 'open',
#     },
#     'python': {
#         'load-io': ast.literal_eval,
#         'load-file': 'open',
#         'dump-io': repr,
#         'dump-file': 'open'
#     }

registry_data_format(
    'json',
    json.load,
    lambda fp, obj: json.dump(fp, obj)
)

registry_data_format(
    'python',
    lambda fp: ast.literal_eval(fp.read()),
    lambda fp, obj: fp.write(repr(obj))
)

registry_data_format(
    'pickle',
    lambda fp: pickle.load(fp),
    lambda fp, obj: pickle.dump(fp, obj)
)
