import enum
import inspect
import struct
from collections import OrderedDict


class c_types(str, enum.Enum):
    pad = 'x'

    char = 'c'

    byte = 'b'
    ubyte = 'B'

    bool = '?'

    short = 'h'
    ushort = 'H'

    int = 'i'
    uint = 'I'

    long = 'l'
    ulong = 'L'

    llong = 'q'
    ullong = 'Q'

    short_float = 'e'
    float = 'f'
    double = 'd'

    ssize_t = 'n'
    size_t = 'N'

    string = 's'
    bytearray = 'p'

    pointer = 'P'


class StructMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if cls.__s_fields__ is None:
            cls.__s_fields__ = OrderedDict()
        else:
            cls.__s_fields__ = cls.__s_fields__.copy()

        new_fields = OrderedDict()
        for name, anno in inspect.get_annotations(cls).items():
            if name not in cls.__s_fields__:
                new_fields[name] = anno

        cls.__s_fields__.update(new_fields)

        if cls.__s_format__ is None:
            cls.__s_format__ = ''

        cls.__s_format__ += ''.join(
            new_fields.values()
        )

        cls.__s_struct__ = struct.Struct(cls.__s_format__)

    def __getattr__(self, item):
        match item:
            case 'size':
                return self.__s_struct__.size
            case 'format':
                return self.__s_format__
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}')")


class Struct(metaclass=StructMeta):
    __s_fields__ = None
    __s_format__ = None
    __s_struct__ = None

    def __init__(self, *args, **kwargs):
        assigned_args = set()
        for name, arg in zip(self.__s_fields__, args):
            assigned_args.add(name)
            setattr(self, name, arg)

        for name, value in kwargs.items():
            if name in assigned_args:
                # TypeError: example_function() got multiple values for argument 'b'
                raise TypeError(f"{self.__class__.__name__}(...) got multiple values for argument '{name}")
            setattr(self, name, value)

    @property
    def field_values(self):
        for field in self.__s_fields__:
            yield getattr(self, field)

    def pack(self):
        return self.__s_struct__.pack(*self.field_values)

    def pack_into(self, buffer, offset=0):
        return self.__s_struct__.pack_into(buffer, offset, *self.field_values)

    @classmethod
    def unpack(cls, buffer):
        return cls(
            *cls.__s_struct__.unpack(buffer)
        )

    @classmethod
    def unpack_from(cls, buffer, offset=0):
        return cls(
            *cls.__s_struct__.unpack(buffer)
        )

    @classmethod
    def iter_unpack(cls, buffer):
        yield from map(
            lambda x: cls(*x),
            cls.__s_struct__.iter_unpack(buffer)
        )

    def to_dict(self):
        return {
            k: getattr(self, k)
            for k in self.__s_fields__
        }

    def __repr__(self):
        dct = self.to_dict()
        kv_string = ', '.join(
            map(
                lambda x: f"{x[0]}={x[1]!r}"
                , dct.items()
            )
        )
        return f'{self.__class__.__name__}' f"({kv_string})"
