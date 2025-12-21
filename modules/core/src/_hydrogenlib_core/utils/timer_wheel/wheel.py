import warnings

from .core import get_current_ms, TaskType, TaskData, WheelCore
from .task import Task


class Wheel:
    @property
    def current_slot(self):
        return self.current_slot

    @property
    def slots_length(self):
        return len(self.core)

    def __init__(self, slots: int, granularity_ms: int):
        self.core = WheelCore(slots, granularity_ms)

    def add_task(self, callback, args=(), kwargs=None, delay=None, id=None, cycle=False):
        if kwargs is None:
            kwargs = {}

        data = TaskData(
            callback, args, kwargs,
            id,
            get_current_ms(), delay,
            True, 0,
            TaskType.cycle if cycle else TaskType.single
        )
        self.core.add_task(
            data
        )
        return Task(data)

    def advance(self):
        self.core.advance()


class MultiWheel:
    def __init__(self, *wheels):
        self.wheels = sorted(wheels, key=lambda w: w.core.granularity_ms)  # 按粒度排序(升序)

    def add_task(self, callback, args=(), kwargs=None, delay=None, id=None, cycle=False):
        for wheel in reversed(self.wheels):
            if delay % wheel.core.granularity_ms == 0:
                return wheel.add_task(callback, args, kwargs, delay, id, cycle)

        wheel = self.wheels[0]  # 取时间粒度最小的轮
        warnings.warn("The task delay is not divisible by the wheel granularity, the task will be added to the wheel "
                      "with the smallest granularity.")
        return wheel.add_task(callback, args, kwargs, delay, id, cycle)
