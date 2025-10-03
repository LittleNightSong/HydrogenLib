from collections import deque

from ..typefunc import get_called_func


class _TreeHead:
    children = []


stack = deque([_TreeHead()])  # type: deque[_TreeHead|CodeStruct]
namespace = {}


class CodeStructMain:
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
        self.root = None
        self._register()

    def _register(self):
        if self.name in namespace:
            raise ValueError(f"Duplicate name: {self.name}")
        # Python called stack: _register, __init__, <function>
        funct = get_called_func(3)
        if funct in namespace:
            raise ValueError(f"Duplicate function: {funct}")
        namespace[funct] = self

    def _generate(self, node, depth):
        if not isinstance(node, _TreeHead):
            prefix = '\t' * depth
            res = f"{prefix}{node.subject}: {node.description}\n"
        else:
            res = ""
        for c in node.children:
            res += self._generate(c, depth + 1)

        return res

    def generate_tree_str(self):
        tree_head = self.root.is_parent_dict
        return self._generate(tree_head, -1)


class CodeStruct:
    def __init__(self, subject=None, description=None):
        self.subject = subject
        self.description = description
        self.children = []
        self.parent = None

        self._called_func = get_called_func(2)
        if self._called_func in namespace:
            namespace.get(self._called_func).root = self
        else:
            raise RuntimeError(f"No root found for {self._called_func}")

    def __enter__(self):
        stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        stack.pop()
        if stack:
            self.parent = stack[-1]
            self.parent.children.append(self)
