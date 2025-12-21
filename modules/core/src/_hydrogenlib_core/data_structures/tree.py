class Node:
    def __init__(self, data=None, *children, parent=None):
        self.data = data
        self.children = list(children)
        self.parent = parent

    def add_child(self, node):
        self.children.append(node)

    def remove_child(self, index):
        self.children.remove(index)

    def index(self, node):
        return self.children.index(node)

    def __str__(self):
        return f"TreeNode: data={self.data}, children_count={len(self.children)}"
