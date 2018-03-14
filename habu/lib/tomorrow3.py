import sys
import traceback
from functools import wraps
from threading import Semaphore
from concurrent.futures import ThreadPoolExecutor


def threads(n, queue_max=None):

    def decorator(f):

        pool = ThreadPoolExecutor(n)
        sem_max = queue_max

        if sem_max is None:
            sem_max = n

        sem = Semaphore(sem_max)

        def wait():
            for _ in range(sem_max):
                sem.acquire()

            for _ in range(sem_max):
                sem.release()

        f.wait = wait

        def exception_catcher(f, *args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception:
                print('[tomorrow3] Caught exception.', file=sys.stderr)
                traceback.print_exc()
                sys.exit(-1)

        @wraps(f)
        def wrapped(*args, **kwargs):

            sem.acquire(blocking=True)
            future = pool.submit(exception_catcher, f, *args, **kwargs)
            future.add_done_callback(lambda _: sem.release())

            return future

        return wrapped

    return decorator
