from time import sleep, time


class Clock:
    """
    时钟类，用于控制任务刷新间隔。
    如果任务消耗的时间大于刷新间隔时间，则sleep一段时间，以保持任务刷新间隔。
    如果任务消耗的时间小于刷新间隔时间，则sleep剩余一段时间，以保持任务刷新间隔。
    示例:
    ```python
    import random
    import time
    def random_sleep(a, b):
        sleep_time = random.randint(a, b)
        time.sleep(sleep_time)

    clock = Clock()
    while True:
        random_sleep(100, 2000)
        clock.strike(1.5)
    ```
    程序将保证每次任务执行时间为1.5秒，当任务消耗时间大于1.5秒时，程序将调整暂停时间，以保持任务刷新间隔。
    """
    def __init__(self):
        self.last_time = None

    def strike(self, interval):
        """
        确保任务以指定的间隔时间执行。
        :param interval: 刷新间隔时间，单位为秒
        """
        if self.last_time is None:
            self.last_time = time()

        current_time = time()
        elapsed_time = current_time - self.last_time
        if elapsed_time >= interval:
            sleep(interval - elapsed_time % interval)
        else:
            sleep(interval - elapsed_time)
        self.last_time = time()
