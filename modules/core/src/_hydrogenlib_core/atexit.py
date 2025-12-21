class ExitFunction:
    def __init__(self, func, embedding=True, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.embedding = embedding

        self.name = None

    def __call__(self):
        if self.embedding:
            self.func(*self.args, **self.kwargs)

    def __repr__(self):
        return f"ExitFunction({self.func.__name__})"


class ExitContainer:
    """
    用法类似于 .hyconfig 模块
    class MyExitContainer(ExitContainer):
        exit_1 = ExitFunction(<some function>, True, <args>, <kwargs>)
        exit_2 = ExitFunction(<some function>, False, <args>, <kwargs>)
        ...

    if __name__ == '__main__':
        # No args should you give
        exit_container = MyExitContainer()
        
        # You can get all exit functions
        print(exit_container.exit_functions)  
        
        # The `embedding` argument is used to determine whether to call the function when the parser exits.
        print(exit_container.embedding("exit_1"))  # True
        
        # If you want to call the function when the parser exits, set it to True.
        exit_container.embedding("exit_2", True)
    
        # Or you can set it to False.
        exit_container.embedding("exit_1", False)
        
        # Your code
        # ...
        
        # When the parser exits, all ExitFunction will be called automatically.

    """
    @property
    def exit_functions(self):
        for _ in dir(self):
            value = getattr(self, _)
            if isinstance(value, ExitFunction):
                yield _, value

    def _build_mapping(self):
        for name, value in self.exit_functions:
            self.__mapping[name] = value

    def _add_atexit(self):
        import atexit
        atexit.register(self._at_exit)

    def _at_exit(self):
        for _, value in self.exit_functions:
            value()

    def __init__(self):
        self.__mapping = {}  # type: dict[str, ExitFunction]
        self._build_mapping()
        self._add_atexit()
    
    def embedding(self, name, value=None):
        if name not in self.__mapping:
            raise KeyError(f"{name} is not in {self.__mapping}")
        
        if value is None:
            return self.__mapping[name].embedding

        self.__mapping[name].embedding = value
        return None

    def origin_function(self, name, value=None):
        if name not in self.__mapping:
            raise KeyError(f"{name} is not in {self.__mapping}")
        
        if value is None:
            return self.__mapping[name].func
        
        self.__mapping[name].func = value
        return None


