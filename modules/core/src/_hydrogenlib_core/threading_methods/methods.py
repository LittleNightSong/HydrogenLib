import threading
from queue import Queue


def to_thread(function, args=(), kwargs={}):
    t = threading.Thread(target=function, args=args, kwargs=kwargs)
    return t


def run_new_thread(function, *args, **kwargs):
    t = to_thread(function, args, kwargs)
    t.start()
    return t


def run_new_daemon_thread(function, *args, **kwargs):
    t = to_thread(function, args, kwargs)
    t.daemon = True
    t.start()
    return t


def stop_thread(thread: threading.Thread):
    """
    This function is **unsafe**. You should use thread.join() instead.
    """
    thread._tstate_lock.release()


def run_with_timeout(func, timeout, *args, **kwargs):
    res = None
    e = None

    def target():
        nonlocal res, e
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            pass

    thread = run_new_thread(target)
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutError()

    return res



def get_tid():
    return threading.get_ident()
