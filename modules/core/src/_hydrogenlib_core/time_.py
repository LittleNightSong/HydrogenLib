import time
from typing import Union


class Time:
    def __init__(self, sec):
        self._sec = sec
        self._hor = 0
        self._min = 0
        self._day = 0

        self.process()

    def process(self):
        if self._sec >= 60:
            _, self._sec = divmod(self._sec, 60)
            self._min += _
        if self._min >= 60:
            _, self._min = divmod(self._min, 60)
            self._hor += _
        if self._hor >= 24:
            _, self._hor = divmod(self._hor, 24)
            self._day += _

    @property
    def sec(self):
        return self._sec

    @property
    def min(self):
        return self._min

    @property
    def hor(self):
        return self._hor

    @property
    def day(self):
        return self._day

    @sec.setter
    def sec(self, v):
        self._sec = v

    @min.setter
    def min(self, v):
        self._min = v

    @hor.setter
    def hor(self, v):
        self._hor = v

    @day.setter
    def day(self, v):
        self._day = v

    @property
    def time_DHMS(self):
        """
        获取时间
        :return: 元组 (天, 时, 分, 秒)
        """
        return self.day, self.hor, self.min, self.sec

    @property
    def seconds(self):
        """
        获取秒数
        :return: 秒数
        """
        return self.day * 24 * 60 * 60 + self.hor * 60 * 60 + self.min * 60 + self.sec

    def __str__(self):
        return f"Day: {self.day}, {self.hor}:{self.min}:{self.sec}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.seconds})"


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

        self.running = False

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        if not self.running:
            raise RuntimeError("Timer not running")

        self.running = False

        self.end_time = time.time()
        self.elapsed_time = Time(self.end_time - self.start_time)

        return self.elapsed_time


class IntervalRecorder:
    def __init__(self):
        self._last_time = None
        self._running = False

    def start(self):
        self._last_time = time.time()
        self._running = True

    def record(self):
        res = time.time() - self._last_time
        self._last_time = time.time()
        return Time(res)

    def lap(self):
        return Time(time.time() - self._last_time)

    def stop(self):
        self._running = False

