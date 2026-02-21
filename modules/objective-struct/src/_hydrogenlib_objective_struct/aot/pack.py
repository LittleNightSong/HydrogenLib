from __future__ import annotations

import array
import typing

from .base import unique_name_generator, is_struct, is_array, get_array_ctype, to_tuple_expression, function_def

if typing.TYPE_CHECKING:
    from .. import struct_type


def create_pack_methods(cls: struct_type.Struct):
    """
    Generate `pack` and `pack_into` method
    """
    with (
        function_def('pack(self)') as pack,
        function_def('pack_into(self, buffer, offset=0)') as pack_into,
    ):
        ung = unique_name_generator()
        flat_fields = []

        def add_code(code):
            pack.add_code(code)
            pack_into.add_code(code)

        def walk(fields, path, parent_name=None):
            # parent name 标识了这个字段的父字段被赋值给了哪个临时变量，这样可以复用已有的临时变量，减少结构体属性访问次数
            name = 'self'  # 这里的 name 是默认的 self，如果当前处理的是内嵌的结构体，那么 name 会被替换成临时变量

            if len(path) > 1:  # 当前处理的是内嵌结构体
                name = ung.next()  # 生成一个临时变量缓存其值
                add_code(f'{name} = {parent_name}.{path[-1]}')

            for field in fields:  # 遍历结构体的所有字段
                if is_struct(field.type):  # 又是一个内嵌的结构体字段
                    walk(field.type.__cfields__, path + (field.name,), name)  # 递归
                elif is_array(field.type):  # 一个数组类型
                    d_ctype = get_array_ctype(field.type)

                    _ = ung.next()
                    add_code(f'{_} = array({d_ctype!r}, {name}.{field.name})')
                    flat_fields.append(f'{_}.tobytes()')

                else:
                    flat_fields.append(f'{name}.{field.name}')  # 普通的字段，添加到传递目标列表中

        walk(cls.__cfields__, ('self',))  # 启动递归函数
        # names = [field.name for field in fields]

        expression = to_tuple_expression(flat_fields, prefix='')
        pack.add_return(f"xpack({expression})")  # 返回打包的结果，将所有字段参数展开传递
        pack_into.add_code(f"xpack_into(buffer, offset, {expression})")
        # print(pack.generate_code())  # Debug
        return (
            pack.exec({'xpack': cls.__cstruct__.pack, 'array': array.array}),
            pack_into.exec({'xpack_into': cls.__cstruct__.pack_into, 'array': array.array})
        )
