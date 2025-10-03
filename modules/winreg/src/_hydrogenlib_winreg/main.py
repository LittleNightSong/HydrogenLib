import sys
from pathlib import Path

if sys.version not in {'3.12', '3.8', '3.7'}:
    import winreg

    reg_hkey = {
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HEKY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HEKY_USERS": winreg.HKEY_USERS,
        "HEKY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,

        "HKCU": winreg.HKEY_CURRENT_USER,  # 缩写
        "HKLM": winreg.HKEY_LOCAL_MACHINE
    }


    def name_to_const(name):
        reg = reg_hkey[str(name).upper()]
        return reg


    def root_to_const(reg_path):
        root = Path(reg_path).root
        reg = name_to_const(root)
        return reg


    def split_reg_path(reg_path):
        path = Path(reg_path)
        root = path.root

        reg = name_to_const(root)
        sub_path = path.relative_to(root)

        return reg, sub_path


    class RegistryPath:
        def __init__(self, path):
            self.path = Path(path)
            self._root_const = root_to_const(path)

        def touch(self):
            reg, sub_path = split_reg_path(self.path)
            try:
                winreg.CreateKey(reg, sub_path)
            except OSError:
                pass

        @property
        def root(self):
            return self._root_const

        @property
        def parent(self):
            return self.__class__(self.path.parent)

        def open(self, mode: str = "r"):
            reg, sub_path = split_reg_path(self.path)

            access = 0
            if 'r' in mode:
                access |= winreg.KEY_READ

            if '+' in mode:
                access |= winreg.KEY_WRITE

            if '*' in mode:
                access |= winreg.KEY_ALL_ACCESS

            if 'e' in mode:
                access |= winreg.KEY_EXECUTE

            if 'n' in mode:
                access |= winreg.KEY_NOTIFY

            handle = winreg.OpenKeyEx(reg, str(sub_path), 0, access)
            return Handle(handle)


    class Handle:
        def __init__(self, handle):
            self._handle = handle

        def __setitem__(self, key, value):
            winreg.SetValueEx(self._handle, key, 0, pytype_to_regtype(value), value)

        def __getitem__(self, item):
            return winreg.QueryValueEx(self._handle, item)

        def __delitem__(self, item):
            try:
                winreg.DeleteValue(self._handle, item)
            except OSError:
                raise KeyError(f"{item} not found.")

        def __iter__(self):
            i = 0
            while True:
                try:
                    name, value, type = winreg.EnumValue(self._handle, i)
                    yield name, value, type
                except OSError:
                    break

                i += 1

        def keys(self):
            i = 0
            while True:
                try:
                    name = winreg.EnumKey(self._handle, i)
                    yield name
                except OSError:
                    break

        def values(self):
            i = 0
            while True:
                try:
                    name = winreg.EnumKey(self._handle, i)
                    yield name
                except OSError:
                    break

        def items(self):
            i = 0
            while True:
                try:
                    name, value, type = winreg.EnumValue(self._handle, i)
                    yield name, value
                except OSError:
                    break

        def pop(self, item):
            try:
                winreg.DeleteValue(self._handle, item)
            except OSError:
                raise KeyError(f"{item} not found.")

        def clear(self):
            for key in self.keys():
                self.pop(key)

        def __repr__(self):
            return f"<Handle {self._handle}>"

        __str__ = __repr__

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            winreg.CloseKey(self._handle)

        def __del__(self):
            winreg.CloseKey(self._handle)

        @classmethod
        def from_path(cls, path):
            hkey, path = split_reg_path(path)
            handle = winreg.CreateKey(hkey, str(path))
            return cls(handle)


    def pytype_to_regtype(pyType: object, big_type: bool = False):
        if isinstance(pyType, int):  # pyType为int
            if big_type:
                return winreg.REG_QWORD
            else:
                return winreg.REG_DWORD
        elif isinstance(pyType, float):  # pyType = float
            return ValueError("REG types not have 'float'.")
        elif isinstance(pyType, str):
            if big_type:
                return winreg.REG_EXPAND_SZ
            else:
                return winreg.REG_SZ
        else:
            return ValueError(f"pyType '{pyType}' don't turn to 'REG_TYPE'.")
