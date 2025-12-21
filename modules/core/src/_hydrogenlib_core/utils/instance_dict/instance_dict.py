import weakref
from collections import UserDict
from typing import Any

from .events import GetEvent, SetEvent, DeleteEvent


class InstanceMappingItem:
    _key: weakref.ReferenceType

    def __init__(self, key_instance, value, parent: 'InstanceMapping' = None):
        self._hasweakref = True
        try:
            self._key = weakref.ref(key_instance, self.delete_callback)
        except TypeError:
            self._key = key_instance  # 如果 key_instance 不是弱引用对象
            self._hasweakref = False
        self.value = value
        self.parent = parent

    @property
    def key(self):
        if self._hasweakref:
            return self._key()
        else:
            return self._key

    @property
    def as_key(self):
        return self.parent.to_key(self.key)

    def delete_callback(self, obj):
        try:
            self.parent.delete(obj)
        except KeyError:
            pass  # 忽略 KeyError


class InstanceMapping[_KT, _VT](UserDict[_KT, _VT]):
    def __init__(self, dct=None):
        super().__init__()
        if isinstance(dct, InstanceMapping):
            for k, v in dct.items():
                self._set(k, v)

    def to_dict(self):
        return {
            i.as_key: i.value for i in self.data.values()
        }

    def to_key(self, value):
        return id(value)

    def _get(self, key, item=False) -> InstanceMappingItem:
        i = super().__getitem__(key)
        return i if item else i.value

    def _set(self, key, value) -> None:
        super().__setitem__(self.to_key(key), InstanceMappingItem(key, value, self))

    def _pop(self, key):
        return super().pop(key)

    def _delete(self, key) -> None:
        super().__delitem__(key)

    def get(self, k, default=None, is_key_id=False) -> Any:
        """
        从 实例字典 中获取值
        :param k: 键
        :param is_key_id: 传入的 k 参数是否是一个 id 值
        :param default: 返回的默认值
        """
        if not is_key_id:  # 如果 k 不作为 id 传入
            k = self.to_key(k)  # 转换为 id

        if not super().__contains__(k):  # 如果 k 不位于字典中
            return default  # 返回默认值

        id_item = super().__getitem__(k)

        event = GetEvent(id_item.key, id_item.value)

        self.get_event(event)

        if not event.is_accepted():
            raise RuntimeError('Get event failed', event)

        return event.result  # 找到项, 返回字典值

    def set(self, k, v, is_key_id=False):
        """
        设置 实例字典 的值
        :param k: 键
        :param v: 值
        :param is_key_id: 传入的是否是一个 id 值
        """
        if not is_key_id:
            k = self.to_key(k)

        event = SetEvent(super().get(k, None), v)
        self.set_event(event)

        if not event.is_accepted():
            raise RuntimeError('Set event failed', event)

        self._set(self.to_key(k), v)

    def delete(self, key, is_key_id=False):
        """
        删除一个 实例字典 项
        :param key: 键
        :param is_key_id: 传入的键是否是一个 id 值
        """
        if not is_key_id:
            key = self.to_key(key)

        event = DeleteEvent(key, self._get(key))
        self.delete_event(event)

        if not event.is_accepted():
            raise RuntimeError('Delete event failed', event)

        self._delete(key)

    def pop(self, key, is_key_id=False):
        """
        弹出一个 实例字典 项
        :param key: 键
        :param is_key_id: 传入的键是否是一个 id 值
        :return: Any
        """
        if not is_key_id:
            key = self.to_key(key)

        self.delete_event(DeleteEvent(key, self._get(key)))

        return self._pop(key)

    def keys(self):
        return [i.key for i in self.data.values()]

    def values(self):
        return [i.value for i in self.data.values()]

    def items(self):
        return [(i.key, i.value) for i in self.data.values()]

    def __getitem__(self, key):
        return super().__getitem__(self.to_key(key)).value

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        super().__delitem__(self.to_key(key))

    def __contains__(self, item):
        return super().__contains__(self.to_key(item))

    def __iter__(self):
        yield from self.keys()

    # 拓展

    def delete_event(self, e: DeleteEvent):
        ...

    def set_event(self, e: SetEvent):
        ...

    def get_event(self, e: GetEvent):
        ...
