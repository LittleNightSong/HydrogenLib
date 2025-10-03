from .vfs_node import *


class VisualFileSystem(AbstractFileSystem):
    TNodeFile = VNodeFile
    TNodeDir = VNodeDir

    def __init__(self, root_node: AbstractFSNode):
        self._root_node = root_node

    def get_node(self, path):
        cur = self._root_node
        try:
            for part in Path(path).parts:
                cur = cur.get_child(part)
            return cur
        except AttributeError:  # get_node 会在键不存在的时候返回 None
            return None

    def mkdirs(self, path):
        cur = self._root_node
        for part in Path(path).parts:
            if not cur.has_child(part):
                new_node = self.TNodeDir(part, self._root_node, cur)
                cur.add_child(new_node)
                new_node.on_create()

            cur = cur.get_child(part)

    def mkfile(self, file) -> None:
        file = Path(file)
        if not self.exists(file):
            raise FileNotFoundError(file)

        node = self.get_node(file.parent)
        new_node = self.TNodeFile(file.name, self._root_node, node)
        node.add_child(new_node)
        new_node.on_create()

    def remove(self, file) -> None:
        p = Path(file)
        node = self.get_node(p.parent)
        fnode = node.get_child(p.name)
        if fnode.is_file():
            node.remove_child(p.name)
            fnode.on_delete()
        else:
            raise IsADirectoryError(p)

    def rmdir(self, path) -> None:
        p = Path(path)
        node = self.get_node(p.parent)
        dirnode = node.get_child(p.name)
        if dirnode.attrs.is_dir:
            if len(dirnode) > 0:
                raise OSError('Directory not empty')

            node.remove_child(p.name)
            dirnode.on_delete()
        else:
            raise NotADirectoryError(path)

    def _rmdirs(self, node: AbstractFSNode):
        for key in node.children:
            child = node.get_child(key)

            if child.attrs.is_dir:
                self._rmdirs(child)
                child.on_delete()
            else:
                child.on_delete()

        node.children.clear()  # 删除所有子节点
        node.on_delete()

    def exists(self, path):
        return self.get_node(path) is not None
