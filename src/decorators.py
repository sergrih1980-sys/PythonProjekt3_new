
def log(filename=None):
    """ Декоратор для логирования """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                log_message = f"Function: {func.__name__}. result: {result}"
                if filename:
                    with open(filename, "a") as f:
                        f.write(f"Function: {func.__name__}. result: {result}, \n")
                else:
                    print(log_message)
                    return result
            except Exception as e:
                log_message = f"Function: {func.__name__} error: {type(e).__name__}. Inputs:{args}. Outputs:{kwargs}. Exception: {e}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_message)
                else:
                    print(log_message)

        return wrapper

    return decorator



@log()
def add(x, y):
    """Функция складывает аргументы полученные на вход"""
    return x + y

print(add(1, 2))
print(add(1, 4))


























