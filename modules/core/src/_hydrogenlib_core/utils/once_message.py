from threading import Event


class OnceMessage:
    """
    一次性消息
    - set(message, timeout=None)
        设置消息内容,如果上一个消息未被读取,则等待上一个消息被读取
        - message: 消息内容
        - timeout: 等待上一个消息被读取的超时时间,单位为秒,默认为 None
    - get(timeout=None)
        获取消息内容,如果消息未被设置,则等待消息被设置
        - timeout: 等待消息被设置超时时间,单位为秒,默认为 None
    - is_set()
        判断消息是否已被设置
    - clear()
        清除消息,一次性消息将还原为未设置状态
    - close()
        关闭一次性消息,将无法再设置和获取消息
    """

    @property
    def closed(self):
        return self._shutdown

    def __init__(self):
        self._msg = None
        self._sented = Event()
        self._geted = Event()
        self._shutdown = False

    def __del__(self):
        self.close()

    def set(self, message, timeout=None):
        if self._shutdown:
            raise RuntimeError("OnceMessage has been closed")
        self._geted.wait(timeout)  # 等待 get 方法被调用
        self._msg = message
        self._sented.set()  # 通知 get 方法消息已设置
        self._geted.clear()  # 清除 _geted 事件，以便下次使用

    def get(self, timeout=None):
        if self._shutdown:
            raise RuntimeError("OnceMessage has been closed")
        if self._sented.wait(timeout):
            self._sented.clear()  # 清除 _sented 事件，以便下次使用
            self._geted.set()  # 通知 set 方法 get 方法已被调用
            return self._msg
        else:
            raise TimeoutError()

    def is_set(self):
        """
        判断消息是否已被设置
        """
        return self._sented.is_set()

    def clear(self):
        """
        清除消息,一次性消息将还原为未设置状态
        如果不进行新的set操作,上一个消息将会被保留
        """
        self._sented.clear()
        self._geted.clear()

    def close(self):
        self._shutdown = True
        self.clear()
