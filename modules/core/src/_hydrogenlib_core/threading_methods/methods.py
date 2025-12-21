import threading as threading
from queue import Queue


def thread(function, args=(), kwargs={}):
    t = threading.Thread(target=function, args=args, kwargs=kwargs)
    return t


def run_new_thread(function, *args, **kwargs):
    t = thread(function, args, kwargs)
    t.start()
    return t


def run_new_daemon_thread(function, *args, **kwargs):
    t = thread(function, args, kwargs)
    t.daemon = True
    t.start()
    return t


def exit_thread(thread: threading.Thread):
    """
    This function is unsafe. You should use thread.join() instead.
    """
    thread._tstate_lock.release()


def run_with_timeout(func, timeout, *args, **kwargs):
    queue = Queue()

    def target():
        try:
            res = func(*args, **kwargs)
            queue.put((res, None))
        except Exception as e:
            queue.put((None, e))

    thread = run_new_thread(target)
    thread.join(timeout)

    result, error = queue.get()
    if error is not None:
        raise error

    return result


def run_in_thread(func, *args, **kwargs):
    queue = Queue()

    def target():
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            res = e

        queue.put(res)

    return queue, run_new_thread(target)


def run_in_thread_with_timeout(func, timeout, *args, **kwargs):
    def wrap():
        return run_with_timeout(func, timeout, *args, **kwargs)

    return run_in_thread(wrap)


def get_tid():
    return threading.get_ident()
