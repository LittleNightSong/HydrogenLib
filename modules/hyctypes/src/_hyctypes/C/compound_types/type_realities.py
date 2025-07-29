from inspect import Signature, get_annotations

from _hycore.typefunc import get_type_name, get_name, get_signature
from .base import CallingConvention as CV, pointer
from .impls import *
from ..methods import get_types_from_signature


class PointerType(AbstractCType, real=Pointer):
    def __init__(self, tp):
        """

        :param tp: 指针目标类型
        """
        self.tp = tp
        self.__real_ctype__ = ctypes.POINTER(as_ctype(tp))

    def __call__(self, obj):
        return Pointer(pointer(obj))

    def _convert_pointer(self, obj):
        return obj.cast(self.tp)

    def _convert_obj(self, obj):
        return Pointer(pointer(obj))

    _convert_mro = {
        Pointer: _convert_pointer,
    }

    def __convert_ctype__(self, obj):
        tp = type(obj)
        return self._convert_mro.get(tp, self._convert_obj)(self, obj)


class ArrayType(AbstractCType, real=Array):
    def __init__(self, tp, length=1):
        """

        :param tp: 数组元素类型
        :param length: 数组长度
        """
        self.tp = tp
        self.length = length
        self.__real_ctype__ = ctypes.POINTER(as_ctype(tp)) * length

    def __call__(self, *args):
        return Array(self.__real_ctype__(*args))

    def __convert_ctype__(self, obj):
        if isinstance(obj, Pointer):
            return ArrayPointer(obj)
        elif hasattr(obj, '__iter__'):
            obj = tuple(obj)  # 先转换成开销小的元组类型
            length = len(obj)
            if length != self.length:
                # 将 obj 转换成 Array 时发生错误: 长度不匹配
                raise TypeError(f'Convert to Array failed: Length mismatch (except {self.length}, got {length})')
            return Array(self.__real_ctype__(*(as_cdata(x) for x in obj)))
        else:
            raise TypeError(f'Convert to Array failed: {obj} is not iterable')


class RefType(AbstractCType, real=Ref):
    __real_ctype__ = ctypes.c_void_p

    def __init__(self, tp):
        """
        :param tp: 引用目标类型
        """
        self.tp = tp

    def __convert_ctype__(self, obj):
        return Ref(obj)

    def __call__(self, obj):
        return Ref(obj)


class AnonymousType(AbstractCType, real=object):
    def __init__(self, tp):
        self.__real_ctype__ = self.__real_type__ = tp


class _This:
    _i = None

    def __new__(cls, *args, **kwargs):
        if cls._i is None:
            cls._i = super().__new__(cls)

        return cls._i


This = _This()


class StructureType(AbstractCType, real=Structure):
    __struct_base__ = None

    @staticmethod
    def config_structure(s, fields=None, anonymous=None, pack=None, align=None):
        fields = fields or getattr(s, '_fields_', None)
        anonymous = anonymous or getattr(s, '_anonymous_', None)
        pack = pack or getattr(s, '_pack_', None)
        align = align or getattr(s, '_align_', None)

        if fields is not None:
            s._fields_ = tuple(fields)
        if anonymous is not None:
            s._anonymous_ = tuple(anonymous)
        if pack is not None:
            s._pack_ = pack
        if align is not None:
            s._align_ = align

        return s

    @staticmethod
    def generate_structure_name(types, head='Structure'):
        return f"{head}_{''.join([get_type_name(tp).removeprefix('c_') for tp in types])}"

    def __init__(self, *fields, anonymous, pack, align, base=None):
        base = base or self.__struct_base__ or ctypes.Structure
        self.__real_ctype__ = s = type(
            self.generate_structure_name(map(lambda x: x[1], fields)),
            (base,), {}
        )

        final_fields = []
        final_anonymous = set(anonymous or ())
        for name, typ in fields:
            if isinstance(typ, AnonymousType):
                final_anonymous.add(name)

            final_fields.append((name, as_ctype(typ)))

        self.config_structure(
            s,
            fields=final_fields,
            anonymous=final_anonymous,
            pack=pack,
            align=align,
        )

    def set_real_type(self, tp):
        if not issubclass(tp, Structure):
            raise TypeError(f"{tp.__name__} is not a subclass of Structure")
        self.__real_type__ = tp

    @classmethod
    def define(cls, maybe_cls, *, pack=None, align=None, anonymous=None, base=None):
        def decorator(ccls):
            # 提取 annotations
            fields = get_annotations(ccls).items()
            inst = cls(*fields, pack=pack, align=align, anonymous=anonymous, base=base)
            inst.set_real_type(ccls)
            ccls.__ctype__ = inst.__real_ctype__

            return inst

        if maybe_cls is None:
            return decorator

        else:
            return decorator(maybe_cls)


class UnionType(StructureType, real=Structure):  # 万能的 Structure!!!
    __struct_base__ = ctypes.Union


class ProtoType(AbstractCType, real=Function):
    @LazyProperty
    def c_argtypes(self):
        return tuple(map(as_ctype, self.argtypes))

    def __init__(self, restype, *argtypes, cv: CV = CV.auto, signature: Signature = None, name: str = None):
        self.argtypes = argtypes
        self.restype = restype
        self.cv = cv
        self.signature = signature
        self.name = name

    def bind(self, dll, name=None):
        if dll.calling_convention != self.cv:
            raise TypeError(f"Calling convention mismatch: {dll.calling_convention} != {self.cv}")
        return Function(dll.addr(name or self.name), self, self.signature)

    @classmethod
    def define(cls, maybe_func=None, *, name: str = None, cv: CV = CV.auto):
        def decorator(func):
            nonlocal name
            name = name or get_name(func)
            signature = get_signature(func)  # 获取函数签名
            types = tuple(get_types_from_signature(signature))
            restype = signature.return_annotation  # 提取 argtypes 和 restype

            # 构建原型
            return cls(
                restype, *types,
                signature=signature, name=name,
                cv=cv
            )

        if maybe_func is None:
            return decorator
        else:
            return decorator(maybe_func)

    @LazyProperty
    def __real_ctype__(self):
        return self.cv.functype(self.restype, *self.c_argtypes)

    def __call__(self, ptr):
        return Function(ptr, self)

    def __str__(self):
        return f"ProtoType([{', '.join(map(str, self.argtypes))}]) -> {self.restype}"
