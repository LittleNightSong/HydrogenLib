from fractions import Fraction


class ProbabilityCounter:
    def __init__(self, init_value=None):
        if init_value is None:
            init_value = {}
        self.count_dict = dict(init_value)

    def __setitem__(self, key, value):
        self.count_dict[key] = value

    def __getitem__(self, item):
        if item not in self.count_dict:
            self.count_dict[item] = 0
        return self.count_dict[item]

    def get(self, key):
        s = sum(self.count_dict.values())
        if s == 0:
            return Fraction()
        return Fraction(self.count_dict[key], s)

    def update(self, data: dict):
        for key, value in data.items():
            if key not in self.count_dict:
                self.count_dict[key] = 0
            self.count_dict[key] += value

    def increment(self, key, value=1):
        if key not in self.count_dict:
            self.count_dict[key] = 0
        self.count_dict[key] += value

    def probabilities(self, keys=None):
        if keys is None:
            keys = list(self.count_dict.keys())
            keys.sort()
        else:
            keys = list(keys)

        return [self.get(key) for key in keys]

    def proabilities_dict(self, keys=None):
        if keys is None:
            keys = list(self.count_dict.keys())
            keys.sort()
        return dict(zip(keys, self.probabilities(keys)))

    def __iter__(self):
        return iter(self.count_dict)

    def __len__(self):
        return len(self.count_dict)


if __name__ == '__main__':
    counter = ProbabilityCounter()
    for i in ['a', 'b', 'c', 'd']:
        counter[i] += 10

    print(counter.probabilities())
