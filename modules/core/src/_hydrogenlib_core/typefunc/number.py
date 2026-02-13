def number_map(n, in_min, in_max, out_min, out_max):
    return (n - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class NumberMapper:
    def __init__(self, in_min, in_max, out_min, out_max):
        self.in_min = in_min
        self.in_max = in_max
        self.out_min = out_min
        self.out_max = out_max
        self.ratio = (out_max - out_min) / (in_max - in_min)

    def calc(self, n):
        return (n - self.in_min) * self.ratio + self.out_min
