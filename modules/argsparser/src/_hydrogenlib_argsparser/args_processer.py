from _hydrogenlib_core.typefunc.function import Function


class Argument:
    def __init__(self, name: str, type):
        self.name = name
        self.type = type

    def transform(self, value):
        try:
            return self.type(value)
        except Exception as e:
            return None


class Arguments:
    def __init__(self, func):
        self.func = Function(func)

        self.arguments: list[Argument] = []

        self.args_supported = False
        self.kwargs_supported = False

    def _parse_arguments(self):
        if self.func.signature.parameters:
            for name, value in self.func.signature.parameters.items():
                self.arguments.append(Argument(name, value.annotation))


class Arguments_Parser:
    def __init__(self, arguments, args):
        self.arguments = arguments  # type: list[Argument]
        self.args = args  # type: list[str]

        self.pos = 0
        self.result = {}
        self.result_args = []
        self.result_kwargs = {}

    def parse(self):
        ...

