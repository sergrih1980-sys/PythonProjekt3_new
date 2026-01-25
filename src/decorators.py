import functools


def log(filename=None):
    """Декоратор для логирования вызова функции: начало, результат, ошибки."""

    def decorator(func):
        @functools.wraps(func)  # Сохраняем имя и __doc__ функции
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                # Формируем сообщение о успешном выполнении
                log_message = (
                    f"Function {func.__name__} OK. "
                    f"Result: {repr(result)}. "
                    f"Args: {repr(args)}, Kwargs: {repr(kwargs)}"
                )
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                return result  # возвращаем результат!

            except Exception as e:
                # Формируем сообщение об ошибке
                error_msg = (
                 f"Function {func.__name__} ERROR. "
                 f"Type: {type(e).__name__}, "
                 f"Message: {e}, "
                 f"Args: {repr(args)}, "
                 f"Kwargs: {repr(kwargs)}"
                )
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_msg + "\n")
                else:
                    print(error_msg)
                raise  # Перебрасываем исключение дальше

        return wrapper

    return decorator



