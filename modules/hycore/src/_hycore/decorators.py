import time


class RetryLimitExceeded(Exception):
    pass


def retry(maybe_func, count: int = 3, delay: int = 1, delay_list: list[int | float] = None, on_error=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            nonlocal delay
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == count - 1:
                        raise RetryLimitExceeded() from e  # 如果是最后一次尝试，则抛出异常

                    if on_error:  # 如果on_error不为空，则调用on_error函数
                        on_error(e)

                    if delay_list:  # 如果delay_list不为空，则使用delay_list中的延迟时间
                        delay = delay_list[i]

                    time.sleep(delay)  # 延时后重试
            return None

        return wrapper

    return decorator(maybe_func) if maybe_func else decorator
