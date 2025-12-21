class _Undefined:
    _i = None

    def __new__(cls, *args, **kwargs):
        if cls._i is None:
            cls._i = super().__new__(cls)

        return cls._i

    def __repr__(self):
        return 'undefined'


undefined = _Undefined()


class Mark:
    def __init__(self, default=None, type=None):
        self.default = default
        self.type = type


def QUERY(default=undefined):
    return Mark(default, 'QUERY')


def PATH(default=undefined):
    return Mark(default, 'PATH')


def FIELD(default=undefined):
    return Mark(default, 'FIELD')


def UPLOAD_FILE(default=undefined):
    return Mark(default, 'UPLOAD_FILE')


def UPLOAD_FILES(default=undefined):
    return Mark(default, 'UPLOAD_FILES')
