class Heap:
    """
    默认大顶堆
    """
    def __init__(self, lst=None, reversed=False):
        self.heap = lst or []
        self.iter_reversed = reversed

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_down(self, index):
        left = self._left_child(index)
        right = self._right_child(index)
        smallest = index

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left

        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _heapify_up(self, index):
        parent = self._parent(index)
        if index > 0 and self.heap[parent] > self.heap[index]:
            self._swap(index, parent)
            self._heapify_up(parent)

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def remove(self, value):
        index = self.heap.index(value)
        self._swap(index, len(self.heap) - 1)
        self.heap.pop()
        self._heapify_down(index)

    def append(self, value):
        self.insert(value)

    def extract_min(self):
        if not self.heap:
            raise IndexError("Heap is empty.")
        min_val = self.heap[0]
        last_val = self.heap.pop()
        if self.heap:
            self.heap[0] = last_val
            self._heapify_down(0)
        return min_val

    def peek(self):
        if not self.heap:
            raise IndexError("Heap is empty.")
        return self.heap[0]

    def copy(self):
        return self.__class__(self.heap.copy())

    def iter(self):
        copy = self.copy()
        while copy:
            yield copy.heap[0]
            last = copy.heap.pop()
            if copy:
                copy.heap[0] = last
                copy._heapify_down(0)

    iter_reversed = False

    def __iter__(self):
        return self.iter() if not self.iter_reversed else reversed(tuple(self.iter()))

    def __len__(self):
        return len(self.heap)
