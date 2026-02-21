from __future__ import annotations

import array
import typing

from .base import unique_name_generator, is_struct, is_array, get_array_ctype, function_def, for_stmt

if typing.TYPE_CHECKING:
    from .. import struct_type


def create_unpack_methods(cls: type[struct_type.Struct]):
    with (
        function_def('unpack(cls, buffer)') as unpack,
        function_def('update(self, buffer)') as update,
        function_def('unpack_from(cls, buffer, offset=0)') as unpack_from,
        function_def('update_from(self, buffer, offset=0)') as update_from,
        function_def('iter_unpack(cls, buffer)') as iter_unpack,
        function_def('iter_update(cls, buffer, obj=None)') as iter_update,
    ):
        unpack.add_decorator('classmethod')  # unpack 是一个类方法
        unpack_from.add_decorator('classmethod')  # unpack_from 也是
        iter_unpack.add_decorator('classmethod')
        iter_update.add_decorator('classmethod')

        ung = unique_name_generator()

        def update_add_code(code):
            update.add_code(code)
            update_from.add_code(code)
            iter_update_inner.add_code(code)

        def unpack_add_code(code):
            unpack.add_code(code)
            unpack_from.add_code(code)
            iter_unpack_inner.add_code(code)

        post_processors = []  # 后处理代码列表
        assigns = []  # 赋值目标列表
        inner_classes = {}  # 内嵌的结构体的类型映射（所有内嵌结构体的类型在生成代码时都会被代替为无意义的名称）

        iter_update.add_code("self = cls() if obj is None else obj")

        iter_unpack_inner = for_stmt("values in x_iter_unpack(buffer)")
        iter_update_inner = for_stmt("values in x_iter_unpack(buffer)")

        iter_unpack.add_node(iter_unpack_inner.node)
        iter_update.add_node(iter_update_inner.node)

        def walk(fields, path, parent_name=None, current_class_name='cls'):
            name = 'self'

            if len(path) > 1:  # 在处理内嵌的结构体
                name = ung.next()  # 临时变量的名称
                update_add_code(f"{name} = {parent_name}.{path[-1]}")

                unpack_add_code(f"{parent_name}.{path[-1]} = {name} = __new__({current_class_name})")  # 组合赋值
            else:
                unpack_add_code(f"{name} = __new__({current_class_name})")  # 不需要临时变量存储根对象
                # update 在这里不需要创建新对象

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

        assign_code = f"{', '.join(assigns)} = x_unpack(buffer)"  # 生成普通的 unpack, update 用的赋值语句
        unpack.add_code(assign_code)
        update.add_code(assign_code)

        assign_code = assign_code.replace("x_unpack(buffer)", "values")  # 生成 iter_xxx 的赋值语句
        iter_unpack_inner.add_code(assign_code)
        iter_update_inner.add_code(assign_code)

        assign_code = assign_code.replace("values", "x_unpack_from(buffer, offset)")  # 生成 xxx_from 的赋值语句
        unpack_from.add_code(assign_code)
        update_from.add_code(assign_code)

        for post_processor in post_processors:
            unpack_add_code(post_processor)
            update_add_code(post_processor)

        unpack.add_return('self')
        update.add_return('self')
        unpack_from.add_return('self')
        update_from.add_return('self')

        iter_unpack_inner.add_code('yield self')  # iter 方法是 yield，而非 return
        iter_update_inner.add_code('yield self')

        # print(unpack.generate_code())
        # print(update.generate_code())
        # print(unpack_from.generate_code())
        # print(update_from.generate_code())
        # print(iter_unpack.generate_code())
        print(iter_update.generate_code())

        globals = {
            v: k for k, v in inner_classes.items()  # 翻转字典
        }

        globals.update(dict(
            __new__=object.__new__,
            x_unpack=cls.__cstruct__.unpack,
            x_unpack_from=cls.__cstruct__.unpack_from,
            x_iter_unpack=cls.__cstruct__.iter_unpack,
            array=array.array
        ))

        return unpack.exec(
            globals
        ), update.exec(
            globals
        ), unpack_from.exec(
            globals
        ), update_from.exec(
            globals
        ), iter_unpack.exec(
            globals
        ), iter_update.exec(
            globals
        )
