from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        total = end - start
        print(f"""
            [Czas przetwarzania danych: {total:.4f} sekund]""")
        return result
    return wrapper
