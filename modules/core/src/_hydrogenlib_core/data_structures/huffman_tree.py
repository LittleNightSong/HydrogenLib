from collections import deque

from bitarray import bitarray

from ..utils.probability_counter import ProbabilityCounter


def get_probabilities(data):
    """
    Returns a dictionary of probabilities for each character in the data
    """
    pc = ProbabilityCounter()
    for i in data:
        pc.increment(i, 1)
    return pc.probabilities()


def get_probabilities_dict(data):
    """
    Returns a dictionary of probabilities for each character in the data
    """
    pc = ProbabilityCounter()
    for i in data:
        pc.increment(i, 1)
    return pc.proabilities_dict()


class HuffmanNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.value = None
        self.probability = None

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def init_left(self):
        if self.left is None:
            self.left = HuffmanNode()
        return self.left

    def init_right(self):
        if self.right is None:
            self.right = HuffmanNode()
        return self.right

    def is_leaf(self):
        return self.left is None and self.right is None

    # >
    def __gt__(self, other):
        return self.probability > other.probability

    def __lt__(self, other):
        return self.probability < other.probability

    # ==
    def __eq__(self, other):
        return self.probability == other.probability

    def __str__(self):
        return f"{self.value}"

    __repr__ = __str__


class HuffmanTree:
    def __init__(self):
        self.root = None
        self.codes = {}

    @staticmethod
    def _build_tree_from_list(root, ls):
        queue = deque([root])
        for i in ls:
            node = queue.popleft()  # type: HuffmanNode
            node.value = i
            queue.append(node.init_left())
            queue.append(node.init_right())

    def _walk(self, node, path: bitarray):
        if not node:
            return
        if node.is_leaf():
            yield path.tobytes(), node.value
        else:
            path.append(0)
            yield from self._walk(node.left, path)
            path[-1] = 1
            yield from self._walk(node.right, path)
            path.pop()

    def walk(self):
        path = bitarray()
        return self._walk(self.root, path)

    @classmethod
    def from_list(cls, ls):
        """
        依次将数据填充到树中
        越靠前的数据，所在树的深度越低
        """
        self = cls()
        self._build_tree_from_list(self.root, ls)
        return self

    @classmethod
    def from_data(cls, probabilities: dict):
        self = cls()
        priority_queue: list[HuffmanNode] = []
        for char, probability in probabilities.items():
            node = HuffmanNode()
            node.value = char
            node.probability = probability
            priority_queue.append(node)

        while len(priority_queue) > 1:
            priority_queue.sort()
            node1 = priority_queue.pop(0)
            node2 = priority_queue.pop(0)

            prob1 = node1.probability
            prob2 = node2.probability

            new_node = HuffmanNode()
            new_node.left = node1
            new_node.right = node2
            new_node.probability = prob1 + prob2
            priority_queue.append(new_node)

        root = priority_queue.pop()
        self.root = root
        return self

    @property
    def huffman_code(self):
        if self.codes is None:
            self.codes = dict(self.walk())
        return self.codes

    @property
    def huffman_codes_dict(self):
        return dict(map(lambda x: (x[1], x[0]), self.walk()))

    def compress(self, data):
        codes = get_huffman_codes_dict(self)
        res = b''
        for char in data:
            res += codes[char]

        return res

    def decompress(self, data):
        res = ''
        current = self.root
        ba = bitarray()
        ba.frombytes(data)
        for bit in ba:
            current = current.left if bit == 0 else current.right
            if current.is_leaf():
                res += current.value
                current = self.root

        return res


if __name__ == '__main__':
    test_str = "aaaaabcdef"
    probabilities = get_probabilities_dict(test_str)
    huffman_tree = HuffmanTree.from_data(probabilities)

    print("Test string:", repr(test_str))
    print(probabilities)

    compressed_data = huffman_tree.compress(test_str)
    decompressed_data = huffman_tree.decompress(compressed_data)

    print(compressed_data)
    print(decompressed_data)
    print(decompressed_data == test_str)
