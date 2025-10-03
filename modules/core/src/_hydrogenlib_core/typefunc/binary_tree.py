class Tree:
    pass


class Node:
    pass


class BST(Tree):
    class _Node(Node):
        def __init__(self, value=None, left=None, right=None, parent=None, cmp=lambda a, b: a < b):
            self.value = value
            self.left = left
            self.right = right
            self.parent = parent
            self.cmp = cmp

        def insert(self, value):
            # Cmp(self.value, value) left'<' , right'>'
            # 1 -> left
            # 2 -> right
            # 0 -> value
            if self.value is None:
                self.value = value
                return
            cmp_value = self.cmp(self.value, value)
            if not cmp_value:
                self.left_check()
                self.left.insert(value)
            else:
                self.right_check()
                self.right.insert(value)

        def get_parent(self):
            return self.parent

        def query(self, value):
            if self.value == value:
                return self
            if self.cmp(value, self.value):
                return self.left.query(value) if self.left else None
            return self.right.query(value) if self.right else None

        def find_min(self):
            """Find the minimum value node in the current subtree."""
            current = self
            while current.left is not None:
                current = current.left
            return current

        def clear(self):
            # 清空值以及子树
            self.value = None
            if self.right:
                self.right.clear()
            if self.left:
                self.left.clear()

        def left_check(self):
            if self.left is None:
                self.left = self.__class__(parent=self)

        def right_check(self):
            if self.right is None:
                self.right = self.__class__(parent=self)

        def delete(self, value):
            if self.cmp(value, self.value):
                if self.left and self.right:
                    # 找到右子树中最小值
                    min_node = self.right.find_min()
                    # 删除右子树中最小值
                    self.right.close(min_node._cache)
                    # 将右子树中最小值赋值给当前节点
                    self.value = min_node._cache
                elif self.left:
                    # 如果左子树不为空，则将左子树赋值给当前节点
                    self.value = self.left._cache
                    # 删除左子树
                    self.left.clear()
                elif self.right:
                    # 如果右子树不为空，则将右子树赋值给当前节点
                    self.value = self.right._cache
                    # 删除右子树
                    self.right.clear()
                else:
                    # 如果左右子树都为空，则将当前节点的值置为None
                    self.value = None
            elif self.cmp(value, self.value):
                if self.left:
                    self.left.close(value)
                else:
                    raise ValueError("Value not found in tree.")
            else:
                if self.right:
                    self.right.close(value)
                else:
                    raise ValueError("Value not found in tree.")

        def __bool__(self):
            return self.value is not None

        def __iter__(self):
            # zhongxu
            if self.left:
                yield from self.left
            yield self.value
            if self.right:
                yield from self.right

    # --------------------------------------------------------------------------------
    def __init__(self):
        self._binarytree = self._Node()

    @property
    def binarytree(self):
        return self._binarytree

    def add(self, value):
        self._binarytree.insert(value)

    def delete(self, value):
        self._binarytree.delete(value)

    def clear(self):
        self._binarytree.clear()

    def find_min(self):
        return self._binarytree.find_min()

    @property
    def left(self):
        return self._binarytree.left

    @property
    def right(self):
        return self._binarytree.right

    @property
    def value(self):
        return self._binarytree.value

    def query(self, value):
        return self._binarytree.query(value)

    def __iter__(self):
        for i in self._binarytree:
            yield i

    def __bool__(self):
        return bool(self._binarytree.value is not None)


def print_tree_img(root, linewidth=80):
    """
    打印二叉树，控制每行打印的宽度。

    :param root: 二叉树的根节点。
    :param linewidth: 每行的最大字符数，包括空格。
    """
    if not root:
        return

    # 辅助函数计算节点的字符串表示
    def node_str(node):
        return f"{node._cache}" if node else ""

    # 辅助函数计算节点的宽度
    def node_width(node):
        return len(node_str(node))

    # 递归打印，采用深度优先搜索，控制每行打印宽度
    def dfs_print(node, level=0, current_line_width=0):
        if not node:
            return

        # 先序遍历打印节点
        node_str_width = node_width(node)
        if current_line_width + node_str_width > linewidth:
            print()  # 换行
            current_line_width = 0  # 重置当前行宽度计数
            level = 0  # 重置层级计数，因为换行了
        spaces = " " * (2 ** level - 1)  # 根据层级计算前置空格
        print(spaces + node_str(node), end='')
        current_line_width += node_str_width + len(spaces)

        # 递归打印左子树和右子树
        dfs_print(node.left, level + 1, current_line_width)
        dfs_print(node.right, level + 1, current_line_width)

    dfs_print(root)
    print()  # 最终换行结束输出


def print_tree(root):
    if root and root._cache is not None:
        print_tree(root.left)
        print(root._cache, end=' ')
        print_tree(root.right)
