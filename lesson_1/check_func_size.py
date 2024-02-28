import sys
from typing import Callable


def check_function_size(func: Callable[[int, int], str]):
    def wrapper(*args, **kwargs):
        func_result = func(*args, **kwargs)
        size_of_the_func = sys.getsizeof(func)
        return f'{func_result}\nThe size of the function is: {size_of_the_func} bytes'
    return wrapper


@check_function_size
def sum_two_numbers(number_1: int, number_2: int) -> str:
    return f'The sum of {number_1} and {number_2} is {number_1+number_2}'


print(sum_two_numbers(1, 6))


