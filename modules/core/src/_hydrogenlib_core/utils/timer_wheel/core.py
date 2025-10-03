import dataclasses as dc
import enum
import time
from collections import deque
from typing import Callable


class MultiError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.errors = args

    def __str__(self) -> str:
        return "\n".join(map(str, self.errors))

    def __iter__(self):
        return self.errors.__iter__()


def get_current_ms():
    return int(time.monotonic())


class TaskType(str, enum.Enum):
    # 单次执行, 周期执行
    single = "single"
    cycle = "cycle"


@dc.dataclass
class TaskData[A, R]:
    callback: Callable[[*A], R]
    args: tuple
    kwargs: dict
    id: str
    start_time: int
    delay: int
    is_vaild: bool

    round: int = 0
    type: str = TaskType.single
    activity: bool = True

    def __call__(self) -> R:
        return self.callback(*self.args, **self.kwargs)

    @property
    def remaining_time(self):
        return self.delay - (get_current_ms() - self.start_time)

    @property
    def is_expired(self):
        return self.remaining_time <= 0


class Slot:
    def __init__(self):
        self.tasks = deque()  # type: deque[TaskData]

    def push(self, task):
        self.tasks.append(task)

    def pop(self):
        return self.tasks.popleft()

    def __len__(self):
        return len(self.tasks)


class WheelCore:
    def __init__(self, slots: int, granularity_ms: int):
        self.slots: list[Slot] = [Slot() for i in range(slots)]  # 创建 slots 个槽
        self.granularity_ms = granularity_ms or 1000
        self.current_slot = 0
        self.last_update_time = None
        self.cancel_tasks = set()

    def add_task(self, task: TaskData):
        ticks = task.delay // self.granularity_ms
        slot = (self.current_slot + ticks) % len(self)
        task.round = ticks // len(self)

        self.slots[slot].push(task)

    def process_slot(self, slot: Slot):
        errors = []
        count = 0
        length = len(slot)
        while count < length:
            task = slot.pop()  # 获取一个任务

            if task.id in self.cancel_tasks or not task.is_vaild:
                self.cancel_tasks.remove(task.id)
                length -= 1  # 减去一个任务
                continue

            if task.activity:
                if task.is_expired:
                    # Run task
                    try:
                        task()
                    except Exception as e:
                        errors.append(e)

                    if task.type == TaskType.cycle:
                        task.start_time = get_current_ms()  # 重新设置开始时间
                        slot.push(task)

                else:
                    slot.push(task)  # 未超时的任务重新加入槽
            # else:
            # 暂停的任务不处理

            count += 1  # 记得统计处理次数

        return errors

    def advance(self):
        current_time = get_current_ms()
        # 计算需要推进的槽数
        ticks = (current_time - self.last_update_time) // self.granularity_ms
        total_errors = []

        for i in range(ticks):
            index = (self.current_slot + i) % len(self)
            errors = self.process_slot(self.slots[index])
            total_errors.extend(errors)

        self.last_update_time = current_time

        if total_errors:
            raise MultiError(*total_errors)  # 一次性抛出所有错误

    def __len__(self):
        return len(self.slots)
