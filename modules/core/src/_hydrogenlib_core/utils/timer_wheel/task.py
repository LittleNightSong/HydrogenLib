from copy import deepcopy

from .core import TaskData, TaskType


class Task:
    def __init__(self, task_data: TaskData):
        self._data = task_data

    @property
    def id(self):
        return self._data.id

    def activity(self, activity: bool = None):
        if activity is not None:
            self._data.activity = activity
        else:
            return self._data.activity

    def cancel(self):
        self._data.is_vaild = False

    def is_canceled(self):
        return self._data.is_vaild

    def delay(self, delay: int = None):
        if delay is not None:
            self._data.delay = delay
        else:
            return self._data.delay

    @property
    def start_time(self):
        return self._data.start_time

    def type(self, tp: TaskType = None):
        if tp is not None:
            self._data.type = tp
        else:
            return self._data.type

    def export(self):
        return deepcopy(self._data)
