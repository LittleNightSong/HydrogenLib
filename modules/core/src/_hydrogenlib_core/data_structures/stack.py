from collections import deque
from copy import copy
from typing import Iterable, Generic, TypeVar


T = TypeVar("T")
class Stack(Generic[T]):
    @property
    def stack(self) -> deque:
        """
        Get stack.
        :return: the deque of stack.
        """
        return copy(self._stack)

    @stack.setter
    def stack(self, stack):
        self._stack = deque(stack)

    def __init__(self, stack: Iterable = None):
        self._stack = deque() if stack is None else deque(stack)

    def push(self, data: T):
        """
        Push data to stack.
        """
        self._stack.append(data)

    def pop(self) -> T | None:
        """
        Pop data from stack(delete last one).
        if stack is empty, return None.
        """
        return self._stack.pop() if not self.is_empty() else None

    def size(self) -> int:
        """
        Get stack size.
        """
        return len(self._stack)

    def is_empty(self) -> bool:
        """
        Check stack is empty.
        """
        return self.size() == 0

    def peek(self) -> T | None:
        """
        Get stack top data.
        """
        return self._stack[-1] if not self.is_empty() else None

    def copy(self) -> "Stack[T]":
        """
        Copy stack.
        """
        return self.__class__(self._stack.copy())

    def as_tuple(self) -> tuple[T, ...]:
        return tuple(self._stack)

    @property
    def top(self) -> T | None:
        """
        Same as `.top()`.
        """
        return self.peek()

    @top.setter
    def top(self, new):
        if not self.is_empty():
            self._stack[-1] = new

    def __str__(self):
        return str(self._stack)

    def __iter__(self):
        return iter(self._stack)

    def __getitem__(self, item) -> T:
        return self._stack[item]

    def __setitem__(self, index, value):
        self._stack[index] = value

    def __len__(self):
        return len(self._stack)

    def __repr__(self):
        return "Stack({self.lst})".format(self=self)
