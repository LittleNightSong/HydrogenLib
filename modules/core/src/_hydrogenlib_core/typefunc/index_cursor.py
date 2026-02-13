class Cursor:
    __slots__ = ("obj", "position")

    def __init__(self, obj, start=0):
        self.obj = obj
        self.position = start

    def get(self, n: int = None):
        if not n:
            return self.obj[self.position]

        if n > 0:
            return self.obj[self.position:self.position + n]
        else:
            return self.obj[self.position + n: self.position]

    def advance(self, n: int = 1):
        if not n:
            raise ValueError("Cannot advance cursor by 0")

        value = self.get(n)
        self.position += n
        return value

    def __rshift__(self, other):
        return self.advance(other)

    def __lshift__(self, other):
        return self.advance(-other)

    def __index__(self):
        return self.position

    def __iter__(self):
        yield from self.obj[self.position:]
