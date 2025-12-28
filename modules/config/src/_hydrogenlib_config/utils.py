import ast
import json

from typing import Literal, Callable, Any

from .core.base import ConfigBase

format_mro: dict[str, dict[Literal['load-io', 'load-file', 'dump-io', 'dump-file'], Callable[[Any, ...], Any]] | str]
format_mro = {  # type: ignore
    'json': {
        'load-io': json.load,
        'load-file': 'open',
        'dump-io': json.dump,
        'dump-file': 'open',
    },
    'python': {
        'load-io': ast.literal_eval,
        'load-file': 'open',
        'dump-io':  repr,
        'dump-file': 'open'
    }
}

def has_field(cfg: ConfigBase, name: str):
    return cfg.__config_fields__.__contains__(name)

def load_from_obj(cfg, obj, extra='ignore'):
    for k, v in obj.items():
        if not has_field(cfg, k):
            match extra:
                case "ignore":
                    continue
                case 'allow':
                    setattr(cfg, k, v)
                case 'error':
                    raise AttributeError(f'{k} not in {cfg.__config_fields__}')
        else:
            setattr(cfg, k, v)

def load_from_file(cfg, file, format='json'):
    format_info = format_mro[format]

    load_function = format_info['load-file']
    if load_function == 'open':
        with open(file, 'r') as f:
            return load_from_obj(cfg, format_info['load-io'](f))
    else:
        return load_function(file)

def load_from_io(cfg, io, format='json'):
    format_info = format_mro[format]

    return load_from_obj(cfg, format_info['load-io'](io))


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
