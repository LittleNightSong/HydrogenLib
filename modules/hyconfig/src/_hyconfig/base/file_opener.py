import os.path
from enum import Enum


class FileOpener:
    class mode(Enum):
        load = 'load'
        save = 'save'
        unknown = 'unknown'

        @property
        def mode(self):
            match self:
                case self.load:
                    return 'r'
                case self.save:
                    return 'w'
                case _:
                    return 'r'

    def open(self, file, mode: mode = mode.load, encoding=None):
        if not os.path.exists(file):
            open(file, 'w').close()
        return open(file, mode.mode, encoding=encoding)
