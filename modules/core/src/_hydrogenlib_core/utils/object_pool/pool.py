from collections import deque
from .item import PoolItem


class Pool:
    def __init__(self, max_size=0):
        self._max_size = max_size
        self._deque = deque(maxlen=max_size)  # type: deque[PoolItem]
    
    def put(self, obj):
        self._deque.append(PoolItem(obj, self))
    
    def request(self, *args, **kwargs):
        item = self._deque.popleft()
        item.reuse(*args, **kwargs)
        self._deque.append(item)
        return item.obj
        
            