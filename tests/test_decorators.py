
from src.decorators import log


def test_success_with_filename(self):
    """Проверяем логирование успешного вызова в файл."""
    @log(self.log_file)
    def add(a, b):
        return a + b

    result = add(3, 4)
    assert result == 7

    # Читаем файл и проверяем сообщение
    with open(self.log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Function add OK" in content
    assert "Result: 7" in content
    assert "Args: (3, 4)" in content


def test_success_no_filename(self, capsys):
    """Проверяем вывод в консоль при filename=None."""
    @log(None)
    def multiply(x, y):
        return x * y

    result = multiply(2, 6)
    assert result == 12

    # Перехватываем вывод
    captured = capsys.readouterr()
    assert "Function multiply OK" in captured.out
    assert "Result: 12" in captured.out
    assert "Args: (2, 6)" in captured.out


def test_no_args_no_kwargs(self, capsys):
    """Функция без аргументов."""
    @log(None)
    def hello():
        return "Hi!"

    result = hello()
    assert result == "Hi!"

    captured = capsys.readouterr()
    assert "Args: ()" in captured.out
    assert "Kwargs: {}" in captured.out

 # Пример использования
   @log("log.txt")  # Логи в файл
def add(x, y):
    """Функция складывает аргументы полученные на вход"""
    return x + y


   @log()  # Логи в консоль
def fail():
    raise ValueError("Пример ошибки")


" Тестируем "
print(add(1, 2))  # → 3
print(add(5, 7))  # → 12
fail()  # Выведет ошибку в консоль
