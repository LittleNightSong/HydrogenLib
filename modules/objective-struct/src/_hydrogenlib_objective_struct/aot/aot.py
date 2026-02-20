from __future__ import annotations

import array
import itertools
import typing
from typing import Any

import typing_inspection.typing_objects

from _hydrogenlib_core.typefunc import enhanced_generator
from .base import *
from ..methods import get_ctype

if typing.TYPE_CHECKING:
    from .. import struct_type

available_characters = tuple(
    chr(i) for i in range(65, 91)
)


@enhanced_generator(history=True)
def unique_name_generator():
    cnt = 0
    while True:
        cnt += 1
        yield from map(lambda x: ''.join(x),
                       itertools.combinations(available_characters, cnt))


def is_struct(tp):
    return hasattr(tp, '__cstruct__')


def is_array(tp):
    if typing_inspection.typing_objects.is_annotated(typing.get_origin(tp)):
        return True
    return False


def get_array_spec(tp):
    ls_type, length = typing.get_args(tp)
    return typing.get_args(ls_type)[0], length


def get_array_ctype(tp) -> str | None | Any:
    return get_ctype(get_array_spec(tp)[0])


def to_tuple_expression(names, prefix='self.'):
    return ', '.join(f'{prefix}{name}' for name in names)


def create_pack_function(cls: struct_type.Struct):
    with function_def('pack(self)') as pack:
        ung = unique_name_generator()
        flat_fields = []

        def walk(fields, path, parent_name=None):
            # parent name 标识了这个字段的父字段被赋值给了哪个临时变量，这样可以复用已有的临时变量，减少结构体属性访问次数
            name = 'self'  # 这里的 name 是默认的 self，如果当前处理的是内嵌的结构体，那么 name 会被替换成临时变量

            if len(path) > 1:  # 当前处理的是内嵌结构体
                name = ung.next()  # 生成一个临时变量缓存其值
                pack.add_code(f'{name} = {parent_name}.{path[-1]}')

            for field in fields:  # 遍历结构体的所有字段
                if is_struct(field.type):  # 又是一个内嵌的结构体字段
                    walk(field.type.__cfields__, path + (field.name,), name)  # 递归
                elif is_array(field.type):  # 一个数组类型
                    d_ctype = get_array_ctype(field.type)

                    _ = ung.next()
                    pack.add_code(f'{_} = array({d_ctype!r}, {name}.{field.name})')
                    flat_fields.append(f'{_}.tobytes()')

                else:
                    flat_fields.append(f'{name}.{field.name}')  # 普通的字段，添加到传递目标列表中

        walk(cls.__cfields__, ('self',))  # 启动递归函数
        # names = [field.name for field in fields]

        pack.add_return("xpack(" + to_tuple_expression(flat_fields, prefix='') + ')')  # 返回打包的结果，将所有字段参数展开传递
        # print(pack.generate_code())  # Debug
        return pack.exec({'xpack': cls.__cstruct__.pack, 'array': array.array})  # 记得传递 xpack 这个函数变量


def create_unpack_and_update_function(cls: type[struct_type.Struct]):
    with (
        function_def('unpack(cls, buffer)') as unpack,
        function_def('update(self, buffer)') as update
    ):
        unpack.add_decorator('classmethod')  # unpack 是一个类方法
        ung = unique_name_generator()

        post_processors = []
        assigns = []  # 赋值目标列表
        inner_classes = {}  # 内嵌的结构体的类型映射（所有内嵌结构体的类型在生成代码时都会被代替为无意义的名称）

        def walk(fields, path, parent_name=None, current_class_name='cls'):
            name = 'self'

            if len(path) > 1:  # 在处理内嵌的结构体
                name = ung.next()  # 临时变量的名称
                update.add_code(f"{name} = {parent_name}.{path[-1]}")
                unpack.add_code(f"{parent_name}.{path[-1]} = {name} = __new__({current_class_name})")  # 组合赋值
            else:
                unpack.add_code(f"{name} = __new__({current_class_name})")  # 不需要临时变量存储根对象

            for field in fields:  # 遍历字段
                field_ref = f'{name}.{field.name}'

                if is_struct(field.type):  # 是个内嵌的结构体
                    if field.type not in inner_classes:  # 如果这个内嵌的结构体类型不在已知的结构体中（没有分配类名称）
                        type_name = ung.next()  # 生成一个唯一的类名
                        inner_classes[field.type] = type_name  # 添加
                    else:
                        type_name = inner_classes[field.type]  # 如果在，那么提取

                    walk(field.type.__cfields__, path + (field.name,), name, type_name)
                elif is_array(field.type):
                    d_ctype = get_array_ctype(field.type)
                    post_processors.append(
                        f'_ = array({d_ctype!r});'
                        f'_.frombytes({field_ref});'
                        f'{field_ref} = _'
                    )
                    assigns.append(field_ref)
                else:
                    assigns.append(field_ref)

        walk(cls.__cfields__, ('A',))

        assign_code = f"{', '.join(assigns)} = xunpack(buffer)"

        unpack.add_code(assign_code)
        update.add_code(assign_code)

        for post_processor in post_processors:
            unpack.add_code(post_processor)
            update.add_code(post_processor)

        unpack.add_return('self')
        update.add_return('self')

        # print(unpack.generate_code())
        # print(update.generate_code())

        globals = {
            v: k for k, v in inner_classes.items()  # 翻转字典
        }
        # globals['__new__'] = object.__new__
        # globals['xunpack'] = cls.__cstruct__.unpack
        globals.update(dict(
            __new__=object.__new__,
            xunpack=cls.__cstruct__.unpack,
            array=array.array
        ))

        return unpack.exec(
            globals
        ), update.exec(
            globals
        )
