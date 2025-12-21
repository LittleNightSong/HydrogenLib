class _Empty:
    ...


class EventBase:
    """
    事件基类
    """
    def __init__(self):
        self.__accepted = True

    def accept(self):
        self.__accepted = True

    def deaccept(self):
        self.__accepted = False

    def is_accepted(self):
        return self.__accepted


class SetEvent(EventBase):
    """
    设置值 事件

    Properties:
        - old: 原始值
        - new: 当前值
    """
    def __init__(self, old, new):
        super().__init__()
        self.old = old
        self.new = new


class DeleteEvent(EventBase):
    """
    删除项 事件

    Properties:
        - key: 作为键的对象
        - value: 原始值
    """
    def __init__(self, key_obj, value):
        super().__init__()
        self.key = key_obj
        self.value = value


class GetEvent(EventBase):
    """
    获取项 事件

    Properties:
        - key: 作为键的对象
        - value: 原始值
    """
    def __init__(self, key_obj, value):
        super().__init__()
        self.key = key_obj
        self.result = value

    def set_result(self, value):
        self.result = value
