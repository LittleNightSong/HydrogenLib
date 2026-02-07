class Range:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        yield from range(self.start, self.end, self.step)
