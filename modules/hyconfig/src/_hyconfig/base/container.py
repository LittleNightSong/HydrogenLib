from .field import Field
from collections import OrderedDict
from _hycore.typefunc import iter_annotations, get_type_name


def validator_mark(func, name=None):
    func.__validator__ = name  # Attr Name
    return func


class SpecialAnnoBase:
    def __generate_field__(self, tp, name, default):
        return Field(tp, default=default, name=name)  # 默认行为


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

            if isinstance(value, SpecialAnnoBase):
                fields[name] = field = value.__generate_field__(typ, name, value)  # 使用来自 SpecialAnnoBase 生成的 Field
                setattr(cls, name, field)
                continue

            # 正常分配 Field
            field = Field(typ, default=value, name=name)

            # 设置字段属性
            fields[name] = field
            setattr(cls, name, field)

        for func in vars(cls).values():
            if hasattr(func, '__validator__'):
                fields[func.__validator__].validator = func

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
    if attrs is None:
        return

    fields = obj.__fields__
    names = names or fields.keys()

    for name in names:
        field = fields[name]
        field_instance = field.get_field_by_obj(obj)
        field_instance.__dict__.update(attrs)
