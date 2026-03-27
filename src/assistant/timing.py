from contextlib import contextmanager
from time import perf_counter


@contextmanager
def timed(label):
    start = perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {perf_counter() - start:.2f}s")
