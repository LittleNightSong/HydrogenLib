from __future__ import annotations

import ast
import itertools
import typing
from typing import Any

import typing_inspection.typing_objects

from _hydrogenlib_core.typefunc import enhanced_generator
from _hydrogenlib_objective_struct.methods import get_ctype


class _objective_node_operator:
    _node: ast.stmt

    @property
    def node(self):
        return self._node

    def add_node(self, node: ast.AST):
        self._node.body.append(node)
        return node

    def add_code(self, code: str):
        tree = ast.parse(code)
        if isinstance(tree, ast.Module):
            self._node.body.extend(tree.body)
            return tree
        elif isinstance(tree, ast.Expr):
            self._node.body.append(tree.value)
            return tree.value
        else:
            self._node.body.append(tree)
            return tree

    # def insert_code(self, index, code: str):
    #     tree = ast.parse(code)
    #     if isinstance(tree, ast.Module):
    #         for node in reversed(tree.body):
    #             self._node.body.insert(index, node)
    #         return tree
    #     elif isinstance(tree, ast.Expr):
    #         self._node.body.insert(index, tree.value)
    #         return tree.value
    #     else:
    #         self._node.body.insert(index, tree)
    #         return tree

    def compile(self):
        module = ast.Module([self._node])
        ast.fix_missing_locations(module)
        return compile(
            module, filename="<string>", mode="exec"
        )

    def exec(self, globals=None, locals=None, closure=None):
        globals = globals or {}
        exec(self.compile(), globals, locals, closure=closure)
        return globals[self._node.name]

    def generate_code(self):
        module = ast.Module([self._node])
        ast.fix_missing_locations(module)
        return ast.unparse(module)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class function_def(_objective_node_operator):
    def __init__(self, signature: str):
        self._signature = signature
        self._node = ast.parse(f'def {signature}: pass').body[0]  # type: ast.FunctionDef
        self._node.body.clear()

    def add_decorator(self, expr: str | ast.expr):
        if isinstance(expr, str):
            node = ast.parse(expr).body[0]

            if not isinstance(node, ast.Expr):
                raise ValueError(expr)

            expr = node.value

        self._node.decorator_list.append(expr)
        return expr

    def add_return(self, expr: str | ast.expr):
        if isinstance(expr, str):
            node = ast.parse(expr).body[0]
            if not isinstance(node, ast.Expr):
                raise ValueError(expr)
            self._node.body.append(ast.Return(node.value))
        else:
            self._node.body.append(ast.Return(expr))


class for_stmt(_objective_node_operator):
    def __init__(self, expr):
        self._node = ast.parse(f"for {expr}: ...").body[0]  # type: ast.For
        self._node.body.clear()

    def exec(self, globals=None, locals=None, closure=None):
        return exec(self.compile(), globals, locals, closure=closure)


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
