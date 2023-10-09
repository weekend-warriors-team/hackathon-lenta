import time


def calculate_execution_time(func):
    """Выводит время выполнения функции."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения функции {func.__name__}: "
              f"{execution_time} секунд.")
        return result
    return wrapper
