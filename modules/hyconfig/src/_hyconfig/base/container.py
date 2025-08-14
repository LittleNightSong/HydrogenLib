from .field import Field
from collections import OrderedDict
from _hycore.typefunc import iter_annotations, get_type_name


def validator_mark(func, name=None):
    func.__validator__ = name  # Attr Name
    return func


class AnnoationSupportContainerBase:
    __fields__ = None  # type: OrderedDict[str, Field]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__()
        if kwargs.get('nofields'):
            return

        cls.__fields__ = fields = OrderedDict()  # type: OrderedDict[str, Field]
        for name, typ, value in iter_annotations(cls):
            if isinstance(value, Field):
                fields[name] = value
                continue  # 不重复创建 Field

            field = Field(typ, default=value, name=name)
            fields[name] = field

            setattr(cls, name, field)

        for name in dir(cls):
            fnc = getattr(cls, name)
            if hasattr(fnc, '__validator__'):
                fields[fnc.__validator__].validator = fnc

    def __iter_items(self):
        for f in self.__fields__.values():
            yield f.name, getattr(self, f.name)

    def __str__(self):
        msg = f'{get_type_name(self)}(' '\n'
        for k, v in self.__iter_items():
            msg += '\t' f'{k}={v}' '\n'
        return msg + ')'

    def __repr__(self):
        return repr({
            k: v for k, v in self.__iter_items()
        })


def update_fields_attrs(obj: AnnoationSupportContainerBase, names=None, attrs: dict=None):
    if attrs is None: return

    fields = obj.__fields__
    names = names or fields.keys()

    for name in names:
        field = fields[name]
        field_instance = field.get_field_by_obj(obj)
        field_instance.__dict__.update(attrs)
