import ast
import builtins as _builtins
from typing import Optional

opers = {
    '+': lambda x, y=None: (x + y) if y is not None else x,
    '-': lambda x, y=None: (x - y) if y is not None else (-x),
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '//': lambda x, y: x // y,
    '%': lambda x, y: x % y,
    '**': lambda x, y: x ** y,
    '<<': lambda x, y: x << y,
    '>>': lambda x, y: x >> y,
    '&': lambda x, y: x & y,
    '|': lambda x, y: x | y,
    '^': lambda x, y: x ^ y,
    '~': lambda x: ~x,
    '<': lambda x, y: min(x, y) if x < y else False,
    '>': lambda x, y: max(x, y) if x > y else False,
    '<=': lambda x, y: min(x, y) if x <= y else False,
    '>=': lambda x, y: max(x, y) if x >= y else False,
    '==': lambda x, y: x if x == y else False,
    '!=': lambda x, y: x if x != y else False,
    'in': lambda x, y: x in y,
    'not in': lambda x, y: x not in y,
    'is': lambda x, y: x is y,
    'is not': lambda x, y: x is not y,
    'not': lambda x: not x,
    'or': lambda x, y: x or y,
    'and': lambda x, y: x and y
}
ast_name_to_operator = {
    'Add': '+',
    'Sub': '-',
    'Mult': '*',
    'Div': '/',
    'FloorDiv': '//',
    'Mod': '%',
    'Pow': '**',
    'LShift': '<<',
    'RShift': '>>',
    'BitAnd': '&',
    'BitOr': '|',
    'BitXor': '^',
    'Invert': '~',
    'Lt': '<',
    'Gt': '>',
    'LtE': '<=',
    'GtE': '>=',
    'Eq': '==',
    'NotEq': '!=',
    'In': 'in',
    'NotIn': 'not in',
    'Is': 'is',
    'IsNot': 'is not',
    'Not': 'not',
    'Or': 'or',
    'And': 'and',
    'UAdd': '+',
    'USub': '-'
}


def _literal_eval(node, globals_: Optional[dict], locals_: Optional[dict], builtins: Optional[dict],
                  local_context: Optional[dict] = None):
    if local_context is None:
        local_context = {}

    args = globals_, locals_, builtins, local_context

    def isin(name):
        return name in local_context or name in locals_ or name in globals_ or name in builtins

    def get(name):
        return local_context.get(name, locals_.get(name, globals_.get(name, builtins.get(name))))

    def op_func(node):
        return opers[ast_name_to_operator[type(node).__name__]]

    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.FormattedValue):  # <formatted value>
        return _literal_eval(node.value, *args)

    elif isinstance(node, ast.List):  # [ast.literal_eval(item) for item in node.elts]
        return [_literal_eval(element, *args) for element in node.elts]

    elif isinstance(node, ast.Tuple):  # tuple(ast.literal_eval(item) for item in node.elts)
        return tuple(_literal_eval(element, *args) for element in node.elts)

    elif isinstance(node, ast.BinOp):
        op = node.op
        func = op_func(op)
        return func(_literal_eval(node.left, *args),
                    _literal_eval(node.right, *args))

    elif isinstance(node, ast.UnaryOp):
        op = node.op
        func = op_func(op)
        return func(_literal_eval(node.operand, *args))

    elif isinstance(node, ast.Compare):
        left = _literal_eval(node.left, *args)
        for op, comparator in zip(node.ops, node.comparators):
            func = op_func(op)
            right = _literal_eval(comparator, *args)
            if not func(left, right):
                return False
            left = func(left, right)
        return bool(left)

    elif isinstance(node, ast.BoolOp):
        func = op_func(node.op)
        res = True
        for value in node.values:
            res = func(res, _literal_eval(value, *args))
        return res

    elif isinstance(node,
                    ast.Dict):  # {ast.literal_eval(k): ast.literal_eval(v) for k, v in zip(node.keys, node.values)}
        return {
            _literal_eval(key, *args):
                _literal_eval(value, *args) for key, value in
            zip(node.keys, node.values)
        }

    elif isinstance(node, ast.Name):  # <variable>
        name = node.id
        if not isin(name):
            raise NameError("name '" + name + "' is not defined")
        else:
            return get(name)

    elif isinstance(node, ast.Call):
        return _literal_eval(node.func, *args)(
            *[_literal_eval(arg, *args)
              for arg in node.args],
            **{
                _literal_eval(key, *args):
                    _literal_eval(value, *args)
                for key, value in node.keywords
            }
        )

    elif isinstance(node, (ast.ListComp, ast.GeneratorExp)):
        results = []
        for comprehension in node.generators:
            iter_values = _literal_eval(comprehension.iter, *args)

            # 处理目标变量
            if isinstance(comprehension.target, ast.Name):
                target_id = comprehension.target.id
            elif isinstance(comprehension.target, ast.Tuple):
                target_ids = [target.id for target in comprehension.target.elts]
            else:
                raise ValueError("Unsupported target type: " + str(type(comprehension.target)))

            for value in iter_values:
                if isinstance(comprehension.target, ast.Name):
                    local_context[target_id] = value
                elif isinstance(comprehension.target, ast.Tuple):
                    for target_id, val in zip(target_ids, value):
                        local_context[target_id] = val

                if comprehension.ifs:
                    condition_passed = all(
                        _literal_eval(condition, *args)
                        for condition in comprehension.ifs
                    )
                    if condition_passed:
                        results.append(_literal_eval(node.elt, *args))
                else:
                    results.append(_literal_eval(node.elt, *args))
        return results

    elif isinstance(node, ast.Attribute):
        return _literal_eval(node.value, *args).__getattribute__(node.attr)

    elif isinstance(node, ast.comprehension):
        return list(_literal_eval(node.iter, *args))

    else:
        raise ValueError("Unsupported type: " + str(type(node)))


def literal_eval(string, globals: Optional[dict] = None, locals: Optional[dict] = None,
                 builtins: bool = False, no_eval: bool = True):
    builtins_dict = {}
    if globals is None: globals = {}
    if locals is None: locals = {}
    if builtins is True: builtins_dict = vars(_builtins)

    if no_eval and 'eval' in builtins_dict:
        del builtins_dict['eval']

    tree = ast.parse(string, mode='eval')
    return _literal_eval(tree.body, globals, locals, builtins_dict)
