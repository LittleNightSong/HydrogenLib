import typing
import weakref

from ...typefunc.properties import alias

if typing.TYPE_CHECKING:
    from .pool import Pool


class PoolObject(typing.Protocol if typing.TYPE_CHECKING else object):
    def __pool_reuse__(self, *args, **kwargs):
        """
        对象被复用时调用
        :param args: 复用传参
        :param kwargs: 复用传参
        :return: None
        """
        pass

    def __pool_keep__(self):
        """
        对象被放回对象池时调用
        应当执行一些清理工作, 如果需要的话
        :return: None
        """
        pass


class PoolItem:
    obj = alias['obj']

    def __init__(self, obj: PoolObject, pool: 'Pool'):
        self._ref = None
        self._obj = obj
        self._pool = pool
    
    def keep(self, obj):
        self._obj = obj
        self._obj.__pool_keep__()
        self._ref = None
    
    def pop(self):
        self._ref = weakref.ref(self._obj, self.keep)  # 建立弱引用, 控制对象生命周期
        self._obj = None

    def reuse(self, *args, **kwargs):
        if self._obj is None:
            raise RuntimeError('对象正在使用中')

        self._obj.__pool_reuse__(*args, **kwargs)
        