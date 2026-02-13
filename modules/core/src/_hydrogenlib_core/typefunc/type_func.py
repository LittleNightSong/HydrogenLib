import inspect
import typing
from typing import Sequence, overload, Literal, Any


def get_subclasses(cls):
    """
    Get all direct subclasses of a class.

    Args:
        cls (type): The class to inspect.

    Returns:
        list: List of direct subclasses.
    """
    if cls is type:
        return []
    return cls.__subclasses__()


def get_subclass_counts(cls):
    """
    Get the number of direct subclasses of a class.

    Args:
        cls (type): The class to inspect.

    Returns:
        int: Number of direct subclasses.
    """
    if cls is type:
        return 0
    return len(cls.__subclasses__())


def get_subclasses_recursion(cls):
    """
    Recursively get all subclasses of a class.

    Args:
        cls (type): The class to inspect.

    Returns:
        list: List of all subclasses recursively.
    """
    if cls is type:
        return []
    return (
            cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_subclasses_recursion(s)]
    )


def get_subclass_counts_recursion(cls):
    """
    Recursively get the number of all subclasses of a class.

    Args:
        cls (type): The class to inspect.

    Returns:
        int: Total number of subclasses recursively.
    """
    if cls is type:
        return 0
    return len(cls.__subclasses__()) + sum(get_subclass_counts_recursion(s) for s in cls.__subclasses__())


@overload
def iter_annotations(obj, *, globals=None, locals=None, eval_str=False, with_value: Literal[False] = False) -> tuple[
    tuple[str, Any]]: ...


@overload
def iter_annotations(obj, *, globals=None, locals=None, eval_str=False, with_value: Literal[True] = True) -> tuple[
    tuple[str, Any, Any | None]]: ...


def iter_annotations(obj, *, globals=None, locals=None, eval_str=False, with_value=False, default_value=None):
    """
    Iterate over all annotations in an object, optionally yielding their values.

    Args:
        obj: The object to inspect.
        globals: Optional globals for annotation evaluation.
        locals: Optional locals for annotation evaluation.
        eval_str (bool): Whether to evaluate string annotations.
        with_value (bool): If True, yield annotation values; else only names and types.
        default_value: Value to yield if attribute is missing.

    Yields:
        tuple: (name, type) or (name, type, value)
    """
    if with_value:
        for name, typ in inspect.get_annotations(obj, globals=globals, locals=locals, eval_str=eval_str).items():
            yield name, typ, getattr(obj, name, default_value)
    else:
        yield from inspect.get_annotations(obj, globals=globals, locals=locals, eval_str=eval_str).items()


def iter_attributes(obj):
    """
    Iterate over all public attributes of an object.

    Args:
        obj: The object to inspect.

    Yields:
        tuple: (name, value) for each public attribute.
    """
    for name in dir(obj):
        if name.startswith("_"):
            continue
        yield name, getattr(obj, name)


empty_set = frozenset()


class AutoSlotsMeta(type):
    """
    Metaclass that automatically generates __slots__ for a class based on annotations and attributes.

    Attributes:
        __slots__ (tuple): Slots for the class.
        __no_slots__ (tuple): Attributes to exclude from slots.
        __migrate_class_vars__ (bool): Whether to migrate class variables.
        __migrated__ (dict): Migrated class variables.
    """
    __slots__: tuple
    __no_slots__: tuple
    __migrate_class_vars__: bool = False
    __migrated__ = None

    def __new__(cls, name, bases, attrs):
        """
        Create a new class with automatically generated __slots__.

        Args:
            name (str): Class name.
            bases (tuple): Base classes.
            attrs (dict): Class attributes.

        Returns:
            type: The new class.
        """
        slots = set(attrs.get("__slots__", ()))
        slots |= set(attrs.get('__annotations__', {}).keys())
        no_slots = set(attrs.get('__no_slots__', empty_set))

        attrs['__slots__'] = tuple(slots - no_slots)

        if attrs.get('__migrate_class_vars__') or getattr(cls, '__migrate_class_vars__', None):
            migrated = {}
            for attr in attrs['__slots__']:
                if attr in attrs:
                    migrated[attr] = attrs[attr]
                    del attrs[attr]

            attrs['__migrated__'] = migrated

        return super().__new__(cls, name, bases, attrs)


class AutoSlots(metaclass=AutoSlotsMeta):
    """
    Class using AutoSlotsMeta to automatically generate __slots__.

    Purpose:
        Reduces memory usage and speeds up attribute access by eliminating the instance dictionary.
    """
    pass


def get_origin(tp):
    """
    Get the origin type of a generic type.

    Args:
        tp: The type to inspect.

    Returns:
        type: The origin type, or tp if not generic.
    """
    origin = typing.get_origin(tp)
    return origin if origin is not None else tp


def split_type(tp):
    """
    Split a generic type into its origin and arguments.

    Args:
        tp: The type to split.

    Returns:
        tuple: (origin, args)
    """
    return get_origin(tp), typing.get_args(tp)


class SingletonType:
    """
    Singleton base class. Ensures only one instance exists.

    Attributes:
        _single_instance: The singleton instance.
    """
    _single_instance = None

    def __new__(cls, *args, **kwargs):
        """
        Create or return the singleton instance.

        Returns:
            SingletonType: The singleton instance.
        """
        if cls._single_instance is None:
            cls._single_instance = super().__new__(cls, *args, **kwargs)
        return cls._single_instance


class AutoRepr:
    """
    Automatically generates __repr__ based on specified attributes.

    Attributes:
        __repr_attrs__ (tuple): Attributes to include in repr.
    """
    __repr_attrs__ = ()

    def __repr__(self):
        """
        Return string representation of the object using __repr_attrs__.

        Returns:
            str: String representation.
        """
        return str(
            {attr: getattr(self, attr) for attr in self.__repr_attrs__}
        )


class AutoStr:
    """
    Automatically generates __str__ based on specified attributes.

    Attributes:
        _str_attrs (tuple): Attributes to include in str.
    """
    _str_attrs = ()

    def __str__(self):
        """
        Return string representation of the object using _str_attrs.

        Returns:
            str: String representation.
        """
        return str(
            {attr: getattr(self, attr) for attr in self._str_attrs}
        )


class AutoInfo(AutoRepr, AutoStr):
    """
    Combines AutoRepr and AutoStr, using _info_attrs for both.

    Attributes:
        _info_attrs (tuple): Attributes to include in both repr and str.
    """
    _info_attrs = ()

    def __repr__(self):
        """
        Return string representation using _info_attrs for repr.
        """
        self._repr_attrs = self._info_attrs
        return super().__repr__()

    def __str__(self):
        """
        Return string representation using _info_attrs for str.
        """
        self._str_attrs = self._info_attrs
        return super().__str__()


class AutoCompare:
    """
    Automatically implements comparison operations based on specified attributes.

    Attributes:
        __compare_attrs__ (tuple): Attributes to use for comparison.
        __cmp_funcs__ (dict): Mapping of comparison operators to functions.
    """
    __compare_attrs__ = ()
    __cmp_funcs__ = {
        'eq': lambda x, y: x == y,
        'ne': lambda x, y: x != y,
        'lt': lambda x, y: x < y,
        'gt': lambda x, y: x > y,
        'le': lambda x, y: x <= y,
        'ge': lambda x, y: x >= y
    }

    def _auto_compare_attrs(self, opt, other, defautl=False):
        """
        Compare attributes based on the specified operator.

        Args:
            opt (str): Comparison operator ('eq', 'ne', etc).
            other: Object to compare with.
            defautl: Default value if comparison cannot be performed.

        Returns:
            bool: Result of comparison.
        """
        if opt not in self.__cmp_funcs__:
            return defautl

        func = self.__cmp_funcs__[opt]

        if not isinstance(other, AutoCompare):
            if self.__compare_attrs__:
                value = getattr(self, self.__compare_attrs__[0])
                return func(value, other)

        if self.__compare_attrs__ is None or other.__compare_attrs__ is None:
            return defautl

        my_attr_values = (
            getattr(self, attr) for attr in self.__compare_attrs__)
        other_attr_values = (
            getattr(other, attr) for attr in other.__compare_attrs__)
        return func(my_attr_values, other_attr_values)

    def __eq__(self, other):
        """
        Equality comparison.
        """
        return self._auto_compare_attrs('eq', other, False)

    def __ne__(self, other):
        """
        Inequality comparison.
        """
        return self._auto_compare_attrs('ne', other, True)

    def __lt__(self, other):
        """
        Less-than comparison.
        """
        return self._auto_compare_attrs('lt', other, False)

    def __gt__(self, other):
        """
        Greater-than comparison.
        """
        return self._auto_compare_attrs('gt', other, False)

    def __le__(self, other):
        """
        Less-than-or-equal comparison.
        """
        return self._auto_compare_attrs('le', other, True)

    def __ge__(self, other):
        """
        Greater-than-or-equal comparison.
        """
        return self._auto_compare_attrs('ge', other, True)


def make_object(attrs: dict, bases: Sequence[type], metaclass: type[type] = type, **kwargs):
    """
    Dynamically create an object with specified attributes, bases, and metaclass.

    Args:
        attrs (dict): Attributes for the new object.
        bases (Sequence[type]): Base classes.
        metaclass (type): Metaclass to use.
        **kwargs: Additional attributes.

    Returns:
        object: The created object instance.
    """
    final_attrs = {**attrs, **kwargs}
    # Build type
    tp = metaclass(
        '<dynamic type>', tuple(bases), final_attrs
    )
    obj = tp()
    return obj