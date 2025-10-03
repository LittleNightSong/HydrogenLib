from ...abstract import *
import dataclasses


class VNodeFile(AbstractFSNode):
    @property
    def attrs(self) -> FSAttrs:
        return dataclasses.replace(self.attrs)  # copy

    def __init__(self, filename, root=None, parent=None):
        filename = str(filename).strip()
        super().__init__(filename, root, parent)
        if '/' in filename or filename in {'..', '.'}:
            raise ValueError('Filename cannot contain "/"')

        self._attrs = FSAttrs(is_file=True, is_dir=False)

    def _error(self, *args, **kwargs):
        raise RuntimeError('File has no children')

    has_node = add_node = remove_node = get_node = _error


class VNodeDir(AbstractFSNode):
    @property
    def attrs(self) -> FSAttrs:
        return dataclasses.replace(self._attrs)

    def __init__(self, dirname, root=None, parent=None):
        super().__init__(dirname, root, parent)
        self._attrs = FSAttrs(is_dir=True, is_file=False)

    def iterdir(self):
        yield from self.children.keys()
