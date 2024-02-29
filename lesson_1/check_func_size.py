import sys
import functools
import tracemalloc
from typing import Callable


def measure_memory(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        tracemalloc.start()
        result = func(*args, **kwargs)

        memory_current, memory_peak = tracemalloc.get_traced_memory()

        print(f"Memory used by '{func.__name__}':\ncurrent: {memory_current} bytes\npeak: {memory_peak} bytes")

        return result

    return wrapper


@measure_memory
def sum_two_numbers(number_1: int, number_2: int) -> str:
    return f'The sum of {number_1} and {number_2} is {number_1+number_2}'


print(sum_two_numbers(1, 6))


